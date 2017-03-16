"""
Test dbcollection/utils/string_ascii.py.
"""


import os
import sys
import pytest
from unittest.mock import patch

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..', '..'))
sys.path.append(lib_path)

from dbcollection.utils import string_ascii


def test_str_to_ascii():
    assert 0

def test_ascii_to_str():
    assert 0

def test_convert_str_to_ascii():
    assert 0

def test_convert_ascii_to_str():
    assert 0