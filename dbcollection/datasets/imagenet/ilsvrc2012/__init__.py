"""
ImageNet ILSVRC 2012 download/process functions.
"""


from __future__ import print_function
from dbcollection.datasets.dbclass import BaseDataset
from .classification import Classification, Raw256


class ILSVRC2012(BaseDataset):
    """ ImageNet ILSVRC 2012 preprocessing/downloading functions """

    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['image_processing', 'classification']

    # init tasks
    tasks = {
        "classification": Classification,
        "raw256": Raw256
    }
    default_task = 'classification'


    def download(self):
        """
        Download and extract files to disk.
        """
        if self.verbose:
            print('\n***************************************************************************')
            print(' Please download this dataset from the official source: www.image-net.org')
            print('***************************************************************************\n')

        return self.keywords
