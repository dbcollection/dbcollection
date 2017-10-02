"""
API methods for processing the metadata of datasets.
"""

from __future__ import print_function
import os

from dbcollection.core.db import fetch_list_datasets
from dbcollection.core.cache import CacheManager


def exists_task(available_datasets_list, name, task):
    """Checks if a task exists for a dataset."""
    if task == '':
        task_ = available_datasets_list[name]['default_task']
    elif task == 'default':
        task_ = available_datasets_list[name]['default_task']
    elif task.endswith('_s'):
        task_ = task[:-2]
    else:
        task_ = task

    if task_ in available_datasets_list[name]['tasks']:
        return True
    else:
        return False


def process(name, task='default', verbose=True, is_test=False):
    """Process a dataset's metadata and stores it to file.

    The data is stored a a HSF5 file for each task composing the dataset's tasks.

    Parameters
    ----------
    name : str
        Name of the dataset.
    task : str, optional
        Name of the task to process.
    verbose : bool, optional
        Displays text information (if true).
    is_test : bool, optional
        Flag used for tests.

    Raises
    ------
    KeyError
        If a task does not exist for a dataset.

    Examples
    --------
    Download the CIFAR10 dataset to disk.

    >>> import dbcollection as dbc
    >>> dbc.process('cifar10', task='classification', verbose=False)

    """
    assert not name is None, 'Must input a valid dataset name: {}'.format(name)

    available_datasets_list = fetch_list_datasets()

    # check if the dataset name exists in the list of available dataset for download
    assert name in available_datasets_list, 'Invalid dataset name: {}'.format(name)

    # Load a cache manager object
    cache_manager = CacheManager(is_test)

    # get data + cache dir paths
    dset_paths = cache_manager.get_dataset_storage_paths(name)
    data_dir = dset_paths['data_dir']
    cache_save_path = dset_paths['cache_dir']

     # setup dataset class
    constructor = available_datasets_list[name]['constructor']
    db = constructor(data_path=data_dir,
                     cache_path=cache_save_path,
                     extract_data=False,
                     verbose=verbose)

    # check if task exists in the list
    if not exists_task(available_datasets_list, name, task):
        raise KeyError('The task \'{\' does not exists for loading/processing.'.format(task))

    if not os.path.exists(cache_save_path):
        os.makedirs(cache_save_path)

    # process metadata
    task_info = db.process(task)

    # update dbcollection.json file with the new data
    keywords = available_datasets_list[name]['keywords']
    cache_manager.update(name, data_dir, task_info, keywords)

    if verbose:
        print('==> Processing complete.')
