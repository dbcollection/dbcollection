"""
Inria Pedestrian Dataset download/process functions.
"""


from dbcollection.datasets import BaseDataset
from .detection import Detection

url_path = 'http://www.vision.caltech.edu.s3-us-west-2.amazonaws.com/'
urls = (
    url_path + 'Image_Datasets/CaltechPedestrians/datasets/INRIA/set00.tar',
    url_path + 'Image_Datasets/CaltechPedestrians/datasets/INRIA/set01.tar',
    url_path + 'Image_Datasets/CaltechPedestrians/datasets/INRIA/annotations.zip',
)
keywords = ('image_processing', 'detection', 'pedestrian')
tasks = {"detection": Detection}
default_task = 'detection'


class Dataset(BaseDataset):
    """Inria Pedestrian Dataset preprocessing/downloading functions."""
    urls = urls
    keywords = keywords
    tasks = tasks
    default_task = default_task
