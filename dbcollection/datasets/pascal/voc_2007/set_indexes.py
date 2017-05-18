"""
Split indexes to train + val + trainval + test sets
"""


import random
import math
import numpy as np
from sklearn.model_selection import train_test_split

from dbcollection.datasets.pascal.voc_2007.test_indexes import test

total = list(range(1,9963+1))

# get train ids
trainval = [idx for idx in total if not idx in test]

# split trainval into train + val (50-50 split)
tmp = np.array(trainval)
train_np, val_np = train_test_split(np.array(trainval), test_size=0.5)
train_np.sort()
val_np.sort()

train = train_np.tolist()
val = val_np.tolist()

# convert to strings
train_ids = [str(value).zfill(6) for value in train]
val_ids = [str(value).zfill(6) for value in val]
trainval_ids = [str(value).zfill(6) for value in trainval]
test_ids = [str(value).zfill(6) for value in test]