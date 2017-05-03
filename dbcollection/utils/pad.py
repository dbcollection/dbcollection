"""
Padding functions.
"""


def pad_list(listA, val=-1):
    """Pad list of lists with 'val' such that all lists have the same length.

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


def pad_list2(listA, val=-1):
    """Pad list of lists of lists with 'val' such that all lists have the same length.

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
    max_nrows = max([len(l) for l in listA])
    max_size = max([len(li) for l in listA for li in l])

    # pad all lists with the a padding value
    out = [[] for i in range(len(listA))]
    return [out[i].append(li + [val]*int(max_size-len(li))) for i, l in enumerate(listA) for li in l]


def unpad_list(listA, val=-1):
    """Unpad list of lists with which has values equal to 'val'.

    Parameters
    ----------
    listA : list of lists
        List of lists of equal sizes.
    val : number
        Value to unpad the lists.

    Returns
    -------
    list of lists
        A list of lists without the padding values.

    Raises
    ------
        None
    """
    # pad list with zeros in order to have all lists of the same size
    assert isinstance(listA, list), 'Input must be a list. Got {}, espected {}' \
                                    .format(type(listA), type(list))

    if isinstance(listA[0], list):
        return [list(filter(lambda x: x != val, l)) for i, l in enumerate(listA)]
    else:
        return list(filter(lambda x: x != val, listA))