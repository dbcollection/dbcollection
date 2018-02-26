"""
Test data for testing the loader api.

The data generator contained in this file produces
a mock of a potential dataset's hdf5 file structure.

Note: The names used are not designed to be real names,
just examples of possible strings.
"""


import os
import numpy as np
import h5py

from dbcollection.core.loader import FieldLoader, SetLoader, DataLoader
from dbcollection.utils.string_ascii import convert_str_to_ascii as str_to_ascii


class HDF5DatasetMetadataGenerator:
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
            "strings_list": lambda x: str_to_ascii(self.generate_string_list(x)),
            "data": lambda x: np.random.randint(0, 10, (x, 10)),
            "number": lambda x: np.array(range(x)),
            "field_with_a_long_name_for_printing": lambda x: np.array(range(x)),
        }

        lists = {
            "list_dummy_data": np.array(range(10)),
            "list_dummy_number": np.array(range(10), dtype=np.uint8),
        }

        dataset = {}
        data_fields = {}
        for set_name in sets:
            dataset[set_name] = self.populate_set(sets[set_name], fields, lists)
            data_fields[set_name] = sorted(dataset[set_name].keys())

        return dataset, data_fields

    def generate_string_list(self, n):
        """Generate a list of strings."""
        template_str = 'string_'
        string_list = [template_str + str(i) for i in range(n)]
        return string_list

    def populate_set(self, size, fields, lists):
        dataset = {}

        for field in fields:
            dataset[field] = fields[field](size)

        for field in lists:
            dataset[field] = lists[field]

        obj_fields = sorted(fields.keys())
        dataset['object_fields'] = str_to_ascii(obj_fields)
        dataset['object_ids'] = np.array([[i] * len(obj_fields) for i in range(size)])

        return dataset

    def populate_hdf5_file(self, hdf5_handler, dataset):
        for set_name in dataset:
            hdf5_set_handler = hdf5_handler.create_group(set_name)
            for field in dataset[set_name]:
                hdf5_set_handler[field] = dataset[set_name][field]
        hdf5_handler.close()

    def load_hdf5_file(self):
        return h5py.File(self.hdf5_filepath, 'r')

    def get_test_data_FieldLoader(self, set_name='train', field='data'):
        """Load data for testing the FieldLoader class."""
        path = "/{set_name}/{field}".format(set_name=set_name, field=field)
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

    def get_test_dataset_DataLoader(self):
        """Return a dataset for testing the FieldLoader class."""
        test_info = self.get_test_DataLoader_info()
        name = test_info["name"]
        task = test_info["task"]
        data_dir = test_info["data_dir"]
        hdf5_file = test_info["hdf5_file"]

        data_loader = DataLoader(name, task, data_dir, hdf5_file)

        return data_loader, self.dataset, self.data_fields

    def get_test_DataLoader_info(self):
        return {
            "name": 'some_db',
            "task": 'task',
            "data_dir": './some/dir',
            "hdf5_file": self.hdf5_filepath,
        }

    def get_test_hdf5_filepath_DataLoader(self):
        return self.hdf5_filepath

