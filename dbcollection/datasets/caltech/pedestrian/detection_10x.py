"""
Caltech Pedestrian detection (10x data) process functions.
"""

from .detection import Detection


class Detection10x(Detection):
    """ Caltech Pedestrian detection (10x data) preprocessing functions """

    skip_step = 10
    file_name = 'detection_10x.h5'