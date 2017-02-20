"""
Select/filter data from the metadata file.

Whenever an user requires to select/filter only a set of the available data
from a specific task, it can use the selection property in the load()
API.

This enables the user to select, for example, only a specific set of
classes from the available class list. The resulting metadata removes
all data objects that do not contain the specified set of classes
automatically.

Also, the user can filter, for example, certain fields like age
or gender from a field automatically by selecting the field values and
the condition which the values should be evaluated.
"""


import numpy as np
from .utils import convert_ascii_to_str


def parse_search_inputs(input_list):
    """
    Parse the input search fields.
    """
    assert len(input_list) > 1, "Select/filter requires at least a field and a value"
    assert isinstance(input_list[0], str), 'needs to be a string'

    if len(input_list) == 2:
        field_name = input_list[0]
        values = input_list[1]
        conditions = 'eq'
    elif len(input_list) == 3:
        field_name = input_list[0]
        values = input_list[1]
        conditions = input_list[2]
    else:
        raise Exception('Too many fields per search: ' + str(len(input_list[i])) + \
                        'It only accepts a maximum of 3 fields.')

    if not isinstance(values, list):
        values = [values]

    if not isinstance(conditions, list):
        conditions = [conditions]

    assert len(values) == len(conditions), 'List size mismatch: {} ! = {}'\
                                           .format(len(values), len(conditions))

    return field_name, values, conditions


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


def get_field_value(handler_field, idx):
    """
    Return the value of a field by its id.
    """
    val = handler_field[idx, :]
    # check if the field is a str
    if val.dtype == np.uint8:
        # convert values to a string
        return convert_ascii_to_str(val)
    else:
        return val


def merge_lists(listA, listB):
    """
    Merge two lists and return a sorted list with unique values.
    """
    if len(listA)>0:
        return sorted(listA + list(set(listB) - set(listA)))
    else:
        return listB


def get_idx_list_filter(hdf5_set, field_name, field_pos, values, conditions):
    """
    Select/discard indexes w.r.t. the input condition(s).

    Returns a list of object and field indexes to keep.
    """
    # initialize list
    keep_object = []
    keep_field = []

    # set a handler to the field
    handler_object = hdf5_set['object_id']

    # cycle all object_ids
    for idx in range(0, handler_object.shape[0]):

        obj = handler_object[idx, :]

        # fetch field value using the id
        field_val = get_field_value(hdf5_set[field_name], obj[field_pos]-1)

        # match values
        for i in range(0, len(values)):
            val = values[i]
            condition = conditions[i]

            if match_vals(field_val, val, condition):
                keep_object.append(idx)
                keep_field.append(obj[field_pos] - 1)
                break

    return keep_object, list(set(keep_field))


def setup_new_field(handler, field_name):
    """
    Create a new field in the hdf5 file.
    """
    new_field_name =  '_temporary_name_' + field_name

    shape = list(handler[field_name].shape)
    shape[0]=0
    shape = tuple(shape)

    dset = handler.create_dataset(
        new_field_name,
        shape=shape,# ([0 for i in range(0, handler[field_name].ndim)]),
        maxshape=handler[field_name].shape,
        chunks=True,
        dtype=handler[field_name].dtype
    )

    return dset, new_field_name


def filter_lists(listA, listB):
    """
    Remove list B from list A.
    """
    return [x for x in listA if x not in listB]


def write_hdf5_selected_indexes(handler_temp, handler, list_idx, is_select):
    """
    Write chunks of data into the new field.
    """

    used_indexes = {}

    if is_select:
        indexes = list_idx
    else:
        indexes = filter_lists(list(range(0, handler.shape[0])), list_idx)

    size_list = len(indexes)
    handler_temp.resize(size_list, axis=0)

    # copy the new values to the temp data field
    for i in range(0, size_list):
        handler_temp[i, :] = handler[indexes[i], :]


def clean_unused_indexes(hdf5_set, field_dict, is_select):
    """
    Remove ids that are not used anymore.
    """
    for field_name in field_dict.keys():
        # fetch data from the dictionary for the current 'field_name'
        handler_field = hdf5_set[field_name]
        indexes_list = field_dict[field_name]

        handler_temp, new_field_name = setup_new_field(hdf5_set, field_name)
        write_hdf5_selected_indexes(handler_temp, handler_field, indexes_list, is_select)

        # delete old field
        del hdf5_set[field_name]

        # create the field again and assign the temp handler's data
        hdf5_set.create_dataset(field_name, data=handler_temp.value, chunks=True)

        # remove the temporary handler
        del hdf5_set[new_field_name]


def filter_data(hdf5_set, searches, is_select):
    """
    Select/discard data of a set w.r.t. input selections.
    """
    object_fields = convert_ascii_to_str(hdf5_set['object_fields'].value)

    # check if searches is a list of lists
    if isinstance(searches, list):
        if not isinstance(searches[0], list):
            searches = [searches]
    else:
        raise Exception('Input should be a list of lists.')

    keep = {}
    for i in range(0, len(searches)):

        # get inputs
        field_name, values, conditions = parse_search_inputs(searches[i])
        field_pos = object_fields.index(field_name)

        # fetch indexes that match the condition criteria
        obj_ids, field_ids = get_idx_list_filter(hdf5_set, field_name, field_pos, values, conditions)

        # update 'field_name' index list
        try:
            keep[field_name] = merge_lists(keep[field_name], field_ids)
        except KeyError:
            keep[field_name] = field_ids

        # update 'object_id' index list
        try:
            keep['object_id'] = merge_lists(keep['object_id'], obj_ids)
        except KeyError:
            keep['object_id'] = obj_ids

    # remove all unused entries
    clean_unused_indexes(hdf5_set, keep, is_select)
