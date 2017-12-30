"""
Load API class.
"""


from __future__ import print_function

from dbcollection.core.cache import CacheManager
from dbcollection.core.loader import DataLoader

from .download import DownloadAPI
from .process import ProcessAPI
from .list_datasets import fetch_list_datasets


class LoadAPI(object):
    """Dataset load API class.

    This class contains methods to correctly load
    a dataset's metadata as a data loader object.

    Parameters
    ----------
    name : str
        Name of the dataset.
    task : str
        Name of the task to load.
    data_dir : str
        Directory path to store the downloaded data.
    verbose : bool
        Displays text information (if true).
    is_test : bool
        Flag used for tests.

    Attributes
    ----------
    name : str
        Name of the dataset.
    task : str
        Name of the task to load.
    data_dir : str
        Directory path to store the downloaded data.
    verbose : bool
        Displays text information (if true).
    is_test : bool
        Flag used for tests.
    cache_manager : CacheManager
        Cache manager object.
    available_datasets_list : list
        List of available datast names for download.

    """

    def __init__(self, name, task, data_dir, verbose, is_test):
        """Initialize class."""
        assert name, 'Must input a valid dataset name: {}'.format(name)
        assert task, 'Must input a valid task name: {}'.format(task)
        assert verbose is not None, 'verbose cannot be empty'
        assert is_test is not None, 'is_test cannot be empty'

        self.name = name
        self.task = task
        self.data_dir = data_dir
        self.verbose = verbose
        self.is_test = is_test
        self.cache_manager = CacheManager(self.is_test)
        self.available_datasets_list = fetch_list_datasets()

        self.parse_task_name()

    def parse_task_name(self):
        """Validate the task name."""
        if self.task == '' or self.task == 'default':
            self.task = self.get_default_task()

    def get_default_task(self):
        """Returns the default task for the dataset."""
        return self.available_datasets_list[self.name]['default_task']

    def run(self):
        """Main method."""
        self.set_dataset_data()
        dataset_loader = self.get_data_loader()
        return dataset_loader

    def set_dataset_data(self):
        """Setup the dataset's metadata."""
        if self.verbose:
            print('==> Setup the dataset\'s metadata.')

        self.get_dataset_files()
        self.set_dataset_metadata()

    def get_dataset_files(self):
        """Download the dataset files if they don't exists in cache."""
        if not self.is_dataset_files_in_cache():
            self.download_dataset()
            self.cache_manager.reload_cache()  # reload the cache's data

    def is_dataset_files_in_cache(self):
        """Check if the dataset is registered in the cache."""
        return self.cache_manager.exists_dataset(self.name)

    def download_dataset(self):
        """Download the dataset to disk."""
        downloader = DownloadAPI(name=self.name,
                                 data_dir=self.data_dir,
                                 extract_data=True,
                                 verbose=self.verbose,
                                 is_test=self.is_test)
        downloader.run()

    def set_dataset_metadata(self):
        """Process the dataset's metadata if it does not exists in cache."""
        if not self.is_dataset_task_in_cache():
            self.process_dataset()
            self.cache_manager.reload_cache()  # reload the cache's

    def is_dataset_task_in_cache(self):
        """Check if the dataset task is registered in the cache."""
        return self.cache_manager.exists_task(self.name, self.task)

    def process_dataset(self):
        """Process the dataset's metadata."""
        processer = ProcessAPI(name=self.name,
                               task=self.task,
                               verbose=self.verbose,
                               is_test=self.is_test)
        processer.run()

    def get_data_loader(self):
        """Return a DataLoader object."""
        if self.verbose:
            print('==> Load the dataset\'s metadata.')

        data_dir_path, hdf5_filepath = self.get_cache_paths()
        return DataLoader(name=self.name,
                          task=self.task,
                          data_dir=data_dir_path,
                          hdf5_filepath=hdf5_filepath)

    def get_cache_paths(self):
        """Return the dataset's data dir + hdf5 metadata paths."""
        dset_paths = self.cache_manager.get_dataset_storage_paths(self.name)
        task_hdf5_filepath = self.cache_manager.get_task_cache_path(self.name, self.task)
        return dset_paths['data_dir'], task_hdf5_filepath
