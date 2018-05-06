"""
Test dbcollection core API: load.
"""


import pytest

from dbcollection.core.api.load import load, LoadAPI


@pytest.fixture()
def mocks_init_class(mocker):
    mock_parse = mocker.patch.object(LoadAPI, "parse_task_name", return_value='taskA')
    mock_cache = mocker.patch.object(LoadAPI, "get_cache_manager")
    return [mock_parse, mock_cache]


def assert_mock_init_class(mocks):
    for mock in mocks:
        assert mock.called


@pytest.fixture()
def test_data():
    return {
        "dataset": 'mnist',
        "task": 'some_task',
        "data_dir": '/some/path/',
        "verbose": True,
    }


class TestCallLoad:
    """Unit tests for the core api load method."""

    def test_call_with_all_input_args(self, mocker, mocks_init_class, test_data):
        mock_run = mocker.patch.object(LoadAPI, "run", return_value={})

        data_loader = load(test_data["dataset"],
                           test_data["task"],
                           test_data["data_dir"],
                           test_data["verbose"])

        assert_mock_init_class(mocks_init_class)
        assert mock_run.called
        assert data_loader == {}

    def test_call_with_named_input_args(self, mocker, mocks_init_class, test_data):
        mock_run = mocker.patch.object(LoadAPI, "run", return_value={})

        data_loader = load(name=test_data["dataset"],
                           task=test_data["task"],
                           data_dir=test_data["data_dir"],
                           verbose=test_data["verbose"])

        assert_mock_init_class(mocks_init_class)
        assert mock_run.called
        assert data_loader == {}

    def test_call_without_optional_input_args(self, mocker, mocks_init_class):
        mock_run = mocker.patch.object(LoadAPI, "run", return_value={})

        data_loader = load('some_dataset')

        assert_mock_init_class(mocks_init_class)
        assert mock_run.called
        assert data_loader == {}

    def test_call__raises_error_no_inputs(self, mocker):
        with pytest.raises(TypeError):
            load()

    def test_call__raises_error_extra_inputs(self, mocker):
        with pytest.raises(TypeError):
            load("some_dataset", "some_task", "some_dir", True, "extra_field")


@pytest.fixture()
def load_api_cls(mocker, mocks_init_class, test_data):
    return LoadAPI(
        name=test_data["dataset"],
        task=test_data["task"],
        data_dir=test_data["data_dir"],
        verbose=test_data["verbose"]
    )


class TestClassLoadAPI:
    """Unit tests for the LoadAPI class."""

    def test_init_with_all_input_args(self, mocker, mocks_init_class, test_data):
        load_api = LoadAPI(name=test_data["dataset"],
                           task=test_data["task"],
                           data_dir=test_data["data_dir"],
                           verbose=test_data["verbose"])

        assert_mock_init_class(mocks_init_class)
        assert load_api.name == test_data["dataset"]
        assert load_api.task == 'taskA'
        assert load_api.data_dir == test_data["data_dir"]
        assert load_api.verbose == test_data["verbose"]

    def test_init__raises_error_no_input_args(self, mocker):
        with pytest.raises(TypeError):
            LoadAPI()

    def test_init__raises_error_too_many_input_args(self, mocker, mocks_init_class, test_data):
        with pytest.raises(TypeError):
            LoadAPI(test_data['dataset'], test_data['task'], test_data['data_dir'], test_data['verbose'], 'extra_input')

    def test_init__raises_error_missing_one_input_arg(self, mocker, mocks_init_class, test_data):
        with pytest.raises(TypeError):
            LoadAPI(test_data['dataset'], test_data['task'], test_data['data_dir'])

    @pytest.mark.parametrize("test_exists_dataset, test_exists_metadata", [
        (False, False),
        (True, False),
        (False, True),
        (True, True)
    ])
    def test_run(self, mocker, load_api_cls, test_exists_dataset, test_exists_metadata):
        mock_exists_dataset = mocker.patch.object(LoadAPI, "dataset_data_exists_in_cache", return_value=test_exists_dataset)
        mock_download = mocker.patch.object(LoadAPI, "download_dataset_data")
        mock_exists_metadata = mocker.patch.object(LoadAPI, "dataset_task_metadata_exists_in_cache", return_value=test_exists_metadata)
        mock_process = mocker.patch.object(LoadAPI, "process_dataset_task_metadata")
        mock_get_loader = mocker.patch.object(LoadAPI, "get_data_loader", return_value={})

        data_loader = load_api_cls.run()

        assert mock_exists_dataset.called
        assert mock_exists_metadata.called
        if test_exists_dataset:
            assert not mock_download.called
        else:
            assert mock_download
        if test_exists_metadata:
            assert not mock_process.called
        else:
            assert mock_process
        assert mock_get_loader.called
        assert data_loader == {}

    def test_download_dataset_data(self, mocker, load_api_cls):
        mock_download = mocker.patch.object(LoadAPI, "download_dataset")
        mock_reload = mocker.patch.object(LoadAPI, "reload_cache")

        load_api_cls.download_dataset_data()

        assert mock_download.called
        assert mock_reload.called

    def test_process_dataset_task_metadata(self, mocker, load_api_cls):
        mock_process = mocker.patch.object(LoadAPI, "process_dataset")
        mock_reload = mocker.patch.object(LoadAPI, "reload_cache")

        load_api_cls.process_dataset_task_metadata()

        assert mock_process.called
        assert mock_reload.called

    def test_get_data_loader(self, mocker, load_api_cls):
        mock_data_dir = mocker.patch.object(LoadAPI, "get_data_dir_path_from_cache", return_value="/some/path/data/")
        mock_hdf5_filepath = mocker.patch.object(LoadAPI, "get_hdf5_file_path_from_cache", return_value="/some/path/to/file")
        mock_loader = mocker.patch.object(LoadAPI, "get_loader_obj", return_value=["data_loader_dummy"])

        data_loader = load_api_cls.get_data_loader()

        assert mock_data_dir.called
        assert mock_hdf5_filepath.called
        assert mock_loader.called
        assert data_loader == ["data_loader_dummy"]

    def test_get_data_dir_path_from_cache(self, mocker, load_api_cls):
        mock_get_metadata = mocker.patch.object(LoadAPI, "get_dataset_metadata", return_value={'data_dir': '/some/path/data'})

        result = load_api_cls.get_data_dir_path_from_cache()

        assert mock_get_metadata.called
        assert result == '/some/path/data'

    def test_get_hdf5_file_path_from_cache(self, mocker, load_api_cls):
        mock_get_metadata = mocker.patch.object(LoadAPI, "get_task_metadata", return_value={'filename': '/some/path/cache/task.h5'})

        result = load_api_cls.get_hdf5_file_path_from_cache()

        assert mock_get_metadata.called
        assert result == '/some/path/cache/task.h5'
