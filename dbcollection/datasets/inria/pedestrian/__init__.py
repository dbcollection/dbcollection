"""
Inria Pedestrian Dataset download/process functions.
"""


from dbcollection.datasets.dbclass import BaseDataset
from .detection import Detection


class Pedestrian(BaseDataset):
    """ Inria Pedestrian Dataset preprocessing/downloading functions """

    # download url
    urls = ['http://www.vision.caltech.edu.s3-us-west-2.amazonaws.com/Image_Datasets/CaltechPedestrians/datasets/INRIA/set00.tar',
            'http://www.vision.caltech.edu.s3-us-west-2.amazonaws.com/Image_Datasets/CaltechPedestrians/datasets/INRIA/set01.tar',
            'http://www.vision.caltech.edu.s3-us-west-2.amazonaws.com/Image_Datasets/CaltechPedestrians/datasets/INRIA/annotations.zip']

    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['image_processing', 'detection', 'pedestrian']

    # init tasks
    tasks = {
        "detection": Detection
    }
    default_task = 'detection'