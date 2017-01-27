__all__ = ['image_processing']

import os
from . import *
#import .image_processing
#from .image_processing import *


#---------------------------------------------------------
# Lists - store ALL lists here
#---------------------------------------------------------

image_processing_list = {
    "cifar10": image_processing.cifar.cifar10.Cifar10,
    #"cifar100": image_processing.cifar.cifar100.Cifar100,
}

# *** MAIN list ***
dataset_list = {
    "image_processing": image_processing_list
}



#---------------------------------------------------------
# Functions
#---------------------------------------------------------

def fetch_dataset_constructor(name):
    """
    Fetches a dataset constructor class.
    """
    for category in dataset_list.keys():
        for dname in dataset_list[category].keys():
            if dname == name:
                return category, dataset_list[category][name]

    raise Exception('Undefined dataset name: '+str(name))


def process(name, data_path, cache_path, download, verbose):
    """
    Download/process data of a dataset.
    """
    # fetch dataset constructor
    category, constructor = fetch_dataset_constructor(name)

    # merge paths with the name+category
    data_path_ = os.path.join(data_path, name)
    cache_path_ = os.path.join(cache_path, category, name)

    # setup dataset constructor
    dataset_loader = constructor(data_path_, cache_path_, verbose)

    # check if the directories exist already
    if not os.path.exists(data_path_):
        os.makedirs(data_path_)
    if not os.path.exists(cache_path_):
        os.makedirs(cache_path_)

    # download data
    dataset_loader.download()

    # process metadata
    cache_info = dataset_loader.process()

    # return some info to update the cache file
    return cache_info, category
