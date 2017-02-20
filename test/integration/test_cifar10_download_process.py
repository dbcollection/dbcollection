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


# download dataset
print('==> dbcollection.download:')
dbclt.download(name='cifar10', data_dir='/home/mf/tmp/download_data', verbose=True)

# load dataset (process metadata file)
print('==> dbcollection.load:')
loader = dbclt.load(name='cifar10', verbose=True)

# print data from the loader
print('Dataset: ' + loader.name)
print('Task: ' + loader.task)
print('Data path: ' + loader.data_dir)
print('Metadata cache path: ' + loader.cache_path)
