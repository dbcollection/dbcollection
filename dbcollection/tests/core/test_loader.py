"""
Test dbcollection/utils/loader.py.
"""


import pytest
import numpy as np
import h5py

import dbcollection as dbc
from dbcollection.core.loader import FieldLoader, SetLoader, DataLoader
from dbcollection.utils.test import TestDatasetGenerator
from dbcollection.utils.string_ascii import convert_ascii_to_str as tostr_


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

def test_FieldLoader_get_single_obj():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    idx = 0
    data = field_loader.get(idx)

    assert np.array_equal(data, set_data['data'][idx])

def test_FieldLoader_get_single_obj_in_memory():
    field_loader, set_data = db_generator.get_test_data_FieldLoader('train')

    field_loader.to_memory = True
    idx = 0
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
    pass

def test_FieldLoader__tostring__():
    pass

def test_FieldLoader__tostring__in_memory():
    pass

def test_FieldLoader__index__single_obj():
    pass

def test_FieldLoader__index__single_obj_in_memory():
    pass

def test_FieldLoader__index__single_objs_single_value():
    pass

def test_FieldLoader__index__single_objs_single_value_in_memory():
    pass

def test_FieldLoader__index__all_objs():
    pass

def test_FieldLoader__index__all_objs_in_memory():
    pass


# -----------------------------------------------------------
# SetLoader tests
# -----------------------------------------------------------

def test_SetLoader__init():
    pass


# -----------------------------------------------------------
# DataLoader tests
# -----------------------------------------------------------

def test_DataLoader__init():
    pass
