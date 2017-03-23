"""
UCF101 action recognition process functions.
"""


from __future__ import print_function, division
import os
import numpy as np
import h5py

from dbcollection.utils.file_load import load_pickle
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii


class Recognition:
    """ UCF101 action recognition preprocessing functions """

    # extracted file names
    data_files = [
        "batches.meta",
        "data_batch_1",
        "data_batch_2",
        "data_batch_3",
        "data_batch_4",
        "data_batch_5",
        "test_batch"
    ]


    def __init__(self, data_path, cache_path, verbose=True):
        """
        Initialize class.
        """
        self.cache_path = cache_path
        self.data_path = data_path
        self.verbose = verbose


    def get_object_list(self, data, labels):
        """
        Groups the data + labels info in a 'list' of indexes.
        """
        #object_id = np.ndarray((data.shape[0], 2), dtype=np.uint16)
        object_id = np.ndarray((data.shape[0], 2), dtype=int)
        for i in range(data.shape[0]):
            object_id[i][0] = i
            object_id[i][1] = labels[i]
        return object_id


    def load_data(self):
        """
        Load the data from the files.
        """
        # merge the path with the extracted folder name
        data_path_ = os.path.join(self.data_path, 'cifar-10-batches-py')

        # load classes name file
        class_names = load_pickle(os.path.join(data_path_, self.data_files[0]))

        # load train data files
        train_batch1 = load_pickle(os.path.join(data_path_, self.data_files[1]))
        train_batch2 = load_pickle(os.path.join(data_path_, self.data_files[2]))
        train_batch3 = load_pickle(os.path.join(data_path_, self.data_files[3]))
        train_batch4 = load_pickle(os.path.join(data_path_, self.data_files[4]))
        train_batch5 = load_pickle(os.path.join(data_path_, self.data_files[5]))

        # concatenate data
        train_data = np.concatenate(
            (
                train_batch1['data'],
                train_batch2['data'],
                train_batch3['data'],
                train_batch4['data'],
                train_batch5['data']
            ),
            axis=0
        )

        train_labels = np.concatenate(
            (
                train_batch1['labels'],
                train_batch2['labels'],
                train_batch3['labels'],
                train_batch4['labels'],
                train_batch5['labels']
            ),
            axis=0
        )

        train_data = train_data.reshape((50000, 3, 32, 32))
        train_data = np.transpose(train_data, (0,2,3,1)) # NxHxWxC
        train_object_list = self.get_object_list(train_data, train_labels)

        # load test data file
        test_batch = load_pickle(os.path.join(data_path_, self.data_files[6]))

        test_data = test_batch['data'].reshape(10000, 3, 32, 32)
        test_data = np.transpose(test_data, (0,2,3,1)) # NxHxWxC
        test_labels = np.array(test_batch['labels'], dtype=np.uint8)
        test_object_list = self.get_object_list(test_data, test_labels)

        #return a dictionary
        return {
            "train": {
                "object_fields": str2ascii(['data', 'class_name']),
                "class_name": str2ascii(class_names['label_names']),
                "data": train_data,
                "labels": train_labels,
                "object_ids": train_object_list,
            },
            "test": {
                "object_fields": str2ascii(['data', 'class_name']),
                "class_name": str2ascii(class_names['label_names']),
                "data": test_data,
                "labels": test_labels,
                "object_ids": test_object_list,
            }
        }


    def classification_metadata_process(self):
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
            sourceg.create_dataset('classes', data=data[set_name]["class_name"], dtype=np.uint8)
            sourceg.create_dataset('images', data=data[set_name]["data"], dtype=np.uint8)
            sourceg.create_dataset('labels', data=data[set_name]["labels"], dtype=np.uint8)

        # add data to the **default** group
        for set_name in ['train', 'test']:
            defaultg = fileh5.create_group('default/' + set_name)
            defaultg.create_dataset('classes', data=data[set_name]["class_name"], dtype=np.uint8)
            defaultg.create_dataset('images', data=data[set_name]["data"], dtype=np.uint8)
            defaultg.create_dataset('object_ids', data=data[set_name]["object_ids"], dtype=np.int32)
            defaultg.create_dataset('object_fields', data=data[set_name]["object_fields"], dtype=np.int32)

        # close file
        fileh5.close()

        # return information of the task + cache file
        return file_name


    def run(self):
        """
        Run task processing.
        """
        return self.classification_metadata_process()
