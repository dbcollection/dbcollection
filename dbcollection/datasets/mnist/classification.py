"""
MNIST classification process functions.
"""


from __future__ import print_function, division
import os
import numpy as np

from dbcollection.datasets import BaseTaskNew, BaseField
from dbcollection.utils.decorators import display_message_processing
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list


class Classification(BaseTaskNew):
    """MNIST Classification preprocessing functions."""

    # metadata filename
    filename_h5 = 'classification'

    classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def load_data(self):
        """
        Loads data from annotation files.
        """
        yield {"train": self.load_data_set(is_test=False)}
        yield {"test": self.load_data_set(is_test=True)}

    def load_data_set(self, is_test):
        """
        Fetches the train/test data.
        """
        assert isinstance(is_test, bool), "Must input a valid boolean input."
        if is_test:
            images, labels, size_set = self.get_test_data()
        else:
            images, labels, size_set = self.get_train_data()

        data = images.reshape(size_set, 28, 28)
        object_list = np.array([[i, labels[i]] for i in range(size_set)])
        classes = str2ascii(self.classes)

        return {
            "classes": classes,
            "images": data,
            "labels": labels,
            "object_fields": str2ascii(['images', 'labels']),
            "object_ids": object_list,
            "list_images_per_class": self.get_list_images_per_class(labels)
        }

    def get_train_data(self):
        """Loads the data of the train set."""
        fname_train_imgs = os.path.join(self.data_path, 'train-images.idx3-ubyte')
        fname_train_lbls = os.path.join(self.data_path, 'train-labels.idx1-ubyte')
        train_images = self.load_images_numpy(fname_train_imgs)
        train_labels = self.load_labels_numpy(fname_train_lbls)
        size_train = 60000
        return train_images, train_labels, size_train

    def get_list_images_per_class(self, set_labels):
        """Builds a list of image indexes per class."""
        images_per_class = []
        labels = np.unique(set_labels)
        for label in labels:
            images_idx = np.where(set_labels == label)[0].tolist()
            images_per_class.append(images_idx)
        return np.array(pad_list(images_per_class, -1), dtype=np.int32)

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

    def get_test_data(self):
        """Loads the data of the test set."""
        fname_test_imgs = os.path.join(self.data_path, 't10k-images.idx3-ubyte')
        fname_test_lbls = os.path.join(self.data_path, 't10k-labels.idx1-ubyte')
        test_images = self.load_images_numpy(fname_test_imgs)
        test_labels = self.load_labels_numpy(fname_test_lbls)
        size_test = 10000
        return test_images, test_labels, size_test

    def process_set_metadata(self, data, set_name):
        """
        Saves the metadata of a set.
        """
        args = {
            "data": data,
            "set_name": set_name,
            "hdf5_manager": self.hdf5_manager,
            "verbose": self.verbose
        }

        # Fields
        if self.verbose:
            print('\n==> Setting up the data fields:')
        ClassLabelField(**args).process()
        image_ids = ImageField(**args).process()


        self.save_field_to_hdf5(set_name, 'classes', data["classes"],
                                dtype=np.uint8, fillvalue=0)
        self.save_field_to_hdf5(set_name, 'images', data["images"],
                                dtype=np.uint8, fillvalue=-1)
        self.save_field_to_hdf5(set_name, 'labels', data["labels"],
                                dtype=np.uint8, fillvalue=0)
        self.save_field_to_hdf5(set_name, 'object_fields', data["object_fields"],
                                dtype=np.uint8, fillvalue=0)
        self.save_field_to_hdf5(set_name, 'object_ids', data["object_ids"],
                                dtype=np.int32, fillvalue=-1)
        self.save_field_to_hdf5(set_name, 'list_images_per_class', data["list_images_per_class"],
                                dtype=np.int32, fillvalue=-1)


# -----------------------------------------------------------
# Data load / set up
# -----------------------------------------------------------

class DatasetAnnotationLoader:
    """Annotation's data loader for the cifar10 dataset (train/test)."""

    def __init__(self, classes, data_path, cache_path, verbose):
        self.classes = classes
        self.data_path = data_path
        self.cache_path = cache_path
        self.verbose = verbose

    def load_train_data(self):
        """Loads the train set annotation data from disk
        and returns it as a dictionary."""
        return self.load_data_set(is_test=False)

    def load_test_data(self):
        """Loads the test set annotation data from disk
        and returns it as a dictionary."""
        return self.load_data_set(is_test=True)

    def load_data_set(self, is_test):
        """
        Fetches the train/test data.
        """
        assert isinstance(is_test, bool), "Must input a valid boolean input."
        images, labels = self.load_data_annotations(is_test)
        return {
            "classes": self.classes,
            "images": images,
            "labels": labels
        }

    def load_data_annotations(self, is_test):
        """Loads the data from the annotations' files."""
        assert isinstance(is_test, bool), "Must input a valid boolean input."
        if is_test:
            images, labels, size_set = self.get_data_test()
        else:
            images, labels, size_set = self.get_data_train()
        images = images.reshape(size_set, 28, 28)
        return images, labels

    def get_data_test(self):
        """Loads the annotation's data of the test set."""
        filename_test_images = os.path.join(self.data_path, 't10k-images.idx3-ubyte')
        filename_test_labels = os.path.join(self.data_path, 't10k-labels.idx1-ubyte')
        test_images = self.load_images_numpy(filename_test_images)
        test_labels = self.load_labels_numpy(filename_test_labels)
        size_test = 10000
        return test_images, test_labels, size_test

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

    def get_data_train(self):
        """Loads the annotation's data of the train set."""
        fname_train_imgs = os.path.join(self.data_path, 'train-images.idx3-ubyte')
        fname_train_lbls = os.path.join(self.data_path, 'train-labels.idx1-ubyte')
        train_images = self.load_images_numpy(fname_train_imgs)
        train_labels = self.load_labels_numpy(fname_train_lbls)
        size_train = 60000
        return train_images, train_labels, size_train


# -----------------------------------------------------------
# Metadata fields
# -----------------------------------------------------------

class ClassLabelField(BaseField):
    """Class label names' field metadata process/save class."""

    @display_message_processing('class labels')
    def process(self):
        """Processes and saves the classes metadata to hdf5."""
        class_names = self.get_class_names()
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='classes',
            data=str2ascii(class_names),
            dtype=np.uint8,
            fillvalue=0
        )

    def get_class_names(self):
        """Returns a list of class names."""
        return self.data['classes']


class ImageField(BaseField):
    """Images' data field process/save class."""

    @display_message_processing('images')
    def process(self):
        """Processes and saves the images metadata to hdf5."""
        images, image_ids = self.get_images()
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='images',
            data=images,
            dtype=np.uint8,
            fillvalue=-1
        )
        return image_ids

    def get_images(self):
        """Returns a np.ndarray of images and a list
        of image ids for each row of 'object_ids' field."""
        images = self.data['images']
        image_ids = list(range(len(images)))
        return images, image_ids


# -----------------------------------------------------------
# Metadata lists
# -----------------------------------------------------------
