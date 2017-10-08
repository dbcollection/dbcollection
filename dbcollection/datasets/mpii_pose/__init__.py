"""
MPII Human Pose Dataset download/process functions.
"""


from dbcollection.core.db import BaseDataset
from .keypoints import Keypoints, KeypointsFull

urls = (
    'http://datasets.d2.mpi-inf.mpg.de/andriluka14cvpr/mpii_human_pose_v1.tar.gz',
    'http://datasets.d2.mpi-inf.mpg.de/andriluka14cvpr/mpii_human_pose_v1_u12_2.zip',
)
keywords = ('image_processing', 'detection', 'human pose', 'keypoints')
tasks = {
    "keypoints": KeypointsFull,    # Contains all the original annotations
    "keypoints_clean": Keypoints,  # clean version (removes invalid annotations)
}
default_task = 'keypoints'


class Dataset(BaseDataset):
    """MPII Pose Dataset preprocessing/downloading functions."""
    urls = urls
    keywords = keywords
    tasks = tasks
    default_task = default_task
