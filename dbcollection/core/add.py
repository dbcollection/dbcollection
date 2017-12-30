"""
Add API class.
"""

from __future__ import print_function

from dbcollection.core.cache import CacheManager


class AddAPI(object):
    """Add dataset API class.

    This class contains methods to correctly register
    a dataset in the cache.

    Parameters
    ----------
    name : str
        Name of the dataset.
    task : str
        Name of the task to load.
    data_dir : str
        Path of the stored data in disk.
    file_path : bool
        Path to the metadata HDF5 file.
    keywords : list of strings
        List of keywords to categorize the dataset.
    is_test : bool
        Flag used for tests.

    Attributes
    ----------
    name : str
        Name of the dataset.
    task : str
        Name of the task to load.
    data_dir : str
        Path of the stored data in disk.
    file_path : bool
        Path to the metadata HDF5 file.
    keywords : list of strings
        List of keywords to categorize the dataset.
    is_test : bool
        Flag used for tests.
    cache_manager : CacheManager
        Cache manager object.

    """

    def __init__(self, name, task, data_dir, file_path, keywords, verbose, is_test):
        """Initialize class."""
        assert name, "Must input a valid name: {}".format(name)
        assert task, "Must input a valid task: {}".format(task)
        assert data_dir, "Must input a valid data_dir: {}".format(data_dir)
        assert file_path, "Must input a valid file_path: {}".format(file_path)
        assert keywords is not None, "keywords cannot be empty"
        assert verbose is not None, "verbose cannot be empty"
        assert is_test is not None, "is_test cannot be empty"

        self.name = name
        self.task = task
        self.data_dir = data_dir
        self.file_path = file_path
        self.keywords = keywords
        self.verbose = verbose
        self.is_test = is_test

        self.cache_manager = CacheManager(self.is_test)

    def run(self):
        """<stuff>.

        ** Main method **

        """
        if self.verbose:
            print('==> Adding a dataset registry to the cache records in disk.')

        self.cache_manager.update(name=self.name,
                                  data_dir=self.data_dir,
                                  cache_tasks={self.task: self.file_path},
                                  cache_keywords=self.keywords,
                                  is_append=True)
