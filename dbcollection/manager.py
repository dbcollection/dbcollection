"""
dbcollection managing functions.
"""


from __future__ import print_function
import os
import sys
import json
from .cache import CacheManager
from .loader import DatasetLoader
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
	select : dict
        Selects indexes from 'field_name' equal to the selected value(s)
        (removes objects ids without those 'field_name''s values)
	filter : dict
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

    # Load a cache manager object
    cache_manager = CacheManager()

    # Check if the dataset's data has already been downloaded.
    # If not, attempt to download the data.
    if not cache_manager.exists_dataset(name):
        if download_data:
            download(name, data_dir, verbose)
        else:
            raise Exception('The dataset \'{}\' is not available on the cache list. '.format(name)+\
                            'BUT it is available for download by setting \'download=True\'.')

    # get data + cache dir paths
    dset_paths = cache_manager.get_dataset_storage_paths(name)

    # get task cache file path
    if not cache_manager.is_task(name, task):
        # get cache default save path
        cache_save_path = os.path.join(cache_manager.default_cache_dir, name)
        if not os.path.exists(cache_save_path):
            utils.create_dir(cache_save_path)

        # preprocess dataset
        cache_info = dataset.process(name, dset_paths['data_dir'], dset_paths['cache_dir'], verbose)

        # update dbcollection.json file with the new data
        cache_manager.update(name, cache_info['data_dir'], cache_info['tasks'], cache_info['keywords'])

    # get task cache file path
    task_cache_path = cache_manager.get_cache_path(name, task)

    # Create a loader
    dataset_loader = DatasetLoader(name, task, dset_paths['data_dir'], task_cache_path)

    # do select processing here
    if select_data:
        if verbose:
            print('Select')
        dataset_loader.select_data(select_data, custom_task_name)

    # do filter processing here
    if filter_data:
        if verbose:
            print('Filter')
        dataset_loader.filter_data(filter_data, custom_task_name)

    # organize data into a list w.r.t. some field_name
    if organize_list:
        if verbose:
            print('Organize fields into lists: {}'.format(organize_list))
        dataset_loader.create_list(organize_list, custom_task_name)

    # do data balancing here
    if balance_sets:
        dataset_loader.balance_sets(balance_sets, custom_task_name)

    # return Loader
    return dataset_loader


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
    """Deletes a dataset's metadata cache files plus dir from disk/cache.

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
            print('The cache data is empty. (no datasets available)')
        else:
            import time

            # delete the entire cache
            print('**WARNING**')
            print('This will delete the entire cache.')
            print('In 10s all your cache files will be deleted.')
            print('If this was set by mistake, proceed to terminate the execution')
            for i in range(10, -1, -1):
                print('{}..'.format(i))
                time.sleep(1)
            cache_manager.delete_cache_all()
            print('Cache deletion complete.')
    else:
        # check if dataset exists in the cache file
        if cache_manager.exists_dataset(name):
            cache_manager.delete_dataset(name, False)
        else:
            print('Dataset {} does not exist.'.format(name))
            #raise Exception('Dataset ' + name + ' does not exist.')


def clear(flag=False, verbose=False):
    """Deletes the cache .json file and the cache dir of all datasets.

    Parameters
    ----------
    flag : bool
        Enables the deletion of the entire dbcollection cache if True.
        Otherwise, do nothing.
    verbose : bool
        Displays text information (if true).

    Returns
    -------
        None

    Raises
    ------
        None
    """
    if flag:
        # Load a cache manager object
        cache_manager = CacheManager()

        # delete cache dir
        if verbose:
            print('Deleting {} cache root directory and all of its contents...'.format(cache_manager.default_cache_dir))
        utils.delete_dir(cache_manager.default_cache_dir)
        if verbose:
            print('Done.')

        # delete cache file
        if verbose:
            print('Deleting {} cache file...'.format(cache_manager.cache_fname))
        utils.delete_file(cache_manager.cache_fname)
        if verbose:
            print('Done.')


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



def query(pattern):
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
    # init list
    query_list = []

    # Load a cache manager object
    cache_manager = CacheManager()

    # check info / dataset lists first
    if pattern in cache_manager.data:
        query_list.append(cache_manager.data[pattern].keys())

    # match default paths
    if pattern in cache_manager.data['info']:
        query_list.append(cache_manager.data['info'][pattern])

    # match datasets/tasks
    if pattern in cache_manager.data['dataset']:
        query_list.append(cache_manager.data['info'][pattern].keys())

    for category in cache_manager.data['dataset']:
        if pattern in cache_manager.data['dataset'][category]:
            query_list.append(cache_manager.data['dataset'][category][pattern])
        for name in cache_manager.data['dataset'][category]:
            if pattern in cache_manager.data['dataset'][category][name]:
                query_list.append(cache_manager.data['dataset'][category][name][pattern])
            if pattern in cache_manager.data['dataset'][category][name]['task']:
                query_list.append(cache_manager.data['dataset'][category][name]['task'][pattern])

    # output list
    if len(query_list) == 1:
        return query_list[0]
    else:
        return query_list


def list(verbose=False):
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

    if verbose:
        print('Printing contents of {}:'.format(cache_manager.cache_fname))

    data_ = cache_manager.data
    if not verbose:
        cat_dataset_dict = {}
        for category in cache_manager.data['dataset'].keys():
            cat_dataset_dict[category] = {}
            for name in cache_manager.data['dataset'][category].keys():
                cat_dataset_dict[category][name] = cache_manager.data['dataset'][category][name]['cache_files']['default']
        data_['dataset'] = cat_dataset_dict

    print(json.dumps(data_, sort_keys=True, indent=4))
