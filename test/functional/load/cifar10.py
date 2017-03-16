#!/usr/bin/env python3

"""
Test loading the cifar10 dataset.
"""


from __future__ import print_function
import os
import sys
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..', '..'))
sys.path.append(lib_path)
import dbcollection.manager as dbc


# delete all cache data + dir
print('==> dbcollection.remove:')
dbc.config_cache(delete_cache=True, is_test=True)

# download/setup dataset
print('==> dbcollection.download:')
dbc.load(name='cifar10', task='default', data_dir='/home/mf/tmp/download_data', verbose=True, is_test=True)

# print data from the loader
dbc.info(is_test=True)

# delete all cache data + dir
print('==> dbcollection.remove:')
dbc.config_cache(delete_cache=True, is_test=True)