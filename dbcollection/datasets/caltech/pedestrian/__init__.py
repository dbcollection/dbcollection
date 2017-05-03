"""
Caltech Pedestrian Dataset download/process functions.
"""


from dbcollection.datasets.dbclass import BaseDataset
from .detection import Detection, Detection10x, Detection30x, DetectionNoSourceGrp, Detection10xNoSourceGrp, Detection30xNoSourceGrp


class Pedestrian(BaseDataset):
    """ Caltech Pedestrian Dataset preprocessing/downloading functions """

    # download url
    url = ['http://www.vision.caltech.edu.s3-us-west-2.amazonaws.com/Image_Datasets/CaltechPedestrians/datasets/USA/set00.tar',
           'http://www.vision.caltech.edu.s3-us-west-2.amazonaws.com/Image_Datasets/CaltechPedestrians/datasets/USA/set01.tar',
           'http://www.vision.caltech.edu.s3-us-west-2.amazonaws.com/Image_Datasets/CaltechPedestrians/datasets/USA/set02.tar',
           'http://www.vision.caltech.edu.s3-us-west-2.amazonaws.com/Image_Datasets/CaltechPedestrians/datasets/USA/set03.tar',
           'http://www.vision.caltech.edu.s3-us-west-2.amazonaws.com/Image_Datasets/CaltechPedestrians/datasets/USA/set04.tar',
           'http://www.vision.caltech.edu.s3-us-west-2.amazonaws.com/Image_Datasets/CaltechPedestrians/datasets/USA/set05.tar',
           'http://www.vision.caltech.edu.s3-us-west-2.amazonaws.com/Image_Datasets/CaltechPedestrians/datasets/USA/set06.tar',
           'http://www.vision.caltech.edu.s3-us-west-2.amazonaws.com/Image_Datasets/CaltechPedestrians/datasets/USA/set07.tar',
           'http://www.vision.caltech.edu.s3-us-west-2.amazonaws.com/Image_Datasets/CaltechPedestrians/datasets/USA/set08.tar',
           'http://www.vision.caltech.edu.s3-us-west-2.amazonaws.com/Image_Datasets/CaltechPedestrians/datasets/USA/set09.tar',
           'http://www.vision.caltech.edu.s3-us-west-2.amazonaws.com/Image_Datasets/CaltechPedestrians/datasets/USA/set10.tar',
           'http://www.vision.caltech.edu.s3-us-west-2.amazonaws.com/Image_Datasets/CaltechPedestrians/datasets/USA/annotations.zip']

    md5_checksum = ''

    # some keywords. These are used to classify datasets for easier
    # categorization.
    keywords = ['image_processing', 'detection', 'pedestrian']

    # init tasks
    tasks = {
        "detection" : Detection,
        "detection_10x" : Detection10x,
        "detection_30x" : Detection30x,
        "detection_d" : DetectionNoSourceGrp,
        "detection_10x_d" : Detection10xNoSourceGrp,
        "detection_30x_d" : Detection30xNoSourceGrp
    }
    default_task = 'detection'