"""
ImageNet ILSVRC 2012 download/process functions.
"""


from __future__ import print_function
from dbcollection.datasets.dbclass import BaseDataset
from .classification import Classification, ClassificationNoSourceGrp, Raw256, Raw256NoSourceGrp


class ILSVRC2012(BaseDataset):
    """ ImageNet ILSVRC 2012 preprocessing/downloading functions """

    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['image_processing', 'classification']

    # init tasks
    tasks = {
        "classification" : Classification,
        "classification_d" : ClassificationNoSourceGrp,
        "raw256" : Raw256,
        "raw256_d" : Raw256NoSourceGrp
    }
    default_task = 'classification'


    def download(self):
        """
        Download and extract files to disk.
        """
        if self.verbose:
            print('***************************************************************************')
            print(' > Please download this dataset from the official source: www.image-net.org')
            print('***************************************************************************')
            print()

        return self.keywords