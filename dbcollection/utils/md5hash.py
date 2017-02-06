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
    return hashlib.md5(open(fname, 'rb').read()).hexdigest()


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
        None

    Raises
    ------
    Exception

    """
    if not get_hash_value(fname) == md5sum:
        raise Exception('File check sum is invalid.')
