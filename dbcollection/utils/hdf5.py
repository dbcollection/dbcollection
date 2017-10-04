"""
hdf5 utility functions
"""

import numpy as np

def hdf5_store_data(h5_handler, field_name, data, dtype=None, chunks=True,
                    compression="gzip", compression_opts=4, fillvalue=-1):
    """Store data of a variable in a hdf5 file."""
    assert h5_handler, "Must input a hdf5 file handler"
    assert field_name, 'Must input a field name.'
    assert data, 'Must input a data field.'
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
