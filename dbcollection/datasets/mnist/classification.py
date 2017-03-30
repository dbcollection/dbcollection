"""
MNIST classification process functions.
"""


from __future__ import print_function, division
import os
import numpy as np
import h5py

from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list


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

        # classes
        classes = str2ascii(self.classes)

        # organize list of image indexes per class
        train_images_per_class = []
        test_images_per_class = []
        labels = np.unique(train_labels)
        for label in labels:
            tr_images_idx = np.where(train_labels == label)[0].tolist()
            train_images_per_class.append(tr_images_idx)

            ts_images_idx = np.where(test_labels == label)[0].tolist()
            test_images_per_class.append(ts_images_idx)

        #return a dictionary
        return {
            "train": {
                "classes": classes,
                "images": train_data,
                "labels": train_labels,
                "object_fields": str2ascii(['images', 'labels']),
                "object_ids": train_object_list,
                "list_images_per_class": np.array(pad_list(train_images_per_class, 1), dtype=np.int32)
            },
            "test": {
                "classes": classes,
                "images": test_data,
                "labels": test_labels,
                "object_fields": str2ascii(['images', 'labels']),
                "object_ids": test_object_list,
                "list_images_per_class": np.array(pad_list(test_images_per_class, 1), dtype=np.int32)
            }
        }


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