"""
API methods for removing a dataset from the cache.
"""

from __future__ import print_function

from dbcollection.core.cache import CacheManager


def remove(name, task=None, delete_data=False, is_test=False):
    """Remove/delete a dataset and/or task from the cache.

    Removes the datasets cache information from the dbcollection.json file.
    The dataset's data files remain on disk if 'delete_data' is set to False,
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
    is_test : bool, optional
        Flag used for tests.

    Examples
    --------
    Remove a dataset from the list.

    >>> import dbcollection as dbc
    >>> dbc.add('new_db', 'new_task', 'new/path/db', 'newdb.h5', ['new_category'])  # add a dataset
    >>> dbc.query('new_db')
    {'new_db': {'tasks': {'new_task': 'newdb.h5'}, 'data_dir': 'new/path/db', 'keywords': ['new_category']}}
    >>> dbc.remove('new_db')  # remove the dataset
    Removed 'new_db' dataset: cache=True, disk=False
    >>> dbc.query('new_db')  # check if the dataset info was removed (retrieves an empty dict)
    {}

    """
    assert not name is None, 'Must input a valid dataset name: {}'.format(name)

    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    # check if dataset exists in the cache file
    if cache_manager.exists_dataset(name):
        if task is None:
            if delete_data:
                cache_manager.delete_dataset(name, True)
            else:
                cache_manager.delete_dataset(name, False)

            print('Removed \'{}\' dataset: cache=True, disk={}'.format(name, delete_data))
        else:
            if cache_manager.delete_task(name, task):
                print('Removed the task \'{}\' from the \'{}\' dataset: cache=True'.format(task, name))
            else:
                print('Do nothing.')
    else:
        print('Dataset \'{}\' does not exist.'.format(name))
