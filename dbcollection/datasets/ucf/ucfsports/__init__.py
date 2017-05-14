"""
UCF-Sports Action recognition download/process functions.
"""


from dbcollection.datasets.dbclass import BaseDataset
from .recognition import Recognition, RecognitionNoSourceGrp
from .detection import Detection, DetectionNoSourceGrp


class UCFSports(BaseDataset):
    """ UCF-Sports action recognition preprocessing/downloading functions """

    # download url
    url = [
        'http://crcv.ucf.edu/data/ucf_sports_actions.zip',
    ]
    md5_checksum = ''

    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['image_processing', 'recognition', 'detection',
                'activity', 'human', 'single person']

    # init tasks
    tasks = {
        "recognition" : Recognition,
        "recognition_d" : RecognitionNoSourceGrp,
        "detection" : Detection,
        "detection_d" : DetectionNoSourceGrp
    }
    default_task = 'recognition'