"""
Test dbcollection/utils/loader.py.
"""


import os
import sys
import numpy as np
import h5py
import pytest

from dbcollection.core.loader import FieldLoader, SetLoader, DataLoader
from dbcollection.utils.test import TestDatasetGenerator
from dbcollection.utils.string_ascii import convert_ascii_to_str as ascii_to_str


# Setup dataset generator
db_generator = TestDatasetGenerator()

# -----------------------------------------------------------
# FieldLoader tests
# -----------------------------------------------------------

def test_FieldLoader__init():
    h5obj = db_generator.load_hdf5_file()

    obj_id = 1
    field_loader = FieldLoader(h5obj['/train/data'], obj_id)

    assert not field_loader._in_memory
    assert field_loader.name == 'data'

@pytest.mark.parametrize("idx", [0, 1, 2, 3, 4])
def test_FieldLoader_get_single_obj(idx):
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    data = field_loader.get(idx)

    assert np.array_equal(data, set_data['data'][idx])

@pytest.mark.parametrize("idx", [0, 1, 2, 3, 4])
def test_FieldLoader_get_single_obj_in_memory(idx):
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    field_loader.to_memory = True
    data = field_loader.get(idx)

    assert np.array_equal(data, set_data['data'][idx])

def test_FieldLoader_get_single_obj_by_arg_name():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    idx = 0
    data = field_loader.get(index=idx)

    assert np.array_equal(data, set_data['data'][idx])

def test_FieldLoader_get_single_obj_by_arg_name_in_memory():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    field_loader.to_memory = True
    idx = 0
    data = field_loader.get(index=idx)

    assert np.array_equal(data, set_data['data'][idx])

def test_FieldLoader_get_single_obj_list_of_equal_indexes():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    idx = [0, 0]
    data = field_loader.get(idx)

    assert np.array_equal(data, set_data['data'][list(set(idx))])

def test_FieldLoader_get_single_obj_list_of_equal_indexes_in_memory():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    field_loader.to_memory = True
    idx = [0, 0]
    data = field_loader.get(idx)

    assert np.array_equal(data, set_data['data'][list(set(idx))])

def test_FieldLoader_get_single_obj_list():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    idx = [0]
    data = field_loader.get(idx)

    assert np.array_equal(data, set_data['data'][idx[0]])

def test_FieldLoader_get_single_obj_list_in_memory():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    field_loader.to_memory = True
    idx = [0]
    data = field_loader.get(idx)

    assert np.array_equal(data, set_data['data'][idx[0]])

def test_FieldLoader_get_single_obj_tuple():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    idx = (0,)
    data = field_loader.get(idx)

    assert np.array_equal(data, set_data['data'][idx[0]])

def test_FieldLoader_get_single_obj_tuple_in_memory():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    field_loader.to_memory = True
    idx = (0,)
    data = field_loader.get(idx)

    assert np.array_equal(data, set_data['data'][idx[0]])

def test_FieldLoader_get_single_obj_raises_error_wrong_format():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    with pytest.raises(TypeError):
        idx = {1}
        data = field_loader.get(idx)

def test_FieldLoader_get_single_obj_raises_error_wrong_format_in_memory():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    field_loader.to_memory = True
    with pytest.raises(TypeError):
        idx = {1}
        data = field_loader.get(idx)

def test_FieldLoader_get_single_obj_empty_list():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    idx = []
    data = field_loader.get(idx)

    assert np.array_equal(data, set_data['data'])

def test_FieldLoader_get_single_obj_empty_list_in_memory():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    field_loader.to_memory = True
    idx = []
    data = field_loader.get(idx)

    assert np.array_equal(data, set_data['data'])

def test_FieldLoader_get_two_obj():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    idx = [1, 2]
    data = field_loader.get(idx)

    assert np.array_equal(data, set_data['data'][idx])

def test_FieldLoader_get_two_obj_in_memory():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    field_loader.to_memory = True
    idx = [1, 2]
    data = field_loader.get(idx)

    assert np.array_equal(data, set_data['data'][idx])

def test_FieldLoader_get_multiple_objs():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    idx = [1, 2, 5, 8]
    data = field_loader.get(idx)

    assert np.array_equal(data, set_data['data'][idx])

def test_FieldLoader_get_multiple_objs_in_memory():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    field_loader.to_memory = True
    idx = [1, 2, 5, 8]
    data = field_loader.get(idx)

    assert np.array_equal(data, set_data['data'][idx])

def test_FieldLoader_get_multiple_objs_unordered():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    idx = [8, 2, 5, 1]
    data = field_loader.get(idx)

    assert not np.array_equal(data, set_data['data'][idx])

def test_FieldLoader_get_multiple_objs_unordered_in_memory():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    field_loader.to_memory = True
    idx = [8, 2, 5, 1]
    data = field_loader.get(idx)

    assert not np.array_equal(data, set_data['data'][idx])

def test_FieldLoader_get_all_obj():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    data = field_loader.get()

    assert np.array_equal(data, set_data['data'])

def test_FieldLoader_get_all_obj_in_memory():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    field_loader.to_memory = True
    data = field_loader.get()

    assert np.array_equal(data, set_data['data'])

def test_FieldLoader_size():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    size = field_loader.size()

    assert size == set_data['data'].shape

def test_FieldLoader_object_field_id():
    field_loader, _ = db_generator.get_test_data_FieldLoader('train')

    obj_id = field_loader.object_field_id()

    assert obj_id is 1

def test_FieldLoader_object_field_id_not_equal():
    field_loader, _ = db_generator.get_test_data_FieldLoader('train')

    obj_id = field_loader.object_field_id()

    assert obj_id is not 2

def test_FieldLoader_info():
    field_loader, _ = db_generator.get_test_data_FieldLoader('train')
    field_loader.info()

def test_FieldLoader_info_no_verbose():
    field_loader, _ = db_generator.get_test_data_FieldLoader('train')
    field_loader.info(False)

def test_FieldLoader_to_memory():
    field_loader, _ = db_generator.get_test_data_FieldLoader('train')

    field_loader.to_memory = True

    assert isinstance(field_loader.data, np.ndarray)

def test_FieldLoader_to_memory_to_disk():
    field_loader, _ = db_generator.get_test_data_FieldLoader('train')

    field_loader.to_memory = True
    field_loader.to_memory = False

    assert isinstance(field_loader.data, h5py._hl.dataset.Dataset)

def test_FieldLoader__len__():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    size = len(field_loader)

    assert size == len(set_data['data'])

def test_FieldLoader__str__():
    field_loader, _ = db_generator.get_test_data_FieldLoader('train')

    if os.name == 'nt':
        matching_str = 'FieldLoader: <HDF5 dataset "data": shape (10, 10), type "<i4">'
    else:
        matching_str = 'FieldLoader: <HDF5 dataset "data": shape (10, 10), type "<i8">'

    assert str(field_loader) == matching_str

def test_FieldLoader__str__in_memory():
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

@pytest.mark.parametrize("idx", [0, 1, 2, 3, 4])
def test_FieldLoader__index__single_obj(idx):
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    data = field_loader[idx]

    assert np.array_equal(data, set_data['data'][idx])

@pytest.mark.parametrize("idx", [0, 1, 2, 3, 4])
def test_FieldLoader__index__single_obj_in_memory(idx):
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    field_loader.to_memory = True
    data = field_loader[idx]

    assert np.array_equal(data, set_data['data'][idx])

def test_FieldLoader__index__single_objs_single_value():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    data = field_loader[0, 0]

    assert np.array_equal(data, set_data['data'][0][0])

def test_FieldLoader__index__single_objs_single_value_in_memory():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    field_loader.to_memory = True
    data = field_loader[0, 0]

    assert np.array_equal(data, set_data['data'][0][0])


# -----------------------------------------------------------
# SetLoader tests
# -----------------------------------------------------------

def test_SetLoader__init():
    h5obj = db_generator.load_hdf5_file()

    dataset = db_generator.dataset
    set_name = 'test'
    set_loader = SetLoader(h5obj[set_name])

    assert set_loader.set == set_name
    assert set_loader.object_fields == ascii_to_str(dataset[set_name]['object_fields'])
    assert set_loader.nelems == 5

def test_SetLoader_get_data_raises_keyerror_missing_field():
    set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

    with pytest.raises(AssertionError):
        field = 'data'
        idx = 0
        data = set_loader.get(idx)

def test_SetLoader_get_data_raises_keyerror_invalid_field():
    set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

    with pytest.raises(KeyError):
        field = 'data_invalid'
        idx = 0
        data = set_loader.get(field, idx)

@pytest.mark.parametrize("idx", [0, 1, 2, 3, 4])
def test_SetLoader_get_data_single_obj(idx):
    set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

    field = 'data'
    data = set_loader.get(field, idx)

    assert np.array_equal(data, set_data[field][idx])

@pytest.mark.parametrize("idx", [0, 1, 2, 3, 4])
def test_SetLoader_get_data_single_obj_in_memory(idx):
    set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

    field = 'data'
    set_loader.fields[field].to_memory = True
    data = set_loader.get(field, idx)

    assert np.array_equal(data, set_data[field][idx])

def test_SetLoader_get_data_two_objs():
    set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

    field = 'data'
    idx = [0, 1]
    data = set_loader.get(field, idx)

    assert np.array_equal(data, set_data[field][idx])

def test_SetLoader_get_data_two_objs_in_memory():
    set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

    field = 'data'
    idx = [0, 1]
    set_loader.fields[field].to_memory = True
    data = set_loader.get(field, idx)

    assert np.array_equal(data, set_data[field][idx])

def test_SetLoader_get_data_two_objs_same_index():
    set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

    field = 'data'
    idx = [0, 0]
    data = set_loader.get(field, idx)

    assert np.array_equal(data, set_data[field][list(set(idx))])

def test_SetLoader_get_data_two_objs_in_memory():
    set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

    field = 'data'
    idx = [0, 0]
    set_loader.fields[field].to_memory = True
    data = set_loader.get(field, idx)

    assert np.array_equal(data, set_data[field][list(set(idx))])

def test_SetLoader_get_data_multiple_objs():
    set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

    field = 'data'
    idx = range(5)
    data = set_loader.get(field, idx)

    assert np.array_equal(data, set_data[field][idx])

def test_SetLoader_get_data_multiple_objs_in_memory():
    set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

    field = 'data'
    idx = range(5)
    set_loader.fields[field].to_memory = True
    data = set_loader.get(field, idx)

    assert np.array_equal(data, set_data[field][idx])

def test_SetLoader_get_data_all_obj():
    set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

    field = 'data'
    data = set_loader.get(field)

    assert np.array_equal(data, set_data[field])

def test_SetLoader_get_data_all_obj_in_memory():
    set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

    field = 'data'
    set_loader.fields[field].to_memory = True
    data = set_loader.get(field)

    assert np.array_equal(data, set_data[field])

def test_SetLoader_get_data_single_obj_object_ids():
    set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

    field = 'object_ids'
    idx = 0
    data = set_loader.get(field, idx)

    assert np.array_equal(data, set_data[field][idx])

def test_SetLoader_get_data_single_obj_object_ids_in_memory():
    set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

    field = 'object_ids'
    idx = 0
    set_loader.fields[field].to_memory = True
    data = set_loader.get(field, idx)

    assert np.array_equal(data, set_data[field][idx])

def test_SetLoader_object_single_obj():
    set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

    idx = 0
    data = set_loader.object(idx)

    assert np.array_equal(data, set_data['object_ids'][idx])

###
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
###

def test_SetLoader_object_single_obj_value():
    set_loader, set_data, fields = db_generator.get_test_dataset_SetLoader('train')

    idx = 0
    data = set_loader.object(idx, True)
    expected = get_expected_object_values(set_data, set_loader.object_fields, idx)

    assert compare_lists(data, expected)

def test_SetLoader_object_two_objs():
    set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

    idx = [0, 1]
    data = set_loader.object(idx)

    assert np.array_equal(data, set_data['object_ids'][idx])

def test_SetLoader_object_two_objs_value():
    set_loader, set_data, fields = db_generator.get_test_dataset_SetLoader('train')

    idx = [0, 1]
    data = set_loader.object(idx, True)
    expected = get_expected_object_values(set_data, set_loader.object_fields, idx)

    assert compare_lists(data, expected)

def test_SetLoader_object_all_objs():
    set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

    data = set_loader.object()

    assert np.array_equal(data, set_data['object_ids'])

def test_SetLoader_object_all_objs_value():
    set_loader, set_data, fields = db_generator.get_test_dataset_SetLoader('train')

    data = set_loader.object(convert_to_value=True)
    idx = range(len(set_data['object_ids']))
    expected = get_expected_object_values(set_data, set_loader.object_fields, idx)

    assert compare_lists(data, expected)

def test_SetLoader_size():
    set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

    field = 'data'
    size = set_loader.size(field)

    assert size == set_data[field].shape

def test_SetLoader_size_object_ids():
    set_loader, set_data, _ = db_generator.get_test_dataset_SetLoader('train')

    size = set_loader.size()

    assert size == set_data['object_ids'].shape

def test_SetLoader_list():
    set_loader, _, set_fields = db_generator.get_test_dataset_SetLoader('train')

    fields = set_loader.list()

    assert fields == tuple(set_fields)

def test_SetLoader_object_field_id():
    set_loader, _, _ = db_generator.get_test_dataset_SetLoader('train')

    obj_id = set_loader.object_field_id('data')

    assert obj_id == 0

def test_SetLoader_object_field_id_raise_error_invalid_field():
    set_loader, _, _ = db_generator.get_test_dataset_SetLoader('train')

    with pytest.raises(KeyError):
        obj_id = set_loader.object_field_id('data_invalid_field')

def test_SetLoader_info():
    set_loader, _, _ = db_generator.get_test_dataset_SetLoader('train')

    set_loader.info()

def test_SetLoader__len__():
    pass

def test_SetLoader__str__():
    pass


# -----------------------------------------------------------
# DataLoader tests
# -----------------------------------------------------------

def test_DataLoader__init():
    pass

def test_DataLoader_get_single_obj():
    pass

def test_DataLoader_get_single_obj_named_args():
    pass

def test_DataLoader_get_single_obj_access_via_SetLoader():
    pass

def test_DataLoader_get_two_objs():
    pass

def test_DataLoader_get_all_objs():
    pass

def test_DataLoader_get_all_objs_no_index():
    pass

def test_DataLoader_object_single_obj():
    pass

def test_DataLoader_object_single_obj_values():
    pass

def test_DataLoader_object_two_objs():
    pass

def test_DataLoader_object_two_obj_values():
    pass

def test_DataLoader_object_all_objs():
    pass

def test_DataLoader_object_all_objs_no_index():
    pass

def test_DataLoader_size_single_field():
    pass

def test_DataLoader_size_default():
    pass

def test_DataLoader_size_single_field_all_sets():
    pass

def test_DataLoader_size_no_inputs():
    pass

def test_DataLoader_list_single_set():
    pass

def test_DataLoader_list_all_sets():
    pass

def test_DataLoader_object_field_id_field1():
    pass

def test_DataLoader_object_field_id_field2():
    pass

def test_DataLoader_info_single_set():
    pass

def test_DataLoader_info_all_sets():
    pass

def test_DataLoader__len__():
    pass

def test_DataLoader__str__():
    pass
