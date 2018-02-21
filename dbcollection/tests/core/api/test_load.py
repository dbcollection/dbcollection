"""
Test dbcollection core API: load.
"""


import pytest

from dbcollection.core.api.load import load, LoadAPI


@pytest.fixture()
def mocks_api(mocker):
    mock_parse = mocker.patch.object(LoadAPI, "parse_task_name", return_value=True)
    mock_cache = mocker.patch.object(LoadAPI, "get_cache_manager")
    mock_run = mocker.patch.object(LoadAPI, "run", return_value=True)
    return [mock_parse, mock_cache, mock_run]


def assert_mock_api(mocks):
    for mock in mocks:
        assert mock.called


def generate_inputs_for_load():
    return {
        "dataset": 'mnist',
        "task": 'some_task',
        "data_dir": '/some/path/',
        "verbose": True,
    }


class TestCallLoad:
    """Unit tests for the core api load method."""

    def test_call_with_dataset_name_only(self, mocker, mocks_api):
        inputs = generate_inputs_for_load()

        data_loader = load(inputs["dataset"])

        assert_mock_api(mocks_api)
        assert data_loader == True

    def test_call_with_all_inputs(self, mocker, mocks_api):
        inputs = generate_inputs_for_load()

        data_loader = load(inputs["dataset"], inputs["task"], inputs["data_dir"], inputs["verbose"])

        assert_mock_api(mocks_api)
        assert data_loader == True

    def test_call_with_all_inputs_named_args(self, mocker, mocks_api):
        inputs = generate_inputs_for_load()

        data_loader = load(name=inputs["dataset"],
                           task=inputs["task"],
                           data_dir=inputs["data_dir"],
                           verbose=inputs["verbose"])

        assert_mock_api(mocks_api)
        assert data_loader == True

    def test_call__raises_error_no_inputs(self, mocker):
        with pytest.raises(TypeError):
            load()

    def test_call__raises_error_extra_inputs(self, mocker):
        with pytest.raises(TypeError):
            load("some_dataset", "some_task", "some_dir", True, "extra_field")

@pytest.fixture
def mocks_init_class(mocker):
    inputs = generate_inputs_for_load()
    mock_parse = mocker.patch.object(LoadAPI, "parse_task_name", return_value=inputs["task"])
    mock_cache = mocker.patch.object(LoadAPI, "get_cache_manager")
    return [mock_parse, mock_cache]


def assert_mock_init_class(mocks):
    for mock in mocks:
        assert mock.called


def mock_run_method(mocker, data_exists, task_exists):
    assert data_exists is not None
    assert task_exists is not None

    mock_data_exists = mocker.patch.object(LoadAPI, "dataset_data_exists_in_cache", return_value=data_exists)
    mock_download = mocker.patch.object(LoadAPI, "download_dataset_data")
    mock_task_exists = mocker.patch.object(LoadAPI, "dataset_task_metadata_exists_in_cache", return_value=task_exists)
    mock_process = mocker.patch.object(LoadAPI, "process_dataset_task_metadata")
    mock_data_loader = mocker.patch.object(LoadAPI, "get_data_loader", return_value=["data_loader_dummy_data"])

    return {
        "data_exists": mock_data_exists,
        "download": mock_download,
        "task_exists": mock_task_exists,
        "process": mock_process,
        "data_loader": mock_data_loader
    }


def eval_run_method_calls(mocks, data_exists, task_exists):
    assert mocks
    assert data_exists is not None
    assert task_exists is not None

    assert mocks["data_exists"].called
    assert mocks["task_exists"].called
    assert mocks["data_loader"].called

    if not data_exists:
        assert mocks["download"].called
    else:
        assert not mocks["download"].called

    if not task_exists:
        assert mocks["process"].called
    else:
        assert not mocks["process"].called


class TestClassLoadAPI:
    """Unit tests for the LoadAPI class."""

    def test_init_with_all_inputs(self, mocker, mocks_init_class):
        inputs = generate_inputs_for_load()

        load_api = LoadAPI(inputs["dataset"], inputs["task"], inputs["data_dir"], inputs["verbose"])

        assert_mock_init_class(mocks_init_class)
        assert load_api.name == inputs["dataset"]
        assert load_api.task == inputs["task"]
        assert load_api.data_dir == inputs["data_dir"]
        assert load_api.verbose == inputs["verbose"]

    def test_init_with_all_inputs_named_args(self, mocker, mocks_init_class):
        inputs = generate_inputs_for_load()

        load_api = LoadAPI(name=inputs["dataset"],
                           task=inputs["task"],
                           data_dir=inputs["data_dir"],
                           verbose=inputs["verbose"])

        assert_mock_init_class(mocks_init_class)
        assert load_api.name == inputs["dataset"]
        assert load_api.task == inputs["task"]
        assert load_api.data_dir == inputs["data_dir"]
        assert load_api.verbose == inputs["verbose"]

    def test_init__raises_error_missing_inputs(self, mocker):
        with pytest.raises(TypeError):
            LoadAPI()

    @pytest.mark.parametrize("dataset, task, data_dir, verbose", [
        ('mnist', 'classification', 'some_dir', None),
        ('mnist', 'some_task', None, True),
        ('some_dataset', None, 'some_dir', False),
        (None, 'some_task', 'some_dir', False),
        (None, None, None, None)
    ])
    def test_init__raises_error_missing_some_inputs(self, mocker, dataset, task, data_dir, verbose):
        with pytest.raises(AssertionError):
            LoadAPI(dataset, task, data_dir, verbose)

    def test_init__raises_error_extra_inputs(self, mocker):
        with pytest.raises(TypeError):
            LoadAPI("some_dataset", "some_task", "some_dir", True, "extra_field")

    def test_run_dataset_data_files_and_task_exist_in_cache(self, mocker, mocks_init_class):
        inputs = generate_inputs_for_load()
        mocks = mock_run_method(mocker, data_exists=True, task_exists=True)

        load_api = LoadAPI(inputs["dataset"], inputs["task"], inputs["data_dir"], inputs["verbose"])
        data_loader = load_api.run()

        assert_mock_init_class(mocks_init_class)
        eval_run_method_calls(mocks, data_exists=True, task_exists=True)

    def test_run_dataset_data_files_exist_task_missing_in_cache(self, mocker, mocks_init_class):
        inputs = generate_inputs_for_load()
        mocks = mock_run_method(mocker, data_exists=True, task_exists=False)

        load_api = LoadAPI(inputs["dataset"], inputs["task"], inputs["data_dir"], inputs["verbose"])
        data_loader = load_api.run()

        assert_mock_init_class(mocks_init_class)
        eval_run_method_calls(mocks, data_exists=True, task_exists=False)

    def test_run_dataset_data_files_missing_task_exists_in_cache(self, mocker, mocks_init_class):
        inputs = generate_inputs_for_load()
        mocks = mock_run_method(mocker, data_exists=False, task_exists=True)

        load_api = LoadAPI(inputs["dataset"], inputs["task"], inputs["data_dir"], inputs["verbose"])
        data_loader = load_api.run()

        assert_mock_init_class(mocks_init_class)
        eval_run_method_calls(mocks, data_exists=False, task_exists=True)

    def test_run_dataset_files_and_task_missing_in_cache(self, mocker, mocks_init_class):
        inputs = generate_inputs_for_load()
        mocks = mock_run_method(mocker, data_exists=False, task_exists=False)

        load_api = LoadAPI(inputs["dataset"], inputs["task"], inputs["data_dir"], inputs["verbose"])
        data_loader = load_api.run()

        assert_mock_init_class(mocks_init_class)
        eval_run_method_calls(mocks, data_exists=False, task_exists=False)
