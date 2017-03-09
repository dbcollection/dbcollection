"""
ImageNet ILSVRC 2012 download/process functions.
"""


from __future__ import print_function
from .classification import ClassificationTask


class ILSVRC2012:
    """ Imagenet ILSVRC 2012 preprocessing/downloading functions """

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
        if self.verbose:
            print('Please download this dataset from the official source: www.image-net.org')

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