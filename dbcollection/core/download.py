"""
API methods for downloading data of datasets.
"""

from __future__ import print_function
import os

from dbcollection.core.db import fetch_list_datasets
from dbcollection.core.cache import CacheManager


def get_dirs(cache_manager, name, data_dir):
    """Parse data directory and cache save path."""
    if data_dir is None or data_dir is '':
        data_dir_ = os.path.join(cache_manager.download_dir, name, 'data')
    else:
        if not os.path.exists(data_dir):
            print('Creating save directory in disk: ' + data_dir)
            os.makedirs(data_dir)

        if os.path.split(data_dir)[1] == name:
            data_dir_ = data_dir
        else:
            data_dir_ = os.path.join(data_dir, name)

    if not os.path.exists(data_dir_):
        os.makedirs(data_dir_)

    cache_save_path = os.path.join(cache_manager.cache_dir, name)
    if not os.path.exists(cache_save_path):
        os.makedirs(cache_save_path)

    return data_dir_, cache_save_path


def download(name=None, data_dir=None, extract_data=True, verbose=True, is_test=False):
    """Download a dataset data to disk.

    This method will download a dataset's data files to disk. After download,
    it updates the cache file with the  dataset's name and path where the data
    is stored.

    Parameters
    ----------
    name : str
        Name of the dataset.
    data_dir : str, optional
        Directory path to store the downloaded data.
    extract_data : bool, optional
        Extracts/unpacks the data files (if true).
	verbose : bool, optional
        Displays text information (if true).
    is_test : bool, optional
        Flag used for tests.

    Examples
    --------
    Download the CIFAR10 dataset to disk.

    >>> import dbcollection as dbc
    >>> dbc.download('cifar10')

    """
    assert not name is None, 'Must input a valid dataset name: {}'.format(name)

    available_datasets_list = fetch_list_datasets()

    # check if the dataset name exists in the list of available dataset for download
    assert name in available_datasets_list, 'Invalid dataset name: {}'.format(name)

    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    # get data dir + cache default save path
    data_dir_, cache_save_path = get_dirs(cache_manager, name, data_dir)

    if verbose:
        print('==> Download {} data to disk...'.format(name))

    # setup dataset class
    constructor = available_datasets_list[name]['constructor']
    db = constructor(data_path=data_dir_,
                     cache_path=cache_save_path,
                     extract_data=extract_data,
                     verbose=verbose)

    # download dataset
    db.download()

    # download/preprocess dataset
    keywords = available_datasets_list[name]['keywords']

    # update dbcollection.json file with the new data
    cache_manager.update(name, data_dir_, {}, keywords)

    if verbose:
        print('==> Download complete.')
