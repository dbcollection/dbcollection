"""
Pascal VOC 2007 download/process functions.
"""


from dbcollection.datasets.dbclass import BaseDataset
from .detection import Detection


class PascalVOC2007(BaseDataset):
    """ Pascal VOC 2007 preprocessing/downloading class """

    # download url
    url = [
        'http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar',
        'http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar',
    ]
    md5_checksum = []

    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['image_processing', 'object_detection']

    # init tasks
    tasks = {
        "detection": Detection

    }
    default_task = 'detection'