"""
Process API class.
"""


from __future__ import print_function
import os

from dbcollection.core.manager import CacheManager

from .metadata import MetadataConstructor


def process(name, task='default', verbose=True):
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

    Raises
    ------
    KeyError
        If a task does not exist for a dataset.

    Examples
    --------
    >>> import dbcollection as dbc

    Download the CIFAR10 dataset to disk.

    >>> dbc.process('cifar10', task='classification', verbose=False)

    """
    assert name, 'Must input a valid dataset name.'

    processer = ProcessAPI(name=name,
                           task=task,
                           verbose=verbose)

    processer.run()


class ProcessAPI(object):
    """Dataset metadata process API class.

    This class contains methods to correctly process
    the dataset's data files and convert their metadata
    to disk.

    Parameters
    ----------
    name : str
        Name of the dataset.
    task : str
        Name of the task to process.
    verbose : bool
        Displays text information (if true).

    Attributes
    ----------
    name : str
        Name of the dataset.
    task : str
        Name of the task to process.
    verbose : bool
        Displays text information (if true).
    extract_data : bool
        Flag to extract data (if True).
    cache_manager : CacheManager
        Cache manager object.

    Raises
    ------
    KeyError
        If a task does not exist for a dataset.

    """

    def __init__(self, name, task, verbose):
        """Initialize class."""
        assert isinstance(name, str), 'Must input a valid dataset name.'
        assert isinstance(task, str), 'Must input a valid task name.'
        assert isinstance(verbose, bool), "Must input a valid boolean for verbose."

        self.name = name
        self.task = task
        self.verbose = verbose
        self.extract_data = False
        self.cache_manager = self.get_cache_manager()

    def get_cache_manager(self):
        return CacheManager()

    def run(self):
        """Main method."""
        if self.verbose:
            print('==> Setup directories to store the data files.')
        self.set_dirs_processed_metadata()

        if self.verbose:
            print('==> Process \'{}\' metadata to disk...'.format(self.name))
        task_info = self.process_dataset()

        if self.verbose:
            print('==> Updating the cache manager')
        self.update_cache(task_info)

        if self.verbose:
            print('==> Dataset processing complete.')

    def set_dirs_processed_metadata(self):
        cache_dir = self.get_dataset_cache_dir_path()
        self.create_dir(cache_dir)

    def get_dataset_cache_dir_path(self):
        cache_dir = self.get_cache_dir_path_from_cache()
        return os.path.join(cache_dir, self.name)

    def get_cache_dir_path_from_cache(self):
        return self.cache_manager.info.cache_dir

    def create_dir(self, path):
        """Create a directory in the disk."""
        if not os.path.exists(path):
            os.makedirs(path)

    def process_dataset(self):
        """Process the dataset's metadata."""
        data_dir = self.get_dataset_data_dir_path()
        cache_dir = self.get_dataset_cache_dir_path()
        task = self.parse_task_name(self.task)
        self.check_if_task_exists_in_database(task)
        return self.process_dataset_metadata(data_dir, cache_dir, task)

    def get_dataset_constructor(self):
        db_metadata = self.get_dataset_metadata_obj(self.name)
        constructor = db_metadata.get_constructor()
        return constructor

    def get_dataset_metadata_obj(self, name):
        return MetadataConstructor(name)

    def get_dataset_data_dir_path(self):
        dataset_metadata = self.get_dataset_metadata_from_cache()
        return dataset_metadata['data_dir']

    def get_dataset_metadata_from_cache(self):
        return self.cache_manager.dataset.get(self.name)

    def parse_task_name(self, task):
        """Parse the input task string."""
        if task == '' or task == 'default':
            task_parsed = self.get_default_task()
        else:
            task_parsed = task
        return task_parsed

    def get_default_task(self):
        """Returns the default task for this dataset."""
        db_metadata = self.get_dataset_metadata_obj(self.name)
        default_task = db_metadata.get_default_task()
        return default_task

    def check_if_task_exists_in_database(self, task):
        """Check if task exists in the list of available tasks for processing."""
        if not self.exists_task(task):
            raise KeyError('The task \'{}\' does not exists for loading/processing.'
                           .format(self.task))

    def exists_task(self, task):
        """Checks if a task exists for a dataset."""
        db_metadata = self.get_dataset_metadata_obj(self.name)
        return task in db_metadata.get_tasks()

    def process_dataset_metadata(self, data_dir, cache_dir, task):
        constructor = self.get_dataset_constructor()
        db = constructor(data_path=data_dir,
                         cache_path=cache_dir,
                         extract_data=self.extract_data,
                         verbose=self.verbose)
        task_info = db.process(task)
        return task_info

    def update_cache(self, task_info):
        """Update the cache manager information for this dataset."""
        cache_dir = self.get_dataset_cache_dir_path()
        self.cache_manager.dataset.update(name=self.name,
                                          cache_dir=cache_dir,
                                          tasks=task_info)
