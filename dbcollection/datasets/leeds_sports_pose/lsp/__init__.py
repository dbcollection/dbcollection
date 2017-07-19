"""
Leeds Sports Pose (LSP) Dataset download/process functions.
"""


from dbcollection.datasets.dbclass import BaseDataset
from .keypoints import Keypoints, KeypointsOriginal


class LSP(BaseDataset):
    """ Leeds Sports Pose (LSP) Dataset preprocessing/downloading functions """

    # download url
    url = ["http://www.comp.leeds.ac.uk/mat4saj/lsp_dataset_original.zip",
           "http://www.comp.leeds.ac.uk/mat4saj/lsp_dataset.zip"]

    md5_checksum = ''

    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['image_processing', 'detection', 'human pose', 'keypoints']

    # init tasks
    tasks = {
        "keypoints": Keypoints,
        "keypoints_original": KeypointsOriginal
    }
    default_task = 'keypoints'