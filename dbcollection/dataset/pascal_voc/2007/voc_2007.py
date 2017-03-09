"""
Pascal VOC 2007 download/process functions.
"""


from __future__ import print_function, division
from .... import utils

from .detection import DetectionTask


class PascalVOC2007:
    """ Pascal VOC 2007 preprocessing/downloading class """

    # download url
    url = [
        'http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar',
        'http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar',
    ]
    md5_checksum = []

    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['image_processing', 'object_detection']

    # object classes
    classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car',  \
              'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike',\
              'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']


    def __init__(self, data_path, cache_path, verbose=True):
        """
        Initialize class.
        """
        self.cache_path = cache_path
        self.data_path = data_path
        self.verbose = verbose


    def download(self, is_download=True):
        """
        Download and extract files to disk.
        """
        # download + extract data and remove temporary files
        if is_download:
            utils.download_extract_all(self.url, self.md5_checksum, self.data_path, False, self.verbose)

        return self.keywords


    def process(self):
        """
        Process metadata for all tasks
        """
        # init tasks
        tasks = {
            "detection": DetectionTask(self.data_path, self.cache_path, self.verbose)
        }

        # process all tasks
        info_output = {}
        for task in tasks:
            if self.verbose:
                print('Processing <{}> task:\n'.format(task))
            info_output[task] = task.run()

        # define a default task
        info_output['default'] = info_output['detection']

        return info_output, self.keywords