"""
Remove API class.
"""


from __future__ import print_function

from dbcollection.core.cache import CacheManager


def remove(name, task=None, delete_data=False, verbose=True, is_test=False):
    """Remove/delete a dataset and/or task from the cache.

    Removes the datasets cache information from the dbcollection.json file.
    The dataset's data files remain in disk if 'delete_data' is set to False,
    otherwise it removes also the data files.

    Also, instead of deleting the entire dataset, removing a specific task
    from disk is also possible by specifying which task to delete. This removes
    the task entry for the dataset and removes the corresponding hdf5 file from
    disk.

    Parameters
    ----------
    name : str
        Name of the dataset to delete.
    task : str, optional
        Name of the task to delete.
    delete_data : bool, optional
        Delete all data files from disk for this dataset if True.
    verbose : bool, optional
        Displays text information (if true).
    is_test : bool, optional
        Flag used for tests.

    Examples
    --------
    Remove a dataset from the list.

    >>> import dbcollection as dbc
    >>> # add a dataset
    >>> dbc.add('new_db', 'new_task', 'new/path/db', 'newdb.h5', ['new_category'])
    >>> dbc.query('new_db')
    {'new_db': {'tasks': {'new_task': 'newdb.h5'}, 'data_dir': 'new/path/db',
    'keywords': ['new_category']}}
    >>> dbc.remove('new_db')  # remove the dataset
    Removed 'new_db' dataset: cache=True, disk=False
    >>> dbc.query('new_db')  # check if the dataset info was removed (retrieves an empty dict)
    {}

    """
    assert name is not None, 'Must input a valid dataset name: {}'.format(name)

    db_remover = RemoveAPI(name=name,
                           task=task,
                           delete_data=delete_data,
                           verbose=verbose,
                           is_test=is_test)

    db_remover.run()

    if verbose:
        print('==> Dataset registry removed.')


class RemoveAPI(object):
    """Dataset remove API class.

    This class contains methods to remove
    a dataset registry from cache. Also, it
    can remove the dataset's files from disk
    if needed.

    Parameters
    ----------
    name : str
        Name of the dataset to delete.
    task : str, optional
        Name of the task to delete.
    delete_data : bool
        Delete all data files from disk for this dataset if True.
    is_test : bool
        Flag used for tests.

    Attributes
    ----------
    name : str
        Name of the dataset to delete.
    task : str
        Name of the task to delete.
    delete_data : bool
        Delete all data files from disk for this dataset if True.
    is_test : bool
        Flag used for tests.
    cache_manager : CacheManager
        Cache manager object.

    """

    def __init__(self, name, task, delete_data, verbose, is_test):
        """Initialize class."""
        assert name, 'Must input a valid dataset name: {}'.format(name)
        assert delete_data is not None, 'delete_data cannot be empty'
        assert verbose is not None, 'verbose cannot be empty'
        assert is_test is not None, 'is_test cannot be empty'

        self.name = name
        self.task = task
        self.delete_data = delete_data
        self.verbose = verbose
        self.is_test = is_test
        self.cache_manager = CacheManager(self.is_test)

    def run(self):
        """Main method."""
        if self.exists_dataset():
            self.remove_registry_from_cache()
        else:
            raise Exception('Dataset \'{}\' does not exist.'.format(self.name))

    def exists_dataset(self):
        """Return True if a dataset name exists in the cache."""
        return self.cache_manager.exists_dataset(self.name)

    def remove_registry_from_cache(self):
        """Remove the dataset or task from cache."""
        if self.task is None:
            self.remove_dataset_registry()
        else:
            self.remove_task_registry()

    def remove_dataset_registry(self):
        """Remove the dataset registry from cache."""
        if self.delete_data:
            self.cache_manager.delete_dataset(self.name, True)
        else:
            self.cache_manager.delete_dataset(self.name, False)
        if self.verbose:
            print('Removed \'{}\' dataset: cache=True, disk={}'
                  .format(self.name, self.delete_data))

    def remove_task_registry(self):
        """Remove the task registry for this dataset from cache."""
        if self.cache_manager.delete_task(self.name, self.task):
            if self.verbose:
                print('Removed the task \'{}\' from the \'{}\' dataset: cache=True'
                      .format(self.task, self.name))
        else:
            if self.verbose:
                raise Exception('The task \'{}\' does not exists for \'{}\' dataset'
                                .format(self.task, self.name))
