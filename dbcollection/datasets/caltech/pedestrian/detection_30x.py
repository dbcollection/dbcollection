"""
Caltech Pedestrian detection (30x data) process functions.
"""

from .detection import Detection


class Detection30x(Detection):
    """ Caltech Pedestrian detection (30x data) preprocessing functions """

    skip_step = 1
    file_name = 'detection_30x.h5'