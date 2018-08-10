"""
Pascal VOC 2007 download/process functions.
"""


from dbcollection.datasets import BaseDataset
from .detection import Detection

urls = (
    'http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar',
    'http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar',
)
keywords = ('image_processing', 'object_detection')
tasks = {"detection": Detection}
default_task = 'detection'


class Dataset(BaseDataset):
    """Pascal VOC 2007 preprocessing/downloading class."""
    urls = urls
    keywords = keywords
    tasks = tasks
    default_task = default_task
