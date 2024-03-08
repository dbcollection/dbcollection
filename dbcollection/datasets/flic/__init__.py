"""
Frames Labeled In Cinema (FLIC) Dataset download/process functions.
"""


from dbcollection.datasets import BaseDataset
from .keypoints import Keypoints


class Dataset(BaseDataset):
    """Frames Labeled In Cinema (FLIC) Dataset preprocessing/downloading functions."""
    urls = ({"url": '0B4K3PZp8xXDJN0Fpb0piVjQ3Y3M',
             "save_name": 'flic.zip',
             "source": 'googledrive'},)
    keywords = ('image_processing', 'detection', 'human_pose', 'keypoints')
    tasks = {"keypoints": Keypoints}
    default_task = 'keypoints'
