"""
Test dbcollection/manager.py.
"""


import os
import sys
import pytest
from unittest.mock import patch

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(lib_path)

from dbcollection import manager


def test_download():
    assert 0

def test_process():
    assert 0

def test_load():
    assert 0

def test_add():
    assert 0

def test_remove():
    assert 0

def test_config_cache():
    assert 0

def test_query():
    assert 0

