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
dbcollection.list()

# get a loader to the dataset
dl_path = '/home/mf/tmp/download_data'
loader = dbcollection.load(name='cifar10',data_path=dl_path, verbose=True)

