"""
Caltech Pedestrian Dataset download/process functions.
"""


from dbcollection.datasets import BaseDataset
from .detection import Detection, Detection10x, Detection30x


urls = (
    'http://www.vision.caltech.edu.s3-us-west-2.amazonaws.com/Image_Datasets/CaltechPedestrians/datasets/USA/set00.tar',
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
    'http://www.vision.caltech.edu.s3-us-west-2.amazonaws.com/Image_Datasets/CaltechPedestrians/datasets/USA/annotations.zip'
)
keywords = ('image_processing', 'detection', 'pedestrian')
tasks = {
    "detection" : Detection,
    "detection_10x" : Detection10x,
    "detection_30x" : Detection30x,
}
default_task = 'detection'


class Dataset(BaseDataset):
    """ Caltech Pedestrian Dataset preprocessing/downloading functions """
    urls = urls
    keywords = keywords
    tasks = tasks
    default_task = default_task
