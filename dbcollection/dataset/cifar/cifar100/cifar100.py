"""
Cifar100 download/process functions.
"""


from __future__ import print_function, division
from .... import utils
from .classification import ClassificationTask


class Cifar100:
    """ Cifar100 preprocessing/downloading functions """

    # download url
    url = 'https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz'
    md5_checksum = 'eb9058c3a382ffc7106e4002c42a8d85'

    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['image_processing', 'classification']


    def __init__(self, data_path, cache_path, verbose=True):
        """
        Initialize class.
        """
        self.cache_path = cache_path
        self.data_path = data_path
        self.verbose = verbose


    def download(self, is_download=True):
        """
        Download and extract files to disk.
        """
        # download + extract data and remove temporary files
        if is_download:
            utils.download_extract_all(self.url, self.md5_checksum, self.data_path, False, self.verbose)

        return self.keywords


    def process(self):
        """
        Process metadata for all tasks
        """
        # init tasks
        tasks = {
            "classification": ClassificationTask(self.data_path, self.cache_path, self.verbose)
        }

        # process all tasks
        info_output = {}
        for task in tasks:
            if self.verbose:
                print('Processing <{}> task:\n'.format(task))
            info_output[task] = task.run()

        # define a default task
        info_output['default'] = info_output['classification']

        return info_output, self.keywords