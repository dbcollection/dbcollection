"""
Test dbcollection core API: load.
"""


import pytest

from dbcollection.core.api.load import load, LoadAPI


@pytest.fixture()
def mocks_init_class(mocker):
    mock_parse = mocker.patch.object(LoadAPI, "parse_task_name", return_value=True)
    mock_cache = mocker.patch.object(LoadAPI, "get_cache_manager")
    return [mock_parse, mock_cache]


def assert_mock_init_class(mocks):
    for mock in mocks:
        assert mock.called


class TestCallLoad:
    """Unit tests for the core api load method."""

    def test_call_with_dataset_name_only(self, mocker, mocks_init_class):
        mock_run = mocker.patch.object(LoadAPI, "run", return_value=True)
        dataset = 'mnist'

        data_loader = load(dataset)

        assert_mock_init_class(mocks_init_class)
        assert mock_run.called
        assert data_loader == True

    def test_call_with_all_inputs(self, mocker, mocks_init_class):
        mock_run = mocker.patch.object(LoadAPI, "run", return_value=True)
        dataset = 'mnist'
        task = 'some_task'
        data_dir = '/some/path/'
        verbose = True

        data_loader = load(dataset, task, data_dir, verbose)

        assert_mock_init_class(mocks_init_class)
        assert mock_run.called
        assert data_loader == True

    def test_call_with_all_inputs_named_args(self, mocker, mocks_init_class):
        mock_run = mocker.patch.object(LoadAPI, "run", return_value=True)
        dataset = 'mnist'
        task = 'some_task'
        data_dir = '/some/path/'
        verbose = True

        data_loader = load(name=dataset,
                           task=task,
                           data_dir=data_dir,
                           verbose=verbose)

        assert_mock_init_class(mocks_init_class)
        assert mock_run.called
        assert data_loader == True

    def test_call__raises_error_no_inputs(self, mocker):
        with pytest.raises(TypeError):
            load()

    def test_call__raises_error_extra_inputs(self, mocker):
        with pytest.raises(TypeError):
            load("some_dataset", "some_task", "some_dir", True, "extra_field")


class TestClassLoadAPI:
    """Unit tests for the LoadAPI class."""
