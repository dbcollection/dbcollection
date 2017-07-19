"""
Frames Labeled In Cinema (FLIC) Dataset download/process functions.
"""


from dbcollection.datasets.dbclass import BaseDataset
from .keypoints import Keypoints


class Flic(BaseDataset):
    """ Frames Labeled In Cinema (FLIC) Dataset preprocessing/downloading functions """

    # download url
    url = [
        ['googledrive', '0B4K3PZp8xXDJN0Fpb0piVjQ3Y3M', 'flic.zip']
    ]

    md5_checksum = ''

    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['image_processing', 'detection', 'human pose', 'keypoints']

    # init tasks
    tasks = {
        "keypoints" : Keypoints
    }
    default_task = 'keypoints'