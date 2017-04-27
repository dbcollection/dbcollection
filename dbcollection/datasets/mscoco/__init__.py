"""
Caltech Pedestrian Dataset download/process functions.
"""


from dbcollection.datasets.dbclass import BaseDataset
from .detection2015 import Detection2015
from .detection2016 import Detection2016
from .captions import Caption
from .keypoints import Keypoint


class MSCOCO(BaseDataset):
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
    keywords = ['image_processing', 'detection', 'keypoint', 'captions']

    # init tasks
    tasks = {
        "detection_2015" : Detection2015,
        "detection_2016" : Detection2016,
        "caption_2015" : Caption,
        "keypoint_2016" : Keypoint
    }

    default_task = 'detection_2016'