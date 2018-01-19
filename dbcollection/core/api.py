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

from .download import download
from .process import process
from .load import load
from .add import AddAPI
from .remove import RemoveAPI
from .config_cache import ConfigAPI
from .query import QueryAPI
from .info import InfoCacheAPI, InfoDatasetAPI

from .list_datasets import fetch_list_datasets


def check_if_dataset_name_is_valid(name):
    """Check if the dataset name exists (is valid) in the list of available dataset for download"""
    available_datasets_list = fetch_list_datasets()
    assert name in available_datasets_list, 'Invalid dataset name: {}'.format(name)


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
    value : str, list, tuple, optional
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


def info_cache(name=None, paths_info=True, datasets_info=True, categories_info=True,
               verbose=True, is_test=False):
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
    verbose : bool, optional
        Displays text information (if true).
    is_test : bool, optional
        Flag used for tests.

    Raises
    ------
    TypeError
        If input arg name is not a string or list/tuple.
    """
    printer = InfoCacheAPI(name=name,
                           paths_info=paths_info,
                           datasets_info=datasets_info,
                           categories_info=categories_info,
                           verbose=verbose,
                           is_test=is_test)

    printer.run()


def info_datasets(db_pattern='', show_downloaded=True, show_available=True,
                  verbose=True, is_test=False):
    """Prints information about available and downloaded datasets.

    Parameters
    ----------
    db_pattern : str
        String for matching dataset names available for downloading in the database.
    show_downloaded : bool, optional
        Print the downloaded datasets stored in cache.
    show_available : bool, optional
        Print the available datasets for load/download with dbcollection.
    verbose : bool, optional
        Displays text information (if true).
    is_test : bool, optional
        Flag used for tests.

    """
    printer = InfoDatasetAPI(db_pattern=db_pattern,
                             show_downloaded=show_downloaded,
                             show_available=show_available,
                             verbose=verbose,
                             is_test=is_test)

    printer.run()
