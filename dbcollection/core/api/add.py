"""
Add API class.
"""


from __future__ import print_function

from dbcollection.core.cache import CacheManager


def add(name, task, data_dir, hdf5_filename, categories=(), verbose=True):
    """Add a dataset/task to the list of available datasets for loading.

    Parameters
    ----------
    name : str
        Name of the dataset.
    task : str
        Name of the task to load.
    data_dir : str
        Path of the stored data in disk.
    hdf5_filename : str
        Path to the metadata HDF5 file.
    categories : list, optional
        List of keyword strings to categorize the dataset.
    verbose : bool, optional
        Displays text information (if true).

    Examples
    --------
    Add a dataset manually to dbcollection.

    >>> import dbcollection as dbc
    >>> dbc.add('new_db', 'new_task', 'new/path/db', 'newdb.h5', ['new_category'])
    >>> dbc.query('new_db')
    {'new_db': {'tasks': {'new_task': 'newdb.h5'}, 'data_dir': 'new/path/db', 'keywords':
    ['new_category']}}

    """
    assert name, "Must input a valid name."
    assert task, "Must input a valid task."
    assert data_dir, "Must input a valid data_dir."
    assert hdf5_filename, "Must input a valid file_path."
    assert isinstance(categories, (list, tuple, str)), "Must input valid categories: (list, tuple or str)."
    assert isinstance(verbose, bool), "Must input a valid boolean for verbose."

    if isinstance(categories, str):
        categories = (categories,)
    else:
        categories = tuple(categories)

    db_adder = AddAPI(name=name,
                      task=task,
                      data_dir=data_dir,
                      hdf5_filename=hdf5_filename,
                      categories=categories,
                      verbose=verbose)

    db_adder.run()


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
    hdf5_filename : str
        Path to the metadata HDF5 file.
    keywords : list of strings
        List of keywords to categorize the dataset.

    Attributes
    ----------
    name : str
        Name of the dataset.
    task : str
        Name of the task to load.
    data_dir : str
        Path of the stored data in disk.
    hdf5_filename : bool
        Path to the metadata HDF5 file.
    keywords : list of strings
        List of keywords to categorize the dataset.
    cache_manager : CacheManager
        Cache manager object.

    """

    def __init__(self, name, task, data_dir, hdf5_filename, categories, verbose):
        """Initialize class."""
        assert name, "Must input a valid name."
        assert task, "Must input a valid task."
        assert data_dir, "Must input a valid data_dir."
        assert hdf5_filename, "Must input a valid file_path."
        assert isinstance(categories, tuple), "Must input a valid list(tuple) of categories."
        assert isinstance(verbose, bool), "Must input a valid boolean for verbose."

        self.name = name
        self.task = task
        self.data_dir = data_dir
        self.hdf5_filename = hdf5_filename
        self.categories = categories
        self.verbose = verbose
        self.cache_manager = self.get_cache_manager()

    def get_cache_manager(self):
        return CacheManager()

    def run(self):
        """Main method."""
        if self.verbose:
            print('==> Adding a dataset registry to the cache records in disk.')

        self.cache_manager.update(name=self.name,
                                  data_dir=self.data_dir,
                                  cache_tasks={self.task: self.file_path},
                                  cache_keywords=self.keywords,
                                  is_append=True)
