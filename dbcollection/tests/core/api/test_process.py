"""
Test dbcollection core API: process.
"""


import pytest

from dbcollection.core.api.process import process, ProcessAPI


class TestCallProcess:
    """Unit tests for the core api process method."""

    def test_call_with_dataset_name(self, mocker):
        mock_cache = mocker.patch.object(ProcessAPI, "get_cache_manager", return_value=True)
        mock_task_exists = mocker.patch.object(ProcessAPI, "check_if_task_exists")
        mock_run = mocker.patch.object(ProcessAPI, "run")
        dataset = 'mnist'

        process(dataset)

        assert mock_cache.called
        assert mock_task_exists.called
        assert mock_run.called

    def test_call_with_all_inputs(self, mocker):
        mock_cache = mocker.patch.object(ProcessAPI, "get_cache_manager", return_value=True)
        mock_task_exists = mocker.patch.object(ProcessAPI, "check_if_task_exists")
        mock_run = mocker.patch.object(ProcessAPI, "run")
        dataset = 'mnist'
        task = ''
        verbose = True

        process(dataset, task=task, verbose=verbose)

        assert mock_cache.called
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
