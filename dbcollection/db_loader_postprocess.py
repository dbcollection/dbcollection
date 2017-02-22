"""
Dataset loader + preprocess functions.
"""

import shutil
from .utils import convert_ascii_to_str

from .loader import DatasetLoader
from .storage import StorageHDF5
from .organize_list import create_list_store_to_hdf5
from .select_filter import filter_data


def select_filter_data_from_dataset(metadata_filename, input_selections, mode):
    """Selects data of the object id list w.r.t. some conditions.

    Parameters
    ----------
    metadata_filename : str
        Metadata file name + path.
    input_selections : list
        Input selection/filter conditions. Format:
        ['field_name', ['value1', 'value2'], ['condition1', 'condition2']]

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # open metadata file
    file = StorageHDF5(metadata_filename, 'r')

    # cycle all sets of the dataset
    for set_name in file.storage.keys():
        filter_data(file.storage[set_name], input_selections, mode)

    # close metadata file
    file.close()


def make_lists_from_fields(metadata_filename, field_list):
    """Organize object_ids by fields.

    Creates a list w.r.t. a data field and organizes all 'object_id' indexes
    for each unique value of the data field.

    Parameters
    ----------
        None

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # open metadata file
    file = StorageHDF5(metadata_filename, 'r')

    # create a new metadata file to store the new variable(s)
    for set_name in file.storage.keys():
        object_fields = convert_ascii_to_str(file.storage[set_name]['object_fields'].value)
        for field_name in field_list:
            field_pos = object_fields.index(field_name)
            create_list_store_to_hdf5(file.storage[set_name], field_name, field_pos)

    # close metadata file
    file.close()


def balance_sets_dataset(metadata_filename, set_opts):
    """Balances data sets.

    Parameters
    ----------
        None

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # open metadata file
    file = StorageHDF5(metadata_filename, 'r')

    # close metadata file
    file.close()


def fetch_dataset_loader(name, task, data_dir, task_cache_path, new_task_cache_path,\
                         select_data, filter_data, organize_list, balance_sets, verbose):
    """Constructs a dataset loader object for a specific task of a dataset.

    Parameters
    ----------
    name : str
        Name of the dataset.
    data_dir : str
        Path to store the data (if the data doesn't exist and the download flag is equal True).
    save_name : str
        Save a custom task with a specified name.
        (usefull to create custom versions of the original).
    task : str
        Specify a specific task to load.
	organize_list : dict
        Organizes the data w.r.t. to other fields. The data must be organized in a
        dictionary with the following format: {"new_field_name":"field_name"}
	select_data : dict
        Selects indexes from 'field_name' equal to the selected value(s)
        (removes objects ids without those 'field_name''s values)
	filter_data : dict
        Removes indexes from 'field_name' equal to the selected value(s)
        (removes objects ids with those 'field_name''s values)
    verbose : bool
        Displays text information (if true).

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # make a copy of the target task metadata file
    # and rename the new copy
    shutil.copy2(task_cache_path, new_task_cache_path)

    # do select processing
    if select_data:
        if verbose:
            print('Select data from fields: ')
            print(select_data)
        select_filter_data_from_dataset(new_task_cache_path, select_data, True)

    # do filter processing
    if filter_data:
        if verbose:
            print('Filter data from fields: ')
            print(filter_data)
        select_filter_data_from_dataset(new_task_cache_path, filter_data, False)

    # organize data into a list w.r.t. some field_name
    if organize_list:
        if verbose:
            print('Organize fields into lists: {}'.format(organize_list))
        make_lists_from_fields(new_task_cache_path, organize_list)

    # do data balancing
    if balance_sets:
        if verbose:
            print('Balance datasets: ')
            print(balance_sets)
        balance_sets_dataset(new_task_cache_path, balance_sets)

    # create a dataset loader object and return it
    return DatasetLoader(name, task, data_dir, new_task_cache_path)
