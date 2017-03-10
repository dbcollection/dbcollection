"""
dbcollection managing functions.
"""


from __future__ import print_function
import os
import json
from .cache import CacheManager
from .loader import DatasetLoader
from . import dataset
from . import utils


def load(name, task='default', is_test=False):
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
          is_download=True, verbose=True, is_test=False):
    """Setup a dataset's metadata and cache files on disk.

    When selecting a dataset name from the list, this method will download
    and process a dataset's metadata and store it on disk. The data is
    contained in a HSF5 file for a specific task previously setup by the
    dataset's loading methods.

    If the user already has the dataset's data files on disk, the download
    step can be skipped by setting the 'is_download' flag to false.

    Parameters
    ----------
    name : str
        Name of the dataset.
    data_dir : str
        Path to store the data (if the data doesn't exist and the download flag is equal True).
    task_name : str
        Specify a specific task to save.
	is_download : bool
        Downloads data from the host to disk (if true).
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

    # Check if the dataset's data has already been downloaded.
    # If not, attempt to download the data.
    if not cache_manager.exists_dataset(name):
        assert os.path.isdir(data_dir), 'Must insert a valid path: data_dir={}'.format(data_dir)

        if verbose:
            print('==> (1/2) Download/setup {} data to disk...'.format(name))

        # get cache default save path
        cache_save_path = os.path.join(cache_manager.default_cache_dir, name)
        if not os.path.exists(cache_save_path):
            os.makedirs(cache_save_path)

        # get data directory to store the data
        if is_download:
            data_dir_ = os.path.join(data_dir, name) or os.path.join(cache_manager. default_data_dir, name)
            if not os.path.exists(data_dir_):
                os.makedirs(data_dir_)
        else:
            data_dir_ = data_dir

        # download/preprocess dataset
        keywords = dataset.download(name, data_dir_, cache_save_path, is_download, verbose)

        # update dbcollection.json file with the new data
        cache_manager.update(name, data_dir_, {}, keywords)

        if verbose:
            print('==> (1/2) Download/setup complete.')

    # get data + cache dir paths
    dset_paths = cache_manager.get_dataset_storage_paths(name)

    # process dataset metadata
    if not cache_manager.is_task(name, 'default'):
        if verbose:
            print('==> (2/2) Processing {} metadata files...'.format(name))
        cache_info = dataset.process(name, dset_paths['data_dir'], dset_paths['cache_dir'], verbose)

        # update dbcollection.json file with the new data
        cache_manager.update(name, cache_info['data_dir'], cache_info['tasks'], cache_info['keywords'])

        if verbose:
            print('==> (2/2) Processing complete.')


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
    #print(query_list)
    #print('*** Query results ***')
    #print(json.dumps(query_list, sort_keys=True, indent=4))


def info(verbose=True, list_datasets=False, is_test=False):
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