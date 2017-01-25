__all__ = ['image_processing']

import os
from . import *


#---------------------------------------------------------
# Lists
#---------------------------------------------------------


# store ALL lists here

image_processing_list = {
    "cifar10": image_processing.cifar.cifar10,
    "cifar100": image_processing.cifar.cifar100,
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
        for dname in category.keys():
            if dname == name:
                return category.name, name
    
    raise 


def process(name, data_path, cache_path, download, verbose):
    """
    Download/process data of a dataset.
    """

    # fetch dataset constructor
    constructor = fetch_dataset_constructor(name)
    dataset_loader = constructor(data_path, cache_path, verbose, clean_cache)

    # check if data already exists in disk
    if not os.path.exists(dir_name):
        # download data
        dataset_loader.download()

    # process metadata
    cache_info = dataset_loader.process()

    return cache_info
