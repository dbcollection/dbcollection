"""
Test dbcollection/utils/loader.py.
"""


import os
import sys
import numpy as np
import h5py
import pytest

from dbcollection.core.loader import FieldLoader, SetLoader, DataLoader
from dbcollection.utils.string_ascii import convert_ascii_to_str as ascii_to_str
from dbcollection.utils.string_ascii import convert_str_to_ascii as str_to_ascii


# -----------------------------------------------------------
# Test data
# -----------------------------------------------------------


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


# Setup test hdf5 file in disk + dataset generator
db_generator = HDF5DatasetMetadataGenerator()


# -----------------------------------------------------------
# Tests
# -----------------------------------------------------------

class TestFieldLoader:
    """Unit tests for the FieldLoader class."""

    def test__init(self,):
        h5obj = db_generator.load_hdf5_file()

        obj_id = 1
        field_loader = FieldLoader(h5obj['/train/data'], obj_id)

        assert not field_loader._in_memory
        assert field_loader.name == 'data'

    class TestGet:
        """Groups tests for the get() method."""

        @pytest.mark.parametrize("idx", [0, 1, 2, 3, 4])
        def test_get_single_obj(self, idx):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            data = field_loader.get(idx)

            assert np.array_equal(data, set_data['data'][idx])

        @pytest.mark.parametrize("idx", [0, 1, 2, 3, 4])
        def test_get_single_obj_in_memory(self, idx):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            field_loader.to_memory = True
            data = field_loader.get(idx)

            assert np.array_equal(data, set_data['data'][idx])

        def test_get_single_obj_by_arg_name(self):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            idx = 0
            data = field_loader.get(index=idx)

            assert np.array_equal(data, set_data['data'][idx])

        def test_get_single_obj_by_arg_name_in_memory(self):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            field_loader.to_memory = True
            idx = 0
            data = field_loader.get(index=idx)

            assert np.array_equal(data, set_data['data'][idx])

        def test_get_single_obj_list_of_equal_indexes(self):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            idx = [0, 0]
            data = field_loader.get(idx)

            assert np.array_equal(data, set_data['data'][list(set(idx))])

        def test_get_single_obj_list_of_equal_indexes_in_memory(self):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            field_loader.to_memory = True
            idx = [0, 0]
            data = field_loader.get(idx)

            assert np.array_equal(data, set_data['data'][list(set(idx))])

        def test_get_single_obj_list(self):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            idx = [0]
            data = field_loader.get(idx)

            assert np.array_equal(data, set_data['data'][idx[0]])

        def test_get_single_obj_list_in_memory(self):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            field_loader.to_memory = True
            idx = [0]
            data = field_loader.get(idx)

            assert np.array_equal(data, set_data['data'][idx[0]])

        def test_get_single_obj_tuple(self):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            idx = (0,)
            data = field_loader.get(idx)

            assert np.array_equal(data, set_data['data'][idx[0]])

        def test_get_single_obj_tuple_in_memory(self):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            field_loader.to_memory = True
            idx = (0,)
            data = field_loader.get(idx)

            assert np.array_equal(data, set_data['data'][idx[0]])

        def test_get_single_obj_raises_error_wrong_format(self):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            with pytest.raises(TypeError):
                idx = {1}
                data = field_loader.get(idx)

        def test_get_single_obj_raises_error_wrong_format_in_memory(self):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            field_loader.to_memory = True
            with pytest.raises(TypeError):
                idx = {1}
                data = field_loader.get(idx)

        def test_get_single_obj_empty_list(self):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            idx = []
            data = field_loader.get(idx)

            assert np.array_equal(data, set_data['data'])

        def test_get_single_obj_empty_list_in_memory(self):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            field_loader.to_memory = True
            idx = []
            data = field_loader.get(idx)

            assert np.array_equal(data, set_data['data'])

        @pytest.mark.parametrize("idx", [0, 1, 2, 3, 4])
        def test_get_single_obj_convert_to_string(self, idx):
            data_field = 'strings_list'
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train', data_field)

            data = field_loader.get(idx, convert_to_str=True)

            assert np.array_equal(data, ascii_to_str(set_data[data_field][idx]))
            assert isinstance(data, str)

        @pytest.mark.parametrize("idx", [0, 1, 2, 3, 4])
        def test_get_single_obj_convert_to_string_in_memory(self, idx):
            data_field = 'strings_list'
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train', data_field)

            field_loader.to_memory = True
            data = field_loader.get(idx, convert_to_str=True)

            assert np.array_equal(data, ascii_to_str(set_data[data_field][idx]))
            assert isinstance(data, str)

        def test_get_multi_obj_convert_to_string(self):
            data_field = 'strings_list'
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train', data_field)

            idx = list(range(3))
            data = field_loader.get(idx, convert_to_str=True)

            assert np.array_equal(data, ascii_to_str(set_data[data_field][idx]))
            assert isinstance(data, list)

        def test_get_multi_obj_convert_to_string_in_memory(self):
            data_field = 'strings_list'
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train', data_field)

            field_loader.to_memory = True
            idx = list(range(3))
            data = field_loader.get(idx, convert_to_str=True)

            assert np.array_equal(data, ascii_to_str(set_data[data_field][idx]))
            assert isinstance(data, list)

        def test_get_two_obj(self):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            idx = [1, 2]
            data = field_loader.get(idx)

            assert np.array_equal(data, set_data['data'][idx])

        def test_get_two_obj_in_memory(self):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            field_loader.to_memory = True
            idx = [1, 2]
            data = field_loader.get(idx)

            assert np.array_equal(data, set_data['data'][idx])

        def test_get_multiple_objs(self):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            idx = [1, 2, 5, 8]
            data = field_loader.get(idx)

            assert np.array_equal(data, set_data['data'][idx])

        def test_get_multiple_objs_in_memory(self):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            field_loader.to_memory = True
            idx = [1, 2, 5, 8]
            data = field_loader.get(idx)

            assert np.array_equal(data, set_data['data'][idx])

        def test_get_multiple_objs_unordered(self):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            idx = [8, 2, 5, 1]
            data = field_loader.get(idx)

            assert not np.array_equal(data, set_data['data'][idx])

        def test_get_multiple_objs_unordered_in_memory(self):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            field_loader.to_memory = True
            idx = [8, 2, 5, 1]
            data = field_loader.get(idx)

            assert not np.array_equal(data, set_data['data'][idx])

        def test_get_all_obj(self):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            data = field_loader.get()

            assert np.array_equal(data, set_data['data'])

        def test_get_all_obj_in_memory(self):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            field_loader.to_memory = True
            data = field_loader.get()

            assert np.array_equal(data, set_data['data'])

    def test_size(self):
        field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

        size = field_loader.size()

        assert size == set_data['data'].shape

    def test_object_field_id(self):
        field_loader, _ = db_generator.get_test_data_FieldLoader('train')

        obj_id = field_loader.object_field_id()

        assert obj_id is 1

    def test_object_field_id_not_equal(self):
        field_loader, _ = db_generator.get_test_data_FieldLoader('train')

        obj_id = field_loader.object_field_id()

        assert obj_id is not 2

    def test_info(self):
        field_loader, _ = db_generator.get_test_data_FieldLoader('train')
        field_loader.info()

    def test_info_no_verbose(self):
        field_loader, _ = db_generator.get_test_data_FieldLoader('train')
        field_loader.info(False)

    def test_to_memory(self):
        field_loader, _ = db_generator.get_test_data_FieldLoader('train')

        field_loader.to_memory = True

        assert isinstance(field_loader.data, np.ndarray)

    def test_to_memory_to_disk(self):
        field_loader, _ = db_generator.get_test_data_FieldLoader('train')

        field_loader.to_memory = True
        field_loader.to_memory = False

        assert isinstance(field_loader.data, h5py._hl.dataset.Dataset)

    def test__len__(self):
        field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

        size = len(field_loader)

        assert size == len(set_data['data'])

    def test__str__(self):
        field_loader, _ = db_generator.get_test_data_FieldLoader('train')

        if os.name == 'nt':
            matching_str = 'FieldLoader: <HDF5 dataset "data": shape (10, 10), type "<i4">'
        else:
            matching_str = 'FieldLoader: <HDF5 dataset "data": shape (10, 10), type "<i8">'

        assert str(field_loader) == matching_str

    def test__str__in_memory(self):
        field_loader, _ = db_generator.get_test_data_FieldLoader('train')

        field_loader.to_memory = True
        if os.name == 'nt':
            if sys.version_info[0] == 2:
                matching_str = 'FieldLoader: <numpy.ndarray "data": shape (10L, 10L), type "int32">'
            else:
                matching_str = 'FieldLoader: <numpy.ndarray "data": shape (10, 10), type "int32">'
        else:
            matching_str = 'FieldLoader: <numpy.ndarray "data": shape (10, 10), type "int64">'

        assert str(field_loader) == matching_str

    class TestIndexing:
        """Groups tests of index slicing."""

        @pytest.mark.parametrize("idx", [0, 1, 2, 3, 4])
        def test__index__single_obj(self, idx):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            data = field_loader[idx]

            assert np.array_equal(data, set_data['data'][idx])

        @pytest.mark.parametrize("idx", [0, 1, 2, 3, 4])
        def test__index__single_obj_in_memory(self, idx):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            field_loader.to_memory = True
            data = field_loader[idx]

            assert np.array_equal(data, set_data['data'][idx])

        def test__index__single_objs_single_value(self):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            data = field_loader[0, 0]

            assert np.array_equal(data, set_data['data'][0][0])

        def test__index__single_objs_single_value_in_memory(self):
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

            field_loader.to_memory = True
            data = field_loader[0, 0]

            assert np.array_equal(data, set_data['data'][0][0])


def get_expected_object_values(set_data, fields, idx):
    """Get the expected values of an object index from the test dataset."""
    assert set_data
    assert fields
    assert idx is not None

    if isinstance(idx, int):
        expected = get_single_object_values(set_data, fields, idx)
    else:
        expected = []
        for i in idx:
            expected.append(get_single_object_values(set_data, fields, idx[i]))
    return expected


def get_single_object_values(set_data, fields, idx):
    data = []
    for field in fields:
        data.append(set_data[field][idx])
    return data


def compare_lists(listA, listB):
    assert listA
    assert listB
    if isinstance(listA[0], list):
        for i in range(len(listA)):
            if not compare_single_lists(listA[i], listB[i]):
                return False
        return True
    else:
        return compare_single_lists(listA, listB)


def compare_single_lists(listA, listB):
    assert listA
    assert listB
    for i in range(len(listA)):
        if not np.array_equal(listA[i], listB[i]):
            return False
    return True


class TestSetLoader:
    """Unit tests for the SetLoader class."""

    def test__init(self):
        h5obj = db_generator.load_hdf5_file()

        dataset = db_generator.dataset
        set_name = 'test'
        set_loader = SetLoader(h5obj[set_name])

        assert set_loader.set == set_name
        assert set_loader.object_fields == ascii_to_str(dataset[set_name]['object_fields'])
        assert set_loader.nelems == 5

    class TestGet:
        """Group tests for the get() method."""

        def test_get_data_raises_keyerror_missing_field(self):
            set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

            with pytest.raises(AssertionError):
                field = 'data'
                idx = 0
                data = set_loader.get(idx)

        def test_get_data_raises_keyerror_invalid_field(self):
            set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

            with pytest.raises(KeyError):
                field = 'data_invalid'
                idx = 0
                data = set_loader.get(field, idx)

        @pytest.mark.parametrize("idx", [0, 1, 2, 3, 4])
        def test_get_data_single_obj(self, idx):
            set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

            field = 'data'
            data = set_loader.get(field, idx)

            assert np.array_equal(data, set_data[field][idx])

        @pytest.mark.parametrize("idx", [0, 1, 2, 3, 4])
        def test_get_data_single_obj_in_memory(self, idx):
            set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

            field = 'data'
            set_loader.fields[field].to_memory = True
            data = set_loader.get(field, idx)

            assert np.array_equal(data, set_data[field][idx])

        def test_get_data_two_objs(self):
            set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

            field = 'data'
            idx = [0, 1]
            data = set_loader.get(field, idx)

            assert np.array_equal(data, set_data[field][idx])

        def test_get_data_two_objs_in_memory(self):
            set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

            field = 'data'
            idx = [0, 1]
            set_loader.fields[field].to_memory = True
            data = set_loader.get(field, idx)

            assert np.array_equal(data, set_data[field][idx])

        def test_get_data_two_objs_same_index(self):
            set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

            field = 'data'
            idx = [0, 0]
            data = set_loader.get(field, idx)

            assert np.array_equal(data, set_data[field][list(set(idx))])

        def test_get_data_two_objs_in_memory(self):
            set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

            field = 'data'
            idx = [0, 0]
            set_loader.fields[field].to_memory = True
            data = set_loader.get(field, idx)

            assert np.array_equal(data, set_data[field][list(set(idx))])

        def test_get_data_multiple_objs(self):
            set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

            field = 'data'
            idx = range(5)
            data = set_loader.get(field, idx)

            assert np.array_equal(data, set_data[field][idx])

        def test_get_data_multiple_objs_in_memory(self):
            set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

            field = 'data'
            idx = range(5)
            set_loader.fields[field].to_memory = True
            data = set_loader.get(field, idx)

            assert np.array_equal(data, set_data[field][idx])

        def test_get_data_all_obj(self):
            set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

            field = 'data'
            data = set_loader.get(field)

            assert np.array_equal(data, set_data[field])

        def test_get_data_all_obj_in_memory(self):
            set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

            field = 'data'
            set_loader.fields[field].to_memory = True
            data = set_loader.get(field)

            assert np.array_equal(data, set_data[field])

        def test_get_data_single_obj_object_ids(self):
            set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

            field = 'object_ids'
            idx = 0
            data = set_loader.get(field, idx)

            assert np.array_equal(data, set_data[field][idx])

        def test_get_data_single_obj_object_ids_in_memory(self):
            set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

            field = 'object_ids'
            idx = 0
            set_loader.fields[field].to_memory = True
            data = set_loader.get(field, idx)

            assert np.array_equal(data, set_data[field][idx])

    class TestObject:
        """Group tests for the object() method."""

        def test_object_single_obj(self):
            set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

            idx = 0
            data = set_loader.object(idx)

            assert np.array_equal(data, set_data['object_ids'][idx])

        def test_object_single_obj_value(self):
            set_loader, set_data, fields = db_generator.get_test_dataset_SetLoader('train')

            idx = 0
            data = set_loader.object(idx, True)
            expected = get_expected_object_values(set_data, set_loader.object_fields, idx)

            assert compare_lists(data, expected)

        def test_object_two_objs(self):
            set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

            idx = [0, 1]
            data = set_loader.object(idx)

            assert np.array_equal(data, set_data['object_ids'][idx])

        def test_object_two_objs_value(self):
            set_loader, set_data, fields = db_generator.get_test_dataset_SetLoader('train')

            idx = [0, 1]
            data = set_loader.object(idx, True)
            expected = get_expected_object_values(set_data, set_loader.object_fields, idx)

            assert compare_lists(data, expected)

        def test_object_all_objs(self):
            set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

            data = set_loader.object()

            assert np.array_equal(data, set_data['object_ids'])

        def test_object_all_objs_value(self):
            set_loader, set_data, fields = db_generator.get_test_dataset_SetLoader('train')

            data = set_loader.object(convert_to_value=True)
            idx = range(len(set_data['object_ids']))
            expected = get_expected_object_values(set_data, set_loader.object_fields, idx)

            assert compare_lists(data, expected)

    def test_size(self):
        set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

        field = 'data'
        size = set_loader.size(field)

        assert size == set_data[field].shape

    def test_size_object_ids(self):
        set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

        size = set_loader.size()

        assert size == set_data['object_ids'].shape

    def test_list(self):
        set_loader, _, set_fields = db_generator.get_test_dataset_SetLoader('train')

        fields = set_loader.list()

        assert fields == tuple(sorted(set_fields))

    def test_object_field_id(self):
        set_loader, _, _ = db_generator.get_test_dataset_SetLoader('train')

        obj_id = set_loader.object_field_id('data')

        assert obj_id == 0

    def test_object_field_id_raise_error_invalid_field(self):
        set_loader, _, _ = db_generator.get_test_dataset_SetLoader('train')

        with pytest.raises(KeyError):
            obj_id = set_loader.object_field_id('data_invalid_field')

    def test_info(self):
        set_loader, _, _ = db_generator.get_test_dataset_SetLoader('train')

        set_loader.info()

    def test__len__(self):
        set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

        nelems = len(set_loader)

        assert nelems == len(set_data['object_ids'])

    def test__str__(self):
        set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

        size = len(set_data['object_ids'])
        matching_str = 'SetLoader: set<train>, len<{}>'.format(size)

        assert str(set_loader) == matching_str


class TestDataLoader:
    """Unit tests for the DataLoader class."""

    def test__init(self):
        name = 'some_db'
        task = 'task'
        data_dir = './some/dir'
        hdf5_file = db_generator.get_test_hdf5_filepath_DataLoader()

        data_loader = DataLoader(name, task, data_dir, hdf5_file)

        assert data_loader.db_name == name
        assert data_loader.task == task
        assert data_loader.data_dir == data_dir
        assert data_loader.hdf5_filepath == hdf5_file
        assert 'train' in data_loader.sets

    class TestGet:
        """Group tests for the get() method."""

        @pytest.mark.parametrize("idx", [0, 1, 2, 3, 4])
        def test_get_single_obj(self, idx):
            data_loader, dataset, _ = db_generator.get_test_dataset_DataLoader()

            set_name = 'train'
            field = 'data'
            data = data_loader.get(set_name, field, idx)

            assert np.array_equal(data, dataset[set_name][field][idx])

        def test_get_single_obj_named_args(self):
            data_loader, dataset, _ = db_generator.get_test_dataset_DataLoader()

            set_name = 'train'
            field = 'data'
            idx = 0
            data = data_loader.get(
                set_name=set_name,
                field=field,
                index=idx
            )

            assert np.array_equal(data, dataset[set_name][field][idx])

        def test_get_single_obj_access_via_SetLoader(self):
            data_loader, dataset, _ = db_generator.get_test_dataset_DataLoader()

            set_name = 'train'
            field = 'data'
            idx = 1
            data = data_loader.sets[set_name].get(field, idx)

            assert np.array_equal(data, dataset[set_name][field][idx])

        def test_get_single_obj_raise_error_invalid_set(self):
            data_loader, dataset, _ = db_generator.get_test_dataset_DataLoader()

            with pytest.raises(KeyError):
                set_name = 'val'
                field = 'data'
                idx = 0
                data = data_loader.get(set_name, field, idx)

        def test_get_two_objs(self):
            data_loader, dataset, _ = db_generator.get_test_dataset_DataLoader()

            set_name = 'train'
            field = 'data'
            idx = (2, 6, )
            data = data_loader.get(set_name, field, idx)

            assert np.array_equal(data, dataset[set_name][field][list(idx)])

        def test_get_all_objs(self):
            data_loader, dataset, _ = db_generator.get_test_dataset_DataLoader()

            set_name = 'train'
            field = 'data'
            data = data_loader.get(set_name, field)

            assert np.array_equal(data, dataset[set_name][field])

        def test_get_all_objs_empty_index(self):
            data_loader, dataset, _ = db_generator.get_test_dataset_DataLoader()

            set_name = 'train'
            field = 'data'
            idx = []
            data = data_loader.get(set_name, field)

            assert np.array_equal(data, dataset[set_name][field])

    class TestObject:
        """Group tests for the object() method."""

        def test_object_single_obj(self):
            data_loader, dataset, _ = db_generator.get_test_dataset_DataLoader()

            set_name = 'train'
            idx = 3
            data = data_loader.object(set_name, idx)

            assert np.array_equal(data, dataset[set_name]['object_ids'][idx])

        def test_object_single_obj_values(self):
            data_loader, dataset, _ = db_generator.get_test_dataset_DataLoader()

            set_name = 'train'
            idx = 3
            data = data_loader.object(set_name, idx, True)
            expected = get_expected_object_values(dataset[set_name],
                                                data_loader.sets[set_name].object_fields,
                                                idx)

            assert compare_lists(data, expected)

        def test_object_single_obj_raise_error_invalid_set(self):
            data_loader, _, _ = db_generator.get_test_dataset_DataLoader()

            with pytest.raises(KeyError):
                set_name = 'val'
                idx = 3
                data = data_loader.object(set_name, idx)

        def test_object_two_objs(self):
            data_loader, dataset, _ = db_generator.get_test_dataset_DataLoader()

            set_name = 'train'
            idx = [3, 4]
            data = data_loader.object(set_name, idx)

            assert np.array_equal(data, dataset[set_name]['object_ids'][idx])

        def test_object_all_objs(self):
            data_loader, dataset, _ = db_generator.get_test_dataset_DataLoader()

            set_name = 'train'
            data = data_loader.object(set_name)

            assert np.array_equal(data, dataset[set_name]['object_ids'])

    class TestSize:
        """Group tests for the size() method."""

        def test_size_single_field(self):
            data_loader, dataset, _ = db_generator.get_test_dataset_DataLoader()

            set_name = 'train'
            field = 'data'
            size = data_loader.size(set_name, field)

            assert size == dataset[set_name][field].shape

        def test_size_default(self):
            data_loader, dataset, _ = db_generator.get_test_dataset_DataLoader()

            set_name = 'train'
            size = data_loader.size(set_name)

            assert size == dataset[set_name]['object_ids'].shape

        def test_size_single_field_all_sets(self):
            data_loader, dataset, _ = db_generator.get_test_dataset_DataLoader()

            field = 'data'
            size = data_loader.size(field=field)
            expected = {}
            for set_name in dataset:
                expected.update({set_name: dataset[set_name][field].shape})

            assert size == expected

        def test_size_no_inputs(self):
            data_loader, dataset, _ = db_generator.get_test_dataset_DataLoader()

            size = data_loader.size()
            expected = {}
            for set_name in dataset:
                expected.update({set_name: dataset[set_name]['object_ids'].shape})

            assert size == expected

        def test_size_raise_error_invalid_set(self):
            data_loader, dataset, _ = db_generator.get_test_dataset_DataLoader()

            with pytest.raises(KeyError):
                set_name = "val"
                size = data_loader.size(set_name)

        def test_size_raise_error_invalid_sfield(self):
            data_loader, dataset, _ = db_generator.get_test_dataset_DataLoader()

            with pytest.raises(KeyError):
                field = "invalid_field_name"
                size = data_loader.size(field=field)

    def test_list_single_set(self):
        data_loader, dataset, _ = db_generator.get_test_dataset_DataLoader()

        set_name= 'train'
        fields = data_loader.list(set_name)

        assert fields == tuple(sorted(dataset[set_name]))

    def test_list_all_sets(self):
        data_loader, dataset, _ = db_generator.get_test_dataset_DataLoader()

        fields = data_loader.list()
        expected = {}
        for set_name in dataset:
            expected[set_name] = tuple(sorted(dataset[set_name]))

        assert fields == expected

    def test_list_raise_error_invalid_set(self):
        data_loader, dataset, _ = db_generator.get_test_dataset_DataLoader()

        with pytest.raises(KeyError):
            set_name = 'val'
            fields = data_loader.list(set_name)

    def test_object_field_id_field1(self):
        data_loader, _, _ = db_generator.get_test_dataset_DataLoader()

        set_name = 'train'
        field = 'data'
        obj_id = data_loader.object_field_id(set_name, field)

        assert obj_id == 0

    def test_object_field_id_field2(self):
        data_loader, _, _ = db_generator.get_test_dataset_DataLoader()

        set_name = 'train'
        field = 'number'
        obj_id = data_loader.object_field_id(set_name, field)

        assert obj_id == 2

    def test_object_field_id_raise_error_invalid_set(self):
        data_loader, _, _ = db_generator.get_test_dataset_DataLoader()

        with pytest.raises(KeyError):
            set_name = 'val'
            field = 'data'
            obj_id = data_loader.object_field_id(set_name, field)

    def test_info_single_set(self):
        data_loader, _, _ = db_generator.get_test_dataset_DataLoader()

        set_name = 'train'
        data_loader.info(set_name)

    def test_info_all_sets(self):
        data_loader, _, _ = db_generator.get_test_dataset_DataLoader()

        data_loader.info()

    def test_info_raise_error_invalid_set(self):
        data_loader, _, _ = db_generator.get_test_dataset_DataLoader()

        with pytest.raises(KeyError):
            set_name = 'val'
            data_loader.info(set_name)

    def test__len__(self):
        data_loader, dataset, _ = db_generator.get_test_dataset_DataLoader()

        size = len(data_loader)

        assert size == len(dataset)

    def test__str__(self):
        data_loader, dataset, _ = db_generator.get_test_dataset_DataLoader()

        matching_str = "DataLoader: some_db ('task' task)"

        assert str(data_loader) == matching_str
