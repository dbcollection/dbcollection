"""
dbcollection managing functions.
"""


from __future__ import print_function
import os
import json
from .cache import CacheManager
from .db_loader_postprocess import fetch_dataset_loader
from . import dataset
from . import utils


def load(name, data_dir=None, task='default', custom_task_name=None, \
         download_data=True, verbose=True, \
         organize_list=None, select_data=None, filter_data=None, balance_sets=None):
    """Loads dataset metadata file.

    Returns a loader with the necessary functions to manage the selected dataset.

    Parameters
    ----------
    name : str
        Name of the dataset.
    data_dir : str
        Path to store the data (if the data doesn't exist and the download flag is equal True).
    save_name : str
        Save a custom task with a specified name.
        (usefull to create custom versions of the original).
    task : str
        Specify a specific task to load.
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
    cache_manager = CacheManager()

    # Check if the dataset's data has already been downloaded.
    # If not, attempt to download the data.
    if not cache_manager.exists_dataset(name):
        if download_data:
            download(name, data_dir, verbose)
            cache_manager = CacheManager() # update the cache_manager by re-opening the cache file
        else:
            raise Exception('The dataset \'{}\' is not available on the cache list. '.format(name)+\
                            'BUT it is available for download by setting \'download=True\'.')

    # get data + cache dir paths
    dset_paths = cache_manager.get_dataset_storage_paths(name)

    # get task cache file path
    if not cache_manager.is_task(name, task):
        if verbose:
            print('Processing metadata files...')

        # get cache default save path
        cache_save_path = os.path.join(cache_manager.default_cache_dir, name)
        if not os.path.exists(cache_save_path):
            utils.create_dir(cache_save_path)

        # preprocess dataset
        cache_info = dataset.process(name, dset_paths['data_dir'], dset_paths['cache_dir'], verbose)

        # update dbcollection.json file with the new data
        cache_manager.update(name, cache_info['data_dir'], cache_info['tasks'], cache_info['keywords'])

        if verbose:
            print('Done.')

    # get task cache file path
    task_cache_path = cache_manager.get_cache_path(name, task)

    # Create a loader
    custom_name = custom_task_name or (task + 'custom')
    #dataset_loader = DatasetLoader(name, task, dset_paths['data_dir'], task_cache_path)
    dataset_loader = fetch_dataset_loader(name, task, dset_paths['data_dir'], task_cache_path, custom_name,\
                                        select_data, filter_data, organize_list, balance_sets, verbose)

    if verbose:
        print('Fetch complete.')

    # return Loader
    return dataset_loader


def construct(name, data_dir, task='default'):
    """Constructs a dataset from a directory.

    This method constructs a dataset based on the hierarchy of a directory,
    where the images are arranged in this way:

    root/
        (sets)
        train/
            (classes)
                dog/
                    (files)
                    dg_1.png
                    dg_n.png
                cat/
                    ct_1.png
                    ct_n.png
                mouse/
                    ms_1.png
                    ms_n.png
        val/
                dog/
                cat/
                mouse/
        test/
        test-dev/

    Parameters
    ----------
    name : str
        Dataset name to add to the list.
	data_dir : str
        Folder path of the dataset's data on disk.
	task : str
        Name of the new task.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    pass


def add(name, data_dir, cache_file_path, task='default'):
    """Add dataset to list.

    Adds a custom dataset to the list.

    Parameters
    ----------
    name : str
        Dataset name to add to the list.
	data_dir : str
        Folder path of the dataset's data on disk.
	cache_file_path : str
        Cache's metadata file path.
	task : str
        Name of the new task.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # Load a cache manager object
    cache_manager = CacheManager()

    # split dir and filename from path
    cache_dir = os.path.dirname(cache_file_path)

    # add dataset info to the dataset
    cache_manager.update(name, 'custom', data_dir, cache_dir, {task:cache_file_path})


def delete(name):
    """Delete a dataset from disk (cache+data).

    Deletes the data+metadata of a dataset on disk (cache file included).

    Parameters
    ----------
    name : str
        Name of the dataset to delete the data from disk.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # Load a cache manager object
    cache_manager = CacheManager()

    # check if dataset exists in the cache file
    if cache_manager.exists_dataset(name):
        cache_manager.delete_dataset(name, True)
    else:
        print('Dataset \'{}\' does not exist.'.format(name))
        #raise Exception('Dataset ' + name + ' does not exist.')


def reset(name=None):
    """Deletes a dataset's metadata cache files/dir.

    Resets the data of the dbcollection.json cache file for a specific dataset
    (it deletes the cache files for this dataset as well, if any).

    Parameters
    ----------
	name : str
        Name of the dataset to reset the cache.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    if name is None:
        print('No dataset was selected. (do nothing)')
        return

    # Load a cache manager object
    cache_manager = CacheManager()

    if name.lower() == 'all':
        if cache_manager.is_empty():
            print('The cache data is empty.')
        else:
            # delete the entire cache
            cache_manager.delete_cache_all()
            print('Deleted all datasets\' metadata from cache.')
    else:
        # check if dataset exists in the cache file
        if cache_manager.exists_dataset(name):
            cache_manager.delete_dataset(name, False)
        else:
            print('Dataset {} does not exist. Skip deletion.'.format(name))


def clear(verbose=True):
    """Deletes the cache .json file and the cache dir of all datasets.

    Parameters
    ----------
    verbose : bool
        Displays text information.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # Load a cache manager object
    cache_manager = CacheManager()

    # delete cache dir
    utils.delete_dir(cache_manager.default_cache_dir)

    # delete cache file
    utils.delete_file(cache_manager.cache_fname)

    if verbose:
        print('Deleted {} directory.'.format(cache_manager.default_cache_dir))
        print('Deleted {} cache file.'.format(cache_manager.cache_fname))


def config(name=None, fields=None, cache_dir_default=None, data_dir_default=None):
    """config cache file.

    Manually setup the configurations of the cache file dbcollection.json.

    Parameters
    ----------
    name : str
        Name of the dataset.
	fields : dict
        Specifies which fields and values to update the dbcollection cache file.
    cache_dir_default : str
        New path to the metadata cache files root directory.
    data_dir_default : str
        New path to the dataset's data storage root directory.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # Load a cache manager object
    cache_manager = CacheManager()

    # change default cache path
    if not cache_dir_default is None:
        cache_manager.default_cache_dir = cache_dir_default

    # change default data path
    if not data_dir_default is None:
        cache_manager.default_data_dir = data_dir_default

    # change paths of a dataset
    if not name is None:
        if isinstance(fields, dict):
            if cache_manager.exists_dataset(name):
                for field_name in fields.keys():
                    cache_manager.change_field(name, field_name, fields[field_name])
            else:
                print('Dataset {} does not exist.'.format(name))
                #raise Exception('Dataset ' + name + ' does not exist.')


def download(name, data_dir, verbose=True):
    """Download dataset.

    Download the data for one (or several) listed dataset(s).

    Parameters
    ----------
    name : str
        Name of the dataset to reset the cache.
    cache : bool
        Force the cache file of the preprocessed data to be deleted for the particular dataset.
	data_dir : str
        Data path to store the dataset's data.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # Load a cache manager object
    cache_manager = CacheManager()

    # get cache default save path
    cache_save_path = os.path.join(cache_manager.default_cache_dir, name)
    if not os.path.exists(cache_save_path):
        utils.create_dir(cache_save_path)

    # get data directory to store the data
    data_dir = os.path.join(data_dir, name) or os.path.join(cache_manager.default_data_dir, name)
    if not os.path.exists(data_dir):
        utils.create_dir(data_dir)

    # download/preprocess dataset
    keywords = dataset.download(name, data_dir, cache_save_path, verbose)

    # update dbcollection.json file with the new data
    cache_manager.update(name, data_dir, {}, keywords)

    print('{} has been successfully downloaded.'.format(name))
    print('')


def query(pattern='info'):
    """Query the cache file.

    list all available datasets for download/preprocess. (tenho que pensar melhor sobre este)

    Parameters:
    -----------
	pattern : str
        Field name used to search for a matching pattern in cache data.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # Load a cache manager object
    cache_manager = CacheManager()

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


def info(verbose=True):
    """List cache data.

    Prints the contents of the dbcollection.json cache file

    Parameters
    ----------
    verbose : bool
        If true, prints the full cache file to the screen.
        Else, prints only the categories + dataset names.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # Load a cache manager object
    cache_manager = CacheManager()

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
