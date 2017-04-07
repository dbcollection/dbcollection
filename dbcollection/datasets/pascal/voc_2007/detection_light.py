"""
Pascal VOC 2007 object detection (light) processing functions.
"""


from __future__ import print_function, division
import os
import h5py
from .detection import Detection


class DetectionLight(Detection):
    """ Pascal VOC 2007 object detection (light - no source) task class """

    def process_metadata(self):
        """
        Process metadata for the  and store it in a hdf5 file.
        """
        # create/open hdf5 file with subgroups for train/val/test
        file_name = os.path.join(self.cache_path, 'detection_light.h5')
        fileh5 = h5py.File(file_name, 'w', version='latest')

        # setup data generator
        data_gen = self.load_data()

        for data in data_gen:
            for set_name in data:

                # add data to the **default** group
                defaultg = fileh5.create_group('default/' + set_name)
                self.add_data_to_default(defaultg, data[set_name])

        # close file
        fileh5.close()

        # return information of the task + cache file
        return file_name
