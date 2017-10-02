"""
API methods for loading the metadata of processed datasets.
"""

from __future__ import print_function
import os

from dbcollection.core.db import fetch_list_datasets
from dbcollection.core.download import download
from dbcollection.core.process import process
from dbcollection.core.cache import CacheManager
from dbcollection.core.loader import DatasetLoader


def load(name=None, task='default', data_dir=None, verbose=True, is_test=False):
    """Returns a metadata loader of a dataset.

    Returns a loader with the necessary functions to manage the selected dataset.

    Parameters
    ----------
    name : str
        Name of the dataset.
    task : str, optional
        Name of the task to load.
    data_dir : str, optional
        Directory path to store the downloaded data.
	verbose : bool, optional
        Displays text information (if true).
    is_test : bool, optional
        Flag used for tests.

    Returns
    -------
    DatasetLoader
       Data loader class.

    Raises
    ------
    Exception
        If dataset is not available for loading.

    Examples
    --------
    Load the MNIST dataset.

    >>> import dbcollection as dbc
    >>> mnist = dbc.load('mnist')
    >>> print('Dataset name: ', mnist.name)
    Dataset name:  mnist

    """
    assert not name is None, 'Must input a valid dataset name: {}'.format(name)

    available_datasets_list = fetch_list_datasets()

    # check if the dataset name exists in the list of available dataset for download
    assert name in available_datasets_list, 'Invalid dataset name: {}'.format(name)

    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    # check if dataset exists. If not attempt to download the dataset
    if not cache_manager.exists_dataset(name):
        download(name, data_dir, True, verbose, is_test)
        cache_manager = CacheManager(is_test) # reopen the cache file

    # check if the task exists inf cache
    if not cache_manager.exists_task(name, task):
        process(name, task, verbose, is_test)
        cache_manager = CacheManager(is_test) # reopen the cache file

    # get data + cache dir paths
    dset_paths = cache_manager.get_dataset_storage_paths(name)

    # get task cache file path
    if task=='' or task=='default':
        task = available_datasets_list[name]['default_task']
    task_cache_path = cache_manager.get_cache_path(name, task)

    # Create a loader
    dataset_loader = DatasetLoader(name, task, dset_paths['data_dir'], task_cache_path)

    # return Loader
    return dataset_loader
