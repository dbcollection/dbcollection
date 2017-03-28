"""
Padding functions.
"""

def pad_list(listA, val=0):
    """Pad list of lists with 'val' shuch that all lists have the same length.

    Parameters
    ----------
    listA : list of lists
        List of lists of different sizes.
    val : number
        Value to pad the lists.

    Returns
    -------
    list of lists
        A list of lists with the same same.

    Raises
    ------
        None
    """
    # pad list with zeros in order to have all lists of the same size
    assert isinstance(listA, list), 'Input must be a list. Got {}, espected {}' \
                                    .format(type(listA), type(list))

    # get size of the biggest list
    max_size = len(max(listA, key=len))

    # pad all lists with the a padding value
    return [l + [val]*int(max_size-len(l)) for l in listA]

