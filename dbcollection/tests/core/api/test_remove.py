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

    def test_call(self, mocker, mocks_init_class, test_data):
        mock_run = mocker.patch.object(RemoveAPI, 'run')

        remove(test_data['dataset'], test_data['task'], test_data['delete_data'], test_data['verbose'])

        assert_mock_call(mocks_init_class)
        assert mock_run.called

    def test_call_with_named_args(self, mocker, mocks_init_class, test_data):
        mock_run = mocker.patch.object(RemoveAPI, 'run')

        remove(name=test_data['dataset'],
               task=test_data['task'],
               delete_data=test_data['delete_data'],
               verbose=test_data['verbose'])

        assert_mock_call(mocks_init_class)
        assert mock_run.called

    def test_call_without_optional_args(self, mocker, mocks_init_class, test_data):
        mock_run = mocker.patch.object(RemoveAPI, 'run')

        remove(test_data['dataset'])

        assert_mock_call(mocks_init_class)
        assert mock_run.called

    def test_call__raises_error_missing_args(self, mocker):
        with pytest.raises(TypeError):
            remove()

    def test_call__raises_error_too_many_args(self, mocker, test_data):
        with pytest.raises(TypeError):
            remove(test_data['dataset'], test_data['task'], test_data['delete_data'], test_data['verbose'], 'extra_input')

class TestClassRemoveAPI:
    """Unit tests for the RemoveAPI class."""
