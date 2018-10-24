"""
Test dbcollection/core/loader.py.
"""


import os
import sys
import numpy as np
from numpy.testing import assert_array_equal
import pandas as pd
import h5py
import pytest
import random
import string

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
    hdf5_filename : str
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
        self.hdf5_filename = self.get_hdf5_filename()
        dataset, data_fields = self.generate_dataset()
        self.dataset = dataset
        self.data_fields = data_fields
        self.generate_data()

    def get_hdf5_filename(self):
        home_dir = os.path.expanduser("~")
        hdf5_filename = os.path.join(home_dir, 'tmp', 'dbcollection', 'dummy.h5')
        return hdf5_filename

    def generate_data(self):
        """Generate the dataset's data if it does not exist."""
        self.remove_hdf5_file()
        hdf5_handler = self.create_hdf5_file()
        self.populate_hdf5_file(hdf5_handler, self.dataset)

    def remove_hdf5_file(self):
        if os.path.exists(self.hdf5_filename):
            os.remove(self.hdf5_filename)

    def create_hdf5_file(self):
        self.create_hdf5_dir()
        return h5py.File(self.hdf5_filename, 'w')

    def create_hdf5_dir(self):
        hdf5_dir = os.path.dirname(self.hdf5_filename)
        if not os.path.exists(hdf5_dir):
            os.makedirs(hdf5_dir)

    def generate_dataset(self):
        """Generate the test dataset and store it to disk."""
        sets = {
            "train": 10,
            "test": 5,
        }

        fields = {
            "filenames": {
                "data": lambda x: str_to_ascii(['fname_' + self.generate_random_string(n=5) for i in range(x)]),
                "type": 'filename'
            },
            "strings_list": {
                "data": lambda x: str_to_ascii(self.generate_string_list(x)),
                "type": 'string'
            },
            "data": {
                "data": lambda x: np.random.randint(0, 10, (x, 10)),
                "type": 'int'
            },
            "number": {
                "data": lambda x: np.array(range(x)),
                "type": 'int'
            },
            "field_with_a_long_name_for_printing": {
                "data": lambda x: np.array(range(x)),
                "type": 'int'
            }
        }

        lists = {
            "list_dummy_data": {
                "data": np.array(range(10)),
                "type": 'list'
            },
            "list_dummy_number": {
                "data": np.array(range(10), dtype=np.uint8),
                "type": 'list'
            }
        }

        dataset = {}
        data_fields = {}
        for set_name in sets:
            dataset[set_name] = self.populate_set(sets[set_name], fields, lists)
            data_fields[set_name] = sorted(dataset[set_name].keys())

        return dataset, data_fields

    def generate_random_string(self, n=5):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

    def generate_string_list(self, n):
        """Generate a list of strings."""
        template_str = 'string_'
        string_list = [template_str + str(i) for i in range(n)]
        return string_list

    def populate_set(self, size, fields, lists):
        dataset = {}
        for field in fields:
            dataset[field] = fields[field]["data"](size)
        for field in lists:
            dataset[field] = lists[field]["data"]

        obj_fields = sorted(fields.keys())
        dataset['__COLUMNS__'] = str_to_ascii(obj_fields)
        types = [fields[field]["type"] for field in obj_fields]
        dataset['__TYPES__'] = str_to_ascii(types)

        return dataset

    def populate_hdf5_file(self, hdf5_handler, dataset):
        for set_name in dataset:
            hdf5_set_handler = hdf5_handler.create_group(set_name)
            for field in dataset[set_name]:
                hdf5_set_handler[field] = dataset[set_name][field]
        hdf5_handler.close()

    def load_hdf5_file(self):
        return h5py.File(self.hdf5_filename, 'r')

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
        info = self.get_test_DataLoader_info()
        set_loader = SetLoader(h5obj[set_name], info['data_dir'])
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
            "data_dir": '/some/dir',
            "hdf5_file": self.hdf5_filename,
        }

    def get_test_hdf5_filename_DataLoader(self):
        return self.hdf5_filename


# Setup test hdf5 file in disk + dataset generator
db_generator = HDF5DatasetMetadataGenerator()


# -----------------------------------------------------------
# Tests
# -----------------------------------------------------------

@pytest.fixture
def field_loader():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')
    return field_loader


@pytest.fixture
def set_data():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')
    return set_data


class TestFieldLoader:
    """Unit tests for the FieldLoader class."""

    def test__init(self):
        h5obj = db_generator.load_hdf5_file()
        column_id = 1
        field_loader = FieldLoader(h5obj['/train/data'], column_id, '/some/dir')
        assert field_loader.name == 'data'
        assert field_loader.data_dir == '/some/dir'
        assert field_loader.column_id == column_id

    class TestGet:
        """Groups tests for the get() method."""

        @pytest.mark.parametrize("idx", [0, 1, 2, 3, 4])
        def test_get_single_obj(self, idx, field_loader, set_data):
            assert_array_equal(field_loader.get(idx), set_data['data'][idx])

        def test_get_single_obj_by_arg_name(self, field_loader, set_data):
            idx = 0
            assert_array_equal(field_loader.get(index=idx), set_data['data'][idx])

        def test_get_single_obj_list_of_equal_indexes(self, field_loader, set_data):
            idx = [0, 0]
            assert_array_equal(field_loader.get(idx), set_data['data'][list(set(idx))])

        def test_get_single_obj_list(self, field_loader, set_data):
            idx = [0]
            assert_array_equal(field_loader.get(idx), set_data['data'][idx[0]])

        def test_get_single_obj_tuple(self, field_loader, set_data):
            idx = (0,)
            assert_array_equal(field_loader.get(idx), set_data['data'][idx[0]])

        def test_get_single_obj_raises_error_wrong_format(self, field_loader, set_data):
            with pytest.raises(TypeError):
                data = field_loader.get({1})

        def test_get_single_obj_empty_list(self, field_loader, set_data):
            with pytest.raises(Exception):
                data = field_loader.get([])

        @pytest.mark.parametrize("idx", [0, 1, 2, 3, 4])
        def test_get_single_obj_convert_to_string(self, idx, field_loader, set_data):
            data_field = 'strings_list'
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train', data_field)
            data = field_loader.get(idx, parse=True)
            assert_array_equal(data, ascii_to_str(set_data[data_field][idx]))
            assert isinstance(data, str)

        def test_get_multi_obj_convert_to_string(self):
            data_field = 'strings_list'
            field_loader, set_data = db_generator.get_test_data_FieldLoader('train', data_field)
            idx = list(range(3))
            data = field_loader.get(idx, parse=True)
            assert_array_equal(data, ascii_to_str(set_data[data_field][idx]))
            assert isinstance(data, list)

        def test_get_two_obj(self, field_loader, set_data):
            idx = [1, 2]
            assert_array_equal(field_loader.get(idx), set_data['data'][idx])

        def test_get_multiple_objs(self, field_loader, set_data):
            idx = [1, 2, 5, 8]
            assert_array_equal(field_loader.get(idx), set_data['data'][idx])

        def test_get_multiple_objs_unordered(self, field_loader, set_data):
            idx = [8, 2, 5, 1]
            assert not np.array_equal(field_loader.get(idx), set_data['data'][idx])

        def test_get_all_obj(self, field_loader, set_data):
            assert_array_equal(field_loader.get(), set_data['data'])

    def test_size(self, field_loader, set_data):
        assert field_loader.size() == set_data['data'].shape

    def test_info(self, field_loader):
        field_loader.info()

    def test_info_no_verbose(self, field_loader):
        field_loader.info(False)

    def test_sample(self, field_loader):
        assert field_loader.sample().shape[0] == 1

    def test_sample_multiple_samples(self, field_loader):
        assert field_loader.sample(5).shape[0] == 5

    def test_sample_multiple_samples_with_replacement(self, field_loader):
        assert field_loader.sample(10, replace=True, random_state=123).shape[0] == 10

    def test_head(self, field_loader):
        assert_array_equal(field_loader.head(), field_loader.get([0, 1, 2, 3, 4]))

    def test_head_sample_first_value(self, field_loader):
        assert_array_equal(field_loader.head(1), field_loader.get(0))

    def test_head_sample_first_six_values(self, field_loader):
        assert_array_equal(field_loader.head(6), field_loader.get([0, 1, 2, 3, 4, 5]))

    def test_head_raises_error_if_number_is_zero(self, field_loader):
        with pytest.raises(AssertionError):
            field_loader.head(0)

    def test_head_raises_error_if_number_is_negative(self, field_loader):
        with pytest.raises(AssertionError):
            field_loader.head(-1)

    def test_tail(self, field_loader):
        idx = list(range(len(field_loader) - 5, len(field_loader)))
        assert_array_equal(field_loader.tail(), field_loader.get(idx))

    def test_tail_sample_last_value(self, field_loader):
        assert_array_equal(field_loader.tail(1), field_loader.get(len(field_loader) - 1))

    def test_tail_sample_last_six_values(self, field_loader):
        idx = list(range(len(field_loader) - 6, len(field_loader)))
        assert_array_equal(field_loader.tail(6), field_loader.get(idx))

    def test_tail_raises_error_if_number_is_zero(self, field_loader):
        with pytest.raises(AssertionError):
            field_loader.tail(0)

    def test_tail_raises_error_if_number_is_negative(self, field_loader):
        with pytest.raises(AssertionError):
            field_loader.tail(-1)

    def test_to_pandas(self, field_loader):
        assert pd.Series.equals(field_loader.to_pandas(), pd.Series(field_loader.data))

    def test_to_pandas_set_name(self, field_loader):
        assert pd.Series.equals(field_loader.to_pandas(name='dummy_name'),
                                pd.Series(field_loader.data, name='dummy_name'))

    def test_values(self, field_loader):
        assert_array_equal(field_loader.values, field_loader.hdf5_handler.value)

    def test__len__(self, field_loader, set_data):
        assert len(field_loader) == len(set_data['data'])

    def test__str__(self, field_loader):
        if os.name == 'nt':
            matching_str = 'FieldLoader: <HDF5 dataset "data": shape (10, 10), type "<i4">'
        else:
            matching_str = 'FieldLoader: <HDF5 dataset "data": shape (10, 10), type "<i8">'
        assert str(field_loader) == matching_str

    class TestIndexing:
        """Groups tests of index slicing."""

        @pytest.mark.parametrize("idx", [0, 1, 2, 3, 4])
        def test__index__single_obj(self, idx, field_loader, set_data):
            assert_array_equal(field_loader[idx], set_data['data'][idx])

        def test__index__single_objs_single_value(self, field_loader, set_data):
            assert_array_equal(field_loader[0, 0], set_data['data'][0][0])


def get_expected_object_values(set_data, fields, idx):
    """Get the expected values of an object index from the test dataset."""
    assert set_data
    assert fields
    assert idx is not None
    if isinstance(idx, int):
        expected = get_single_object_values(set_data, fields, idx)
    else:
        expected = [get_single_object_values(set_data, fields, idx[i]) for i in idx]
    return expected


def get_single_object_values(set_data, fields, idx):
    return [set_data[field][idx] for field in fields]


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


@pytest.fixture
def set_loader():
    set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')
    return set_loader


@pytest.fixture
def set_fields():
    set_loader, _, set_fields = db_generator.get_test_dataset_SetLoader('train')
    return set_fields


class TestSetLoader:
    """Unit tests for the SetLoader class."""

    def test__init(self):
        h5obj = db_generator.load_hdf5_file()
        dataset = db_generator.dataset
        set_name = 'test'
        data_dir = '/some/dir'
        set_loader = SetLoader(h5obj[set_name], data_dir)
        columns = ascii_to_str(dataset[set_name]['__COLUMNS__'])
        assert set_loader.set == set_name
        assert set_loader.columns == columns
        assert set_loader.num_elements == 5
        assert_array_equal(set_loader.shape, np.array([5, len(columns)]))

    class TestGet:
        """Group tests for the get() method."""

        def test_get_data_raises_keyerror_invalid_field(self, set_loader, set_data):
            with pytest.raises(AssertionError):
                data = set_loader.get(index=0, field='data_invalid')

        @pytest.mark.parametrize("idx", [0, 1, 2, 3, 4])
        def test_get_data_single_obj(self, idx, set_loader, set_data):
            field = 'data'
            assert_array_equal(set_loader.get(idx, field), set_data[field][idx])

        def test_get_data_two_objs(self, set_loader, set_data):
            field = 'data'
            idx = [0, 1]
            assert_array_equal(set_loader.get(idx, field), set_data[field][idx])

        def test_get_data_two_objs_same_index(self, set_loader, set_data):
            field = 'data'
            idx = [0, 0]
            assert_array_equal(set_loader.get(idx, field), set_data[field][idx[0]])

        def test_get_data_multiple_objs(self, set_loader, set_data):
            field = 'data'
            idx = range(5)
            assert_array_equal(set_loader.get(idx, field), set_data[field][idx])

        def test_get_data_all_obj(self, set_loader, set_data):
            field = 'data'
            assert_array_equal(set_loader.get(field=field), set_data[field])

    def test_size(self, set_loader, set_data):
        assert set_loader.size() == set_data['data'].shape[0]

    def test_list(self, set_loader, set_fields):
        expected = [name for name in sorted(set_fields) if name not in ['__COLUMNS__', '__TYPES__']]
        assert sorted(set_loader.list()) == expected

    def test_get_column_id(self, set_loader):
        assert set_loader.get_column_id('data') == 0

    def test_get_column_id_raise_error_invalid_field(self, set_loader):
        with pytest.raises(KeyError):
            obj_id = set_loader.get_column_id('data_invalid_field')

    def test_info(self, set_loader):
        set_loader.info()

    def test_sample(self, set_loader):
        assert len(set_loader.sample()) == 5

    def test_sample_multiple_samples(self, set_loader):
        assert len(set_loader.sample(5)) == 5

    def test_sample_multiple_samples_with_replacement(self, set_loader):
        assert len(set_loader.sample(10, replace=True, random_state=123)) == 10

    def test_head(self, set_loader):
        samples = set_loader.head()
        expected = set_loader.get([0, 1, 2, 3, 4])
        for i in range(len(samples)):
            for j in range(len(samples[i])):
                assert_array_equal(samples[i][j], expected[i][j])

    def test_head_sample_first_value(self, set_loader):
        sample = set_loader.head(1)
        expected = set_loader.get(0)
        for i in range(len(sample)):
            assert_array_equal(sample[i], expected[i])

    def test_head_sample_first_six_values(self, set_loader):
        samples = set_loader.head(6)
        expected = set_loader.get([0, 1, 2, 3, 4, 5])
        for i in range(len(samples)):
            for j in range(len(samples[i])):
                assert_array_equal(samples[i][j], expected[i][j])

    @pytest.mark.parametrize('n', [0, -1])
    def test_head_raises_error_if_number_is_zero_or_negative(self, set_loader, n):
        with pytest.raises(AssertionError):
            set_loader.head(n)

    def test_tail(self, set_loader):
        idx = list(range(len(set_loader) - 5, len(set_loader)))
        samples = set_loader.tail()
        expected = set_loader.get(idx)
        for i in range(len(samples)):
            for j in range(len(samples[i])):
                assert_array_equal(samples[i][j], expected[i][j])

    def test_tail_sample_last_value(self, set_loader):
        sample = set_loader.tail(1)
        expected = set_loader.get(len(set_loader) - 1)
        for i in range(len(sample)):
            assert_array_equal(sample[i], expected[i])

    def test_tail_sample_last_six_values(self, set_loader):
        idx = list(range(len(set_loader) - 6, len(set_loader)))
        samples = set_loader.tail(6)
        expected = set_loader.get(idx)
        for i in range(len(samples)):
            for j in range(len(samples[i])):
                assert_array_equal(samples[i][j], expected[i][j])

    @pytest.mark.parametrize('n', [0, -1])
    def test_tail_raises_error_if_number_is_zero_or_negative(self, set_loader, n):
        with pytest.raises(AssertionError):
            set_loader.tail(n)

    def test_to_pandas(self, set_loader):
        df = set_loader.to_pandas()
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == set_loader.columns

    def test_to_pandas_custom_column_names(self, set_loader):
        columns = ['custom_' + column for column in set_loader.columns]
        df = set_loader.to_pandas(columns=columns)
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == columns

    def test__len__(self, set_loader, set_data):
        assert len(set_loader) == len(set_data['data'])

    def test__str__(self, set_loader, set_data):
        size = len(set_data['data'])
        matching_str = 'SetLoader: set<train>, len<{}>'.format(size)
        assert str(set_loader) == matching_str


@pytest.fixture
def data_loader():
    data_loader, _, _ = db_generator.get_test_dataset_DataLoader()
    return data_loader


@pytest.fixture
def dataset():
    _, dataset, _ = db_generator.get_test_dataset_DataLoader()
    return dataset


class TestDataLoader:
    """Unit tests for the DataLoader class."""

    def test__init(self):
        name = 'some_db'
        task = 'task'
        data_dir = '/some/dir'
        hdf5_file = db_generator.get_test_hdf5_filename_DataLoader()
        data_loader = DataLoader(name, task, data_dir, hdf5_file)
        assert data_loader.dataset == name
        assert data_loader.task == task
        assert data_loader.data_dir == data_dir
        assert data_loader.hdf5_filename == hdf5_file
        assert 'train' in data_loader.sets

    class TestGet:
        """Group tests for the get() method."""

        @pytest.mark.parametrize("idx", [0, 1, 2, 3, 4])
        def test_get_single_obj(self, idx, data_loader, dataset):
            set_name = 'train'
            field = 'data'
            assert_array_equal(data_loader.get(set_name, idx, field),
                               dataset[set_name][field][idx])

        def test_get_single_obj_named_args(self, data_loader, dataset):
            set_name = 'train'
            field = 'data'
            idx = 0
            assert_array_equal(data_loader.get(set_name=set_name, field=field, index=idx),
                               dataset[set_name][field][idx])

        def test_get_single_obj_access_via_SetLoader(self, data_loader, dataset):
            set_name = 'train'
            field = 'data'
            idx = 1
            assert_array_equal(data_loader._sets_loader[set_name].get(idx, field),
                               dataset[set_name][field][idx])

        def test_get_single_obj_raise_error_invalid_set(self, data_loader, dataset):
            with pytest.raises(KeyError):
                data = data_loader.get('val', 'data', 0)

        def test_get_two_objs(self, data_loader, dataset):
            set_name = 'train'
            field = 'data'
            idx = (2, 6, )
            assert_array_equal(data_loader.get(set_name, idx, field),
                               dataset[set_name][field][list(idx)])

        def test_get_all_objs(self, data_loader, dataset):
            set_name = 'train'
            field = 'data'
            assert_array_equal(data_loader.get(set_name, field=field), dataset[set_name][field])

        def test_get_all_objs_empty_index(self, data_loader, dataset):
            set_name = 'train'
            field = 'data'
            assert_array_equal(data_loader.get(set_name, field=field), dataset[set_name][field])

    class TestSize:
        """Group tests for the size() method."""

        def test_size_single_field(self, data_loader, dataset):
            set_name = 'train'
            assert data_loader.size(set_name) == dataset[set_name]['data'].shape[0]

        def test_size_no_inputs(self, data_loader, dataset):
            size = data_loader.size()
            expected = {set_name: len(dataset[set_name]['data']) for set_name in dataset}
            assert size == expected

        def test_size_raise_error_invalid_set(self, data_loader):
            with pytest.raises(KeyError):
                size = data_loader.size("val")

        def test_size_raise_error_invalid_sfield(self, data_loader):
            with pytest.raises(KeyError):
                size = data_loader.size(set_name="invalid_set_name")

    def test_list_single_set(self, data_loader, dataset):
        set_name= 'train'
        expected = [name for name in sorted(dataset[set_name]) if name not in ['__COLUMNS__', '__TYPES__']]
        assert sorted(data_loader.list(set_name)) == expected

    def test_list_all_sets(self, data_loader, dataset):
        fields = data_loader.list()
        expected = {}
        for set_name in sorted(dataset):
            expected[set_name] = sorted([name for name in dataset[set_name] if name not in ['__COLUMNS__', '__TYPES__']])
            fields[set_name] = sorted(fields[set_name])
        assert fields == expected

    def test_list_raise_error_invalid_set(self, data_loader):
        with pytest.raises(KeyError):
            fields = data_loader.list('val')

    def test_get_column_id_field1(self, data_loader):
        assert data_loader.get_column_id('train', 'data') == 0

    def test_get_column_id_field2(self, data_loader):
        assert data_loader.get_column_id(set_name='train', field='number') == 3

    def test_get_column_id_raise_error_invalid_set(self, data_loader):
        with pytest.raises(KeyError):
            obj_id = data_loader.get_column_id('val', 'data')

    def test_info_single_set(self, data_loader):
        data_loader.info('train')

    def test_info_all_sets(self, data_loader):
        data_loader.info()

    def test_info_raise_error_invalid_set(self, data_loader):
        with pytest.raises(KeyError):
            data_loader.info('val')

    def test_sample(self, data_loader):
        assert len(data_loader.sample('train')) == 5

    def test_sample_multiple_samples(self, data_loader):
        assert len(data_loader.sample('test', 5)) == 5

    def test_sample_multiple_samples_with_replacement(self, data_loader):
        assert len(data_loader.sample('train', 10, replace=True, random_state=123)) == 10

    def test_sample_raises_error_no_inputs(self, data_loader):
        with pytest.raises(TypeError):
            data_loader.sample()

    def test_head(self, data_loader):
        set_name = 'train'
        samples = data_loader.head(set_name)
        expected = data_loader.get(set_name, [0, 1, 2, 3, 4])
        for i in range(len(samples)):
            for j in range(len(samples[i])):
                assert_array_equal(samples[i][j], expected[i][j])

    def test_head_sample_first_value(self, data_loader):
        set_name = 'test'
        sample = data_loader.head(set_name, 1)
        expected = data_loader.get(set_name, 0)
        for i in range(len(sample)):
            assert_array_equal(sample[i], expected[i])

    def test_head_sample_first_six_values(self, data_loader):
        set_name = 'train'
        samples = data_loader.head(set_name, 6)
        expected = data_loader.get(set_name, [0, 1, 2, 3, 4, 5])
        for i in range(len(samples)):
            for j in range(len(samples[i])):
                assert_array_equal(samples[i][j], expected[i][j])

    def test_head_raises_error_no_inputs(self, data_loader):
        with pytest.raises(TypeError):
            data_loader.head()

    @pytest.mark.parametrize('n', [0, -1])
    def test_head_raises_error_if_number_is_zero_or_negative(self, data_loader, n):
        with pytest.raises(AssertionError):
            data_loader.head('train', n)

    def test_tail(self, data_loader):
        set_name = 'train'
        set_size = len(data_loader._sets_loader[set_name])
        idx = list(range(set_size - 5, set_size))
        samples = data_loader.tail(set_name)
        expected = data_loader.get(set_name, idx)
        for i in range(len(samples)):
            for j in range(len(samples[i])):
                assert_array_equal(samples[i][j], expected[i][j])

    def test_tail_sample_last_value(self, data_loader):
        set_name = 'train'
        set_size = len(data_loader._sets_loader[set_name])
        sample = data_loader.tail(set_name, 1)
        expected = data_loader.get(set_name, set_size - 1)
        for i in range(len(sample)):
            assert_array_equal(sample[i], expected[i])

    def test_tail_sample_last_six_values(self, data_loader):
        set_name = 'train'
        set_size = len(data_loader._sets_loader[set_name])
        idx = list(range(set_size - 6, set_size))
        samples = data_loader.tail(set_name, 6)
        expected = data_loader.get(set_name, idx)
        for i in range(len(samples)):
            for j in range(len(samples[i])):
                assert_array_equal(samples[i][j], expected[i][j])

    @pytest.mark.parametrize('n', [0, -1])
    def test_tail_raises_error_if_number_is_zero_or_negative(self, data_loader, n):
        with pytest.raises(AssertionError):
            data_loader.tail('train', n)

    def test_tail_raises_error_no_inputs(self, data_loader):
        with pytest.raises(TypeError):
            data_loader.tail()

    def test_dtypes(self, data_loader):
        dtypes = data_loader.dtypes
        for set_name in data_loader.sets:
            assert dtypes[set_name] == data_loader._sets_loader[set_name].dtypes

    def test_shape(self, data_loader):
        shape = data_loader.shape
        for set_name in data_loader.sets:
            assert_array_equal(shape[set_name], data_loader._sets_loader[set_name].shape)

    def test_columns(self, data_loader):
        columns = data_loader.columns
        for set_name in data_loader.sets:
            assert columns[set_name] == data_loader._sets_loader[set_name].columns

    def test__len__(self, data_loader, dataset):
        assert len(data_loader) == len(dataset)

    def test__str__(self, data_loader):
        assert str(data_loader) == "DataLoader: some_db ('task' task)"
