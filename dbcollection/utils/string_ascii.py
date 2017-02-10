"""
String-to-ascii and ascii-to-string convertion functions.
"""


import numpy as np


def str_to_ascii(input_str):
    """Convert string to ascii numpy array.

    Converts a single string of characters into a numpy array
    coded as ascii.

    Parameters
    ----------
    input_str : str
        String data.

    Returns
    -------
    numpy.uint8
       Single numpy array.

    Raises
    ------
        None
    """
    return np.array([ord(c) for c in input_str], dtype=np.uint8)


def ascii_to_str(input_array):
    """Convert ascii numpy array to a string.

    Parameters
    ----------
    input_array : numpy.array
        Input array vector (should be of type dtype=numpy.uint8)

    Returns
    -------
    str
       Single string.

    Raises
    ------
        None
    """
    return "".join([chr(item) for item in input_array])


def convert_str_to_ascii(inp_str):
    """Convert a list of strings into a numpy array (uint8).

    Converts a string or list of strings to a numpy array. The array size is
    defined by the size of string plus one. This is needed for ascii to str
    convertion in lua using ffi.string() which expects a 0 at the end of an
    array.

    If a list of strings is used, the size of the array is defined by the size
    of the longest string (plus one), and zero padded to maitain the array
    shape.

    Parameters
    ----------
    inp_str : str/list
        String or list of strings to convert to an ascii array.

    Returns
    -------
    numpy.uint8
        Array containing all strings converted to numpy arrays in ascii format.

    Raises
    ------
        None
    """
    # check if list
    if not isinstance(inp_str, list):
        inp_str = [inp_str]

    # get max size of the list strings
    max_size = max([len(a) for a in inp_str])

    # allocate array
    ascii_array = np.zeros([len(inp_str), max_size+1], dtype=np.uint8)

    # iteratively copy data to the array
    for i, val in enumerate(inp_str):
        ascii_array[i, :len(val)] = str_to_ascii(val)

    if len(inp_str) > 1:
        return ascii_array
    else:
        return ascii_array[0]


def convert_ascii_to_str(input_array):
    """Convert a numpy array to a string (or a list of strings)

    Parameters
    ----------
    input_array : numpy.uint8
        Numpy array in ascii format.

    Returns
    -------
    str/list
        String or list of strings.

    Raises
    ------
        None
    """
    list_str = input_array.tolist()
    if input_array.ndim > 1:
        return [ascii_to_str(list(filter(lambda x: x > 0, str_))) for str_ in list_str]
    else:
        return ascii_to_str(list(filter(lambda x: x > 0, list_str)))
