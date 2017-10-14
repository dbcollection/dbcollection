"""
hdf5 utility functions.
"""


import numpy as np


def hdf5_write_data(h5_handler, field_name, data, dtype=None, chunks=True,
                    compression="gzip", compression_opts=4, fillvalue=-1):
    """Write/store data into a hdf5 file.

    Parameters
    ----------
    h5_handler : h5py._hl.group.Group
        Handler for an HDF5 group object.
    field_name : str
        Field name.
    data : np.ndarray
        Data array.
    dtype : np.dtype, optional
        Data type.
    chunks : bool, optional
        Store data as chunks if True.
    compression : str, optional
        Compression algorithm type.
    compression_opts : int, optional
        Compression option (range: [1,10])
    fillvalue : int/float, optional
        Value to pad the data.

    Returns
    -------
    h5py._hl.dataset.Dataset
        Handler for an HDF5 dataset object.
    """
    assert h5_handler, "Must input a hdf5 file handler"
    assert field_name, 'Must input a field name.'
    assert isinstance(data, np.ndarray), 'Data must be a numpy array.'

    if dtype is None:
        dtype = data.dtype

    h5_field = h5_handler.create_dataset(name=field_name,
                                         data=data,
                                         shape=data.shape,
                                         dtype=dtype,
                                         chunks=chunks,
                                         compression=compression,
                                         compression_opts=compression_opts,
                                         fillvalue=fillvalue)
    return h5_field
