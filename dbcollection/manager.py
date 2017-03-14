"""
dbcollection managing functions.
"""


from __future__ import print_function
import os
import json

from dbcollection import dataset
from dbcollection import utils
from dbcollection.utils.cache import CacheManager
from dbcollection.utils.loader import DatasetLoader


def download(name=None, data_dir=None, verbose=True, is_test=False):
    """Download a dataset data to disk.

    This method will download a dataset's data files to disk. After download,
    it updates the cache file with the  dataset's name and path where the data
    is stored.

    Parameters
    ----------
    name : str
        Name of the dataset.
    data_dir : str
        Path to store the data (if the data doesn't exist and the download flag is equal True).
	verbose : bool
        Displays text information (if true).
    is_test : bool
        Flag used for integration tests.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    if data_dir is None:
        data_dir_ = os.path.join(cache_manager.default_cache_dir, name, 'data')
    else:
        assert os.path.isdir(data_dir), 'Must insert a valid path: data_dir={}'.format(data_dir)
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
    keywords = dataset.download(name, data_dir_, cache_save_path, True, verbose)

    # update dbcollection.json file with the new data
    cache_manager.update(name, data_dir_, {}, keywords)

    if verbose:
        print('==> Download complete.')


def process(name=None, verbose=True, is_test=False):
    """Process a dataset's metadata and stores it to file.

    The data is stored a a HSF5 file for each task composing the dataset's tasks.

    Parameters
    ----------
    name : str
        Name of the dataset.
    verbose : bool
        Displays text information (if true).
    is_test : bool
        Flag used for integration tests.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    # get data + cache dir paths
    dset_paths = cache_manager.get_dataset_storage_paths(name)

    # process dataset metadata
    if verbose:
        print('==> Processing {} metadata ...'.format(name))
    cache_info = dataset.process(name, dset_paths['data_dir'], dset_paths['cache_dir'], verbose)

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
        Specify a specific task to load.
    is_test : bool
        Flag used for integration tests.

    Returns
    -------
    DatasetLoader
       Data loader class.

    Raises
    ------
    Exception
        If dataset is not available for loading.
    """
    assert not name is None, 'Must input a valid name for the dataset: {}'.format(name)

    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    # check if dataset exists. If not attempt to download the dataset
    if not cache_manager.exists_dataset(name):
        download(name, data_dir, verbose, is_test)
        cache_manager = CacheManager(is_test) # reopen the cache file

    # get task cache file path
    if not cache_manager.is_task(name, task):
        if not cache_manager.is_task(name, 'default'):
            process(name, verbose, is_test)
            cache_manager = CacheManager(is_test) # reopen the cache file
        else:
            raise Exception('Dataset name/task not available in cache for load.')

    # get data + cache dir paths
    dset_paths = cache_manager.get_dataset_storage_paths(name)

    # get task cache file path
    task_cache_path = cache_manager.get_cache_path(name, task)

    # Create a loader
    dataset_loader = DatasetLoader(name, task, dset_paths['data_dir'], task_cache_path)

    # return Loader
    return dataset_loader


def add(name=None, task=None, data_dir=None, file_path=None, keywords=[], is_test=False):
    """Add a dataset/task to the available datasets in cache.

    Parameters
    ----------
    name : str
        Name of the dataset.
    task : str
        Specify a specific task to load.
    data_dir : str
        Path to store the data (if the data doesn't exist and the download flag is equal True).
	file_path : bool
        Path to the metadata HDF5 file.
    keywords : list of strings
        List of keywords to categorize the dataset.
    is_test : bool
        Flag used for integration tests.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    assert not name is None, "Must input a valid name: {}".format(name)
    assert not task is None, "Must input a valid task: {}".format(task)
    assert data_dir is None, "Must input a valid data_dir: {}".format(data_dir)
    assert file_path is None, "Must input a valid file_path: {}".format(file_path)

    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    # update the cache for the dataset
    cache_manager.update(name, data_dir, {task: file_path}, keywords, True)


def remove(name, delete_data=False, is_test=False):
    """Delete a dataset from the cache.

    Removes the datasets cache information from the dbcollection.json file.
    The dataset's data files remain on disk if 'delete_data' is set to False,
    otherwise it removes also the data files.

    Parameters
    ----------
    name : str
        Name of the dataset to delete the data from disk.
    is_test : bool
        Flag used for integration tests.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    # check if dataset exists in the cache file
    if cache_manager.exists_dataset(name):
        if delete_data:
            cache_manager.delete_dataset(name, True)
        else:
            cache_manager.delete_dataset(name, False)

        print('Removed dataset {}: cache=True, disk={}'.format(name, delete_data))
    else:
        print('Dataset \'{}\' does not exist.'.format(name))


def config_cache(field=None, value=None, delete_cache=False, clear_cache=False, is_test=False):
    """Configurates the cache file.

    This method allows to configure the cache file directly by selecting
    any data field/value. The user can also manually configure the file
    if he/she desires.

    To modify any entry in the cache file, simply input the field name
    you want to change along with the new data you want to insert. This
    applies to any field/data in the file.

    Another thing available is to reset/clear the entire cache paths/configs
    from the file by simply enabling the 'clear_cache' flag to true.

    Also, there is an option to completely remove the cache file+folder
    from the disk by enabling the 'delete_cache' flag to true. This will
    remove the cache dbcollection.json and the dbcollection/ folder from
    disk.

    Parameters
    ----------
	field : str
        Name of the field to update/modify in the cache file.
    value : str, list, table
        Value to update the field.
    delete_cache : bool
        Flag indicating to delete the dataset's data from disk.
    clear_cache : bool
        Flag indicating to delete the cache file from disk.
    is_test : bool
        Flag used for integration tests.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    if delete_cache:
        # delete cache dir
        utils.os.delete_dir(cache_manager.default_cache_dir)

        # delete cache file
        os.remove(cache_manager.cache_fname)

        print('Deleted {} cache file.'.format(cache_manager.cache_fname))
        print('Deleted {} directory.'.format(cache_manager.default_cache_dir))

    else:
        if clear_cache:
            # delete the entire cache
            cache_manager.delete_cache_all()
            print('Deleted all datasets\' metadata information from cache.')
        else:
            if field is None:
                print('No dataset was selected. (do nothing)')
            else:
                print(cache_manager.modify_field(field, value))


def query(pattern='info', is_test=False):
    """Do simple queries to the cache.

    list all available datasets for download/preprocess. (tenho que pensar melhor sobre este)

    Parameters:
    -----------
	pattern : str
        Field name used to search for a matching pattern in cache data.
    is_test : bool
        Flag used for integration tests.

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


def info(list_datasets=False, is_test=False):
    """Prints the cache file contents.

    Prints the contents of the dbcollection.json cache file to the screen.

    Parameters
    ----------
    verbose : bool
        If true, prints the full cache file to the screen.
        Else, prints only the categories + dataset names.
    list_datasets : bool
        Print available datasets in the dbcollection package.
    is_test : bool
        Flag used for integration tests.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    if list_datasets:
        print('dbcollection available datasets: ', dataset.available_datasets)
    else:
        print('Printing contents of {}:\n'.format(cache_manager.cache_fname))

        data = cache_manager.data

        # print info header
        print('*** Paths info ***')
        print(json.dumps(data['info'], sort_keys=True, indent=4))
        print('')

        # print datasets
        print('*** Dataset info ***')
        print(json.dumps(data['dataset'], sort_keys=True, indent=4))
        print('')

        # print categories
        print('*** Dataset categories ***')
        print(json.dumps(data['category'], sort_keys=True, indent=4))
        print('')