"""
Test dbcollection core API: remove.
"""


import pytest

from dbcollection.core.api.remove import remove, RemoveAPI


@pytest.fixture()
def mocks_init_class(mocker):
    mock_cache = mocker.patch.object(RemoveAPI, "get_cache_manager", return_value=True)
    return [mock_cache]


def assert_mock_call(mocks):
    for mock in mocks:
        assert mock.called


@pytest.fixture()
def test_data():
    return {
        "dataset": 'some_db',
        "task": "taskA",
        "delete_data": False,
        "verbose": True,
    }


class TestCallRemove:
    """Unit tests for the core api remove method."""

    def test_call_with_all_input_args(self, mocker, mocks_init_class, test_data):
        mock_run = mocker.patch.object(RemoveAPI, 'run')

        remove(test_data['dataset'],
               test_data['task'],
               test_data['delete_data'],
               test_data['verbose'])

        assert_mock_call(mocks_init_class)
        assert mock_run.called

    def test_call_with_named_input_args(self, mocker, mocks_init_class, test_data):
        mock_run = mocker.patch.object(RemoveAPI, 'run')

        remove(name=test_data['dataset'],
               task=test_data['task'],
               delete_data=test_data['delete_data'],
               verbose=test_data['verbose'])

        assert_mock_call(mocks_init_class)
        assert mock_run.called

    def test_call_without_optional_input_args(self, mocker, mocks_init_class):
        mock_run = mocker.patch.object(RemoveAPI, 'run')

        remove('datasetX')

        assert_mock_call(mocks_init_class)
        assert mock_run.called

    def test_call__raises_error_no_input_args(self, mocker):
        with pytest.raises(TypeError):
            remove()

    def test_call__raises_error_too_many_args(self, mocker, test_data):
        with pytest.raises(TypeError):
            remove(test_data['dataset'], test_data['task'], test_data['delete_data'], test_data['verbose'], 'extra_input')


@pytest.fixture()
def remove_api_cls(mocker, mocks_init_class, test_data):
    return RemoveAPI(
        name=test_data['dataset'],
        task=test_data['task'],
        delete_data=test_data['delete_data'],
        verbose=test_data['verbose']
    )


class TestClassRemoveAPI:
    """Unit tests for the RemoveAPI class."""

    def test_init_with_all_input_args(self, mocker, mocks_init_class, test_data):
        remove_api = RemoveAPI(name=test_data['dataset'],
                               task=test_data['task'],
                               delete_data=test_data['delete_data'],
                               verbose=test_data['verbose'])

        assert_mock_call(mocks_init_class)
        assert remove_api.name == test_data['dataset']
        assert remove_api.task == test_data['task']
        assert remove_api.delete_data == test_data['delete_data']
        assert remove_api.verbose == test_data['verbose']

    def test_init__raises_error_no_input_args(self, mocker, mocks_init_class, test_data):
        with pytest.raises(TypeError):
            RemoveAPI()

    def test_init__raises_error_too_many_input_args(self, mocker, mocks_init_class, test_data):
        with pytest.raises(TypeError):
            RemoveAPI(test_data['dataset'], test_data['task'], test_data['delete_data'], test_data['verbose'], 'extra_input')

    def test_init__raises_error_missing_one_input_arg(self, mocker, mocks_init_class, test_data):
        with pytest.raises(TypeError):
            RemoveAPI(test_data['dataset'], test_data['task'], test_data['delete_data'])

    def test_run(self, mocker, remove_api_cls):
        mock_remove_db = mocker.patch.object(RemoveAPI, 'remove_dataset')

        remove_api_cls.run()

        assert mock_remove_db.called

    def test_remove_dataset_exists_dataset(self, mocker, remove_api_cls):
        mock_exists_db = mocker.patch.object(RemoveAPI, 'exists_dataset', return_value=True)
        mock_remove_registry = mocker.patch.object(RemoveAPI, 'remove_registry_from_cache')

        remove_api_cls.remove_dataset()

        assert mock_exists_db.called
        assert mock_remove_registry.called

    def test_remove_dataset_does_not_exist_dataset(self, mocker, remove_api_cls):
        mock_exists_db = mocker.patch.object(RemoveAPI, 'exists_dataset', return_value=True)

        with pytest.raises(Exception):
            remove_api_cls.remove_dataset()

        assert mock_exists_db.called

    def test_remove_registry_from_cache_exists_task(self, mocker, remove_api_cls):
        mock_remove_task = mocker.patch.object(RemoveAPI, 'remove_task_registry')
        mock_remove_db = mocker.patch.object(RemoveAPI, 'remove_dataset_registry')

        remove_api_cls.remove_registry_from_cache()

        assert mock_remove_task.called
        assert not mock_remove_db.called

    def test_remove_registry_from_cache_task_is_empty(self, mocker, remove_api_cls):
        mock_remove_task = mocker.patch.object(RemoveAPI, 'remove_task_registry')
        mock_remove_db = mocker.patch.object(RemoveAPI, 'remove_dataset_registry')

        remove_api_cls.task = ''
        remove_api_cls.remove_registry_from_cache()

        assert not mock_remove_task.called
        assert mock_remove_db.called

    def test_remove_dataset_registry(self, mocker, remove_api_cls):
        mock_remove_files = mocker.patch.object(RemoveAPI, 'remove_dataset_data_files_from_disk')
        mock_remove_cache = mocker.patch.object(RemoveAPI, 'remove_dataset_entry_from_cache')

        remove_api_cls.delete_data = False
        remove_api_cls.remove_dataset_registry()

        assert not mock_remove_files.called
        assert mock_remove_cache.called

    def test_remove_dataset_registry_and_data_files(self, mocker, remove_api_cls):
        mock_remove_files = mocker.patch.object(RemoveAPI, 'remove_dataset_data_files_from_disk')
        mock_remove_cache = mocker.patch.object(RemoveAPI, 'remove_dataset_entry_from_cache')

        remove_api_cls.delete_data = True
        remove_api_cls.remove_dataset_registry()

        assert mock_remove_files.called
        assert mock_remove_cache.called

    def test_remove_dataset_data_files_from_disk(self, mocker, remove_api_cls):
        mock_get_dir = mocker.patch.object(RemoveAPI, 'get_dataset_data_dir', return_value='/some/dir/path')
        mock_rmtree = mocker.patch('shutil.rmtree')

        remove_api_cls.remove_dataset_data_files_from_disk()

        assert mock_get_dir.called
        assert mock_rmtree.called
