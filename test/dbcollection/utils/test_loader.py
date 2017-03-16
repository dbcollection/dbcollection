"""
Test dbcollection/utils/loader.py.
"""


import os
import sys
import pytest
from unittest.mock import patch

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..', '..'))
sys.path.append(lib_path)

from dbcollection.utils.loader import DatasetLoader


def test_get():
    assert 0

def test_object__get_idx():
    assert 0

def test_object__get_values():
    assert 0

def test_size__default():
    assert 0

def test_size__full():
    assert 0

def test_list():
    assert 0

def test_object_field_id__succeed():
    assert 0

def test_object_field_id__fail():
    assert 0