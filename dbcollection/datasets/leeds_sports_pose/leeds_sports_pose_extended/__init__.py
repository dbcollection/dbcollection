"""
Leeds Sports Pose Exntended (LSPe) Dataset download/process functions.
"""


from dbcollection.datasets import BaseDataset
from .keypoints import Keypoints

urls = (
    'http://sam.johnson.io/research/lspet_dataset.zip',
    {
        'url': 'http://sam.johnson.io/research/lsp_dataset.zip',
        'extract_dir': 'lsp_dataset',
    },
)
keywords = ('image_processing', 'detection', 'human_pose', 'keypoints')
tasks = {"keypoints": Keypoints}
default_task = 'keypoints'


class Dataset(BaseDataset):
    """Leeds Sports Pose extended (LSPe) Dataset preprocessing/downloading functions."""
    urls = urls
    keywords = keywords
    tasks = tasks
    default_task = default_task
