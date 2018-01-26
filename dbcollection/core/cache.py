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
        self.cache_filename = self._get_cache_filename()

    def _get_cache_filename(self):
        """Return the cache file name + path."""
        home_dir = os.path.expanduser("~")
        filename = 'dbcollection.json'
        return os.path.join(home_dir, filename)


class CacheManagerDataset:
    """Manage the cache's dataset configurations."""

    def __init__(self):
        """Initializes the class."""
        pass

class CacheManagerCategory:
    """Manage the cache's category configurations."""

    def __init__(self):
        """Initializes the class."""
        pass


class CacheManagerInfo:
    """Manage the cache's information configurations."""

    def __init__(self):
        """Initializes the class."""
        pass
