"""
Cifar100 download/process functions.
"""


from dbcollection.datasets.dbclass import BaseDataset
from .classification import Classification


class Cifar100(BaseDataset):
    """ Cifar100 preprocessing/downloading functions """

    # download url
    url = 'https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz'
    md5_checksum = 'eb9058c3a382ffc7106e4002c42a8d85'

    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['image_processing', 'classification']

    # init tasks
    tasks = {
        "classification": Classification
    }
    default_task = 'classification'