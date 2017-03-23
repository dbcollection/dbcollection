"""
MNIST download/process functions.
"""


from __future__ import print_function, division
import os
import shutil

from .classification import Classification


class MNIST:
    """ Cifar10 preprocessing/downloading functions """

    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['classification']


    def __init__(self, data_path, cache_path, extract_data, verbose=True):
        """
        Initialize class.
        """
        self.cache_path = cache_path
        self.data_path = data_path
        self.extract_data = extract_data
        self.verbose = verbose


    def download(self, is_download=True):
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


    def process(self):
        """
        Process metadata for all tasks
        """
        # init tasks
        tasks = {
            "classification": Classification(self.data_path, self.cache_path, self.verbose)
        }

        # process all tasks
        info_output = {}
        for task in tasks:
            if self.verbose:
                print('Processing ::{}:: task:\n'.format(task))
            info_output[task] = tasks[task].run()

        # define a default task
        info_output['default'] = info_output['classification']

        return info_output, self.keywords