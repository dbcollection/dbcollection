"""
COCO Keypoints process functions.
"""


from __future__ import print_function, division
import os
import numpy as np
import h5py

from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list


class Keypoint:
    """ COCO Keypoints preprocessing functions """


    def __init__(self, data_path, cache_path, verbose=True):
        """
        Initialize class.
        """
        self.cache_path = cache_path
        self.data_path = data_path
        self.verbose = verbose


    def process_metadata(self):
        """
        Process metadata and store it in a hdf5 file.
        """

        # load data to memory
        data = self.load_data()

        # create/open hdf5 file with subgroups for train/val/test
        file_name = os.path.join(self.cache_path, 'classification.h5')
        fileh5 = h5py.File(file_name, 'w', version='latest')

        # add data to the **source** group
        for set_name in ['train', 'test']:
            sourceg = fileh5.create_group('source/' + set_name)
            sourceg.create_dataset('images', data=data[set_name]["images"], dtype=np.uint8)
            sourceg.create_dataset('labels', data=data[set_name]["labels"], dtype=np.uint8)

        # add data to the **default** group
        for set_name in ['train', 'test']:
            defaultg = fileh5.create_group('default/' + set_name)
            defaultg.create_dataset('classes', data=data[set_name]["classes"], dtype=np.uint8)
            defaultg.create_dataset('images', data=data[set_name]["images"], dtype=np.uint8)
            defaultg.create_dataset('labels', data=data[set_name]["labels"], dtype=np.uint8)
            defaultg.create_dataset('object_fields', data=data[set_name]["object_fields"], dtype=np.uint8)
            defaultg.create_dataset('object_ids', data=data[set_name]["object_ids"], dtype=np.int32)
            defaultg.create_dataset('list_images_per_class', data=data[set_name]["list_images_per_class"], dtype=np.int32)

        # close file
        fileh5.close()

        # return information of the task + cache file
        return file_name


    def run(self):
        """
        Run task processing.
        """
        return self.process_metadata()