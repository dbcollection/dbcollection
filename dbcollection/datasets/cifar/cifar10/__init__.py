"""
Cifar10 download/process functions.
"""


from dbcollection.datasets.dbclass import BaseDataset
from .classification import Classification


class Cifar10(BaseDataset):
    """ Cifar10 preprocessing/downloading functions """

    # download url
    url = 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz'
    md5_checksum = 'c58f30108f718f92721af3b95e74349a'

    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['image_processing', 'classification']

    # init tasks
    tasks = {
        "classification": Classification
    }
    default_task = 'classification'