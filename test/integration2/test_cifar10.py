#!/usr/bin/env python3


"""
Test downloading the cifar10 dataset.
"""


from __future__ import print_function
import os
import sys
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(lib_path)
import dbcollection.manager as dbc


# delete all cache data + dir
print('==> dbcollection.remove:')
dbc.config_cache(delete_cache=True, is_test=True)

# download dataset
print('==> dbcollection.load:')
loader = dbc.load(name='cifar10', task='classification',  data_dir='/home/mf/tmp/download_data', is_test=True)

# print data from the loader
dbc.info(is_test=True)

# print data from the loader
print('######### info #########')
print('Dataset: ' + loader.name)
print('Task: ' + loader.task)
print('Data path: ' + loader.data_dir)
print('Metadata cache path: ' + loader.cache_path)

# delete all cache data + dir
print('==> dbcollection.remove:')
dbclt.manage_cache(delete_cache=True, is_test=True)