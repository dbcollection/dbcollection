"""
Test utility functions/classes.
"""


from __future__ import print_function
import dbcollection as dbc


class TestBaseDB:
    """ Test Class for loading datasets.

    Parameters
    ----------
    name : str
        Name of the dataset.
    task : str
        Name of the task.
    data_dir : str
        Path of the dataset's data directory on disk.
    verbose : bool, optional
        Be verbose.

    Attributes
    ----------
    name : str
        Name of the dataset.
    task : str
        Name of the task.
    data_dir : str
        Path of the dataset's data directory on disk.
    verbose : bool
        Be verbose.

    """

    def __init__(self, name, task, data_dir, verbose=True):
        """Initialize class."""
        assert name, "Must insert input arg: name"
        assert task, "Must insert input arg: task"
        assert data_dir, "Must insert input arg: data_dir"

        self.name = name
        self.task = task
        self.data_dir = data_dir
        self.verbose = verbose

    def delete_cache(self):
        """Delete all cache data + dir"""
        print('\n==> dbcollection: config_cache()')
        dbc.config_cache(delete_cache=True, is_test=True)

    def list_datasets(self):
        """Print dbcollection info"""
        print('\n==> dbcollection: info()')
        dbc.info_cache(is_test=True)

    def print_info(self, loader):
        """Print information about the dataset to the screen

        Parameters
        ----------
        loader : DataLoader
            Data loader object of a dataset.
        """
        print('\n######### info #########')
        print('Dataset: ' + loader.db_name)
        print('Task: ' + loader.task)
        print('Data path: ' + loader.data_dir)
        print('Metadata cache path: ' + loader.hdf5_filepath)

    def load(self):
        """Return a data loader object for a dataset.

        Returns
        -------
        DataLoader
            A data loader object of a dataset.
        """
        print('\n==> dbcollection: load()')
        return dbc.load(name=self.name,
                        task=self.task,
                        data_dir=self.data_dir,
                        verbose=self.verbose,
                        is_test=True)

    def download(self, extract_data=True):
        """Download a dataset to disk.

        Parameters
        ----------
        extract_data : bool
            Flag signaling to extract data to disk (if True).
        """
        print('\n==> dbcollection: download()')
        dbc.download(name=self.name,
                     data_dir=self.data_dir,
                     extract_data=extract_data,
                     verbose=self.verbose,
                     is_test=True)

    def process(self):
        """Process dataset"""
        print('\n==> dbcollection: process()')
        dbc.process(name=self.name,
                    task=self.task,
                    verbose=self.verbose,
                    is_test=True)

    def run(self, mode):
        """Run the test script.

        Parameters
        ----------
        mode : str
            Task name to execute.

        Raises
        ------
        Exception
            If an invalid mode was inserted.
        """
        assert mode, 'Must insert input arg: mode'

        # delete all cache data + dir
        self.delete_cache()

        if mode is 'load':
            # download/setup dataset
            loader = self.load()

            # print data from the loader
            self.print_info(loader)

        elif mode is 'download':
            # download dataset
            self.download()

        elif mode is 'process':
            # download dataset
            self.download(False)

            # process dataset task
            self.process()

        else:
            raise Exception('Invalid mode:', mode)

        # print data from the loader
        self.list_datasets()

        # delete all cache data + dir before terminating
        self.delete_cache()
