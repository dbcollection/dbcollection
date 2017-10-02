"""
API methods for adding a dataset to the cache.
"""

from __future__ import print_function

from dbcollection.core.cache import CacheManager


def add(name, task, data_dir, file_path, keywords=[], is_test=False):
    """Add a dataset/task to the list of available datasets for loading.

    Parameters
    ----------
    name : str
        Name of the dataset.
    task : str
        Name of the task to load.
    data_dir : str
        Path of the stored data on disk.
    file_path : bool
        Path to the metadata HDF5 file.
    keywords : list of strings, optional
        List of keywords to categorize the dataset.
    is_test : bool, optional
        Flag used for tests.

    Examples
    --------
    Add a dataset manually to dbcollection.

    >>> import dbcollection as dbc
    >>> dbc.add('new_db', 'new_task', 'new/path/db', 'newdb.h5', ['new_category'])
    >>> dbc.query('new_db')
    {'new_db': {'tasks': {'new_task': 'newdb.h5'}, 'data_dir': 'new/path/db', 'keywords': ['new_category']}}

    """
    assert name, "Must input a valid name: {}".format(name)
    assert task, "Must input a valid task: {}".format(task)
    assert data_dir, "Must input a valid data_dir: {}".format(data_dir)
    assert file_path, "Must input a valid file_path: {}".format(file_path)

    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    # update the cache for the dataset
    cache_manager.update(name, data_dir, {task: file_path}, keywords, True)
