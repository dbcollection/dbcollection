"""
MNIST classification process functions.
"""


from __future__ import print_function, division
import os
import numpy as np

from dbcollection.datasets import BaseTask
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list
from dbcollection.utils.hdf5 import hdf5_write_data


class Classification(BaseTask):
    """MNIST Classification preprocessing functions."""

    # metadata filename
    filename_h5 = 'classification'

    classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def load_images_numpy(self, fname):
        """Load images from file as numpy array."""
        with open(fname, 'rb') as f:
            annotations = f.read(16)
            data = np.fromfile(f, dtype=np.int8)
        return data

    def load_labels_numpy(self, fname):
        """Load labels from file as numpy array."""
        with open(fname, 'rb') as f:
            annotations = f.read(8)
            data = np.fromfile(f, dtype=np.int8)
        return data

    def load_data_train(self):
        """
        Fetch train data.
        """
        # files path
        fname_train_imgs = os.path.join(self.data_path, 'train-images.idx3-ubyte')
        fname_train_lbls = os.path.join(self.data_path, 'train-labels.idx1-ubyte')

        # read files to memory
        train_images = self.load_images_numpy(fname_train_imgs)
        train_labels = self.load_labels_numpy(fname_train_lbls)

        size_train = 60000

        # reshape images
        train_data = train_images.reshape(size_train, 28, 28)

        # get object_id lists
        train_object_list = np.array([[i, train_labels[i]] for i in range(size_train)])

        # classes
        classes = str2ascii(self.classes)

        # organize list of image indexes per class
        train_images_per_class = []
        labels = np.unique(train_labels)
        for label in labels:
            tr_images_idx = np.where(train_labels == label)[0].tolist()
            train_images_per_class.append(tr_images_idx)

        return {
            "classes": classes,
            "images": train_data,
            "labels": train_labels,
            "object_fields": str2ascii(['images', 'labels']),
            "object_ids": train_object_list,
            "list_images_per_class": np.array(pad_list(train_images_per_class, 1), dtype=np.int32)
        }

    def load_data_test(self):
        """
        Fetch test data.
        """
        # files path
        fname_test_imgs = os.path.join(self.data_path, 't10k-images.idx3-ubyte')
        fname_test_lbls = os.path.join(self.data_path, 't10k-labels.idx1-ubyte')

        # read files to memory
        test_images = self.load_images_numpy(fname_test_imgs)
        test_labels = self.load_labels_numpy(fname_test_lbls)

        size_test = 10000

        # reshape images
        test_data = test_images.reshape(size_test, 28, 28)

        # get object_id lists
        test_object_list = np.array([[i, test_labels[i]] for i in range(size_test)])

        # classes
        classes = str2ascii(self.classes)

        # organize list of image indexes per class
        test_images_per_class = []
        labels = np.unique(test_labels)
        for label in labels:
            ts_images_idx = np.where(test_labels == label)[0].tolist()
            test_images_per_class.append(ts_images_idx)

        return {
            "classes": classes,
            "images": test_data,
            "labels": test_labels,
            "object_fields": str2ascii(['images', 'labels']),
            "object_ids": test_object_list,
            "list_images_per_class": np.array(pad_list(test_images_per_class, 1), dtype=np.int32)
        }

    def load_data(self):
        """
        Load the data from the files.
        """
        # train set
        yield {"train": self.load_data_train()}

        # test set
        yield {"test": self.load_data_test()}

    def add_data_to_source(self, hdf5_handler, data, set_name=None):
        """
        Store data annotations in a nested tree fashion.

        It closely follows the tree structure of the data.
        """
        hdf5_write_data(hdf5_handler, 'images', data["images"], dtype=np.uint8, fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'labels', data["labels"], dtype=np.uint8, fillvalue=0)

    def add_data_to_default(self, hdf5_handler, data, set_name=None):
        """
        Add data of a set to the default group.

        For each field, the data is organized into a single big matrix.
        """
        hdf5_write_data(hdf5_handler, 'classes',
                        data["classes"], dtype=np.uint8,
                        fillvalue=0)
        hdf5_write_data(hdf5_handler, 'images',
                        data["images"], dtype=np.uint8,
                        fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'labels',
                        data["labels"], dtype=np.uint8,
                        fillvalue=0)
        hdf5_write_data(hdf5_handler, 'object_fields',
                        data["object_fields"], dtype=np.uint8,
                        fillvalue=0)
        hdf5_write_data(hdf5_handler, 'object_ids',
                        data["object_ids"], dtype=np.int32,
                        fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'list_images_per_class',
                        data["list_images_per_class"], dtype=np.int32,
                        fillvalue=-1)
