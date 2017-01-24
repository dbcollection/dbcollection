#!/usr/bin/env python
# Copyright (C) 2017, Farrajota @ https://github.com/farrajota
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


"""
dbcollection managing functions.
"""


def load(name, data_path, cache_path, save_name, task, download, verbose, make_list, select, filter):
    """
    Returns a loader class with the necessary functions to manage the selected dataset.

    Parameters:
    -----------
        - name: name of the dataset [Type=String]
		- data_path: path to store the data (if the data doesn't exist and the download flag is equal True) [Type=String, (default=data_path_default)]
		- cache_path: path to store the cache metadata (if the cache file doesn't exist and the download flag is equal True) [Type=String, (default=cache_path_default)]
		- save_name: save the metadata file with a new name (usefull to create custom versions of the original) [Type=Boolean]
		- task: specify a specific task to load [Type=String, (default='default')]
		- download: [Type=Boolean, (default=True)]
		- verbose: [Type=Boolean, (default=True)]
		- make_list: organizes the data w.r.t. to other fields. The data must be organized in a dictionary with the following format: {"new_field_name":"field_name"}  [Type=Dictionary]
		- select: selects indexes from 'field_name' equal to the selected value(s) (removes objects ids without those 'field_name''s values) [Type=Dictionary]
		- filter: removes indexes from 'field_name' equal to the selected value(s) (removes objects ids with those 'field_name''s values) [Type=Dictionary]
    """
    pass


def add(name, data_path, cache_path, category, task):
    """
    Adds a custom dataset to the list.

    Parameters:
    -----------
        - name: dataset name [Type=String]
		- data_path: data's folder path on disk [Type=String]
		- cache_path: cache's metadata storage path [Type=String]
		- category: name of the category [Type=String]
		- task: name of the task [Type=String]
    """
    pass


def delete(name, data=False, cache=True):
    """
    Deletes the data of a dataset.

    Parameters:
    -----------
        - name: name of the dataset to delete the data from disk [Type=String]
		- data: flag indicating if the data folder is to be deleted from disk [Type=Boolean, (default=False)]
		- cache: flag indicating if the metadata cache file is to be deleted from disk [Type=Boolean, (default=True)]
    """
    pass


def config(name, fields, default_paths):
    """
    Manually setup the configurations of the cache file dbcollection.json.

    Parameters:
    -----------
        - name: name of the dataset (Type=String)
		- fields: specifies which fields and values to update the dbcollection cache file (Type=Dictionary)
		- default_paths: updates the default cache/data paths (Type=Dictionary)

    """
    pass


def download(name, path):
    """
    Download the data for one (or several) listed dataset(s).

    Parameters:
    -----------
        - cache: force the cache file of the preprocessed data to be deleted for the particular dataset (type=Boolean)
		- data: force the dataset's data files to be deleted for the particular dataset (type=Boolean)
		- name: name of the dataset to reset the cache (Type=String)
    """
    pass


def reset(cache, data, name):
    """
    Resets the data of the dbcollection.json cache file for a specific dataset (it deletes the cache files for this dataset as well, if any).

    Parameters:
    -----------
        - cache: force the cache file of the preprocessed data to be deleted for the particular dataset (type=Boolean)
		- data: force the dataset's data files to be deleted for the particular dataset (type=Boolean)
		- name: name of the dataset to reset the cache (Type=String)
    """
    pass



def query(info, search):
    """
    list all available datasets for download/preprocess. (tenho que pensar melhor sobre este)

    Parameters:
    -----------
        - info:  (Type=List)
		- search: (Type=Dictionary)
    """
    pass



