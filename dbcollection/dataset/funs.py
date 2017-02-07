"""
Functions to download/process a dataset using a constructor.
"""

import os
from .list_datasets import datasets


def fetch_dataset_constructor(name):
    """Fetches a dataset constructor class.

    Parameters
    ----------
    name : str
        Name of the dataset.

    Returns
    -------
    str
        Name of the category of the dataset
    <class object>
        Dataset class constructor to download/preprocess data.

    Raises
    ------
    Exception
        If a dataset name does not appear on the list.
    """
    for category in datasets.keys():
        if name in datasets[category].keys():
            return category, datasets[category][name]

    raise Exception('Undefined dataset name: {}'.format(name))


def setup_dataset_constructor(name, data_dir, cache_dir, verbose=True, is_download=True):
    """Config the dataset constructor class.

    Parameters
    ----------
    name : str
        Name of the dataset
    data_dir : str
        Directory path on the disk.
    cache_dir : bool
        Indicates if the cache_dir should be deleted.
    verbose : bool
        Display messages on the screen.

    Returns
    -------
    <class>
        Dataset class object contianing the download/preprocess data methods.
    str
        Dataset's data directory.
    str
        Dataset's metadata cache directory.
    str
        Category name.

    Raises
    ------
        None
    """
    # fetch dataset constructor
    category, constructor = fetch_dataset_constructor(name)

    # merge paths with the name+category
    if is_download:
        data_dir_ = os.path.join(data_dir, name)
    else:
        data_dir_ = data_dir
    cache_dir_ = os.path.join(cache_dir, category, name)

    # setup dataset constructor
    dataset_loader = constructor(data_dir_, cache_dir_, verbose)

    return dataset_loader, data_dir_, cache_dir_, category


def download(name, data_dir, cache_dir, verbose=True):
    """Download data of a dataset.

    Parameters
    ----------
    name : str
        Name of the dataset
    data_dir : str
        Directory path on the disk.
    cache_dir : bool
        Indicates if the cache_dir should be deleted.
    verbose : bool
        Display messages on the screen.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # get dataset constructor
    dataset_loader, data_dir_, cache_dir_, category = setup_dataset_constructor(name, data_dir, cache_dir, verbose, True)

    # check if the directories exist already
    if not os.path.exists(data_dir_):
        os.makedirs(data_dir_)

    # download data
    dataset_loader.download()

    return data_dir


def process(name, data_dir, cache_dir, verbose):
    """Process metadata of a dataset.

    Parameters
    ----------
    name : str
        Name of the dataset
    data_dir : str
        Directory path on the disk.
    cache_dir : bool
        Indicates if the cache_dir should be deleted.
    verbose : bool
        Display messages on the screen.

    Returns
    -------
    dict
        Dataset's metadata information such as data dir,cache dir, category and task(s).

    Raises
    ------
        None
    """
    # get dataset constructor
    dataset_loader, data_dir, cache_dir, category = setup_dataset_constructor(name, data_dir, cache_dir, verbose, False)

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
