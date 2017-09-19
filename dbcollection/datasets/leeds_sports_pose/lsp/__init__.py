"""
Leeds Sports Pose (LSP) Dataset download/process functions.
"""


from dbcollection.datasets.dbclass import BaseDataset
from .keypoints import Keypoints, KeypointsOriginal


class LSP(BaseDataset):
    """ Leeds Sports Pose (LSP) Dataset preprocessing/downloading functions """

    # download url
    urls = [
        'http://sam.johnson.io/research/lsp_dataset_original.zip',
        {
            'url': 'http://sam.johnson.io/research/lsp_dataset.zip',
            'extract_dir': 'lsp_dataset'
        }
    ]

    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['image_processing', 'detection', 'human pose', 'keypoints']

    # init tasks
    tasks = {
        "keypoints": Keypoints,
        "keypoints_original": KeypointsOriginal
    }
    default_task = 'keypoints'