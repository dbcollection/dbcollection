"""
Test dbcollection/utils/loader.py.
"""


import pytest
import numpy as np

import dbcollection as dbc
from dbcollection.core.loader import FieldLoader, SetLoader,DataLoader
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
    pass

def test_FieldLoader_get_single_obj_in_memory():
    pass

def test_FieldLoader_get_single_obj_list_of_equal_indexes():
    pass

def test_FieldLoader_get_single_obj_list_of_equal_indexes_in_memory():
    pass

def test_FieldLoader_get_two_obj():
    pass

def test_FieldLoader_get_two_obj_in_memory():
    pass

def test_FieldLoader_get_multiple_objs():
    pass

def test_FieldLoader_get_multiple_objs_in_memory():
    pass

def test_FieldLoader_get_all_obj():
    pass

def test_FieldLoader_get_all_obj_in_memory():
    pass

def test_FieldLoader_size():
    pass

def test_FieldLoader_object_field_id():
    pass

def test_FieldLoader_info():
    pass

def test_FieldLoader_to_memory():
    pass

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
