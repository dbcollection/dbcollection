"""
MD5 hash string functions.
"""

import hashlib


def get_hash_value(fname):
    """Retrieve the checksum of a file.

    Parameters
    ----------
    fname : str
        File name + path on disk.

    Returns
    -------
    str
        Checksum string.

    Raises
    ------
        None
    """
    try:
        return hashlib.md5(open(fname, 'rb').read()).hexdigest()
    except (IOError, OSError):
        raise IOError('Error opening file: {}'.format(fname))


def check_file_integrity_md5(fname, md5sum):
    """Check the integrity of a file using md5 hash.

    Parameters
    ----------
    fname : str
        File name + path on disk.
    md5sum : str
        MD5 checksum.

    Returns
    -------
    bool
        Return true if the checksum of the file matches the input checksum. 
        Otherwise, return false

    Raises
    ------
        None
    """
    return get_hash_value(fname) == md5sum
