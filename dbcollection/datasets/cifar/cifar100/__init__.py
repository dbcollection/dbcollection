"""
Cifar100 download/process functions.
"""


from dbcollection.datasets import BaseDataset
from .classification import Classification


urls = ({'url': 'https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz',
         'md5hash': 'eb9058c3a382ffc7106e4002c42a8d85'},)
keywords = ('image_processing', 'classification')
tasks = {"classification": Classification}
default_task = 'classification'


class Dataset(BaseDataset):
    """ Cifar100 preprocessing/downloading functions """
    urls = urls
    keywords = keywords
    tasks = tasks
    default_task = default_task
