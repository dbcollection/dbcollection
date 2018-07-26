"""
MPII Human Pose Dataset download/process functions.
"""


from dbcollection.datasets import BaseDatasetNew
from .keypoints import Keypoints, KeypointsClean


urls = (
    'http://datasets.d2.mpi-inf.mpg.de/andriluka14cvpr/mpii_human_pose_v1.tar.gz',
    'http://datasets.d2.mpi-inf.mpg.de/andriluka14cvpr/mpii_human_pose_v1_u12_2.zip',
)
keywords = ('image_processing', 'detection', 'human_pose', 'keypoints')
tasks = {
    "keypoints": Keypoints,             # Contains all the original annotations
    "keypoints_clean": KeypointsClean,  # clean version (removes invalid annotations)
}
default_task = 'keypoints'


class Dataset(BaseDatasetNew):
    """MPII Pose Dataset preprocessing/downloading functions."""
    urls = urls
    keywords = keywords
    tasks = tasks
    default_task = default_task
