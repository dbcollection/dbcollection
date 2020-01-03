"""
Methods for parsing data from columns to the original format.

Data types available:

- filename
- string
- number
- boolean
- array
- list[string]
- list[number]
- list[boolean]
- list[list[number]]
"""


import os
import numpy as np
from dbcollection.core.exceptions import TypeFormatError
from dbcollection.utils.pad import unpad_list, unsqueeze_list
from dbcollection.utils.string_ascii import convert_ascii_to_str


def parse_data_format_by_type(data, ctype, path=None, pad_value=-1):
    """Converts a ndarray to a data type.

    Parameters
    ----------
    data : np.ndarray
        Input data.
    ctype : str
        Type format of the data.
    path : str, optional
        Directory path of the file names. If exists, the path is
        concatenated with the parsed string. Default: None.
    pad_value : str | int, optional
        Value used to pad the input data.

    Returns
    -------
    str | int | float | bool | list | ndarray
    """
    if ctype == 'filename':
        data_parsed = parse_filename(data=data, path=path)
    elif ctype == 'string':
        data_parsed = parse_string(data=data)
    elif ctype == 'number':
        data_parsed = parse_number(data=data)
    elif ctype == 'boolean':
        data_parsed = parse_boolean(data=data)
    elif ctype == 'array':
        data_parsed = data
    elif ctype == 'list[string]':
        data_parsed = parse_list_string(data=data)
    elif ctype == 'list[number]':
        data_parsed = parse_list_number(data=data, pad_value=pad_value)
    elif ctype == 'list[boolean]':
        data_parsed = parse_list_boolean(data=data, pad_value=pad_value)
    elif ctype == 'list[list[number]]':
        data_parsed = parse_list_of_lists_number(data=data, pad_value=pad_value)
    else:
        raise TypeFormatError("Invalid data type format: {}".format(ctype))
    return data_parsed


def parse_filename(data, path=None):
    """Converts a ndarray to a string or a list of strings with a
    directory path prefixed.

    Parameters
    ----------
    data : np.ndarray
        Input data.
    path : str, optional
        Directory path of the file names. If exists, the path is
        concatenated with the parsed string. Default: None.

    Returns
    -------
    str | list
    """
    data_parsed = parse_string(data)
    if path:
        if isinstance(data_parsed, str):
            data_parsed = [data_parsed]
        data_parsed = [_concat_path_filename(path, filename) for filename in data_parsed]
    return _parse_output(data_parsed)


def _parse_output(data):
    if isinstance(data, list):
        if len(data) > 1:
            return data
        else:
            return data[0]
    else:
        return data


def _concat_path_filename(path, filename):
    if filename[0] == '/':
        filename = filename[1:]
    return os.path.join(path, filename)


def parse_string(data):
    """Converts a ndarray to a string.

    Parameters
    ----------
    data : np.ndarray
        Input data.

    Returns
    -------
    str | list
    """
    data_parsed = convert_ascii_to_str(data)
    return _parse_output(data_parsed)


def parse_number(data):
    """Converts a ndarray to a number or list of numbers.

    Parameters
    ----------
    data : np.ndarray
        Input data.

    Returns
    -------
    int | float | list
    """
    data_parsed = data.tolist()
    return _parse_output(data_parsed)


def parse_boolean(data):
    """Converts a ndarray to a boolean or list of booleans.

    Parameters
    ----------
    data : np.ndarray
        Input data.

    Returns
    -------
    bool | list
    """
    assert data.dtype == np.uint8, "Data type is not valid: expected {}, got {}".format(np.uint8, data.dtype)
    data_parsed = [bool(val) for val in data]
    return _parse_output(data_parsed)


def parse_list_string(data, pad_value=''):
    """Converts a padded ndarray to a list of lists of strings.

    Parameters
    ----------
    data : np.ndarray
        Input data.

    Returns
    -------
    list
    """
    data_parsed = [convert_ascii_to_str(data_) for data_ in data]
    data_unpad = [unpad_list(l, val=pad_value) for l in data_parsed]
    return _parse_output(data_unpad)


def parse_list_number(data, pad_value=-1):
    """Converts a padded ndarray to a list of lists of numbers.

    Parameters
    ----------
    data : np.ndarray
        Input data.

    Returns
    -------
    list
    """
    return unpad_list(data.tolist(), val=pad_value)


def parse_list_boolean(data, pad_value=-1):
    """Converts a padded ndarray to a list of lists of booleans.

    Parameters
    ----------
    data : np.ndarray
        Input data.

    Returns
    -------
    list
    """
    data_unpad = unpad_list(data.tolist(), val=pad_value)
    return [[bool(value) for value in l] for l in data_unpad]


def parse_list_of_lists_number(data, pad_value=-1):
    """Converts a padded ndarray to a list of lists of lists
    of numbers.

    Parameters
    ----------
    data : np.ndarray
        Input data.

    Returns
    -------
    list
    """
    return [unsqueeze_list(l, val=pad_value) for l in data.tolist()]
