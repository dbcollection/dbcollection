#!/usr/bin/env python

"""
Test file_extraction.py
"""


import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..', '..'))
#sys.path.append(lib_path)
sys.path.insert(0, lib_path)

from dbcollection.utils.file_extraction import *



def test_get_file_extension():
    pass

"""
def test_extract_file_zip():
    pass

def test_extract_file_tar():
    pass

def test_get_extractor_method():
    pass

def test_extract_file():
    pass
"""