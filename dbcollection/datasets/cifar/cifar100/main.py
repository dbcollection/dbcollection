"""
Cifar100 download/process functions.
"""


from __future__ import print_function, division
from dbcollection.utils.url import download_extract_all

from .classification import Classification


class Cifar100:
    """ Cifar100 preprocessing/downloading functions """

    # download url
    url = 'https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz'
    md5_checksum = 'eb9058c3a382ffc7106e4002c42a8d85'

    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['image_processing', 'classification']


    def __init__(self, data_path, cache_path, extract_data, verbose=True):
        """
        Initialize class.
        """
        self.cache_path = cache_path
        self.data_path = data_path
        self.extract_data = extract_data
        self.verbose = verbose


    def download(self):
        """
        Download and extract files to disk.
        """
        # download + extract data and remove temporary files
        download_extract_all(self.url, self.md5_checksum, self.data_path,
                             self.extract_data, self.verbose)

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