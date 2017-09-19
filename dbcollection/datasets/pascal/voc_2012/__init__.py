"""
Pascal VOC 2012 download/process functions.
"""


from dbcollection.datasets.dbclass import BaseDataset
from .detection import Detection


class PascalVOC2012(BaseDataset):
    """ Pascal VOC 2012 preprocessing/downloading class """

    # download url
    urls = ['http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar']

    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['image_processing', 'object_detection']

    # init tasks
    tasks = {
        "detection" : Detection

    }
    default_task = 'detection'