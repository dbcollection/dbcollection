#!/usr/bin/env python
# Copyright (C) 2017, Farrajota @ https://github.com/farrajota
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
from os.path import expanduser

cache_path = expanduser("~") # cache path

cache_fname = ''
if sys.platform == 'win32':
    cache_fname = cache_path + '\\' + 'dbcollection.json'
else:
    cache_fname = cache_path + '/' + 'dbcollection.json'

def get_cache_filepath():
    """
    Returns the path for the .dbcollection.json file. 
    """
    return cache_fname


def get_cache_path():
    """
    Returns the path to save the dataset files.
    """
   

