"""
Cifar10 classification process functions.
"""


from __future__ import print_function, division
import os
import numpy as np

from dbcollection.datasets import BaseTaskNew
from dbcollection.utils.file_load import load_pickle
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list


class Classification(BaseTaskNew):
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

    def load_data(self):
        """
        Loads data from annotation files.
        """
        yield {"train": self.load_data_set(is_test=False)}
        yield {"test": self.load_data_set(is_test=True)}

    def load_data_set(self, is_test):
        """Fetches the train/test data."""
        assert isinstance(is_test, bool), "Must input a valid boolean input."
        images, labels, class_names = self.load_data_annotations(is_test)

        object_list = self.get_object_list(images, labels)
        images_per_class = self.get_images_per_class(labels)

        return {
            "object_fields": str2ascii(['images', 'classes']),
            "class_name": str2ascii(class_names['label_names']),
            "images": images,
            "labels": labels,
            "object_ids": object_list,
            "list_images_per_class": images_per_class
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

    def get_object_list(self, data, labels):
        """Groups the data + labels to a list of indexes."""
        object_id = np.ndarray((data.shape[0], 2), dtype=np.int32)
        for i in range(data.shape[0]):
            object_id[i][0] = i
            object_id[i][1] = labels[i]
        return object_id

    def get_images_per_class(self, labels):
        """Returns a list of image indexes per class."""
        images_per_class = []
        unique_labels = np.unique(labels)
        for label in unique_labels:
            images_idx = np.where(labels == label)[0].tolist()
            images_per_class.append(images_idx)
        return np.array(pad_list(images_per_class, -1), dtype=np.int32)

    def process_set_metadata(self, data, set_name):
        """
        Saves the metadata of a set.
        """
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
