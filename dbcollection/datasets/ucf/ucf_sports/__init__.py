"""
UCF-Sports Action recognition download/process functions.
"""


from dbcollection.core.db import BaseDataset
from .recognition import Recognition
from .detection import Detection


urls = ('http://crcv.ucf.edu/data/ucf_sports_actions.zip')
keywords = ('image_processing', 'recognition', 'detection',
            'activity', 'human', 'single person')
tasks = {
    "recognition": Recognition,
    "detection": Detection
}
default_task = 'recognition'


class Dataset(BaseDataset):
    """UCF-Sports action recognition preprocessing/downloading functions """
    urls = urls
    keywords = keywords
    tasks = tasks
    default_task = default_task
