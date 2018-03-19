"""
Remove API class.
"""


from __future__ import print_function
import shutil

from dbcollection.core.manager import CacheManager


def remove(name, task='', delete_data=False, verbose=True):
    """Remove/delete a dataset and/or task from the cache.

    Removes the dataset's information registry from the dbcollection.json cache file.
    The dataset's data files remain in disk if 'delete_data' is not enabled.
    If you intended to remove the data files as well, the 'delete_data' input arg
    must be set to 'True' in order to also remove the data files.

    Moreover, if the intended action is to remove a task of the dataset from the cache
    registry, this can be achieved by specifying the task name to be deleted. This
    effectively removes only that task entry for the dataset. Note that deleting a task
    results in removing the associated HDF5 metadata file from disk.

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
    assert name, 'Must input a valid dataset name.'

    db_remover = RemoveAPI(name=name,
                           task=task,
                           delete_data=delete_data,
                           verbose=verbose)

    db_remover.run()


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

    Attributes
    ----------
    name : str
        Name of the dataset to delete.
    task : str
        Name of the task to delete.
    delete_data : bool
        Delete all data files from disk for this dataset if True.
    cache_manager : CacheManager
        Cache manager object.

    """

    def __init__(self, name, task, delete_data, verbose):
        """Initialize class."""
        assert isinstance(name, str), 'Must input a valid dataset name.'
        assert isinstance(task, str), 'Must input a valid task name.'
        assert isinstance(delete_data, bool), "Must input a valid boolean for delete_data."
        assert isinstance(verbose, bool), "Must input a valid boolean for verbose."

        self.name = name
        self.task = task
        self.delete_data = delete_data
        self.verbose = verbose
        self.cache_manager = self.get_cache_manager()

    def get_cache_manager(self):
        return CacheManager()

    def run(self):
        """Main method."""
        self.remove_dataset()

        if self.verbose:
            self.print_msg_registry_removal()

    def remove_dataset(self):
        """Removes the dataset from cache (and disk if selected)."""
        if self.exists_dataset():
            self.remove_registry_from_cache()
        else:
            raise Exception('Dataset \'{}\' does not exist in the cache.'.format(self.name))

    def exists_dataset(self):
        """Return True if a dataset name exists in the cache."""
        return self.cache_manager.dataset.exists(self.name)

    def remove_registry_from_cache(self):
        """Remove the dataset or task from cache."""
        if any(self.task):
            self.remove_task_registry()
        else:
            self.remove_dataset_registry()

    def remove_dataset_registry(self):
        """Removes the dataset registry from cache."""
        if self.delete_data:
            self.remove_dataset_data_files_from_disk()
        self.remove_dataset_entry_from_cache()

    def remove_dataset_data_files_from_disk(self):
        """Removes the directory containing the data files from disk."""
        data_dir = self.get_dataset_data_dir()
        shutil.rmtree(data_dir)

    def get_dataset_data_dir(self):
        dataset_metadata = self.cache_manager.dataset.get(self.name)
        return dataset_metadata["data_dir"]

    def remove_dataset_entry_from_cache(self):
        """Removes the dataset registry from cache."""
        self.cache_manager.dataset.delete(self.name)

    def remove_task_registry(self):
        """Remove the task registry for this dataset from cache."""
        self.cache_manager.task.delete(self.name, self.task)

    def print_msg_registry_removal(self):
        """Prints to screen the success message."""
        if any(self.task):
            print('Removed the task \'{}\' from the \'{}\' dataset: cache=True'
                  .format(self.task, self.name))
        else:
            print('Removed \'{}\' dataset: cache=True, disk={}'
                  .format(self.name, self.delete_data))
