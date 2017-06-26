"""
Cifar10 classification process functions.
"""


from __future__ import print_function, division
import os
import numpy as np

from dbcollection.datasets.dbclass import BaseTask

from dbcollection.utils.file_load import load_pickle
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list


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
        #object_id = np.ndarray((data.shape[0], 2), dtype=np.uint16)
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


    def load_data_train(self):
        """
        Fetch the training data.
        """
        # merge the path with the extracted folder name
        data_path_ = os.path.join(self.data_path, 'cifar-10-batches-py')

        class_names = self.get_class_names(data_path_)

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
        train_data = np.transpose(train_data, (0, 2, 3, 1)) # NxHxWxC
        train_object_list = self.get_object_list(train_data, train_labels)

        # organize list of image indexes per class
        train_images_per_class = []
        labels = np.unique(train_labels)
        for label in labels:
            images_idx = np.where(train_labels == label)[0].tolist()
            train_images_per_class.append(images_idx)

        return {
            "object_fields": str2ascii(['images', 'classes']),
            "class_name": str2ascii(class_names['label_names']),
            "data": train_data,
            "labels": train_labels,
            "object_ids": train_object_list,
            "list_images_per_class": np.array(pad_list(train_images_per_class, 1), dtype=np.int32)
        }


    def load_data_test(self):
        """
        Fetch the testing data.
        """
        # merge the path with the extracted folder name
        data_path_ = os.path.join(self.data_path, 'cifar-10-batches-py')

        class_names = self.get_class_names(data_path_)

        # load test data file
        test_batch = load_pickle(os.path.join(data_path_, self.data_files[6]))

        test_data = test_batch['data'].reshape(10000, 3, 32, 32)
        test_data = np.transpose(test_data, (0, 2, 3, 1)) # NxHxWxC
        test_labels = np.array(test_batch['labels'], dtype=np.uint8)
        test_object_list = self.get_object_list(test_data, test_labels)

        # organize list of image indexes per class
        test_images_per_class = []
        labels = np.unique(test_labels)
        for label in labels:
            images_idx = np.where(test_labels == label)[0].tolist()
            test_images_per_class.append(images_idx)

        return {
            "object_fields": str2ascii(['images', 'classes']),
            "class_name": str2ascii(class_names['label_names']),
            "data": test_data,
            "labels": test_labels,
            "object_ids": test_object_list,
            "list_images_per_class": np.array(pad_list(test_images_per_class, 1), dtype=np.int32)
        }


    def load_data(self):
        """
        Load the data from the files.
        """
        # train set
        yield {"train" : self.load_data_train()}

        # test set
        yield {"test" : self.load_data_test()}


    def add_data_to_source(self, handler, data, set_name=None):
        """
        Store data annotations in a nested tree fashion.

        It closely follows the tree structure of the data.
        """
        handler.create_dataset('classes', data=data["class_name"], dtype=np.uint8)
        handler.create_dataset('images', data=data["data"], dtype=np.uint8)
        handler.create_dataset('labels', data=data["labels"], dtype=np.uint8)


    def add_data_to_default(self, handler, data, set_name=None):
        """
        Add data of a set to the default group.

        For each field, the data is organized into a single big matrix.
        """
        handler.create_dataset('classes', data=data["class_name"], dtype=np.uint8)
        handler.create_dataset('images', data=data["data"], dtype=np.uint8)
        handler.create_dataset('object_ids', data=data["object_ids"], dtype=np.int32)
        handler.create_dataset('object_fields', data=data["object_fields"], dtype=np.int32)
        handler.create_dataset('list_images_per_class', data=data["list_images_per_class"], dtype=np.int32)