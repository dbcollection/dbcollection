"""
Test utility functions/classes.
"""


from __future__ import print_function
import os
import numpy as np
import h5py

import dbcollection as dbc
from dbcollection.core.loader import FieldLoader, SetLoader, DataLoader
from dbcollection.utils.string_ascii import convert_str_to_ascii as str_to_ascii


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


class TestDatasetGenerator:
    """Generates a simple dataset to be used in tests.

    Attributes
    ----------
    hdf5_filepath : str
        File name + path for thetest HDF5 file.
    task : str
        Name of the task.
    data_dir : str
        Path of the dataset's data directory on disk.
    verbose : bool
        Be verbose.

    """

    def __init__(self, verbose=True):
        """Initialize class."""
        self.verbose = verbose
        self.hdf5_filepath = self.get_hdf5_filepath()

        dataset, data_fields = self.generate_dataset()
        self.dataset = dataset
        self.data_fields = data_fields

        self.generate_data()

    def get_hdf5_filepath(self):
        home_dir = os.path.expanduser("~")
        hdf5_filepath = os.path.join(home_dir, 'tmp', 'dbcollection', 'dummy.h5')
        return hdf5_filepath

    def generate_data(self):
        """Generate the dataset's data if it does not exist."""
        self.remove_hdf5_file()
        hdf5_handler = self.create_hdf5_file()
        self.populate_hdf5_file(hdf5_handler, self.dataset)

    def remove_hdf5_file(self):
        if os.path.exists(self.hdf5_filepath):
            os.remove(self.hdf5_filepath)

    def create_hdf5_file(self):
        self.create_hdf5_dir()
        return h5py.File(self.hdf5_filepath, 'w')

    def create_hdf5_dir(self):
        hdf5_dir = os.path.dirname(self.hdf5_filepath)
        if not os.path.exists(hdf5_dir):
            os.makedirs(hdf5_dir)

    def generate_dataset(self):
        """Generate the test dataset and store it to disk."""
        sets = {
            "train": 10,
            "test": 5,
        }

        fields = {
            "data": lambda x: np.random.randint(0, 10, (x, 10)),
            "number": lambda x: np.array(range(x)),
            "field_with_a_long_name_for_printing": lambda x: np.array(range(x)),
        }

        lists = {
            "dummy_data": np.array(range(10)),
            "dummy_number": np.array(range(10), dtype=np.uint8),
        }

        dataset = {}
        data_fields = {}
        for set_name in sets:
            dataset[set_name] = self.populate_set(sets[set_name], fields, lists)
            data_fields[set_name] = sorted(dataset[set_name].keys())

        return dataset, data_fields

    def populate_set(self, size, fields, lists):
        dataset = {}

        for field in fields:
            dataset[field] = fields[field](size)

        for field in lists:
            dataset[field] = lists[field]

        data_fields = sorted(dataset.keys())
        dataset['object_fields'] = str_to_ascii(data_fields)
        dataset['object_ids'] = np.array([[i] * len(fields) for i in range(size)])

        return dataset

    def populate_hdf5_file(self, hdf5_handler, dataset):
        for set_name in dataset:
            hdf5_set_handler = hdf5_handler.create_group(set_name)
            for field in dataset[set_name]:
                hdf5_set_handler[field] = dataset[set_name][field]
        hdf5_handler.close()

    def load_hdf5_file(self):
        return h5py.File(self.hdf5_filepath, 'r')

    def get_test_data_FieldLoader(self, set_name='train'):
        """Load data for testing the FieldLoader class."""
        path = "/{}/data".format(set_name)
        field_loader = self.load_hdf5_file_FieldLoader(path)
        set_data = self.dataset[set_name]
        return field_loader, set_data

    def load_hdf5_file_FieldLoader(self, path):
        assert path
        h5obj = self.load_hdf5_file()
        obj_id = 1
        field_loader = FieldLoader(h5obj[path], obj_id)
        return field_loader

    def get_test_dataset_SetLoader(self, set_name='train'):
        """Return a dataset for testing the FieldLoader class."""
        set_loader = self.load_hdf5_file_SetLoader(set_name)

        set_data = self.dataset[set_name]
        set_fields = self.data_fields[set_name]

        return set_loader, set_data, set_fields

    def load_hdf5_file_SetLoader(self, set_name):
        assert set_name
        h5obj = self.load_hdf5_file()
        set_loader = SetLoader(h5obj[set_name])
        return set_loader

    def get_test_dataset_DataLoader(self, set_name):
        """Return a dataset for testing the FieldLoader class."""
        name = 'some_db'
        task = 'task'
        data_dir = './some/dir'
        hdf5_file = self.hdf5_filepath

        data_loader = DataLoader(name, task, data_dir, hdf5_file)

        return data_loader, self.dataset, self.data_fields
