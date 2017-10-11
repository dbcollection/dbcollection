"""
Inria Pedestrian detection process functions.
"""


from dbcollection.datasets.caltech.caltech_pedestrian.detection import Detection as CaltechDetection


class Detection(CaltechDetection):
    """Inria Pedestrian detection preprocessing functions."""

    # metadata filename
    filename_h5 = 'detection'

    skip_step = 1

    classes = ['person', 'person-fa', 'people', 'person?']

    sets = {
        "train": ['set00'],
        "test": ['set01']
    }
