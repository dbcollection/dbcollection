"""
Functions to download/process a dataset using a constructor.
"""


from __future__ import print_function
import os
from .dblist import datasets


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
    class
        Dataset class constructor to download/preprocess data.

    Raises
    ------
    KeyError
        If a dataset name does not exist on the list.
    """
    try:
        return datasets[name]
    except KeyError:
        raise KeyError('Undefined dataset name: {}'.format(name))


def setup_dataset_constructor(name, data_dir, cache_dir, extract_data=True, verbose=True):
    """Config the dataset constructor class.

    Parameters
    ----------
    name : str
        Name of the dataset
    data_dir : str
        Directory path on the disk.
    cache_dir : bool
        Indicates if the cache_dir should be deleted.
    extract_data : bool
        Extracts/unpacks the data files (if true).
    verbose : bool
        Display messages on the screen.

    Returns
    -------
    class
        Dataset class object contianing the download/preprocess data methods.

    Raises
    ------
        None
    """
    # check if the directories exist already
    assert os.path.exists(data_dir), 'Data directory does not exist: {}'.format(data_dir)

    # check if the directories exist already
    assert os.path.exists(cache_dir), 'Cache directory does not exist: {}'.format(cache_dir)

    # fetch dataset constructor
    constructor = fetch_dataset_constructor(name)

    # setup dataset constructor
    return constructor(data_dir, cache_dir, extract_data, verbose)


def exists(name):
    """Checks if a dataset name exists for download.

    Parameters
    ----------
    name : str
        Name of the dataset.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    for category in datasets:
        if name in datasets[category]:
            return True
    return False


def download(name, data_dir, cache_dir, extract_data=True, verbose=True):
    """Download data of a dataset.

    Parameters
    ----------
    name : str
        Name of the dataset
    data_dir : str
        Directory path on the disk.
    cache_dir : bool
        Indicates if the cache_dir should be deleted.
    extract_data : bool
        Extracts/unpacks the data files (if true).
    verbose : bool
        Display messages on the screen.
    is_download : bool
        Enables/disables data download/extraction.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # get dataset constructor
    dataset_loader = setup_dataset_constructor(name, data_dir, cache_dir, extract_data, verbose)

    # download data
    return dataset_loader.download()


def process(name, task, data_dir, cache_dir, verbose):
    """Process metadata of a dataset.

    Parameters
    ----------
    name : str
        Name of the dataset
    task : str
        Name of the task to process.
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
    dataset_loader = setup_dataset_constructor(name, data_dir, cache_dir, False, verbose)

    # check if the directories exist already
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # process metadata
    try:
        cache_info, keywords = dataset_loader.process(task)
    except KeyError:
        raise KeyError('The task ::{}:: does not exists for loading/processing.'.format(task))

    # return some info to update the cache file
    return {
        'data_dir' : data_dir,
        'cache_dir' : cache_dir,
        'tasks' : cache_info,
        'keywords' : keywords
    }
