"""
COCO Detection 2015 process functions.
"""


import os

from .detection2015 import Detection2015


class Detection2016(Detection2015):
    """ COCO Detection (2015) preprocessing functions """

    # metadata filename
    filename_h5 = 'detection_2016'

    image_dir_path = {
        "train" : 'train2014',
        "val" : 'val2014',
        "test" : 'test2014',
        "test-dev" : "test2015"
    }

    annotation_path = {
        "train" : os.path.join('annotations', 'instances_train2014.json'),
        "val" : os.path.join('annotations', 'instances_val2014.json'),
        "test" : os.path.join('annotations', 'image_info_test2015.json'),
        "test-dev" : os.path.join('annotations', 'image_info_test-dev2015.json')
    }


class Detection2016NoSourceGrp(Detection2016):
    """ COCO Detection (2016) (default grp only - no source group) task class """

    # metadata filename
    filename_h5 = 'detection_2016_d'

    def add_data_to_source(self, handler, data):
        """
        Dummy method
        """
        # do nothing