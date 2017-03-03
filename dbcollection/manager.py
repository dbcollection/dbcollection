"""
dbcollection managing functions.
"""


from __future__ import print_function
import os
import json
from .cache import CacheManager
from .loader import DatasetLoader
from .postprocess import fetch_dataset_loader
from . import dataset
from . import utils


def load(name, task='default', verbose=True, is_test=False):
    """Loads dataset metadata file.

    Returns a loader with the necessary functions to manage the selected dataset.

    Parameters
    ----------
    name : str
        Name of the dataset.
    task : str
        Specify a specific task to load.
	verbose : bool
        Displays text information (if true).
    is_test : bool
        Flag used for integration tests.

    Returns
    -------
    DatasetLoader
       Loader class.

    Raises
    ------
        None
    """

    if verbose:
        print('Fetching {} metadata from disk:'.format(name))

    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    # get data + cache dir paths
    dset_paths = cache_manager.get_dataset_storage_paths(name)

    # get task cache file path
    if not cache_manager.is_task(name, task):
        raise Exception('Dataset/task not available for load.')

    # get task cache file path
    task_cache_path = cache_manager.get_cache_path(name, task)

    # Create a loader
    dataset_loader = DatasetLoader(name, task, dset_paths['data_dir'], task_cache_path)

    # return Loader
    return dataset_loader


def setup(name, data_dir=None, task_name=None,\
          organize_list=None, \
          select_data=None, filter_data=None, \
          balance_sets=None, \
          is_download=True, verbose=True, is_test=False):
    """Description

    Parameters
    ----------
    name : str
        Name of the dataset.
    data_dir : str
        Path to store the data (if the data doesn't exist and the download flag is equal True).
    save_name : str
        Save a custom task with a specified name.
        (usefull to create custom versions of the original).
    task_name : str
        Specify a specific task to save.
	download : bool
        Downloads data from the host to disk (if true).
	verbose : bool
        Displays text information (if true).
	organize_list : dict
        Organizes the data w.r.t. to other fields. The data must be organized in a
        dictionary with the following format: {"new_field_name":"field_name"}
	select_data : dict
        Selects indexes from 'field_name' equal to the selected value(s)
        (removes objects ids without those 'field_name''s values)
	filter_data : dict
        Removes indexes from 'field_name' equal to the selected value(s)
        (removes objects ids with those 'field_name''s values)
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

    # Check if the dataset's data has already been downloaded.
    # If not, attempt to download the data.
    if not cache_manager.exists_dataset(name):
        assert data_dir, 'Must insert a valid path: data_dir={}'.format(data_dir)

        # get cache default save path
        cache_save_path = os.path.join(cache_manager.default_cache_dir, name)
        if not os.path.exists(cache_save_path):
            utils.create_dir(cache_save_path)

        # get data directory to store the data
        data_dir_ = os.path.join(data_dir, name) or os.path.join(cache_manager. default_data_dir, name)
        if not os.path.exists(data_dir_):
            utils.create_dir(data_dir_)

        # download/preprocess dataset
        keywords = dataset.download(name, data_dir_, cache_save_path, is_download, verbose)

        # update dbcollection.json file with the new data
        cache_manager.update(name, data_dir_, {}, keywords)

    # get data + cache dir paths
    dset_paths = cache_manager.get_dataset_storage_paths(name)

    # process dataset metadata
    if not cache_manager.is_task(name, 'default'):
        cache_info = dataset.process(name, dset_paths['data_dir'], dset_paths['cache_dir'], verbose)

        # update dbcollection.json file with the new data
        cache_manager.update(name, cache_info['data_dir'], cache_info['tasks'], cache_info['keywords'])

    # post-process


def remove(name, is_test=False):
    """Delete a dataset from disk (cache+data).

    Deletes the data+metadata of a dataset on disk (cache file included).

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
        cache_manager.delete_dataset(name, True)
    else:
        print('Dataset \'{}\' does not exist.'.format(name))


def manage_cache(field=None, value=None, delete_cache=False, clear_cache=False, verbose=True, is_test=False):
    """Manages the cache file.

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
	name : str
        Name of the dataset to reset the cache.
    clear_cache : bool
        Flag indicating to delete the cache file+data from disk.
    verbose : bool
        Displays text information.
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
        utils.delete_dir(cache_manager.default_cache_dir)

        # delete cache file
        utils.delete_file(cache_manager.cache_fname)

        if verbose:
            print('Deleted {} directory.'.format(cache_manager.default_cache_dir))
            print('Deleted {} cache file.'.format(cache_manager.cache_fname))

    else:
        if clear_cache:
            # delete the entire cache
            cache_manager.delete_cache_all()
            print('Deleted all datasets\' metadata information from cache.')
        else:
            if field is None:
                print('No dataset was selected. (do nothing)')
            else:
                cache_manager.modify_field(field, value)


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

    #print(query_list)
    print('*** Query results ***')
    print(json.dumps(query_list, sort_keys=True, indent=4))


def info(verbose=True, is_test=False):
    """Display the cache data contents to the screen.

    Prints the contents of the dbcollection.json cache file to the screen.

    Parameters
    ----------
    verbose : bool
        If true, prints the full cache file to the screen.
        Else, prints only the categories + dataset names.
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

    print('Printing contents of {}:'.format(cache_manager.cache_fname))
    print('')
    if verbose:
        data = cache_manager.data
    else:
        # display all datasets
        data = {
            'info' : cache_manager.data['info'],
            'dataset' : [db for db in cache_manager.data['dataset'].keys()],
            'category' : [cat for cat in cache_manager.data['category'].keys()],
        }

    # print info header
    print('*** Cache info ***')
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