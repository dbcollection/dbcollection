"""
Class to manage the dbcollection.json cache file.
"""


from __future__ import print_function
import os
import shutil
import errno
import json
import warnings


class CacheManager:
    """Manage dbcollection configurations and stores them inside a cache file stored in disk.

    Parameters
    ----------
    is_test : bool
        Flag used for tests.

    Attributes
    ----------
    is_test : bool
        Flag used for tests.
    cache_filename : str
        Cache file path + name.
    cache_dir : str
        Default directory to store all dataset's metadata files.
    download_dir : str
        Default save dir path for downloaded data.
    data : dict
        Cache contents.

    """

    def __init__(self):
        """Initializes the class."""
        self.manager = CacheDataManager()
        self.info = CacheManagerInfo(self.manager)
        self.dataset = CacheManagerDataset(self.manager)
        self.category = CacheManagerCategory(self.manager)


class CacheDataManager:
    """Cache's data write/read methods."""

    def __init__(self):
        """Initialize class."""
        self.cache_filename = self._get_cache_filename()
        self.data = self.read_data_cache()
        self._cache_dir = self._get_cache_dir()
        self.info = CacheManagerInfo(self.data["info"])

    def _get_cache_filename(self):
        """Return the cache file name + path."""
        home_dir = os.path.expanduser("~")
        filename = 'dbcollection.json'
        return os.path.join(home_dir, filename)

    def read_data_cache(self):
        """Loads data from the cache file.

        Returns
        -------
        dict
            Data containing information of all datasets and categories.

        """
        if os.path.exists(self.cache_filename):
            return self.read_data_cache_file()
        else:
            data = self._empty_data()
            self.write_data_cache(data)
            return data

    def read_data_cache_file(self):
        """Read the cache file data to memory.

        Returns
        -------
        dict
            Data structure of the cache (file).

        """
        with open(self.cache_filename, 'r') as json_data:
            return json.load(json_data)

    def _empty_data(self):
        """Returns an empty (dummy) template of the cache data structure."""
        return {
            "info": {
                "root_cache_dir": self._get_default_cache_dir(),
                "root_downloads_dir": self._get_default_downloads_dir(),
            },
            "dataset": {},
            "category": {}
        }

    def _get_default_cache_dir(self):
        """Returns the pre-defined path of the cache's root directory."""
        default_cache_dir = os.path.join(os.path.expanduser("~"), 'dbcollection')
        return default_cache_dir

    def _get_default_downloads_dir(self):
        """Returns the pre-defined path of the cache's downloads directory."""
        default_downloads_dir = os.path.join(self._get_default_cache_dir(), 'downloads')
        return default_downloads_dir

    def write_data_cache(self, data):
        """Writes data to the cache file.

        Parameters
        ----------
        name : str
            Name of the dataset.

        Raises
        ------
        IOError
            If the file cannot be opened.

        """
        assert data, 'Must input a non-empty dictionary.'
        with open(self.cache_filename, 'w') as file_cache:
            json.dump(data, file_cache, sort_keys=True, indent=4, ensure_ascii=False)
        self.data = data  # must assign the new data or risk problems

    def _set_cache_dir(self, path):
        """Set the root cache dir to store all metadata files"""
        assert path, 'Must input a directory path'
        self._cache_dir = path
        self.data['info']['root_cache_dir'] = self._cache_dir
        self.write_data_cache(self.data)

    def _get_cache_dir(self):
        """Get the root cache dir path."""
        return self.data['info']['root_cache_dir']

    cache_dir = property(_get_cache_dir, _set_cache_dir)

    def reset_cache_dir(self):
        """Reset the root cache dir path."""
        self._set_cache_dir(self._get_default_cache_dir())

    def _set_download_dir(self, path):
        """Set the root save dir path for downloaded data."""
        assert path, 'Must input a non-empty path.'
        self.data['info']['root_downloads_dir'] = path
        self.write_data_cache(self.data)

    def _get_download_dir(self):
        """Get the root save dir path."""
        return self.data['info']['root_downloads_dir']

    download_dir = property(_get_download_dir, _set_download_dir)

    def reset_download_dir(self):
        """Reset the root download dir path."""
        return self._set_download_dir(self._get_default_downloads_dir())

    def reset_cache(self, force_reset=False):
        """Resets the cache file contents.

        Resets the cache file by removing all info about
        the datasets/categories/info from the cache file.
        Basically, it empties the cache contents.

        Parameters
        ----------
        force_reset : bool, optional
            Forces the cache to be reset (emptied) if True.

        Warning
        -------
        UserWarning
            If force_reset is False, display a warning to the user.

        """
        if force_reset:
            self.write_data_cache(self._empty_data())
        else:
            msg = 'All information about stored datasets will be lost if you proceed! ' + \
                  'Set \'force_reset=True\' to proceed with the reset of dbcollection.json.'
            warnings.warn(msg, UserWarning, stacklevel=2)


class CacheManagerDataset:
    """Manage the cache's dataset configurations."""

    def __init__(self, manager):
        """Initialize class."""
        assert manager, "Must input a valid cache manager."
        self.manager = manager


class CacheManagerCategory:
    """Manage the cache's category configurations."""

    def __init__(self, manager):
        """Initialize class."""
        assert manager, "Must input a valid cache manager."
        self.manager = manager


class CacheManagerInfo:
    """Manage the cache's information configurations."""

    def __init__(self, manager):
        """Initialize class."""
        assert manager, "Must input a valid cache manager."
        self.manager = manager

    def _set_cache_dir(self, path):
        """Set the root cache dir to store all metadata files"""
        assert path, 'Must input a directory path'
        self.manager.cache_dir = path

    def _get_cache_dir(self):
        """Get the root cache dir path."""
        return self.manager.cache_dir

    cache_dir = property(_get_cache_dir, _set_cache_dir)

    def reset_cache_dir(self):
        """Reset the root cache dir path."""
        self.manager.reset_cache_dir()

    def _set_download_dir(self, path):
        """Set the root save dir path for downloaded data."""
        assert path, 'Must input a non-empty path.'
        self.manager.download_dir = path

    def _get_download_dir(self):
        """Get the root save dir path."""
        return self.manager.download_dir

    download_dir = property(_get_download_dir, _set_download_dir)
