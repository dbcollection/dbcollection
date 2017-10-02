"""
Test dbcollection dataset methods/classes
"""

import pytest
from dbcollection.core.db import fetch_list_datasets

def test_fetch_list_datasets():
    db_list = fetch_list_datasets()
    assert 'mnist' in db_list

if __name__ == '__main__':
    test_fetch_list_datasets()
    