"""
Test dbcollection/dataset/funs.py.
"""


import os
import sys
import pytest
from unittest.mock import patch

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..', '..'))
sys.path.append(lib_path)

from dbcollection.dataset import funs


def test_fetch_dataset_constructor__succeed():
    assert 0

def test_fetch_dataset_constructor__fail():
    assert 0

def test_setup_dataset_constructor():
    assert 0

def test_exists():
    assert 0

def test_download():
    assert 0

def test_process():
    assert 0

