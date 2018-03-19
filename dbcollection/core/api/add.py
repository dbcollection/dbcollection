"""
Add API class.
"""


from __future__ import print_function

from dbcollection.core.manager import CacheManager


def add(name, task, data_dir, hdf5_filename, categories=(), verbose=True, force_overwrite=False):
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
    force_overwrite : bool, optional
        Forces the overwrite of data in cache

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

    if isinstance(categories, str):
        categories = (categories,)
    else:
        categories = tuple(categories)

    db_adder = AddAPI(name=name,
                      task=task,
                      data_dir=data_dir,
                      hdf5_filename=hdf5_filename,
                      categories=categories,
                      verbose=verbose,
                      force_overwrite=force_overwrite)

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
    categories : tuple
        List of keyword strings to categorize the dataset.
    verbose : bool
        Displays text information.
    force_overwrite : bool
        Forces the overwrite of data in cache

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
    categories : tuple
        Tuple of keyword strings to categorize the dataset.
    verbose : bool
        Displays text information.
    force_overwrite : bool
        Forces the overwrite of data in cache
    cache_manager : CacheManager
        Cache manager object.

    """

    def __init__(self, name, task, data_dir, hdf5_filename, categories, verbose, force_overwrite):
        """Initialize class."""
        assert isinstance(name, str), "Must input a valid name."
        assert isinstance(task, str), "Must input a valid task."
        assert isinstance(data_dir, str), "Must input a valid data_dir."
        assert isinstance(hdf5_filename, str), "Must input a valid file_path."
        assert isinstance(categories, tuple), "Must input a valid list(tuple) of categories."
        assert isinstance(verbose, bool), "Must input a valid boolean for verbose."
        assert isinstance(force_overwrite, bool), "Must input a valid boolean for force_overwrite."

        self.name = name
        self.task = task
        self.data_dir = data_dir
        self.hdf5_filename = hdf5_filename
        self.categories = categories
        self.verbose = verbose
        self.force_overwrite = force_overwrite
        self.cache_manager = self.get_cache_manager()

    def get_cache_manager(self):
        return CacheManager()

    def run(self):
        """Main method."""
        self.add_dataset_to_cache()

        if self.verbose:
            print('==> Dataset successfully registered.')

    def add_dataset_to_cache(self):
        if self.dataset_exists_in_cache(self.name):
            self.update_dataset_cache_data()
            self.add_task_to_cache()
        else:
            self.add_new_data_to_cache()

    def dataset_exists_in_cache(self, name):
        return self.cache_manager.dataset.exists(name)

    def update_dataset_cache_data(self):
        if any(self.data_dir):
            self.cache_manager.dataset.update(
                name=self.name,
                data_dir=self.data_dir
            )

    def add_task_to_cache(self):
        if self.check_if_task_exists_in_cache():
            if self.force_overwrite:
                self.update_task_entry_in_cache()
            else:
                msg = "'{}' already exists in cache for '{}'. ".format(self.task, self.name) + \
                      "To overwrite it, you must set 'force_overwrite=True'."
                raise Exception(msg)
        else:
            self.add_task_entry_to_cache()

    def check_if_task_exists_in_cache(self):
        return self.cache_manager.task.exists(self.name, self.task)

    def update_task_entry_in_cache(self):
        self.cache_manager.task.update(
            name=self.name,
            task=self.task,
            filename=self.hdf5_filename,
            categories=self.categories
        )

    def add_task_entry_to_cache(self):
        self.cache_manager.task.add(
            name=self.name,
            task=self.task,
            filename=self.hdf5_filename,
            categories=self.categories
        )

    def add_new_data_to_cache(self):
        self.cache_manager.dataset.add(
            name=self.name,
            data_dir=self.data_dir,
            tasks={
                self.task: {
                    "filename": self.hdf5_filename,
                    "categories": self.categories
                }
            }
        )
