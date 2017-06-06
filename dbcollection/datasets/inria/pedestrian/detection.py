"""
Inria Pedestrian detection process functions.
"""


from dbcollection.datasets.caltech.pedestrian.detection import Detection as CaltechDetection


class Detection(CaltechDetection):
    """ Inria Pedestrian detection preprocessing functions """

    # metadata filename
    filename_h5 = 'detection'

    skip_step = 1

    classes = ['person', 'person-fa', 'people', 'person?']

    sets = {
        "train" : ['set00'],
        "test" : ['set01']
    }


class DetectionNoSourceGrp(Detection):
    """ Inria Pedestrian detection (default grp only - no source group) task class """

    # metadata filename
    filename_h5 = 'keypoint_d'

    def add_data_to_source(self, handler, data):
        """
        Dummy method
        """
        # do nothing