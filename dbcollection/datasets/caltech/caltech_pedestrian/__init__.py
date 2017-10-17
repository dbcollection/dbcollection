"""
Caltech Pedestrian Dataset download/process functions.
"""


from dbcollection.datasets import BaseDataset
from .detection import Detection, Detection10x, Detection30x

url_path = 'http://www.vision.caltech.edu.s3-us-west-2.amazonaws.com/'
urls = (
    url_path + 'Image_Datasets/CaltechPedestrians/datasets/USA/set00.tar',
    url_path + 'Image_Datasets/CaltechPedestrians/datasets/USA/set01.tar',
    url_path + 'Image_Datasets/CaltechPedestrians/datasets/USA/set02.tar',
    url_path + 'Image_Datasets/CaltechPedestrians/datasets/USA/set03.tar',
    url_path + 'Image_Datasets/CaltechPedestrians/datasets/USA/set04.tar',
    url_path + 'Image_Datasets/CaltechPedestrians/datasets/USA/set05.tar',
    url_path + 'Image_Datasets/CaltechPedestrians/datasets/USA/set06.tar',
    url_path + 'Image_Datasets/CaltechPedestrians/datasets/USA/set07.tar',
    url_path + 'Image_Datasets/CaltechPedestrians/datasets/USA/set08.tar',
    url_path + 'Image_Datasets/CaltechPedestrians/datasets/USA/set09.tar',
    url_path + 'Image_Datasets/CaltechPedestrians/datasets/USA/set10.tar',
    url_path + 'Image_Datasets/CaltechPedestrians/datasets/USA/annotations.zip',
)
keywords = ('image_processing', 'detection', 'pedestrian')
tasks = {
    "detection": Detection,
    "detection_10x": Detection10x,
    "detection_30x": Detection30x,
}
default_task = 'detection'


class Dataset(BaseDataset):
    """ Caltech Pedestrian Dataset preprocessing/downloading functions """
    urls = urls
    keywords = keywords
    tasks = tasks
    default_task = default_task
