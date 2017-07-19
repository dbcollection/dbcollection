"""
UCF101-Action recognition download/process functions.
"""


from dbcollection.datasets.dbclass import BaseDataset
from .recognition import Recognition


class UCF101(BaseDataset):
    """ UCF101-Action recognitio preprocessing/downloading functions """

    # download url
    url = [
        'http://crcv.ucf.edu/data/UCF101/UCF101.rar',
        'http://crcv.ucf.edu/data/UCF101/UCF101TrainTestSplits-RecognitionTask.zip',
        'http://crcv.ucf.edu/data/UCF101/UCF101TrainTestSplits-DetectionTask.zip'
    ]
    md5_checksum = ''

    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['image_processing', 'recognition',
                'activity', 'human', 'single person']

    # init tasks
    tasks = {
        "recognition": Recognition
    }
    default_task = 'recognition'