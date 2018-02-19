"""
Test dbcollection core API: load.
"""


import pytest

from dbcollection.core.api.load import load, LoadAPI


@pytest.fixture()
def mocks_init_class(mocker):
    mock_parse = mocker.patch.object(LoadAPI, "parse_task_name", return_value=True)
    mock_cache = mocker.patch.object(LoadAPI, "get_cache_manager")
    mock_run = mocker.patch.object(LoadAPI, "run", return_value=True)
    return [mock_parse, mock_cache, mock_run]


def assert_mock_init_class(mocks):
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

    def test_call_with_dataset_name_only(self, mocker, mocks_init_class):
        inputs = generate_inputs_for_load()

        data_loader = load(inputs["dataset"])

        assert_mock_init_class(mocks_init_class)
        assert data_loader == True

    def test_call_with_all_inputs(self, mocker, mocks_init_class):
        inputs = generate_inputs_for_load()

        data_loader = load(inputs["dataset"], inputs["task"], inputs["data_dir"], inputs["verbose"])

        assert_mock_init_class(mocks_init_class)
        assert data_loader == True

    def test_call_with_all_inputs_named_args(self, mocker, mocks_init_class):
        inputs = generate_inputs_for_load()

        data_loader = load(name=inputs["dataset"],
                           task=inputs["task"],
                           data_dir=inputs["data_dir"],
                           verbose=inputs["verbose"])

        assert_mock_init_class(mocks_init_class)
        assert data_loader == True

    def test_call__raises_error_no_inputs(self, mocker):
        with pytest.raises(TypeError):
            load()

    def test_call__raises_error_extra_inputs(self, mocker):
        with pytest.raises(TypeError):
            load("some_dataset", "some_task", "some_dir", True, "extra_field")


class TestClassLoadAPI:
    """Unit tests for the LoadAPI class."""

    def test_init_with_all_inputs(self, mocker):
        inputs = generate_inputs_for_load()
        mock_parse = mocker.patch.object(LoadAPI, "parse_task_name", return_value=inputs["task"])
        mock_cache = mocker.patch.object(LoadAPI, "get_cache_manager")

        load_api = LoadAPI(inputs["dataset"], inputs["task"], inputs["data_dir"], inputs["verbose"])

        assert mock_parse.called
        assert mock_cache.called
        assert load_api.name == inputs["dataset"]
        assert load_api.task == inputs["task"]
        assert load_api.data_dir == inputs["data_dir"]
        assert load_api.verbose == inputs["verbose"]

    def test_init_with_all_inputs_named_args(self, mocker):
        inputs = generate_inputs_for_load()
        mock_parse = mocker.patch.object(LoadAPI, "parse_task_name", return_value=inputs["task"])
        mock_cache = mocker.patch.object(LoadAPI, "get_cache_manager")

        load_api = LoadAPI(name=inputs["dataset"],
                           task=inputs["task"],
                           data_dir=inputs["data_dir"],
                           verbose=inputs["verbose"])

        assert mock_parse.called
        assert mock_cache.called
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
