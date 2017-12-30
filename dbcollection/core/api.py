"""
API methods for managing datasets.

This module contains several methods for easy management of datasets. These include methods for:

- downloading datasets' data files from online sources (urls)
- processing/parsing data files + annotations into a HDF5 file to store metadata information
- loading dataset's metadata into a data loader object
- add/remove datasets to/from cache
- managing the cache file
- querying the cache file for some dataset/keyword
- displaying information about available datasets in cache or for download

These methods compose the core API for dealing with dataset management.
Users should be able to take advantage of most functionality by using only these
functions to manage and query their datasets in a simple and easy way.
"""


from __future__ import print_function
import os
import sys
import shutil
import pkgutil
import json

import dbcollection.datasets as datasets
from dbcollection.core.cache import CacheManager
from dbcollection.core.loader import DataLoader

from .download import DownloadAPI
from .process import ProcessAPI
from .load import LoadAPI
from .add import AddAPI
from .remove import RemoveAPI
from .config_cache import ConfigAPI
from .query import QueryAPI
from .info import InfoAPI

from .list_datasets import fetch_list_datasets


def check_if_dataset_name_is_valid(name):
    """Check if the dataset name exists (is valid) in the list of available dataset for download"""
    available_datasets_list = fetch_list_datasets()
    assert name in available_datasets_list, 'Invalid dataset name: {}'.format(name)


def download(name, data_dir=None, extract_data=True, verbose=True, is_test=False):
    """Download a dataset data to disk.

    This method will download a dataset's data files to disk. After download,
    it updates the cache file with the  dataset's name and path where the data
    is stored.

    Parameters
    ----------
    name : str
        Name of the dataset.
    data_dir : str, optional
        Directory path to store the downloaded data.
    extract_data : bool, optional
        Extracts/unpacks the data files (if true).
    verbose : bool, optional
        Displays text information (if true).
    is_test : bool, optional
        Flag used for tests.

    Examples
    --------
    Download the CIFAR10 dataset to disk.

    >>> import dbcollection as dbc
    >>> dbc.download('cifar10')

    """
    assert name, 'Must input a valid dataset name: {}'.format(name)
    check_if_dataset_name_is_valid(name)

    downloader = DownloadAPI(name=name,
                             data_dir=data_dir,
                             extract_data=extract_data,
                             verbose=verbose,
                             is_test=is_test)

    downloader.run()

    if verbose:
        print('==> Dataset download complete.')


def process(name, task='default', verbose=True, is_test=False):
    """Process a dataset's metadata and stores it to file.

    The data is stored a a HSF5 file for each task composing the dataset's tasks.

    Parameters
    ----------
    name : str
        Name of the dataset.
    task : str, optional
        Name of the task to process.
    verbose : bool, optional
        Displays text information (if true).
    is_test : bool, optional
        Flag used for tests.

    Raises
    ------
    KeyError
        If a task does not exist for a dataset.

    Examples
    --------
    Download the CIFAR10 dataset to disk.

    >>> import dbcollection as dbc
    >>> dbc.process('cifar10', task='classification', verbose=False)

    """
    assert name, 'Must input a valid dataset name: {}'.format(name)
    check_if_dataset_name_is_valid(name)

    processer = ProcessAPI(name=name,
                           task=task,
                           verbose=verbose,
                           is_test=is_test)

    processer.run()

    if verbose:
        print('==> Dataset processing complete.')


def load(name, task='default', data_dir=None, verbose=True, is_test=False):
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
    DataLoader
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
    >>> print('Dataset name: ', mnist.db_name)
    Dataset name:  mnist

    """
    assert name, 'Must input a valid dataset name: {}'.format(name)
    check_if_dataset_name_is_valid(name)

    loader = LoadAPI(name=name,
                     task=task,
                     data_dir=data_dir,
                     verbose=verbose,
                     is_test=is_test)

    data_loader = loader.run()

    if verbose:
        print('==> Dataset loading complete.')

    return data_loader


def add(name, task, data_dir, file_path, keywords=(), verbose=True, is_test=False):
    """Add a dataset/task to the list of available datasets for loading.

    Parameters
    ----------
    name : str
        Name of the dataset.
    task : str
        Name of the task to load.
    data_dir : str
        Path of the stored data in disk.
    file_path : bool
        Path to the metadata HDF5 file.
    keywords : list of strings, optional
        List of keywords to categorize the dataset.
    verbose : bool, optional
        Displays text information (if true).
    is_test : bool, optional
        Flag used for tests.

    Examples
    --------
    Add a dataset manually to dbcollection.

    >>> import dbcollection as dbc
    >>> dbc.add('new_db', 'new_task', 'new/path/db', 'newdb.h5', ['new_category'])
    >>> dbc.query('new_db')
    {'new_db': {'tasks': {'new_task': 'newdb.h5'}, 'data_dir': 'new/path/db', 'keywords':
    ['new_category']}}

    """
    assert name, "Must input a valid name: {}".format(name)
    assert task, "Must input a valid task: {}".format(task)
    assert data_dir, "Must input a valid data_dir: {}".format(data_dir)
    assert file_path, "Must input a valid file_path: {}".format(file_path)

    db_adder = AddAPI(name=name,
                      task=task,
                      data_dir=data_dir,
                      file_path=file_path,
                      keywords=keywords,
                      verbose=verbose,
                      is_test=is_test)

    db_adder.run()

    if verbose:
        print('==> Dataset registry complete.')


def remove(name, task=None, delete_data=False, verbose=True, is_test=False):
    """Remove/delete a dataset and/or task from the cache.

    Removes the datasets cache information from the dbcollection.json file.
    The dataset's data files remain in disk if 'delete_data' is set to False,
    otherwise it removes also the data files.

    Also, instead of deleting the entire dataset, removing a specific task
    from disk is also possible by specifying which task to delete. This removes
    the task entry for the dataset and removes the corresponding hdf5 file from
    disk.

    Parameters
    ----------
    name : str
        Name of the dataset to delete.
    task : str, optional
        Name of the task to delete.
    delete_data : bool, optional
        Delete all data files from disk for this dataset if True.
    verbose : bool, optional
        Displays text information (if true).
    is_test : bool, optional
        Flag used for tests.

    Examples
    --------
    Remove a dataset from the list.

    >>> import dbcollection as dbc
    >>> # add a dataset
    >>> dbc.add('new_db', 'new_task', 'new/path/db', 'newdb.h5', ['new_category'])
    >>> dbc.query('new_db')
    {'new_db': {'tasks': {'new_task': 'newdb.h5'}, 'data_dir': 'new/path/db',
    'keywords': ['new_category']}}
    >>> dbc.remove('new_db')  # remove the dataset
    Removed 'new_db' dataset: cache=True, disk=False
    >>> dbc.query('new_db')  # check if the dataset info was removed (retrieves an empty dict)
    {}

    """
    assert name is not None, 'Must input a valid dataset name: {}'.format(name)

    db_remover = RemoveAPI(name=name,
                           task=task,
                           delete_data=delete_data,
                           verbose=verbose,
                           is_test=is_test)

    db_remover.run()

    if verbose:
        print('==> Dataset registry removed.')


def config_cache(field=None, value=None, delete_cache=False, delete_cache_dir=False,
                 delete_cache_file=False, reset_cache=False, verbose=True, is_test=False):
    """Configure the cache file.

    This method allows to configure the cache file directly by selecting
    any data field/value. The user can also manually configure the file
    if he/she desires.

    To modify any entry in the cache file, simply input the field name
    you want to change along with the new data you want to insert. This
    applies to any field/data in the file.

    Another thing available is to reset/clear the entire cache paths/configs
    from the file by simply enabling the 'reset_cache' flag to true.

    Also, there is an option to completely remove the cache file+folder
    from the disk by enabling 'delete_cache' to True. This will remove the
    cache dbcollection.json and the dbcollection/ folder from disk.

    Parameters
    ----------
    field : str, optional
        Name of the field to update/modify in the cache file.
    value : str, list, table, optional
        Value to update the field.
    delete_cache : bool, optional
        Delete/remove the dbcollection cache file + directory.
    delete_cache_dir : bool, optional
        Delete/remove the dbcollection cache directory.
    delete_cache_file : bool, optional
        Delete/remove the dbcollection.json cache file.
    reset_cache : bool, optional
        Reset the cache file.
    verbose : bool, optional
        Displays text information (if true).
    is_test : bool, optional
        Flag used for tests.

    Examples
    --------
    Delete the cache by removing the dbcollection.json cache file.
    This will NOT remove the file contents in dbcollection/. For that,
    you must set the *delete_cache_dir* argument to True.

    >>> import dbcollection as dbc
    >>> dbc.config_cache(delete_cache_file=True)
    """
    manager = ConfigAPI(field=field,
                        value=value,
                        delete_cache=delete_cache,
                        delete_cache_dir=delete_cache_dir,
                        delete_cache_file=delete_cache_file,
                        reset_cache=reset_cache,
                        verbose=verbose,
                        is_test=is_test)

    manager.run()


def query(pattern='info', verbose=True, is_test=False):
    """Do simple queries to the cache.

    list all available datasets for download/preprocess.

    Parameters
    ----------
    pattern : str, optional
        Field name used to search for a matching pattern in cache data.
    verbose : bool, optional
        Displays text information (if true).
    is_test : bool, optional
        Flag used for tests.

    """
    assert isinstance(pattern, str), 'Must insert a string value as input. ' + \
                                     'Expected "str", got "{}"'.format(pattern)

    query = QueryAPI(pattern=pattern,
                     verbose=verbose,
                     is_test=is_test)

    return query.run()


def print_paths_info(data):
    """Prints the cache paths content."""
    print('--------------')
    print('  Paths info ')
    print('--------------')
    print(json.dumps(data['info'], sort_keys=True, indent=4))
    print('')


def print_datasets_info(data, names=None):
    """Prints the datasets contents like name or available tasks."""
    print('----------------')
    print('  Dataset info ')
    print('----------------')
    if names:
        for name in sorted(names):
            print(json.dumps({name: data['dataset'][name]}, sort_keys=True, indent=4))
    else:
        print(json.dumps(data['dataset'], sort_keys=True, indent=4))
    print('')


def print_categories_info(data, names=None):
    """Prints the categories information of the cache."""
    if any(data['category']):
        print('------------------------')
        print('  Datasets by category ')
        print('------------------------\n')
        max_size_name = max([len(name) for name in data['category']]) + 7
        if names:
            for category in data['category']:
                list_datasets = []
                for name in names:
                    if name in data['category'][category]:
                        list_datasets.append(name)
                if any(list_datasets):
                    print("{:{}}".format('   > {}: '.format(category), max_size_name) +
                          "{}".format(sorted(list_datasets)))
        else:
            for name in data['category']:
                print("{:{}}".format('   > {}: '.format(name), max_size_name) +
                      "{}".format(sorted(data['category'][name])))
        print('')


def info_cache(name=None, paths_info=True, datasets_info=True, categories_info=True, is_test=False):
    """Prints the cache contents and other information.

    Parameters
    ----------
    name : str/list/tuple, optional
        Name or list of names of datasets to be selected for print.
    paths_info : bool, optional
        Print the paths info to screen.
    datasets_info : bool, optional
        Print the datasets info to screen.
    categories_info : bool, optional
        Print the categories keywords info to screen.
    is_test : bool, optional
        Flag used for tests.

    Raises
    ------
    TypeError
        If input arg name is not a string or list/tuple.
    """
    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    if name:
        # filter info about the datasets
        if isinstance(name, str):
            names = (name,)
        elif isinstance(name, list) or isinstance(name, tuple):
            names = tuple(name)
        else:
            raise TypeError('Input \'name\' must be either a string or a list/tuple.')
    else:
        names = None

    data = cache_manager.data

    if paths_info:
        print_paths_info(data)

    if datasets_info:
        print_datasets_info(data, names)

    if categories_info:
        print_categories_info(data, names)


def info_datasets(db_pattern='', show_downloaded=True, show_available=True, is_test=False):
    """Prints information about available and downloaded datasets.

    Parameters
    ----------
    db_pattern : str
        String for matching dataset names available for downloading in the database.
    show_downloaded : bool, optional
        Print the downloaded datasets stored in cache.
    show_available : bool, optional
        Print the available datasets for load/download with dbcollection.

    """
    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    available_datasets_list = fetch_list_datasets()

    if show_downloaded:
        print('----------------------------------------')
        print('  Available datasets in cache for load ')
        print('----------------------------------------')
        data = cache_manager.data
        for name in sorted(data['dataset']):
            tasks = list(sorted(data['dataset'][name]['tasks'].keys()))
            print('  - {}  {}'.format(name, tasks))
        print('')

    if show_available:
        print('-----------------------------------')
        print('  Available datasets for download ')
        print('-----------------------------------')
        if any(db_pattern):
            for name in sorted(available_datasets_list):
                if db_pattern in name:
                    tasks = list(sorted(available_datasets_list[name]['tasks'].keys()))
                    print('  - {}  {}'.format(name, tasks))
        else:
            for name in sorted(available_datasets_list):
                tasks = list(sorted(available_datasets_list[name]['tasks'].keys()))
                print('  - {}  {}'.format(name, tasks))
