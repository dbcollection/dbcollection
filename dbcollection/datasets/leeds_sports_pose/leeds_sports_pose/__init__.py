"""
Leeds Sports Pose (LSP) Dataset download/process functions.
"""


from dbcollection.datasets import BaseDataset
from .keypoints import Keypoints, KeypointsOriginal

urls = (
    'http://sam.johnson.io/research/lsp_dataset_original.zip',
    {
        'url': 'http://sam.johnson.io/research/lsp_dataset.zip',
        'extract_dir': 'lsp_dataset',
    },
)
keywords = ('image_processing', 'detection', 'human_pose', 'keypoints')
tasks = {
    "keypoints": Keypoints,
    "keypoints_original": KeypointsOriginal,
}
default_task = 'keypoints'


class Dataset(BaseDataset):
    """Leeds Sports Pose (LSP) Dataset preprocessing/downloading functions."""
    urls = urls
    keywords = keywords
    tasks = tasks
    default_task = default_task
