"""
Test dbcollection core API: process.
"""


import pytest

from dbcollection.core.api.process import process, ProcessAPI


class TestCallProcess:
    """Unit tests for the core api process method."""

    def test_call_with_dataset_name(self, mocker):
        mock_cache = mocker.patch.object(ProcessAPI, "get_cache_manager", return_value=True)
        mock_data_dir = mocker.patch.object(ProcessAPI, "get_dataset_data_dir_path", return_value='/some/path/cache/db')
        mock_cache_dir = mocker.patch.object(ProcessAPI, "get_dataset_cache_dir_path", return_value='/some/path/cache')
        mock_task_exists = mocker.patch.object(ProcessAPI, "check_if_task_exists_in_database")
        mock_run = mocker.patch.object(ProcessAPI, "run")
        dataset = 'mnist'

        process(dataset)

        assert mock_cache.called
        assert mock_data_dir.called
        assert mock_cache_dir.called
        assert mock_task_exists.called
        assert mock_run.called

    def test_call_with_all_inputs(self, mocker):
        mock_cache = mocker.patch.object(ProcessAPI, "get_cache_manager", return_value=True)
        mock_data_dir = mocker.patch.object(ProcessAPI, "get_dataset_data_dir_path", return_value='/some/path/cache/db')
        mock_cache_dir = mocker.patch.object(ProcessAPI, "get_dataset_cache_dir_path", return_value='/some/path/cache')
        mock_task_exists = mocker.patch.object(ProcessAPI, "check_if_task_exists_in_database")
        mock_run = mocker.patch.object(ProcessAPI, "run")
        dataset = 'mnist'
        task = ''
        verbose = True

        process(dataset, task=task, verbose=verbose)

        assert mock_cache.called
        assert mock_data_dir.called
        assert mock_cache_dir.called
        assert mock_task_exists.called
        assert mock_run.called

    def test_call__raises_error_no_inputs(self, mocker):
        with pytest.raises(TypeError):
            process()

    def test_call__raises_error_invalid_dataset_name(self, mocker):
        with pytest.raises(AssertionError):
            process('invalid_dataset_name')


class TestClassDownloadAPI:
    """Unit tests for the DownloadAPI class."""

    def test_init_with_all_inputs(self, mocker):
        mock_cache = mocker.patch.object(ProcessAPI, "get_cache_manager", return_value=True)
        mock_data_dir = mocker.patch.object(ProcessAPI, "get_dataset_data_dir_path", return_value='/some/path/cache/db')
        mock_cache_dir = mocker.patch.object(ProcessAPI, "get_dataset_cache_dir_path", return_value='/some/path/cache')
        dataset = 'mnist'
        task = 'default'
        verbose = True

        process_api = ProcessAPI(dataset, task, verbose)

        assert mock_cache.called
        assert mock_data_dir.called
        assert mock_cache_dir.called
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
