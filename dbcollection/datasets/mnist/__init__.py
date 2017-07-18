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

    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['classification']

    # init tasks
    tasks = {
        "classification": Classification
    }
    default_task = 'classification'


    def download(self):
        """
        Download and extract files to disk.
        """
        # copy files to the specified data directory
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
        fname_train_imgs = os.path.join(path, 'train-images.idx3-ubyte')
        fname_train_lbls = os.path.join(path, 'train-labels.idx1-ubyte')
        fname_test_imgs = os.path.join(path, 't10k-images.idx3-ubyte')
        fname_test_lbls = os.path.join(path, 't10k-labels.idx1-ubyte')

        shutil.copy2(fname_train_imgs, self.data_path)
        shutil.copy2(fname_train_lbls, self.data_path)
        shutil.copy2(fname_test_imgs, self.data_path)
        shutil.copy2(fname_test_lbls, self.data_path)

        return self.keywords