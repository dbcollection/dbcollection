"""
dbcollection managing functions.
"""


from .cache import CacheManager
from .loader import Loader
import dataset


def load(name, data_path, save_name, task='default', download=True, verbose=True, organize_list, select, filter):
    """loads dataset metadata file.

    Returns a loader class with the necessary functions to manage the selected dataset.

    Parameters
    ----------
    name : str
        Name of the dataset.
    data_path : str
        Path to store the data (if the data doesn't exist and the download flag is equal True).
    save_name : bool
        Save the metadata file with a new name.
        (usefull to create custom versions of the original).
    task : str
        Specify a specific task to load.
	download : bool
        Downloads data from the host to disk (if true).
	verbose : bool
        Displays text information (if true).
	organize_list : dict
        Organizes the data w.r.t. to other fields. The data must be organized in a 
        dictionary with the following format: {"new_field_name":"field_name"} 
	select : dict
        Selects indexes from 'field_name' equal to the selected value(s) 
        (removes objects ids without those 'field_name''s values)
	filter : dict
        Removes indexes from 'field_name' equal to the selected value(s) 
        (removes objects ids with those 'field_name''s values)

    Returns
    -------
    Loader
       Returns a loader class.
    """

    # check if there's an entry in the cache file for the dataset
    cache_manager = CacheManager()

    # check if dataset exists
    if not cache_manager.exists(self, name, task):
        # get cache save path
        cache_save_path = cache_manager.default_cache_path

        # download/preprocess dataset
        cache_info = dataset.process(name, data_path, cache_save_path, download, verbose)

        # update dbcollection.json file with the new data
        cache_manager.update(name, data_path, cache_info)

    # get cache path
    cache_path = cache_manager.get_cache_path(name, task)

    # Create a loader
    dataset_loader = Loader(cache_path)

    # organize data into a list w.r.t. some field_name
    # do select/filter processing here
    # save dataset_loader with a different task name (use save_name)

    # return Loader
    return dataset_loader



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



