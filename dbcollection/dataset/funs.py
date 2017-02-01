"""
Functions to download/process a dataset using a constructor.
"""

import os
from .list import dataset_list


def fetch_dataset_constructor(name):
    """
    Fetches a dataset constructor class.
    """
    for category in dataset_list.keys():
        for dname in dataset_list[category].keys():
            if dname == name:
                return category, dataset_list[category][name]

    raise Exception('Undefined dataset name: '+str(name))


def setup_dataset_constructor(name, data_dir, cache_dir, verbose=True):
    """
    Config the dataset consturctor class.
    """
    # fetch dataset constructor
    category, constructor = fetch_dataset_constructor(name)

    # merge paths with the name+category
    data_dir_ = os.path.join(data_dir, name)
    cache_dir_ = os.path.join(cache_dir, category, name)

    # setup dataset constructor
    dataset_loader = constructor(data_dir_, cache_dir_, verbose)

    return dataset_loader, data_dir_, cache_dir_, category


def download(name, data_dir, cache_dir, verbose=True):
    """
    Donwload data of a dataset.
    """
    # get dataset constructor
    dataset_loader, data_dir, cache_dir, category = setup_dataset_constructor(name, data_dir, cache_dir, verbose)

    # check if the directories exist already
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # download data
    dataset_loader.download()


def process(name, data_dir, cache_dir, verbose):
    """
    Download/process data of a dataset.
    """
    # get dataset constructor
    dataset_loader, data_dir, cache_dir, category = setup_dataset_constructor(name, data_dir, cache_dir, verbose)

    # check if the directories exist already
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # process metadata
    cache_info = dataset_loader.process()

    # return some info to update the cache file
    return {
        'data_dir' : data_dir,
        'cache_dir' : cache_dir,
        'task' : cache_info,
        'category' : category
    }
