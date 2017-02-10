"""
Functions to create lists of organized objects by field.

The user can easily create lookup lists for any number of existing data fields
that compose the set of data of a dataset. By simply selecting a field, the
organize list property creates lists of objects indexes for each field's id.

For example, creating a list of objects belonging only to a specific class is
simply a matter of selecting the 'field_name' of the classes and it will
automatically link all object_ids that contain that each specific id of the
class field.
"""


import numpy as np


def list_chunks(handler, field_name, field_pos, num_objects, chunk_size=1000):

    list_id = {}

    # cycle all object_ids in order and fill the temporary dictionary
    for idx in range(0, num_objects):
        # list of ids of a single object entry
        object_id_list = handler['object_id'][idx, :]

        # object_id's field index value
        field_id = object_id_list[field_pos] - 1

        # add to the table
        try:
            list_id[field_id].append(idx+1)
        except KeyError:
            list_id[field_id] = [idx+1]

        # check if the counter is equal to chunk_size
        if (idx+1) % chunk_size == 0:
            yield list_id
            list_id = {} # reset list

    # check if the dictionary still has any values inside
    if any(list_id):
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


def update_field_list_size(field_dict, chunk_dict):
    """
    Update each element size with the new data from the chuck_dict.
    """
    max_size = 0
    for key in chunk_dict.keys():
        field_dict[key] += len(chunk_dict[key])
        max_size = max(max_size, field_dict[key])
    return max_size


def write_chunks_to_field(handler, chunk_list):
    """
    Update the metadata file with the new data.
    """
    for key in chunk_list.keys():
        # get last idx with data (i.e., != 0)
        idx_min = handler[key, :].argmin(axis=0)
        for i, val in enumerate(chunk_list[key]):
            handler[key, idx_min+i] = val


def setup_new_field(handler, list_field_name, num_objects, size_field):
    """
    Create a new field in the hdf5 file.
    """
    # config the new list field
    if num_objects < 4e9:
        dtype = np.int32
    else:
        dtype = np.int64

    dset = handler.create_dataset(
        list_field_name,
        shape=(size_field, 0),
        maxshape=(size_field, num_objects),
        chunks=True,
        dtype=dtype
    )

    return dset, generate_dict_with_zeros(size_field)


def create_list_store_to_hdf5(handler, field_name, field_pos):
    """
    Write chunks to the hdf5 metadata file.
    """
    # craft the new field name
    list_field_name = 'list_' + field_name

    # cycle all sets of the dataset
    for set_name in handler.keys():
        # fetch a data handler for the set
        hdf5_set = handler[set_name]

        # get total size of the 'object_id' list
        num_objects = hdf5_set['object_id'].shape[0]
        size_field = hdf5_set[field_name].shape[0]

        # create a generator of data indexes
        gen = list_chunks(hdf5_set, field_name, field_pos, num_objects)

        # setup the new list field
        dset, field_list_size = setup_new_field(hdf5_set, list_field_name, num_objects, size_field)

        # initialize maximum size of the new field (axis=1)
        curr_max_size = 0

        # add the rest of the chunks
        for chunk_dict in gen:

            # check the max size of row of the chunk list
            new_max_size = update_field_list_size(field_list_size, chunk_dict)

            # check if the id of the max
            if new_max_size > curr_max_size:
                # resize the dataset to accommodate the next chunk of rows
                dset.resize(new_max_size, axis=1)
                # update the new max size
                curr_max_size = new_max_size

            # write the next chunk
            write_chunks_to_field(dset, chunk_dict)
