"""
Cifar10 classification process functions.
"""


from __future__ import print_function, division
import os
import numpy as np

from dbcollection.datasets import BaseTaskNew, BaseField
from dbcollection.utils.decorators import display_message_processing
from dbcollection.utils.file_load import load_pickle
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list


class Classification(BaseTaskNew):
    """Cifar10 Classification preprocessing functions."""

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

    def load_data(self):
        """
        Loads data from annotation files.
        """
        loader = DatasetAnnotationLoader(
            data_files=self.data_files,
            data_path=self.data_path,
            cache_path=self.cache_path,
            verbose=self.verbose
        )
        yield {"train": loader.load_train_data()}
        yield {"test": loader.load_test_data()}

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
        label_ids = LabelIdField(**args).process()
        ObjectFieldNamesField(**args).process()
        ObjectIdsField(**args).process(image_ids, label_ids)

        # Lists
        if self.verbose:
            print('\n==> Setting up ordered lists:')
        ImagesPerClassList(**args).process()


# -----------------------------------------------------------
# Data load / set up
# -----------------------------------------------------------

class DatasetAnnotationLoader:
    """Annotation's data loader for the cifar10 dataset (train/test)."""

    def __init__(self, data_files, data_path, cache_path, verbose):
        self.data_files = data_files
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
        """Fetches the train/test data."""
        assert isinstance(is_test, bool), "Must input a valid boolean input."
        images, labels, class_names = self.load_data_annotations(is_test)
        return {
            "classes": class_names,
            "images": images,
            "labels": labels
        }

    def load_data_annotations(self, is_test):
        """Loads the data from the annotations' files."""
        assert isinstance(is_test, bool), "Must input a valid boolean input."
        data_path = os.path.join(self.data_path, 'cifar-10-batches-py')
        class_names = self.get_class_names(data_path)
        if is_test:
            data, labels = self.get_data_test(data_path)
        else:
            data, labels = self.get_data_train(data_path)
        data = np.transpose(data, (0, 2, 3, 1))  # NxHxWxC
        return data, labels, class_names

    def get_class_names(self, path):
        """Returns the class names/labels."""
        assert path, "Must input a valid path."
        filename = os.path.join(path, self.data_files[0])
        return self.load_annotation_file(filename)

    def load_annotation_file(self, path):
        """Reads the data from annotation file from disk."""
        return load_pickle(path)

    def get_data_train(self, path):
        assert path, "Must input a valid path."
        batch1 = self.load_annotation_file(os.path.join(path, self.data_files[1]))
        batch2 = self.load_annotation_file(os.path.join(path, self.data_files[2]))
        batch3 = self.load_annotation_file(os.path.join(path, self.data_files[3]))
        batch4 = self.load_annotation_file(os.path.join(path, self.data_files[4]))
        batch5 = self.load_annotation_file(os.path.join(path, self.data_files[5]))

        data = np.concatenate(
            (batch1['data'], batch2['data'], batch3['data'], batch4['data'], batch5['data']),
            axis=0
        )
        data = self.reshape_array(data, 50000)
        labels = np.concatenate(
            (batch1['labels'], batch2['labels'], batch3['labels'], batch4['labels'], batch5['labels']),
            axis=0
        )

        return data, labels

    def reshape_array(self, data, size_array):
        """Reshapes the numpy array to a fixed format."""
        return data.reshape(size_array, 3, 32, 32)

    def get_data_test(self, path):
        assert path, "Must input a valid path."
        batch = self.load_annotation_file(os.path.join(path, self.data_files[6]))
        data = self.reshape_array(batch['data'], 10000)
        labels = np.array(batch['labels'], dtype=np.uint8)
        return data, labels


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


class LabelIdField(BaseField):
    """Label id field metadata process/save class."""

    @display_message_processing('labels')
    def process(self):
        """Processes and saves the labels metadata to hdf5."""
        labels, label_ids = self.get_labels()
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='labels',
            data=labels,
            dtype=np.uint8,
            fillvalue=0
        )
        return label_ids

    def get_labels(self):
        """Returns a np.ndarray of labels and a list
        of label ids for each row of 'object_ids' field."""
        labels = self.data['labels']
        label_ids = list(range(len(labels)))
        return labels, label_ids


class ObjectFieldNamesField(BaseField):
    """Object field names metadata process/save class."""

    def process(self):
        """Processes and saves the labels metadata to hdf5."""
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='object_fields',
            data=str2ascii(['images', 'labels']),
            dtype=np.uint8,
            fillvalue=0
        )


class ObjectIdsField(BaseField):
    """Object ids' field metadata process/save class."""

    def process(self, image_ids, label_ids):
        """Processes and saves the object ids metadata to hdf5."""
        # images, labels
        object_ids = [[image_ids[i], label_ids[i]] for i, _ in enumerate(label_ids)]
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='object_ids',
            data=np.array(object_ids, dtype=np.int32),
            dtype=np.int32,
            fillvalue=-1
        )


# -----------------------------------------------------------
# Metadata lists
# -----------------------------------------------------------

class ImagesPerClassList(BaseField):
    """Images per class list metadata process/save class."""

    @display_message_processing('images per class list')
    def process(self):
        """Processes and saves the list ids metadata to hdf5."""
        images_per_class = self.get_image_ids_per_class()
        images_per_class_array = self.convert_list_to_array(images_per_class)
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='list_images_per_class',
            data=images_per_class_array,
            dtype=np.int32,
            fillvalue=-1
        )

    def get_image_ids_per_class(self):
        """Returns a list of lists of image filename ids per class id."""
        images_per_class = []
        labels = self.data['labels']
        unique_labels = np.unique(labels)
        for label in unique_labels:
            images_idx = np.where(labels == label)[0].tolist()
            images_per_class.append(images_idx)
        return images_per_class

    def convert_list_to_array(self, list_ids):
        """Pads a list of listsand converts it into a numpy.ndarray."""
        padded_list = pad_list(list_ids, val=-1)
        return np.array(padded_list, dtype=np.int32)
