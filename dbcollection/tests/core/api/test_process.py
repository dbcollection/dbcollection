"""
Test dbcollection core API: process.
"""


import pytest

from dbcollection.core.api.process import process, ProcessAPI


@pytest.fixture()
def mocks_init_class(mocker):
    mock_cache = mocker.patch.object(ProcessAPI, "get_cache_manager", return_value=True)
    mock_data_dir = mocker.patch.object(ProcessAPI, "get_dataset_data_dir_path", return_value='/some/path/cache/db')
    mock_cache_dir = mocker.patch.object(ProcessAPI, "get_dataset_cache_dir_path", return_value='/some/path/cache')
    mock_exists = mocker.patch.object(ProcessAPI, 'check_if_task_exists_in_database')
    return [mock_cache, mock_data_dir, mock_cache_dir, mock_exists]


def assert_mock_init_class(mocks):
    for mock in mocks:
        assert mock.called


class TestCallProcess:
    """Unit tests for the core api process method."""

    def test_call_with_dataset_name(self, mocker, mocks_init_class):
        mock_run = mocker.patch.object(ProcessAPI, "run")
        dataset = 'mnist'

        process(dataset)

        assert_mock_init_class(mocks_init_class)
        assert mock_run.called

    def test_call_with_all_inputs(self, mocker, mocks_init_class):
        mock_run = mocker.patch.object(ProcessAPI, "run")
        dataset = 'mnist'
        task = ''
        verbose = True

        process(dataset, task=task, verbose=verbose)

        assert_mock_init_class(mocks_init_class)
        assert mock_run.called

    def test_call__raises_error_no_inputs(self, mocker):
        with pytest.raises(TypeError):
            process()

    def test_call__raises_error_invalid_dataset_name(self, mocker):
        with pytest.raises(KeyError):
            process('invalid_dataset_name')


class TestClassDownloadAPI:
    """Unit tests for the DownloadAPI class."""

    def test_init_with_all_inputs(self, mocker, mocks_init_class):
        dataset = 'mnist'
        task = 'default'
        verbose = True

        process_api = ProcessAPI(dataset, task, verbose)

        assert_mock_init_class(mocks_init_class)
        assert process_api.name == dataset
        assert process_api.task == 'classification'  # default task name for mnist
        assert process_api.verbose == verbose

    def test_init__raises_error_missing_inputs(self, mocker):
        with pytest.raises(TypeError):
            ProcessAPI()

    @pytest.mark.parametrize("dataset, task, verbose", [
        ('mnist', 'classification', None),
        ('mnist', None, True),
        (None, '', False),
        ('', 'default', False),
        (None, None, None)
    ])
    def test_init__raises_error_missing_some_inputs(self, mocker, dataset, task, verbose):
        with pytest.raises(AssertionError):
            ProcessAPI(dataset, task, verbose)

    @pytest.mark.parametrize("test_task", ['classification', 'some_task', 'another_task'])
    def test_parse_task_name(self, mocker, mocks_init_class, test_task):
        process_api = ProcessAPI('mnist', test_task, True)

        assert_mock_init_class(mocks_init_class)
        assert process_api.parse_task_name(test_task) == test_task

    @pytest.mark.parametrize("test_task", ['', 'default'])
    def test_parse_task_name_to_default(self, mocker, mocks_init_class, test_task):
        process_api = ProcessAPI('mnist', '', True)

        assert_mock_init_class(mocks_init_class)
        assert process_api.parse_task_name(test_task) == "classification"

    def test_run(self, mocker, mocks_init_class):
        mock_create = mocker.patch.object(ProcessAPI, "create_dir")
        mock_process = mocker.patch.object(ProcessAPI, "process_dataset", return_value="some_info")
        mock_update = mocker.patch.object(ProcessAPI, "update_cache")
        dataset = 'mnist'
        task = 'some_task'
        verbose = True

        process_api = ProcessAPI(dataset, task, verbose)
        process_api.run()

        assert_mock_init_class(mocks_init_class)
        assert mock_create.called
        assert mock_process.return_value == "some_info"
        assert mock_update.called
