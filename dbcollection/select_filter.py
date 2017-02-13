"""
Select data from the metadata file.

Whenever an user requires to select only a set of the available data
from a specific task, it can use the selection property in the load()
API.

This enables the user to select, for example, only a specific set of
classes from the available class list. The resulting metadata removes
all data objects that do not contain the specified set of classes
automatically.
"""


def match_vals(val1, val2, condition):
    """
    Match values w.r.t. an input condition.
    """
    if condition == 'eq':
        return val1 == val2
    elif condition == 'ne':
        return val1 != val2
    elif condition == 'lt':
        return val1 < val2
    elif condition == 'le':
        return val1 <= val2
    elif condition == 'gt':
        return val1 > val2
    elif condition == 'ge':
        return val1 >= val2
    else:
        raise SyntaxError('Invalid condition: {}'.format(condition))


def generate_index_list(handler, val, operation, is_select, chunk_size=1000):
    """
    Generate a list of indexes.
    """
    # intialize list + counter
    keep = []
    counter = 0

    # cycle all data values
    for idx in range(0, handler.shape[0]):
        field_val = handler[idx]

        # fill the list
        if match_vals(field_val, val, operation):
            if is_select:
                keep.append(idx)
                counter += 1
        else:
            if not is_select:
                keep.append(idx)
                counter += 1

        # check if the list is filled with enough data
        if counter % chunk_size == 0:
            yield keep
            keep = []
            counter = 0

    # check if the list still has any values inside
    if any(keep):
        yield keep


def generate_index_list_objects(handler, field_name, field_pos, indexes, chunk_size=1000):
    """
    Generate a list of indexes to keep from 'object_id'
    """
    # set a handler for 'object_id' and field_name
    handler_object = handler['object_id']
    handler_field = handler[field_name]

    # intialize a list + counter
    keep = []
    counter = 0

    # cycle all objects
    for idx in range(0, handler_object.shape[0]):
        # list of ids of a single object entry
        object_id_list = handler_object[idx, :]

        # object_id's field index value
        field_id = object_id_list[field_pos] - 1

        # check if the id exists in the index list
        if field_id in indexes.keys():
            keep.append(idx)
            counter += 1

        if counter % chunk_size == 0:
            yield keep
            keep = []
            counter = 0

    # check if the list still has any values inside
    if any(keep):
        yield keep


def setup_new_field(handler, field_name):
    """
    Create a new field in the hdf5 file.
    """
    new_field_name =  '_temporary_name_' + field_name

    dset = handler.create_dataset(
        new_field_name,
        shape=([0 for i in range(0, handler[field_name].ndim)]),
        maxshape=handler[field_name].shape,
        chunks=True,
        dtype=handler[field_name].dtype
    )

    return dset, new_field_name


def write_hdf5_selected_indexes(handler_temp, handler, list_idx):
    """
    Write chunks of data into the new field.
    """

    used_indexes = {}

    data_size = 0
    for chunk in list_idx:
        size_chunk = len(chunk)

        # resize the dataset to accommodate the next chunk of cols
        handler_temp.resize(data_size + size_chunk, axis=0)

        # copy the new values to the temp data field
        for i in range(0, size_chunk):
            handler_temp[data_size + i, :] = handler[chunk[i], :]
            used_indexes[chunk[i]] = 1

        # increment size
        data_size = data_size + size_chunk

    # Output a table with all the used to be used to discard data
    # from the 'object_id' field
    return used_indexes


def filter_data(handler, field_name, val, operation, is_select):
    """
    Filter/keep indexes in a data field.
    """
    # set a handler to the field
    handler_field = handler[field_name]

    # get a generator of the matched list
    gen_list = generate_index_list(handler_field, val, operation, is_select)

    # create new temporary field and store only the wanted indexes
    handler_temp, new_field_name = setup_new_field(handler, field_name)
    used_indexes = write_hdf5_selected_indexes(handler_temp, handler_field, gen_list)

    # delete old field
    del handler[field_name]

    # create the field again and assign the temp handler's data
    handler.create_dataset(field_name, data=handler_temp.value, chunk=True)

    # remove the temporary handler
    del handler[new_field_name]

    return used_indexes


def remove_unused_indexes(handler, field_name, field_pos, indexes):
    """
    Remove any object_id that has removed indexes from the field_name.
    """
    # set a handler to the 'object_id' field
    handler_field = handler['object_id']

    # craft a generator of chunks of 'object_id' indexes to copy
    gen_list = generate_index_list_objects(handler, field_name, field_pos, indexes)

    # create new temporary field and store only the wanted indexes
    handler_temp, new_field_name = setup_new_field(handler['object_id'], 'object_id')
    write_hdf5_selected_indexes(handler_temp, handler_field, gen_list)

    # delete old field
    del handler['object_id']

    # create the field again and assign the temp handler's data
    handler.create_dataset('object_id', data=handler_temp.value, chunk=True)

    # remove the temporary handler
    del handler[new_field_name]


def field_data_filter(handler, field_name, field_pos, conditions, is_select):
    """
    Select values from a field.
    """
    main_indexes = []
    for condition in conditions:
        val = condition[0]
        operation = condition[1]

        # cycle all sets of the dataset
        for set_name in handler.keys():

            # fetch a data handler for the set
            hdf5_set = handler[set_name]

            # filter field data w.r.t. the input conditions
            used_indexes = filter_data(hdf5_set, field_name, val, operation, is_select)
            indexes = get_filter_indexes(hdf5_set, field_name, val, operation, is_select)

            # merge the resulting index list to the main list
            main_indexes = sorted(main_indexes + list(set(indexes) - set(main_indexes)))

    # filter object_id that contain different ids comparing with the input field
    remove_unused_indexes(hdf5_set, field_name, field_pos, main_indexes)
