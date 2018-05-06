"""
Test dbcollection core API: process.
"""


import os
import pytest

from dbcollection.core.api.process import process, ProcessAPI


@pytest.fixture()
def mocks_init_class(mocker):
    mock_cache = mocker.patch.object(ProcessAPI, "get_cache_manager", return_value=True)
    return [mock_cache]


def assert_mock_init_class(mocks):
    for mock in mocks:
        assert mock.called


@pytest.fixture()
def test_data():
    return {
        "dataset": 'some_dataset',
        "task": 'some_task',
        "verbose": False
    }


class TestCallProcess:
    """Unit tests for the core api process method."""

    def test_call_with_all_input_args(self, mocker, mocks_init_class, test_data):
        mock_run = mocker.patch.object(ProcessAPI, "run")

        process(test_data["dataset"], test_data["task"], test_data["verbose"])

        assert_mock_init_class(mocks_init_class)
        assert mock_run.called

    def test_call_with_named_input_args(self, mocker, mocks_init_class, test_data):
        mock_run = mocker.patch.object(ProcessAPI, "run")

        process(name=test_data["dataset"],
                task=test_data["task"],
                verbose=test_data["verbose"])

        assert_mock_init_class(mocks_init_class)
        assert mock_run.called

    def test_call_without_optional_input_args(self, mocker,  mocks_init_class, test_data):
        mock_run = mocker.patch.object(ProcessAPI, "run")

        process('some_dataset')

        assert_mock_init_class(mocks_init_class)
        assert mock_run.called

    def test_call__raises_error_no_inputs(self, mocker):
        with pytest.raises(TypeError):
            process()

    def test_call__raises_error_too_many_args(self, mocker):
        with pytest.raises(TypeError):
            process('some_dataset', 'some_task', True, 'extra_field')


@pytest.fixture()
def process_api_cls(mocker, mocks_init_class, test_data):
    return ProcessAPI(
        name=test_data['dataset'],
        task=test_data['task'],
        verbose=test_data['verbose']
    )


class TestClassProcessAPI:
    """Unit tests for the ProcessAPI class."""

    def test_init_with_all_input_args(self, mocker, mocks_init_class, test_data):
        process_api = ProcessAPI(name=test_data['dataset'],
                                 task=test_data['task'],
                                 verbose=test_data['verbose'])

        assert_mock_init_class(mocks_init_class)
        assert process_api.name == test_data["dataset"]
        assert process_api.task == test_data["task"]
        assert process_api.verbose == test_data["verbose"]

    def test_init__raises_error_no_input_args(self, mocker, mocks_init_class, test_data):
        with pytest.raises(TypeError):
            ProcessAPI()

    def test_init__raises_error_too_many_input_args(self, mocker, mocks_init_class, test_data):
        with pytest.raises(TypeError):
            ProcessAPI(test_data['dataset'], test_data['task'], test_data['verbose'], 'extra_input')

    def test_init__raises_error_missing_one_input_arg(self, mocker, mocks_init_class, test_data):
        with pytest.raises(TypeError):
            ProcessAPI(test_data['dataset'], test_data['task'])

    def test_run(self, mocker, process_api_cls):
        mock_set_dirs = mocker.patch.object(ProcessAPI, "set_dirs_processed_metadata")
        mock_process = mocker.patch.object(ProcessAPI, "process_dataset", return_value={'dummy': 'data'})
        mock_update = mocker.patch.object(ProcessAPI, "update_cache")

        process_api_cls.run()

        assert mock_set_dirs.called
        assert mock_process.called
        assert mock_update.called

    def test_set_dirs_processed_metadata(self, mocker, process_api_cls):
        mock_get_dir = mocker.patch.object(ProcessAPI, "get_dataset_cache_dir_path", return_value='/path/dir/cache')
        mock_create_dir = mocker.patch.object(ProcessAPI, "create_dir")

        process_api_cls.set_dirs_processed_metadata()

        assert mock_get_dir.called
        assert mock_create_dir.called

    def test_get_dataset_cache_dir_path(self, mocker, process_api_cls):
        mock_get_dir = mocker.patch.object(ProcessAPI, "get_cache_dir_path_from_cache", return_value='/path/dir/cache')

        result = process_api_cls.get_dataset_cache_dir_path()

        assert mock_get_dir.called
        assert result == os.path.join('/path/dir/cache', process_api_cls.name)

    def test_process_dataset(self, mocker, process_api_cls):
        mock_data_dir = mocker.patch.object(ProcessAPI, 'get_dataset_data_dir_path', return_value='/some/path/data/dir')
        mock_cache_dir = mocker.patch.object(ProcessAPI, 'get_dataset_cache_dir_path', return_value='/some/path/cache/dir')
        mock_parse_task = mocker.patch.object(ProcessAPI, "parse_task_name", return_value='correct_task')
        mock_check_exists = mocker.patch.object(ProcessAPI, "check_if_task_exists_in_database")
        mock_process_metadata = mocker.patch.object(ProcessAPI, "process_dataset_metadata", return_value={})

        result = process_api_cls.process_dataset()

        assert mock_data_dir.called
        assert mock_cache_dir.called
        assert mock_parse_task.called
        assert mock_check_exists.called
        assert mock_process_metadata.called
        assert result == {}

    def test_get_dataset_data_dir_path(self, mocker, process_api_cls):
        mock_get_metadata = mocker.patch.object(ProcessAPI, "get_dataset_metadata_from_cache", return_value={'data_dir': '/some/dir/path'})

        result = process_api_cls.get_dataset_data_dir_path()

        assert mock_get_metadata.called
        assert result == '/some/dir/path'

    @pytest.mark.parametrize("task", ['', 'default', 'classification', 'recognition', 'another_task'])
    def test_parse_task_name(self, mocker, process_api_cls, task):
        mock_get_default = mocker.patch.object(ProcessAPI, "get_default_task", return_value='default_task')

        result = process_api_cls.parse_task_name(task)

        if not (task == '' or task == 'default'):
            assert not mock_get_default.called
            assert result == task
        else:
            assert mock_get_default.called
            assert result == 'default_task'

    def test_get_default_task(self, mocker, process_api_cls):
        mock_get_metadata = mocker.patch.object(ProcessAPI, "get_dataset_metadata_obj", return_value=mocker.MagicMock())

        process_api_cls.get_default_task()

        assert mock_get_metadata.called

    def test_check_if_task_exists_in_database__dataset_exists(self, mocker, process_api_cls):
        mock_exists = mocker.patch.object(ProcessAPI, "exists_task", return_value=True)

        process_api_cls.check_if_task_exists_in_database('some_task')

        assert mock_exists.called

    def test_check_if_task_exists_in_database__dataset_does_not_exist(self, mocker, process_api_cls):
        mock_exists = mocker.patch.object(ProcessAPI, "exists_task", return_value=False)

        with pytest.raises(KeyError):
            process_api_cls.check_if_task_exists_in_database('invalid_task')

        assert mock_exists.called

    def test_process_dataset_metadata(self, mocker, process_api_cls):
        mock_constructor = mocker.patch.object(ProcessAPI, "get_dataset_constructor", return_value=mocker.MagicMock())

        result = process_api_cls.process_dataset_metadata('/some/path/data', '/some/path/cache', 'taskA')

        assert mock_constructor.called
