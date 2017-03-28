"""
ImageNet ILSVRC 2012 download/process functions.
"""


from __future__ import print_function
from .classification import Classification


class ILSVRC2012:
    """ Imagenet ILSVRC 2012 preprocessing/downloading functions """

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
        if self.verbose:
            print('Please download this dataset from the official source: www.image-net.org')

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