"""
Cifar10 classification process functions.
"""


from __future__ import print_function, division
import os
import numpy as np

from dbcollection.datasets import BaseTask

from dbcollection.utils.file_load import load_pickle
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list
from dbcollection.utils.hdf5 import hdf5_write_data


class Classification(BaseTask):
    """ Cifar10 Classification preprocessing functions """

    # metadata filename
    filename_h5 = 'classification'

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

    def get_object_list(self, data, labels):
        """
        Groups the data + labels info in a 'list' of indexes.
        """
        # object_id = np.ndarray((data.shape[0], 2), dtype=np.uint16)
        object_id = np.ndarray((data.shape[0], 2), dtype=int)
        for i in range(data.shape[0]):
            object_id[i][0] = i
            object_id[i][1] = labels[i]
        return object_id

    def get_class_names(self, path):
        """
        Returns the class names/labels.
        """
        return load_pickle(os.path.join(path, self.data_files[0]))

    def load_data_set(self, is_test):
        """
        Fetch train/test data.
        """
        # merge the path with the extracted folder name
        data_path_ = os.path.join(self.data_path, 'cifar-10-batches-py')

        class_names = self.get_class_names(data_path_)

        # load test data file
        if is_test:
            batch = load_pickle(os.path.join(data_path_, self.data_files[6]))
            data = batch['data'].reshape(10000, 3, 32, 32)
            labels = np.array(batch['labels'], dtype=np.uint8)
        else:
            batch1 = load_pickle(os.path.join(data_path_, self.data_files[1]))
            batch2 = load_pickle(os.path.join(data_path_, self.data_files[2]))
            batch3 = load_pickle(os.path.join(data_path_, self.data_files[3]))
            batch4 = load_pickle(os.path.join(data_path_, self.data_files[4]))
            batch5 = load_pickle(os.path.join(data_path_, self.data_files[5]))

            # concatenate data
            data = np.concatenate(
                (
                    batch1['data'],
                    batch2['data'],
                    batch3['data'],
                    batch4['data'],
                    batch5['data']
                ),
                axis=0,
            )
            data = data.reshape((50000, 3, 32, 32))

            labels = np.concatenate(
                (
                    batch1['labels'],
                    batch2['labels'],
                    batch3['labels'],
                    batch4['labels'],
                    batch5['labels']
                ),
                axis=0,
            )

        data = np.transpose(data, (0, 2, 3, 1))  # NxHxWxC
        object_list = self.get_object_list(data, labels)

        # organize list of image indexes per class
        images_per_class = []
        unique_labels = np.unique(labels)
        for label in unique_labels:
            images_idx = np.where(labels == label)[0].tolist()
            images_per_class.append(images_idx)

        return {
            "object_fields": str2ascii(['images', 'classes']),
            "class_name": str2ascii(class_names['label_names']),
            "data": data,
            "labels": labels,
            "object_ids": object_list,
            "list_images_per_class": np.array(pad_list(images_per_class, 1), dtype=np.int32)
        }

    def load_data(self):
        """
        Load the data from the files.
        """
        # train set
        yield {"train": self.load_data_set(False)}

        # test set
        yield {"test": self.load_data_set(True)}

    # def add_data_to_source(self, hdf5_handler, data, set_name=None):
    #    """
    #    Store data annotations in a nested tree fashion.
    #
    #    It closely follows the tree structure of the data.
    #    """
    #    hdf5_write_data(hdf5_handler, 'classes', data["class_name"], dtype=np.uint8, fillvalue=0)
    #    hdf5_write_data(hdf5_handler, 'images', data["data"], dtype=np.uint8, fillvalue=-1)
    #    hdf5_write_data(hdf5_handler, 'labels', data["labels"], dtype=np.uint8, fillvalue=1)

    def add_data_to_default(self, hdf5_handler, data, set_name=None):
        """
        Add data of a set to the default group.

        For each field, the data is organized into a single big matrix.
        """
        hdf5_write_data(hdf5_handler, 'classes', data["class_name"], dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'labels', data["labels"], dtype=np.uint8, fillvalue=1)
        hdf5_write_data(hdf5_handler, 'images', data["data"], dtype=np.uint8, fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'object_ids',
                        data["object_ids"], dtype=np.int32, fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'object_fields',
                        data["object_fields"], dtype=np.uint8, fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'list_images_per_class',
                        data["list_images_per_class"], dtype=np.int32, fillvalue=-1)
