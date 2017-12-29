"""
Process API class.
"""

from __future__ import print_function
import os

from dbcollection.core.cache import CacheManager

from .list_datasets import fetch_list_datasets


class ProcessAPI(object):
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

    def __init__(self, name, task, verbose, is_test):
        """Initialize class."""
        assert name, 'Must input a valid dataset name: {}'.format(name)
        assert name, 'Must input a valid task name: {}'.format(task)
        assert verbose is not None, 'verbose cannot be empty'
        assert is_test is not None, 'is_test cannot be empty'

        self.name = name
        self.task = task
        self.verbose = verbose
        self.is_test = is_test
        self.extract_data = False
        self.cache_manager = CacheManager(self.is_test)
        self.available_datasets_list = fetch_list_datasets()

        self.check_if_task_exists()

    def check_if_task_exists(self):
        """Check if task exists in the list of available tasks for processing."""
        if not self.exists_task():
            raise KeyError('The task \'{}\' does not exists for loading/processing.'
                           .format(self.task))

    def exists_task(self):
        """Checks if a task exists for a dataset."""
        if self.task == '':
            task_ = self.get_default_task()
        elif self.task == 'default':
            task_ = self.get_default_task()
        elif self.task.endswith('_s'):
            task_ = self.task[:-2]
        else:
            task_ = self.task
        return task_ in self.available_datasets_list[self.name]['tasks']

    def get_default_task(self):
        """Returns the default task for this dataset."""
        return self.available_datasets_list[self.name]['default_task']

    def run(self):
        """Process the metadata of the dataset into an HDF5 file.

        ** Main method **

        """
        self.set_dataset_dirs()
        self.process_dataset()
        self.update_cache()

    def set_dataset_dirs(self):
        """Set the dataset's data + cache dirs in disk."""
        if self.verbose:
            print('==> Setup directories to store the data files.')

        dset_paths = self.cache_manager.get_dataset_storage_paths(self.name)
        self.save_data_dir = dset_paths['data_dir']
        self.save_cache_dir = dset_paths['cache_dir']
        self.create_dir(self.save_cache_dir)

    def create_dir(self, path):
        """Create a directory in the disk."""
        if not os.path.exists(path):
            os.makedirs(path)

    def process_dataset(self):
        """Process the dataset's metadata."""
        if self.verbose:
            print('==> Process \'{}\' metadata to disk...'.format(self.name))

        constructor = self.available_datasets_list[self.name]['constructor']
        db = constructor(data_path=self.save_data_dir,
                         cache_path=self.save_cache_dir,
                         extract_data=self.extract_data,
                         verbose=self.verbose)

        self.task_info = db.process(self.task)

    def update_cache(self):
        """Update the cache manager information for this dataset."""
        if self.verbose:
            print('==> Updating the cache manager')

        keywords = self.available_datasets_list[self.name]['keywords']
        self.cache_manager.update(self.name,
                                  self.save_data_dir,
                                  self.task_info,
                                  keywords)
