"""
ImageNet ILSVRC 2012 download/process functions.
"""


from __future__ import print_function
from dbcollection.datasets import BaseDataset
from .classification import Classification, Raw256

urls = ()
keywords = ('image_processing', 'classification')
tasks = {
    "classification": Classification,
    "raw256": Raw256,
}
default_task = 'classification'


class Dataset(BaseDataset):
    """ImageNet ILSVRC 2012 preprocessing/downloading functions."""
    urls = urls
    keywords = keywords
    tasks = tasks
    default_task = default_task

    def download(self):
        """
        Download and extract files to disk.
        """
        if self.verbose:
            print('\n***************************************************************************')
            print(' Please download this dataset from the official source: www.image-net.org')
            print('***************************************************************************\n')
            print('When setting up this dataset for the first time, ' +
                  'please link the folder containing the downloaded data.')

        return self.keywords
