"""
UCF101-Action recognition download/process functions.
"""


from dbcollection.datasets import BaseDataset
from .recognition import Recognition

urls = (
    'http://crcv.ucf.edu/data/UCF101/UCF101.rar',
    'http://crcv.ucf.edu/data/UCF101/UCF101TrainTestSplits-RecognitionTask.zip',
    'http://crcv.ucf.edu/data/UCF101/UCF101TrainTestSplits-DetectionTask.zip',
)
keywords = ('image_processing', 'recognition', 'activity', 'human', 'single_person')
tasks = {"recognition": Recognition}
default_task = 'recognition'


class Dataset(BaseDataset):
    """UCF101-Action recognition preprocessing/downloading functions."""
    urls = urls
    keywords = keywords
    tasks = tasks
    default_task = default_task
