#!/usr/bin/env python3


"""
Test downloading + preprocessing the cifar10 dataset.
"""


from __future__ import print_function
import os
import sys
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(lib_path)
import dbcollection.manager as dbclt

# list cache file contents
print('==> dbcollection.list:')
dbclt.list(True)

# list cache file contents
print('==> dbcollection.clear:')
dbclt.clear(True, True)

# list cache file contents
print('==> dbcollection.list:')
dbclt.list(True)

# reset cache
print('==> dbcollection.reset:')
dbclt.reset()

# list cache file contents
print('==> dbcollection.list:')
dbclt.list(True)

# query the dataset name
print('==> dbcollection.query:')
print(dbclt.query('info'))

# remove dataset from the disk + cache file (if it exists)
print('==> dbcollection.delete:')
#dbclt.delete(name='cifar10', delete_data=True, delete_cache=True)
dbclt.delete(name='cifar10')

# download dataset
#print('==> dbcollection.download:')
#dbclt.download(name='cifar10', data_path='/home/mf/tmp/download_data', verbose=True)

# load dataset (process metadata file)

# list all cache

# configure dataset cache

# query the dataset name

# delete dataset

# list all cache
