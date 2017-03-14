"""
Cifar10 classification process functions.
"""


from __future__ import print_function, division
import os
import numpy as np

from dbcollection.utils.storage import StorageHDF5
from dbcollection.utils.file_load import load_pickle
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii


class Classification:
    """ Cifar10 Classification preprocessing functions """

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
            "object_fields": ['data', 'class_name'],
            "class_name": class_names['label_names'],
            "train_data": train_data,
            "train_labels": train_labels,
            "train_object_id_list": train_object_list,
            "test_data": test_data,
            "test_labels": test_labels,
            "test_object_id_list": test_object_list
        }


    def classification_metadata_process(self):
        """
        Process metadata and store it in a hdf5 file.
        """

        # load data to memory
        data = self.load_data()

        # create/open hdf5 file with subgroups for train/val/test
        file_name = os.path.join(self.cache_path, 'classification.h5')
        fileh5 = StorageHDF5(file_name, 'w')

        # add data to the **source** group
        fileh5.add_data('source/train', 'classes', str2ascii(data["class_name"]), np.uint8)
        fileh5.add_data('source/train', 'data', data["train_data"], np.uint8)
        fileh5.add_data('source/train', 'labels', data["train_labels"], np.uint8)

        fileh5.add_data('source/test', 'classes', str2ascii(data["class_name"]), np.uint8)
        fileh5.add_data('source/test', 'data', data["test_data"], np.uint8)
        fileh5.add_data('source/test', 'labels', data["test_labels"], np.uint8)

        # add data to the **default** group
        # write data to the metadata file
        fileh5.add_data('default/train', 'classes', str2ascii(data["class_name"]), np.uint8)
        fileh5.add_data('default/train', 'data', data["train_data"], np.uint8)
        fileh5.add_data('default/train', 'object_ids', data["train_object_id_list"], np.int32)
        # object fields is necessary to identify which fields compose 'object_id'
        fileh5.add_data('default/train', 'object_fields', str2ascii(data['object_fields']), np.uint8)

        fileh5.add_data('default/test', 'classes', str2ascii(data["class_name"]), np.uint8)
        fileh5.add_data('default/test', 'data', data["test_data"], np.uint8)
        fileh5.add_data('default/test', 'object_ids', data["test_object_id_list"], np.int32)
        # object fields is necessary to identify which fields compose 'object_id'
        fileh5.add_data('default/test', 'object_fields', str2ascii(data['object_fields']), np.uint8)

        # close file
        fileh5.close()

        # return information of the task + cache file
        return file_name


    def run(self):
        """
        Run task processing.
        """
        return self.classification_metadata_process()
