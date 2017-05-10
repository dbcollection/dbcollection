"""
MPII Human Pose Dataset download/process functions.
"""


from dbcollection.datasets.dbclass import BaseDataset
from .keypoints import Keypoints, KeypointsNoSourceGrp


class MPIIPose(BaseDataset):
    """ Frames Labeled In Cinema (FLIC) Dataset preprocessing/downloading functions """

    # download url
    url = ["http://datasets.d2.mpi-inf.mpg.de/andriluka14cvpr/mpii_human_pose_v1.tar.gz",
           "http://datasets.d2.mpi-inf.mpg.de/andriluka14cvpr/mpii_human_pose_v1_u12_2.zip"]

    md5_checksum = ''

    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['image_processing', 'detection', 'human pose', 'keypoints']

    # init tasks
    tasks = {
        "keypoints" : Keypoints,
        "keypoints_d" : KeypointsNoSourceGrp
    }
    default_task = 'keypoints'