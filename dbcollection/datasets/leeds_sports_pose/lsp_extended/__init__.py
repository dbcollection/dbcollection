"""
Leeds Sports Pose Exntended (LSPe) Dataset download/process functions.
"""


from dbcollection.datasets.dbclass import BaseDataset
from .keypoints import Keypoints


class LSPe(BaseDataset):
    """ Leeds Sports Pose Extended (LSPe) Dataset preprocessing/downloading functions """

    # download url
    urls = [
        'http://sam.johnson.io/research/lspet_dataset.zip',
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
        "keypoints": Keypoints
    }
    default_task = 'keypoints'