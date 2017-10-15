"""
Cifar10 download/process functions.
"""


from dbcollection.datasets import BaseDataset
from .classification import Classification


urls = ({'url': 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz',
         'md5hash': 'c58f30108f718f92721af3b95e74349a'},)
keywords = ('image_processing', 'classification')
tasks = {"classification": Classification}
default_task = 'classification'


class Dataset(BaseDataset):
    """ Cifar10 preprocessing/downloading functions """
    urls = urls
    keywords = keywords
    tasks = tasks
    default_task = default_task
