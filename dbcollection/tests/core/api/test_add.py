"""
Test dbcollection core API: add.
"""


import pytest

from dbcollection.core.api.add import add, AddAPI


class TestCallAdd:
    """Unit tests for the core api add method."""

    def test_call_add(self, mocker):
        mock_cache = mocker.patch.object(AddAPI, "get_cache_manager", return_value=True)
        mock_run = mocker.patch.object(AddAPI, "run")
        dataset = 'some_db'
        task = 'taskA'
        data_dir = '/some/dir/data'
        hdf5_filename = '/some/dir/db/hdf5_file.h5'
        categories = ['categoryA', 'categoryB', 'categoryC']
        verbose = True

        add(dataset, task, data_dir, hdf5_filename, categories, verbose)

        assert mock_cache.called
        assert mock_run.called

class TestClassAddAPI:
    """Unit tests for the AddAPI class."""
