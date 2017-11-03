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


def get_dataset_attributes(name):
    """Loads a module, checks for key attributes and returns them."""
    __import__(name)
    module = sys.modules[name]
    try:
        db_fields = {
            "urls": getattr(module, 'urls'),
            "keywords": getattr(module, 'keywords'),
            "tasks": getattr(module, 'tasks'),
            "default_task": getattr(module, 'default_task'),
            "constructor": getattr(module, 'Dataset')
        }
        return db_fields
    except AttributeError:
        return None


def fetch_list_datasets():
    """Get all datasets into a dictionary.

    Returns
    -------
    dict
        A dictionary where keys are names of datasets and values are
        a dictionary containing information like urls or keywords of
        a dataset.
    """
    db_list = {}
    for _, modname, ispkg in pkgutil.walk_packages(path=datasets.__path__,
                                                   prefix=datasets.__name__ + '.',
                                                   onerror=lambda x: None):
        if ispkg:
            paths = modname.split('.')
            db = get_dataset_attributes(modname)
            if db:
                dbname = paths[-1]
                db_list.update({dbname: db})
    return db_list


def get_dirs(cache_manager, name, data_dir):
    """Parse data directory and cache save path."""
    if data_dir is None or data_dir is '':
        data_dir_ = os.path.join(cache_manager.download_dir, name)
    else:
        if not os.path.exists(data_dir):
            data_dir_ = os.path.join(data_dir, name)
        else:
            data_dir_ = data_dir

    if not os.path.exists(data_dir_):
        print('Creating save directory in disk: ' + data_dir_)
        os.makedirs(data_dir_)

    cache_save_path = os.path.join(cache_manager.cache_dir, name)
    if not os.path.exists(cache_save_path):
        os.makedirs(cache_save_path)

    return data_dir_, cache_save_path


def download(name=None, data_dir=None, extract_data=True, verbose=True, is_test=False):
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
    assert name is not None, 'Must input a valid dataset name: {}'.format(name)

    available_datasets_list = fetch_list_datasets()

    # check if the dataset name exists in the list of available dataset for download
    assert name in available_datasets_list, 'Invalid dataset name: {}'.format(name)

    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    # get data dir + cache default save path
    data_dir_, cache_save_path = get_dirs(cache_manager, name, data_dir)

    if verbose:
        print('==> Download {} data to disk...'.format(name))

    # setup dataset class
    constructor = available_datasets_list[name]['constructor']
    db = constructor(data_path=data_dir_,
                     cache_path=cache_save_path,
                     extract_data=extract_data,
                     verbose=verbose)

    # download dataset
    db.download()

    # download/preprocess dataset
    keywords = available_datasets_list[name]['keywords']

    # update dbcollection.json file with the new data
    cache_manager.update(name, data_dir_, {}, keywords)

    if verbose:
        print('==> Download complete.')


def exists_task(available_datasets_list, name, task):
    """Checks if a task exists for a dataset."""
    if task == '':
        task_ = available_datasets_list[name]['default_task']
    elif task == 'default':
        task_ = available_datasets_list[name]['default_task']
    elif task.endswith('_s'):
        task_ = task[:-2]
    else:
        task_ = task
    return task_ in available_datasets_list[name]['tasks']


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
    assert name is not None, 'Must input a valid dataset name: {}'.format(name)

    available_datasets_list = fetch_list_datasets()

    # check if the dataset name exists in the list of available dataset for download
    assert name in available_datasets_list, 'Invalid dataset name: {}'.format(name)

    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    # get data + cache dir paths
    dset_paths = cache_manager.get_dataset_storage_paths(name)
    data_dir = dset_paths['data_dir']
    cache_save_path = dset_paths['cache_dir']

    # setup dataset class
    constructor = available_datasets_list[name]['constructor']
    db = constructor(data_path=data_dir,
                     cache_path=cache_save_path,
                     extract_data=False,
                     verbose=verbose)

    # check if task exists in the list
    if not exists_task(available_datasets_list, name, task):
        raise KeyError('The task \'{}\' does not exists for loading/processing.'.format(task))

    if not os.path.exists(cache_save_path):
        os.makedirs(cache_save_path)

    # process metadata
    task_info = db.process(task)

    # update dbcollection.json file with the new data
    keywords = available_datasets_list[name]['keywords']
    cache_manager.update(name, data_dir, task_info, keywords)

    if verbose:
        print('==> Processing complete.')


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
    assert name is not None, 'Must input a valid dataset name: {}'.format(name)

    available_datasets_list = fetch_list_datasets()

    # check if the dataset name exists in the list of available dataset for download
    assert name in available_datasets_list, 'Invalid dataset name: {}'.format(name)

    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    if task == '' or task == 'default':
        task = available_datasets_list[name]['default_task']

    # check if dataset exists. If not attempt to download the dataset
    if not cache_manager.exists_dataset(name):
        download(name, data_dir, True, verbose, is_test)
        cache_manager.reload_cache()  # reload the cache's data

    # check if the task exists inf cache
    if not cache_manager.exists_task(name, task):
        process(name, task, verbose, is_test)
        cache_manager.reload_cache()  # reload the cache's

    # get data + cache dir paths
    dset_paths = cache_manager.get_dataset_storage_paths(name)

    # get task cache file path
    task_cache_path = cache_manager.get_task_cache_path(name, task)

    # Create a loader
    dataset_loader = DataLoader(name, task, dset_paths['data_dir'], task_cache_path)

    # return Loader
    return dataset_loader


def add(name, task, data_dir, file_path, keywords=(), is_test=False):
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
    {'new_db': {'tasks': {'new_task': 'newdb.h5'}, 'data_dir': 'new/path/db', 'keywords':
    ['new_category']}}

    """
    assert name, "Must input a valid name: {}".format(name)
    assert task, "Must input a valid task: {}".format(task)
    assert data_dir, "Must input a valid data_dir: {}".format(data_dir)
    assert file_path, "Must input a valid file_path: {}".format(file_path)

    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    # update the cache for the dataset
    cache_manager.update(name, data_dir, {task: file_path}, keywords, True)


def remove(name, task=None, delete_data=False, is_test=False):
    """Remove/delete a dataset and/or task from the cache.

    Removes the datasets cache information from the dbcollection.json file.
    The dataset's data files remain on disk if 'delete_data' is set to False,
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

    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    # check if dataset exists in the cache file
    if cache_manager.exists_dataset(name):
        if task is None:
            if delete_data:
                cache_manager.delete_dataset(name, True)
            else:
                cache_manager.delete_dataset(name, False)

            print('Removed \'{}\' dataset: cache=True, disk={}'.format(name, delete_data))
        else:
            if cache_manager.delete_task(name, task):
                print('Removed the task \'{}\' from the \'{}\' dataset: cache=True'
                      .format(task, name))
            else:
                print('Do nothing.')
    else:
        print('Dataset \'{}\' does not exist.'.format(name))


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
    This will NOT remove the contents of the dbcollection/. For that,
    just set the *delete_cache_dir* flag to True.

    >>> import dbcollection as dbc
    >>> dbc.config_cache(delete_cache_file=True)
    """

    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    if delete_cache:
        delete_cache_dir = True
        delete_cache_file = True

    if delete_cache_dir:
        # delete cache dir
        if os.path.exists(cache_manager.cache_dir):
            shutil.rmtree(cache_manager.cache_dir)
            if verbose:
                print('Deleted {} directory.'.format(cache_manager.cache_dir))

    if delete_cache_file:
        # delete the entire cache
        if os.path.exists(cache_manager.cache_filename):
            os.remove(cache_manager.cache_filename)
            if verbose:
                print('Deleted {} cache file.'.format(cache_manager.cache_filename))
    else:
        if reset_cache:
            # reset the cache file
            cache_manager.reset_cache(force_reset=True)
        else:
            if field is not None:
                if verbose:
                    print(cache_manager.modify_field(field, value))


def query(pattern='info', is_test=False):
    """Do simple queries to the cache.

    list all available datasets for download/preprocess.

    Parameters
    ----------
    pattern : str, optional
        Field name used to search for a matching pattern in cache data.
    is_test : bool, optional
        Flag used for tests.

    """
    assert isinstance(pattern, str), 'Must insert a string value as input. ' + \
                                     'Expected "str", got "{}"'.format(pattern)
    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    # init list
    query_list = []

    # check info / dataset lists first
    if pattern in cache_manager.data:
        query_list.append({pattern: cache_manager.data[pattern]})

    # match default paths
    if pattern in cache_manager.data['info']:
        query_list.append({'info': {pattern: cache_manager.data['info'][pattern]}})

    # match datasets/tasks
    if pattern in cache_manager.data['dataset']:
        query_list.append({'dataset': {pattern: cache_manager.data['dataset'][pattern]}})

    for name in cache_manager.data['dataset']:
        if pattern in cache_manager.data['dataset'][name]:
            query_list.append({
                'dataset': {
                    name: {
                        pattern: cache_manager.data['dataset'][name][pattern]
                    }
                }
            })
        if pattern in cache_manager.data['dataset'][name]['tasks']:
            query_list.append({
                'dataset': {
                    name: {
                        'tasks': {
                            pattern: cache_manager.data['dataset'][name]['tasks'][pattern]
                        }
                    }
                }
            })
        if pattern in cache_manager.data['dataset'][name]['keywords']:
            query_list.append({
                'dataset': {
                    name: {
                        'keywords': {
                            pattern: cache_manager.data['dataset'][name]['keywords']
                        }
                    }
                }
            })

    # match category
    if pattern in cache_manager.data['category']:
        query_list.append({
            'category': {
                pattern: list(cache_manager.data['category'][pattern])
            }
        })
    for category in cache_manager.data['category']:
        if pattern in cache_manager.data['category'][category]:
            query_list.append({'category': {category: [pattern, ]}})

    return query_list


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
        Name or list of names to be selected for print.
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
