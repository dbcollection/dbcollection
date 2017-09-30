"""
MNIST download/process functions.
"""

from __future__ import print_function, division
import os
import shutil

from dbcollection.datasets.dbclass import BaseDataset
from .classification import Classification


class MNIST(BaseDataset):
    """ Cifar10 preprocessing/downloading functions """

    urls = ["http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz",
            "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz",
            "http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz",
            "http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz"]


    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['classification']

    # init tasks
    tasks = {
        "classification": Classification
    }
    default_task = 'classification'