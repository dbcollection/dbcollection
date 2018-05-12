"""
Cifar100 classification process functions.
"""


from __future__ import print_function, division
import os
import numpy as np

from dbcollection.datasets import BaseTaskNew

from dbcollection.utils.file_load import load_pickle
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list
from dbcollection.utils.hdf5 import hdf5_write_data


class Classification(BaseTaskNew):
    """ Cifar100 Classification preprocessing functions """

    # metadata filename
    filename_h5 = 'classification'

    # extracted file names
    data_files = [
        "meta",
        "train",
        "test",
    ]

    # classes
    coarse_classes = [
        'aquatic mammals',
        'fish',
        'flowers',
        'food containers',
        'fruit and vegetables',
        'household electrical devices',
        'household furniture',
        'insects',
        'large carnivores',
        'large man-made outdoor things',
        'large natural outdoor scenes',
        'large omnivores and herbivores',
        'medium-sized mammals',
        'non-insect invertebrates',
        'people',
        'reptiles',
        'small mammals',
        'trees',
        'vehicles 1',
        'vehicles 2',
    ]

    finer_classes = [
        'beaver', 'dolphin', 'otter', 'seal', 'whale',
        'aquarium fish', 'flatfish', 'ray', 'shark', 'trout',
        'orchids', 'poppies', 'roses', 'sunflowers', 'tulips',
        'bottles', 'bowls', 'cans', 'cups', 'plates',
        'apples', 'mushrooms', 'oranges', 'pears', 'sweet peppers',
        'clock', 'computer keyboard', 'lamp', 'telephone', 'television',
        'bed', 'chair', 'couch', 'table', 'wardrobe',
        'bee', 'beetle', 'butterfly', 'caterpillar', 'cockroach',
        'bear', 'leopard', 'lion', 'tiger', 'wolf',
        'bridge', 'castle', 'house', 'road', 'skyscraper',
        'cloud', 'forest', 'mountain', 'plain', 'sea',
        'camel', 'cattle', 'chimpanzee', 'elephant', 'kangaroo',
        'fox', 'porcupine', 'possum', 'raccoon', 'skunk',
        'crab', 'lobster', 'snail', 'spider', 'worm',
        'baby', 'boy', 'girl', 'man', 'woman',
        'crocodile', 'dinosaur', 'lizard', 'snake', 'turtle',
        'hamster', 'mouse', 'rabbit', 'shrew', 'squirrel',
        'maple', 'oak', 'palm', 'pine', 'willow',
        'bicycle', 'bus', 'motorcycle', 'pickup truck', 'train',
        'lawn-mower', 'rocket', 'streetcar', 'tank', 'tractor'
    ]

    def load_data(self):
        """
        Fetches the train/test data.
        """
        yield {"train": self.load_data_set(is_test=False)}
        yield {"test": self.load_data_set(is_test=True)}

    def load_data_set(self, is_test):
        """Fetches the train/test data."""
        assert isinstance(is_test, bool), "Must input a valid boolean input."
        images, labels, coarse_labels = self.load_data_annotations(is_test)

        object_list = self.get_object_list(images, labels, coarse_labels)
        images_per_class = self.get_images_per_class(labels)
        images_per_superclass = self.get_images_per_class(coarse_labels)

        return {
            "images": images,
            "classes": str2ascii(self.finer_classes),
            "coarse_classes": str2ascii(self.coarse_classes),
            "labels": labels,
            "coarse_labels": coarse_labels,
            "object_fields": str2ascii(['images', 'classes', 'superclasses']),
            "object_ids": object_list,
            "list_images_per_class": images_per_class,
            "list_images_per_superclass": images_per_superclass
        }

    def load_data_annotations(self, is_test):
        """Loads the data from the annotations' files."""
        assert isinstance(is_test, bool), "Must input a valid boolean input."
        data_path = os.path.join(self.data_path, 'cifar-100-python')
        if is_test:
            return self.get_data_test(data_path)
        else:
            return self.get_data_train(data_path)

    def get_data_test(self, path):
        """Loads the test data annotations from disk."""
        assert path, "Must input a valid path."
        annotations = self.load_annotation_file(os.path.join(path, self.data_files[2]))
        return self.parse_data_annotations(annotations, 10000)

    def load_annotation_file(self, path):
        """Reads the data from annotation file from disk."""
        return load_pickle(path)

    def parse_data_annotations(self, annotations, size_data):
        """Parses the annotations' data."""
        data = annotations['data'].reshape(size_data, 3, 32, 32)
        data = np.transpose(data, (0, 2, 3, 1))  # NxHxWxC
        labels = np.array(annotations['fine_labels'], dtype=np.uint8)
        coarse_labels = np.array(annotations['coarse_labels'], dtype=np.uint8)
        return data, labels, coarse_labels

    def get_data_train(self, path):
        """Loads the train data annotations from disk."""
        assert path, "Must input a valid path."
        annotations = self.load_annotation_file(os.path.join(path, self.data_files[1]))
        return self.parse_data_annotations(annotations, 50000)

    def get_object_list(self, data, fine_labels, coarse_labels):
        """Groups the data + labels to a list of indexes."""
        object_id = np.ndarray((data.shape[0], 3), dtype=int)
        for i in range(data.shape[0]):
            object_id[i][0] = i
            object_id[i][1] = fine_labels[i]
            object_id[i][2] = coarse_labels[i]
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
        self.save_field_to_hdf5(set_name, 'images', data["images"],
                                dtype=np.uint8, fillvalue=-1)
        self.save_field_to_hdf5(set_name, 'classes', data["classes"],
                                dtype=np.uint8, fillvalue=0)
        self.save_field_to_hdf5(set_name, 'superclasses', data["coarse_classes"],
                                dtype=np.uint8, fillvalue=0)
        self.save_field_to_hdf5(set_name, 'labels', data["labels"],
                                dtype=np.uint8, fillvalue=0)
        self.save_field_to_hdf5(set_name, 'coarse_labels', data["coarse_labels"],
                                dtype=np.uint8, fillvalue=0)
        self.save_field_to_hdf5(set_name, 'object_fields', data["object_fields"],
                                dtype=np.uint8, fillvalue=0)
        self.save_field_to_hdf5(set_name, 'object_ids', data["object_ids"],
                                dtype=np.int32, fillvalue=-1)
        self.save_field_to_hdf5(set_name, 'list_images_per_class', data["list_images_per_class"],
                                dtype=np.int32, fillvalue=-1)
        self.save_field_to_hdf5(set_name, 'list_images_per_superclass', data["list_images_per_superclass"],
                                dtype=np.int32, fillvalue=-1)
