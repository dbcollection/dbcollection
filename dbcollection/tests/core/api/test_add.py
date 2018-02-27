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
        "categories": ['categoryA', 'categoryB', 'categoryC'],
        "verbose": True
    }


class TestCallAdd:
    """Unit tests for the core api add method."""

    def test_call(self, mocker, mocks_init_class, test_data):
        mock_run = mocker.patch.object(AddAPI, "run")

        add(test_data['dataset'], test_data['task'], test_data['data_dir'],
            test_data['hdf5_filename'], test_data['categories'], test_data['verbose'])

        assert_mock_call(mocks_init_class)
        assert mock_run.called

    def test_call_with_named_args(self, mocker, mocks_init_class, test_data):
        mock_run = mocker.patch.object(AddAPI, "run")

        add(name=test_data['dataset'],
            task=test_data['task'],
            data_dir=test_data['data_dir'],
            hdf5_filename=test_data['hdf5_filename'],
            categories=test_data['categories'],
            verbose=test_data['verbose'])

        assert_mock_call(mocks_init_class)
        assert mock_run.called

    def test_call_without_optional_inputs(self, mocker, mocks_init_class, test_data):
        mock_run = mocker.patch.object(AddAPI, "run")

        add(test_data['dataset'], test_data['task'], test_data['data_dir'], test_data['hdf5_filename'])

        assert_mock_call(mocks_init_class)
        assert mock_run.called

    def test_call__raises_error_missing_inputs(self, mocker):
        with pytest.raises(TypeError):
            add("db", "task", "data dir", "filename", [], False, 'extra field')


class TestClassAddAPI:
    """Unit tests for the AddAPI class."""
