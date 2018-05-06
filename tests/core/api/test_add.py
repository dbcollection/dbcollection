"""
Test dbcollection core API: add.
"""


import pytest

from dbcollection.core.api.add import add, AddAPI


@pytest.fixture()
def mocks_init_class(mocker):
    mock_cache = mocker.patch.object(AddAPI, "get_cache_manager", return_value=True)
    return [mock_cache]


def assert_mock_call(mocks):
    for mock in mocks:
        assert mock.called


@pytest.fixture()
def test_data():
    return {
        "dataset": 'some_db',
        "task": "taskA",
        "data_dir": '/some/dir/data',
        "hdf5_filename": '/some/dir/db/hdf5_file.h5',
        "categories": ('categoryA', 'categoryB', 'categoryC'),
        "verbose": True,
        "force_overwrite": False
    }


class TestCallAdd:
    """Unit tests for the core api add method."""

    def test_call_with_all_input_args(self, mocker, mocks_init_class, test_data):
        mock_run = mocker.patch.object(AddAPI, "run")

        add(test_data['dataset'],
            test_data['task'],
            test_data['data_dir'],
            test_data['hdf5_filename'],
            test_data['categories'],
            test_data['verbose'],
            test_data['force_overwrite'])

        assert_mock_call(mocks_init_class)
        assert mock_run.called

    def test_call_with_named_input_args(self, mocker, mocks_init_class, test_data):
        mock_run = mocker.patch.object(AddAPI, "run")

        add(name=test_data['dataset'],
            task=test_data['task'],
            data_dir=test_data['data_dir'],
            hdf5_filename=test_data['hdf5_filename'],
            categories=test_data['categories'],
            verbose=test_data['verbose'],
            force_overwrite=test_data['force_overwrite'])

        assert_mock_call(mocks_init_class)
        assert mock_run.called

    def test_call_without_optional_input_args(self, mocker, mocks_init_class, test_data):
        mock_run = mocker.patch.object(AddAPI, "run")

        add(test_data['dataset'], test_data['task'], test_data['data_dir'], test_data['hdf5_filename'])

        assert_mock_call(mocks_init_class)
        assert mock_run.called

    def test_call__raises_error_no_inputs(self, mocker):
        with pytest.raises(TypeError):
            add("db", "task", "data dir")

    def test_call__raises_error_extra_inputs(self, mocker):
        with pytest.raises(TypeError):
            add("db", "task", "data dir", "filename", [], False, False, 'extra field')


@pytest.fixture()
def add_api_cls(mocker, mocks_init_class, test_data):
    return AddAPI(
        name=test_data['dataset'],
        task=test_data['task'],
        data_dir=test_data['data_dir'],
        hdf5_filename=test_data['hdf5_filename'],
        categories=test_data['categories'],
        verbose=test_data['verbose'],
        force_overwrite=test_data['force_overwrite'],
    )


class TestClassAddAPI:
    """Unit tests for the AddAPI class."""

    def test_init_with_all_input_args(self, mocker, mocks_init_class, test_data):
        add_api = AddAPI(name=test_data['dataset'],
                         task=test_data['task'],
                         data_dir=test_data['data_dir'],
                         hdf5_filename=test_data['hdf5_filename'],
                         categories=test_data['categories'],
                         verbose=test_data['verbose'],
                         force_overwrite=test_data['force_overwrite'])

        assert_mock_call(mocks_init_class)
        assert add_api.name == test_data['dataset']
        assert add_api.task == test_data['task']
        assert add_api.data_dir == test_data['data_dir']
        assert add_api.hdf5_filename == test_data['hdf5_filename']
        assert add_api.categories == test_data['categories']
        assert add_api.verbose == test_data['verbose']
        assert add_api.force_overwrite == test_data['force_overwrite']

    def test_init__raises_error_no_input_args(self, mocker):
        with pytest.raises(TypeError):
            AddAPI()

    def test_init__raises_error_too_many_input_args(self, mocker):
        with pytest.raises(TypeError):
            AddAPI("db", "task", "data dir", "filename", [], False, True, 'extra field')

    def test_init__raises_error_missing_one_input_arg(self, mocker):
        with pytest.raises(TypeError):
            AddAPI("db", "data dir", "filename", [], False, True)

    def test_run(self, mocker, add_api_cls):
        mock_add = mocker.patch.object(AddAPI, "add_dataset_to_cache")

        add_api_cls.run()

        assert mock_add.called

    def test_run__raises_error_if_method_called_with_inputs(self, mocker, add_api_cls):
        with pytest.raises(TypeError):
            add_api_cls.run('some input')

    def test_add_dataset_to_cache__dataset_exists(self, mocker, add_api_cls):
        mock_exists = mocker.patch.object(AddAPI, "dataset_exists_in_cache", return_value=True)
        mock_update_cache = mocker.patch.object(AddAPI, "update_dataset_cache_data")
        mock_add_task = mocker.patch.object(AddAPI, "add_task_to_cache")

        add_api_cls.add_dataset_to_cache()

        assert mock_exists.called
        assert mock_update_cache.called
        assert mock_add_task.called

    def test_add_dataset_to_cache__dataset_does_not_exist(self, mocker, add_api_cls):
        mock_exists = mocker.patch.object(AddAPI, "dataset_exists_in_cache", return_value=False)
        mock_add_new = mocker.patch.object(AddAPI, "add_new_data_to_cache")

        add_api_cls.add_dataset_to_cache()

        assert mock_exists.called
        assert mock_add_new.called

    def test_add_task_to_cache__task_exists(self, mocker, add_api_cls):
        mock_exists = mocker.patch.object(AddAPI, "check_if_task_exists_in_cache", return_value=True)
        mock_update_task = mocker.patch.object(AddAPI, "update_task_entry_in_cache")
        mock_add_task = mocker.patch.object(AddAPI, "add_task_entry_to_cache")

        add_api_cls.force_overwrite = True
        add_api_cls.add_task_to_cache()

        assert mock_exists.called
        assert mock_update_task.called
        assert not mock_add_task.called

    def test_add_task_to_cache__task_exists_raises_exception(self, mocker, add_api_cls):
        mock_exists = mocker.patch.object(AddAPI, "check_if_task_exists_in_cache", return_value=True)
        mock_update_task = mocker.patch.object(AddAPI, "update_task_entry_in_cache")
        mock_add_task = mocker.patch.object(AddAPI, "add_task_entry_to_cache")

        add_api_cls.force_overwrite = False
        with pytest.raises(Exception):
            add_api_cls.add_task_to_cache()

        assert mock_exists.called
        assert not mock_update_task.called
        assert not mock_add_task.called

    def test_add_task_to_cache__task_does_not_exist(self, mocker, add_api_cls):
        mock_exists = mocker.patch.object(AddAPI, "check_if_task_exists_in_cache", return_value=False)
        mock_update_task = mocker.patch.object(AddAPI, "update_task_entry_in_cache")
        mock_add_task = mocker.patch.object(AddAPI, "add_task_entry_to_cache")

        add_api_cls.add_task_to_cache()

        assert mock_exists.called
        assert not mock_update_task.called
        assert mock_add_task.called
