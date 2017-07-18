"""
Caltech Pedestrian Dataset download/process functions.
"""


import os
import sys

from dbcollection.datasets.dbclass import BaseDataset
from .detection import Detection2015, Detection2016
from .captions import Caption2015, Caption2016
from .keypoints import Keypoints2016


class COCO(BaseDataset):
    """ Microsoft COCO Dataset preprocessing/downloading functions """

    # download url
    url = [
        'http://msvocds.blob.core.windows.net/coco2014/train2014.zip',
        'http://msvocds.blob.core.windows.net/coco2014/val2014.zip',
        'http://msvocds.blob.core.windows.net/coco2014/test2014.zip',
        'http://msvocds.blob.core.windows.net/coco2015/test2015.zip',
        'http://msvocds.blob.core.windows.net/annotations-1-0-3/instances_train-val2014.zip',
        'http://msvocds.blob.core.windows.net/annotations-1-0-3/person_keypoints_trainval2014.zip',
        'http://msvocds.blob.core.windows.net/annotations-1-0-3/captions_train-val2014.zip',
        'http://msvocds.blob.core.windows.net/annotations-1-0-4/image_info_test2014.zip',
        'http://msvocds.blob.core.windows.net/annotations-1-0-4/image_info_test2015.zip'
    ]

    md5_checksum = ''

    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['image_processing', 'detection', 'keypoint', 'captions', 'human', 'pose']

    # init tasks
    tasks = {
        "detection" : Detection2015,
        "detection_2015" : Detection2015,
        "detection_2016" : Detection2016,

        "caption" : Caption2015,
        "caption_2015" : Caption2015,
        "caption_2016" : Caption2016,

        "keypoints" : Keypoints2016,
        "keypoints_2016" : Keypoints2016,
    }

    default_task = 'detection'
