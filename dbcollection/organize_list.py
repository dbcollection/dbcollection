"""
Functions to create lists of organized objects by field.
"""


import numpy as np


def list_chuncks(handler, field_name, num_objects, chunck_size):

    list_id = {}
    field_pos = handler.object_field_id(field_name) # <---fix this. (get field id)

    # cycle all object_ids in order and fill the temporary dictionary
    for idx in range(0,num_objects):
        # list of ids of a single object entry
        object_id_list = handler.object(idx)

        # object_id's field index value
        field_id = object_id_list[field_pos]

        # add to the table
        try:
            list_id[field_id].append(idx+1)
        except ValueError:
            list_id[field_id] = [idx+1]

        # check if the counter is equal to chunck_size
        if (idx+1) % chunck_size == 0:
            yield list_id
            list_id = {} # reset list

    yield list_id


def get_dict_max_row_size(dict_table):
    """
    Get the maximum lenght of the elements of a dictionary
    """
    max_size, idkey = 0, 0
    for key in dict_table.keys():
        val = len(dict_table[key])
        if max_size < val:
            max_size = val
            idkey = key
    return max_size, idkey


def generate_dict_with_zeros(size):
    """
    Generate a dictionary filled with zeros.
    """
    d = {}
    for i in range(0, size):
        d[i] = 0
    return d


def update_field_list_size(field_dict, chunck_dict):
    """
    Update each element size with the new data from the chuck_dict.
    """
    max_size = 0
    for key in chunck_dict.keys():
        field_dict[key] += chunck_dict[key]
        max_size = max(max_size, field_dict[key])
    return max_size


def write_chuncks_to_field(handler, chunck_list):
    """
    Update the metadata file with the new data.
    """
    for key in chunck_list.keys():
        # get last idx with data (i.e., != 0)
        idx_min = handler[key, :].argmin(axis=0)
        for i, val in enumerate(chunck_list[key]):
            handler[key, idx_min+i] = val


def create_list_store_to_hdf5(field_name, chunck_size):
    """
    Write chuncks to the hdf5 metadata file.
    """
    # craft the new field name
    list_field_name = 'list_' + field_name

    # cycle all sets of the dataset
    for set_name in self.file.storage.keys():
        # fetch a data handler for the set
        hdf5_set = self.file.storage[set_name]

        # get total size of the 'object_id' list
        num_objects = hdf5_set['object_id'].shape[0]
        size_field = hdf5_set[field_name].shape[0]

        # create a generator of indexes
        gen = list_chuncks(hdf5_set, field_name, chunck_size)

        # config new field
        data = np.zeros()
        maxshape = (size_field,)

        if size_field < 4e9:
            dtype = np.int32
        else:
            dtype = np.int64

        dset = hdf5_set.create_dataset(
            list_field_name,
            shape=(size_field,0),
            maxshape=(None, None),
            chunks=chunck_size,
            dtype=dtype
        )

        # initialize list with zeros
        field_list_size = generate_dict_with_zeros(size_field)
        curr_max_size = 0

        # add the rest of the chuncks
        for chunck_dict in gen:

            # check the max size of row of the chunck list
            new_max_size = update_field_list_size(field_list_size, chunck_dict)

            # check if the id of the max
            if new_max_size > curr_max_size:
                # resize the dataset to accommodate the next chunk of rows
                dset.resize(new_max_size, axis=1)

            # write the next chunk
            write_chuncks_to_field(dset, chunck_dict)
