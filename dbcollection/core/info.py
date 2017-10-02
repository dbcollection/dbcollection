"""
API methods for printing information of the cache.
"""

from __future__ import print_function
import json

from dbcollection.core.db import fetch_list_datasets
from dbcollection.core.cache import CacheManager


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
        for name in names:
            print(json.dumps(data['dataset'][name], sort_keys=True, indent=4))
    else:
        print(json.dumps(data['dataset'], sort_keys=True, indent=4))
    print('')


def print_categories_info(data, names=None):
    """Prints the categories information of the cache."""
    if any(data['category']):
        print('------------------------')
        print('  Datasets by category ')
        print('------------------------\n')
        if names:
            max_size_name = max([len(name) for name in names]) + 7
            for name in names:
                print("{:{}}".format('   > {}: '.format(name), max_size_name)
                    + "{}".format(sorted(data['category'][name])))
        else:
            max_size_name = max([len(name) for name in data['category']]) + 7
            for name in data['category']:
                    print("{:{}}".format('   > {}: '.format(name), max_size_name)
                        + "{}".format(sorted(data['category'][name])))
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
            names = (name)
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


def info_datasets(db_pattern='', show_downloaded=True, show_available=True, is_test=True):
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
