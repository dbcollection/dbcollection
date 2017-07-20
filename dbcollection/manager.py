"""
dbcollection managing functions.
"""


from __future__ import print_function
import os
import json
import shutil

import dbcollection.datasets.funs as dataset
from dbcollection.datasets.dblist import available_datasets
from dbcollection.cache import CacheManager
from dbcollection.loader import DatasetLoader


def download(name=None, data_dir=None, extract_data=True, verbose=True, is_test=False):
    """Download a dataset data to disk.

    This method will download a dataset's data files to disk. After download,
    it updates the cache file with the  dataset's name and path where the data
    is stored.

    Parameters
    ----------
    name : str
        Name of the dataset.
    data_dir : str
        Directory path to store the downloaded data.
        (optional, default=None)
    extract_data : bool
        Extracts/unpacks the data files (if true).
        (optional, default=True)
	verbose : bool
        Displays text information (if true).
        (optional, default=True)
    is_test : bool
        Flag used for tests.
        (optional, default=False)

    Returns
    -------
        None

    Raises
    ------
        None

    Examples
    --------
    Download the CIFAR10 dataset to disk.

    >>> import dbcollection as dbc
    >>> dbc.download('cifar10')
    """
    assert not name is None, 'Must input a valid dataset name: {}'.format(name)

    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    if data_dir is None or data_dir is '':
        data_dir_ = os.path.join(cache_manager.default_cache_dir, name, 'data')
    else:
        #assert os.path.isdir(data_dir), 'Must insert a valid path: data_dir={}'.format(data_dir)
        if not os.path.exists(data_dir):
            print('Creating save directory in disk: ' + data_dir)
            os.makedirs(data_dir)

        if os.path.split(data_dir)[1] == name:
            data_dir_ = data_dir
        else:
            data_dir_ = os.path.join(data_dir, name)

    if not os.path.exists(data_dir_):
        os.makedirs(data_dir_)

    # get cache default save path
    cache_save_path = os.path.join(cache_manager.default_cache_dir, name)
    if not os.path.exists(cache_save_path):
        os.makedirs(cache_save_path)

    if verbose:
        print('==> Download {} data to disk...'.format(name))

    # download/preprocess dataset
    keywords = dataset.download(name, data_dir_, cache_save_path, extract_data, verbose)

    # update dbcollection.json file with the new data
    cache_manager.update(name, data_dir_, {}, keywords)

    if verbose:
        print('==> Download complete.')


def process(name, task='all', verbose=True, is_test=False):
    """Process a dataset's metadata and stores it to file.

    The data is stored a a HSF5 file for each task composing the dataset's tasks.

    Parameters
    ----------
    name : str
        Name of the dataset.
    task : str
        Name of the task to process.
        (optional, default='all')
    verbose : bool
        Displays text information (if true).
        (optional, default=True)
    is_test : bool
        Flag used for tests.
        (optional, default=False)

    Returns
    -------
        None

    Raises
    ------
        None

    Examples
    --------
    Download the CIFAR10 dataset to disk.

    >>> import dbcollection as dbc
    >>> dbc.process('cifar10', task='classification', verbose=False)
    """
    assert not name is None, 'Must input a valid dataset name: {}'.format(name)

    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    # get data + cache dir paths
    dset_paths = cache_manager.get_dataset_storage_paths(name)

    # process dataset metadata
    if verbose:
        print('==> Processing {} metadata ...'.format(name))
    cache_info = dataset.process(name, task, dset_paths['data_dir'], dset_paths['cache_dir'], verbose)

    # update dbcollection.json file with the new data
    cache_manager.update(name, cache_info['data_dir'], cache_info['tasks'], cache_info['keywords'])

    if verbose:
        print('==> Processing complete.')


def load(name=None, task='default', data_dir=None, verbose=True, is_test=False):
    """Returns a metadata loader of a dataset.

    Returns a loader with the necessary functions to manage the selected dataset.

    Parameters
    ----------
    name : str
        Name of the dataset.
    task : str
        Name of the task to load.
        (optional, default='default')
    data_dir : str
        Directory path to store the downloaded data.
        (optional, default=None)
	verbose : bool
        Displays text information (if true).
        (optional, default=True)
    is_test : bool
        Flag used for tests.
        (optional, default=False)

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
    task_cache_path = cache_manager.get_cache_path(name, task)

    # Create a loader
    dataset_loader = DatasetLoader(name, task, dset_paths['data_dir'], task_cache_path)

    # return Loader
    return dataset_loader


def add(name=None, task=None, data_dir=None, file_path=None, keywords=[], is_test=False):
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
    keywords : list of strings
        List of keywords to categorize the dataset.
    is_test : bool
        Flag used for tests.

    Returns
    -------
        None

    Raises
    ------
        None

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
    task : str
        Name of the task to delete.
        (optional, default=None)
    delete_data : bool
        Delete all data files from disk for this dataset if True.
        (optional, default=False)
    is_test : bool
        Flag used for tests.
        (optional, default=False)

    Returns
    -------
        None

    Raises
    ------
        None

    Examples
    --------
    Remove a dataset from the list.

    >>> import dbcollection as dbc
    >>> dbc.add('new_db', 'new_task', 'new/path/db', 'newdb.h5', ['new_category'])  # add a dataset
    >>> dbc.query('new_db')
    {'new_db': {'tasks': {'new_task': 'newdb.h5'}, 'data_dir': 'new/path/db', 'keywords': ['new_category']}}
    >>> dbc.remove('new_db')  # remove the dataset
    Removed 'new_db' dataset: cache=True, disk=False
    >>> dbc.query('new_db')  # check if the dataset info was removed (retrieves an empty dict)
    {}

    """
    assert not name is None, 'Must input a valid dataset name: {}'.format(name)

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
                print('Removed the task \'{}\' from the \'{}\' dataset: cache=True'.format(task, name))
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
	field : str
        Name of the field to update/modify in the cache file.
        (optional, default=None)
    value : str, list, table
        Value to update the field.
        (optional, default=None)
    delete_cache : bool
        Delete/remove the dbcollection cache file + directory.
        (optional, default=False)
    delete_cache_dir : bool
        Delete/remove the dbcollection cache directory.
        (optional, default=False)
    delete_cache_file : bool
        Delete/remove the dbcollection.json cache file.
        (optional, default=False)
    reset_cache : bool
        Reset the cache file.
        (optional, default=False)
    verbose : bool
        Displays text information (if true).
        (optional, default=True)
    is_test : bool
        Flag used for tests.
        (optional, default=False)

    Returns
    -------
        None

    Raises
    ------
        None

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
        if os.path.exists(cache_manager.default_cache_dir):
            shutil.rmtree(cache_manager.default_cache_dir)
            if verbose:
                print('Deleted {} directory.'.format(cache_manager.default_cache_dir))

    if delete_cache_file:
        # delete the entire cache
        if os.path.exists(cache_manager.cache_fname):
            os.remove(cache_manager.cache_fname)
            if verbose:
                print('Deleted {} cache file.'.format(cache_manager.cache_fname))
    else:
        if reset_cache:
            # reset the cache file
            cache_manager.reset_cache()
        else:
            if not field is None:
                if verbose:
                    print(cache_manager.modify_field(field, value))


def query(pattern='info', is_test=False):
    """Do simple queries to the cache.

    list all available datasets for download/preprocess.

    Parameters:
    -----------
	pattern : str
        Field name used to search for a matching pattern in cache data.
        (optional, default='info')
    is_test : bool
        Flag used for tests.
        (optional, default=False)

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    # init list
    query_list = {}

    # check info / dataset lists first
    if pattern in cache_manager.data:
        query_list.update({pattern : cache_manager.data[pattern]})

    # match default paths
    if pattern in cache_manager.data['info']:
        query_list.update({pattern : cache_manager.data['info'][pattern]})

    # match datasets/tasks
    if pattern in cache_manager.data['dataset']:
        query_list.update({pattern : cache_manager.data['dataset'][pattern]})

    # match datasets/tasks
    if pattern in cache_manager.data['category']:
        query_list.update({pattern : list(cache_manager.data['category'][pattern].keys())})

    for name in cache_manager.data['dataset']:
        if pattern in cache_manager.data['dataset'][name]:
            query_list.update({pattern : cache_manager.data['dataset'][name][pattern]})
        if pattern in cache_manager.data['dataset'][name]['tasks']:
            query_list.update({pattern : cache_manager.data['dataset'][name]['tasks'][pattern]})
        if pattern in cache_manager.data['dataset'][name]['keywords']:
            query_list.update({pattern : cache_manager.data['dataset'][name]['keywords'][pattern]})

    return query_list


def info(name=None, paths_info=True, datasets_info=True, categories_info=True, is_test=False):
    """Prints the cache contents and other information.

    This method provides a dual functionality: (1) It displays
    the cache file content that shows which datasets are
    available for loading right now; (2) It can display all
    available datasets to use in the dbcollection package, and
    if a name is provided, it displays what tasks it contains
    for loading.

    The default is to display the cache file contents to the
    screen. To list the available datasets, set the 'name'
    input argument to 'all'. To list the tasks of a specific
    dataset, set the 'name' input argument to the name of the
    desired dataset (e.g., 'cifar10').

    Parameters
    ----------
    name : str
        Name of the dataset to display information.
        (optional, default=None)
    paths_info : bool
        Print the paths info to screen.
        (optional, default=True)
    datasets_info : bool/str
        Print the datasets info to screen.
        If a string is provided, it selects
        only the information of that string
        (dataset name).
        (optional, default=True)
    categories_info : bool/str
        Print the paths info to screen.
        If a string is provided, it selects
        only the information of that string
        (dataset name).
        (optional, default=True)
    is_test : bool
        Flag used for tests.
        (optional, default=False)

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    if name:
        db_list = available_datasets()

        if name == 'all':
            print('\nAvailable datasets for load/download:')
            for db_name in sorted(db_list):
                print('   - ' + str(db_name))
        else:
            assert name in db_list, 'Invalid dataset name: ' + str(name)

            print('\nAvailable tasks for {}:'.format(name))
            for task in db_list[name]:
                print('   -- ' + str(task))
    else:
        print('Printing contents of {}:\n'.format(cache_manager.cache_fname))

        data = cache_manager.data

        # print info header
        if paths_info:
            print('--------------')
            print('  Paths info ')
            print('--------------')
            print(json.dumps(data['info'], sort_keys=True, indent=4))
            print('')

        # print datasets
        if datasets_info:
            print('----------------')
            print('  Dataset info ')
            print('----------------')
            if isinstance(datasets_info, bool):
                print(json.dumps(data['dataset'], sort_keys=True, indent=4))
            elif isinstance(datasets_info, str):
                print(json.dumps(data['dataset'][datasets_info], sort_keys=True, indent=4))
            else:
                raise Exception('Invalid input argument datasets_info: {}.'.format(datasets_info)
                                + ' Must be either a string or a bool.')
            print('')

        #print('*** Datasets by category ***\n')
        if categories_info:
            print('------------------------')
            print('  Datasets by category ')
            print('------------------------\n')
            try:
                max_size_name = max([len(name) for name in data['category']]) + 7

                if isinstance(categories_info, bool):
                    for name in data['category']:
                        print("{:{}}".format('   > {}: '.format(name), max_size_name)
                            + "{}".format( sorted(data['category'][name])))
                elif isinstance(categories_info, str):
                    for name in data['category']:
                        l = [dset for dset in data['category'][name] if dset == categories_info]
                        print("{:{}}".format('   > {}: '.format(name), max_size_name)
                            + "{}".format( sorted(l)))
                else:
                    raise Exception('Invalid input argument categories_info: {}.'.format(categories_info)
                                    + ' Must be either a string or a bool.')
            except:
                print('')
