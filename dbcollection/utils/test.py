"""
Test utility functions/classes.
"""


from __future__ import print_function
import dbcollection as dbc


class TestBaseDB:
    """ Test Class for loading datasets """

    def __init__(self, name, task, data_dir, verbose=True):
        """
        Initialize class.

        Parameters
        ----------
            options :

        """
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
        dbc.info(is_test=True)


    def print_info(self):
        """Print information about the dataset to the screen"""
        print('\n######### info #########')
        print('Dataset: ' + self.dataset.name)
        print('Task: ' + self.dataset.task)
        print('Data path: ' + self.dataset.data_dir)
        print('Metadata cache path: ' + self.dataset.cache_path)


    def load(self):
        """Load dataset to memory"""
        print('\n==> dbcollection: load()')
        self.dataset = dbc.load(name=self.name,
                                task=self.task,
                                data_dir=self.data_dir,
                                verbose=self.verbose,
                                is_test=True)


    def download(self, extract_data=True):
        """Download dataset to memory"""
        print('\n==> dbcollection: download()')
        dbc.download(name=self.name,
                     data_dir=self.data_dir,
                     extract_data=extract_data,
                     verbose=self.verbose,
                     is_test=True)


    def process(self):
        """Process dataset"""
        print('\n==> dbcollection: process()')
        self.dataset = dbc.process(name=self.name,
                                   task=self.task,
                                   verbose=self.verbose,
                                   is_test=True)


    def run(self, mode):
        """Run the test script"""
        assert mode, 'Must insert input arg: mode'

        # delete all cache data + dir
        self.delete_cache()

        if mode is 'load':
            # download/setup dataset
            self.load()

            # print data from the loader
            self.print_info()

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
