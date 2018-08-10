"""
Pascal VOC 2012 download/process functions.
"""


from dbcollection.datasets import BaseDataset
from .detection import Detection

urls = ('http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar',)
keywords = ('image_processing', 'object_detection')
tasks = {"detection": Detection}
default_task = 'detection'


class Dataset(BaseDataset):
    """Pascal VOC 2012 preprocessing/downloading class."""
    urls = urls
    keywords = keywords
    tasks = tasks
    default_task = default_task
