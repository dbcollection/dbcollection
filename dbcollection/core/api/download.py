"""
Download API class.
"""


from __future__ import print_function
import os

from dbcollection.core.cache import CacheManager

from .list_datasets import fetch_list_datasets, check_if_dataset_name_is_valid


def download(name, data_dir=None, extract_data=True, verbose=True):
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

    Examples
    --------
    Download the CIFAR10 dataset to disk.

    >>> import dbcollection as dbc
    >>> dbc.download('cifar10')

    """
    assert name, 'Must input a valid dataset name: {}'.format(name)
    check_if_dataset_name_is_valid(name)

    downloader = DownloadAPI(name=name,
                             data_dir=data_dir,
                             extract_data=extract_data,
                             verbose=verbose)

    downloader.run()

    if verbose:
        print('==> Dataset download complete.')


class DownloadAPI(object):
    """Dataset download API class.

    This class contains methods to correctly download
    a dataset's data files to disk.

    Parameters
    ----------
    name : str
        Name of the dataset.
    data_dir : str
        Directory path to store the downloaded data.
    extract_data : bool
        Extracts/unpacks the data files (if true).
    verbose : bool
        Displays text information (if true).

    Attributes
    ----------
    name : str
        Name of the dataset.
    data_dir : str
        Directory path to store the downloaded data.
    save_data_dir : str
        Data files save dir path.
    save_cache_dir : str
        Cache save dir path.
    extract_data : bool
        Flag to extract data (if True).
    verbose : bool
        Flag to display text information (if true).
    available_datasets_list : dict
        Dictionary of available datasets.
    cache_manager : CacheManager
        Cache manager object.

    """

    def __init__(self, name, data_dir, extract_data, verbose):
        """Initialize class."""
        assert name, 'Must input a valid dataset name: {}'.format(name)
        assert extract_data is not None, 'extract_data cannot be empty'
        assert verbose is not None, 'verbose cannot be empty'

        self.name = name
        self.data_dir = data_dir
        self.extract_data = extract_data
        self.verbose = verbose
        self.cache_manager = self.get_cache_manager()
        self.available_datasets_list = fetch_list_datasets()

        self.save_data_dir = self.get_download_data_dir()
        self.save_cache_dir = self.get_download_cache_dir()

    def get_cache_manager(self):
        return CacheManager()

    def get_download_data_dir(self):
        if self.data_dir:
            return self.data_dir
        else:
            return self.get_download_data_dir_from_cache()

    def get_download_data_dir_from_cache(self):
        """Create a dir path from the cache information for this dataset."""
        save_data_dir = os.path.join(self.cache_manager.manager.download_dir, self.name)
        self.create_dir(save_data_dir)
        return save_data_dir

    def create_dir(self, path):
        """Create a directory in the disk."""
        if not os.path.exists(path):
            if self.verbose:
                print('Creating save directory in disk: {}'.format(path))
            os.makedirs(path)

    def get_download_cache_dir(self):
        cache_save_path = os.path.join(self.cache_manager.manager.cache_dir, self.name)
        self.create_dir(cache_save_path)
        return cache_save_path

    def run(self):
        """Main method."""
        self.download_dataset()
        self.update_cache()

    def download_dataset(self):
        """Download the dataset to disk."""
        if self.verbose:
            print('==> Download {} data to disk...'.format(self.name))

        constructor = self.get_dataset_constructor()
        db = constructor(data_path=self.save_data_dir,
                         cache_path=self.save_cache_dir,
                         extract_data=self.extract_data,
                         verbose=self.verbose)
        db.download()

    def get_dataset_constructor(self):
        return self.available_datasets_list[self.name]['constructor']

    def update_cache(self):
        """Update the cache manager information for this dataset."""
        if self.verbose:
            print('==> Updating the cache manager')

        keywords = self.available_datasets_list[self.name]['keywords']
        self.cache_manager.update(self.name,
                                  self.save_data_dir,
                                  {},
                                  keywords)
