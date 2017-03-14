"""
MNIST classification process functions.
"""


from __future__ import print_function, division
import os
import numpy as np

from dbcollection.utils.storage import StorageHDF5
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii


class Classification:
    """ Cifar10 Classification preprocessing functions """

    classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


    def __init__(self, data_path, cache_path, verbose=True):
        """
        Initialize class.
        """
        self.cache_path = cache_path
        self.data_path = data_path
        self.verbose = verbose


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


    def load_data(self):
        """
        Load the data from the files.
        """
        # files path
        fname_train_imgs = os.path.join(self.data_path, 'train-images.idx3-ubyte')
        fname_train_lbls = os.path.join(self.data_path, 'train-labels.idx1-ubyte')
        fname_test_imgs = os.path.join(self.data_path, 't10k-images.idx3-ubyte')
        fname_test_lbls = os.path.join(self.data_path, 't10k-labels.idx1-ubyte')

        # read files to memory
        train_images = self.load_images_numpy(fname_train_imgs)
        train_labels = self.load_labels_numpy(fname_train_lbls)
        test_images = self.load_images_numpy(fname_test_imgs)
        test_labels = self.load_labels_numpy(fname_test_lbls)

        size_train = 60000
        size_test = 10000

        # reshape images
        train_data = train_images.reshape(size_train, 28, 28)
        test_data = test_images.reshape(size_test, 28, 28)

        # get object_id lists
        train_object_list = np.array([[i, train_labels[i]] for i in range(size_train)])
        test_object_list = np.array([[i, test_labels[i]] for i in range(size_test)])

        #return a dictionary
        return {
            "train": {
                "images": train_data,
                "labels": train_labels,
                "object_fields": ['data', 'labels'],
                "object_ids": train_object_list
            },
            "test": {
                "images": test_data,
                "labels": test_labels,
                "object_fields": ['data', 'labels'],
                "object_ids": test_object_list
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
        fileh5 = StorageHDF5(file_name, 'w')

        # add data to the **source** group
        fileh5.add_data('train/source', 'data', data["train"]["images"], np.uint8)
        fileh5.add_data('train/source', 'labels', data["train"]["labels"], np.uint8)

        fileh5.add_data('test/source', 'data', data["test"]["images"], np.uint8)
        fileh5.add_data('test/source', 'labels', data["test"]["labels"], np.uint8)

        # add data to the **default** group
        # write data to the metadata file
        fileh5.add_data('train/default', 'classes', str2ascii(self.classes), np.uint8)
        fileh5.add_data('train/default', 'data',  data["train"]["images"], np.uint8)
        fileh5.add_data('train/default', 'labels', data["train"]["labels"], np.uint8)
        fileh5.add_data('train/default', 'object_ids', data["train"]["object_ids"], np.int32)
        # object fields is necessary to identify which fields compose 'object_id'
        fileh5.add_data('train/default', 'object_fields', str2ascii(data['train']["object_fields"]), np.uint8)

        fileh5.add_data('test/default', 'classes', str2ascii(self.classes), np.uint8)
        fileh5.add_data('test/default', 'data', data["test"]["images"], np.uint8)
        fileh5.add_data('test/default', 'labels', data["test"]["labels"], np.uint8)
        fileh5.add_data('test/default', 'object_ids', data["test"]["object_ids"], np.int32)
        # object fields is necessary to identify which fields compose 'object_id'
        fileh5.add_data('test/default', 'object_fields', str2ascii(data['test']["object_fields"]), np.uint8)

        # close file
        fileh5.close()

        # return information of the task + cache file
        return file_name


    def run(self):
        """
        Run task processing.
        """
        return self.classification_metadata_process()