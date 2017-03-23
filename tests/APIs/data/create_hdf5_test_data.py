"""
Generates a test file emulating some data structure.
"""


import os
import numpy as np
import h5py

from dbcollection.utils.string_ascii import convert_str_to_ascii as toascii

data = {
    "train" : {
        "filenames" : [
            'file1', 'file2', 'file3', 'file4', 'file5',
            'file6', 'file7', 'file8', 'file9', 'file10'
        ],
        "labels" : list(range(1, 11)),
        "data" : [[val, val, val, val] for val in range(1, 11)],
        "object_ids" : [[val, val, val] for val in range(0, 10)],
        "object_fields" : ['filenames', 'labels', 'data']
    },
    "test" : {
        "filenames" : [
            'file10', 'file20', 'file30', 'file40', 'file50',
            'file60', 'file70', 'file80', 'file90', 'file100'
        ],
        "labels" : [i*10 for i in range(1, 11)],
        "data" : [[val*10, val*10, val*10, val*10] for val in range(1, 11)],
        "object_ids" : [[val, val, val] for val in range(0, 10)],
        "object_fields" : ['filenames', 'labels', 'data']
    }
}

# create file
path = os.path.split(os.path.abspath(__file__))[0]
filename = os.path.join(path, 'test_data.h5')

if os.path.exists(filename):
    os.remove(filename)

h5 = h5py.File(filename, 'w', version='latest')

defaultg = h5.create_group('default')

## add data to file
for set_name in data:
    grp = defaultg.create_group(set_name)
    grp.create_dataset("filenames", data=toascii(data[set_name]["filenames"]), dtype=np.uint8)
    grp.create_dataset("labels", data=data[set_name]["labels"], dtype=np.uint8)
    grp.create_dataset("data", data=data[set_name]["data"], dtype=np.uint8)
    grp.create_dataset("object_ids", data=data[set_name]["object_ids"], dtype=np.uint8)
    grp.create_dataset("object_fields", data=toascii(data[set_name]["object_fields"]), dtype=np.uint8)

h5.close()
