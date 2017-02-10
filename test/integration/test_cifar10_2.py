#!/usr/bin/env python3


"""
Test downloading + preprocessing the cifar10 dataset.
"""


import os
import sys
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path, '..', '..'))
sys.path.append(lib_path)
import dbcollection


# list cache file contents
dbcollection.manager.list(True)

# get a loader to the dataset
dl_path = '/home/mf/tmp/download_data'
loader = dbcollection.manager.load(name='cifar10',data_dir=dl_path, verbose=True)

# print data from the loader
print('Dataset: ' + loader.name)
print('Category: ' + loader.category)
print('Task: ' + loader.task)
print('Data path: ' + loader.data_dir)
print('Metadata cache path: ' + loader.cache_path)

# remove dataset from the disk + cache file
dbcollection.manager.delete(name='cifar10',delete_data=True, delete_cache=True)
