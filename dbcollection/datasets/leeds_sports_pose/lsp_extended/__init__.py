"""
Leeds Sports Pose Exntended (LSPe) Dataset download/process functions.
"""


from dbcollection.datasets.dbclass import BaseDataset
from .keypoints import Keypoints


class LSPe(BaseDataset):
    """ Leeds Sports Pose Extended (LSPe) Dataset preprocessing/downloading functions """

    # download url
    url = ["http://www.comp.leeds.ac.uk/mat4saj/lsp_dataset.zip",
           "http://www.comp.leeds.ac.uk/mat4saj/lspet_dataset.zip"]

    md5_checksum = ''

    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['image_processing', 'detection', 'human pose', 'keypoints']

    # init tasks
    tasks = {
        "keypoints": Keypoints
    }
    default_task = 'keypoints'