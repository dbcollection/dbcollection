"""
UCF-Sports Action recognition download/process functions.
"""


from dbcollection.datasets import BaseDataset
from .recognition import Recognition


urls = ('http://crcv.ucf.edu/data/ucf_sports_actions.zip',)
keywords = ('image_processing', 'recognition', 'detection',
            'activity', 'human', 'single_person')
tasks = {"recognition": Recognition}
default_task = 'recognition'


class Dataset(BaseDataset):
    """UCF-Sports action recognition preprocessing/downloading functions."""
    urls = urls
    keywords = keywords
    tasks = tasks
    default_task = default_task
