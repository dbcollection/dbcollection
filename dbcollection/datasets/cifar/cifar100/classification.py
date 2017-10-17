"""
Cifar100 classification process functions.
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

    def get_object_list(self, data, fine_labels, coarse_labels):
        """
        Groups the data + labels info in a 'list' of indexes.
        """
        object_id = np.ndarray((data.shape[0], 3), dtype=int)
        for i in range(data.shape[0]):
            object_id[i][0] = i
            object_id[i][1] = fine_labels[i]
            object_id[i][2] = coarse_labels[i]
        return object_id

    def get_class_names(self, path):
        """
        Returns the class names/labels.
        """
        return load_pickle(os.path.join(path, self.data_files[0]))

    def load_data_set(self, is_test):
        """
        Load train/test data.
        """
        # merge the path with the extracted folder name
        data_path_ = os.path.join(self.data_path, 'cifar-100-python')

        # load classes name file
        class_names = self.get_class_names(data_path_)

        # load test data file
        if is_test:
            batch = load_pickle(os.path.join(data_path_, self.data_files[2]))
            data = batch['data'].reshape(10000, 3, 32, 32)
        else:
            batch = load_pickle(os.path.join(data_path_, self.data_files[1]))
            data = batch['data'].reshape(50000, 3, 32, 32)

        data = np.transpose(data, (0, 2, 3, 1))  # NxHxWxC
        labels = np.array(batch['fine_labels'], dtype=np.uint8)
        coarse_labels = np.array(batch['coarse_labels'], dtype=np.uint8)
        object_list = self.get_object_list(data, labels, coarse_labels)

        # organize list of image indexes per class
        images_per_class = []
        unique_labels = np.unique(labels)
        for label in unique_labels:
            images_idx = np.where(labels == label)[0].tolist()
            images_per_class.append(images_idx)

        # organize list of image indexes per superclass
        images_per_superclass = []
        unique_coarse_labels = np.unique(coarse_labels)
        for coarse_label in unique_coarse_labels:
            images_idx = np.where(coarse_labels == coarse_label)[0].tolist()
            images_per_superclass.append(images_idx)

        return {
            "object_fields": str2ascii(['images', 'classes', 'superclasses']),
            "data": data,
            "class_name": str2ascii(self.finer_classes),
            "coarse_class_name": str2ascii(self.coarse_classes),
            "labels": labels,
            "coarse_labels": coarse_labels,
            "object_id_list": object_list,
            "list_images_per_class": np.array(pad_list(images_per_class, 1), dtype=np.int32),
            "list_images_per_superclass": np.array(pad_list(images_per_superclass, 1),
                                                   dtype=np.int32),
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
    #    hdf5_write_data(hdf5_handler, 'superclasses', data["coarse_class_name"], dtype=np.uint8,
    #                    fillvalue=0)
    #    hdf5_write_data(hdf5_handler, 'images', data["data"], dtype=np.uint8, fillvalue=-1)
    #    hdf5_write_data(hdf5_handler, 'labels', data["labels"], dtype=np.uint8, fillvalue=-1)
    #    hdf5_write_data(hdf5_handler, 'coarse_labels', data["coarse_labels"], dtype=np.uint8,
    #                    fillvalue=-1)

    def add_data_to_default(self, hdf5_handler, data, set_name=None):
        """
        Add data of a set to the default group.

        For each field, the data is organized into a single big matrix.
        """
        hdf5_write_data(hdf5_handler, 'classes', data["class_name"], dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'superclasses',
                        data["coarse_class_name"], dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'images', data["data"], dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'labels', data["labels"], dtype=np.uint8, fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'coarse_labels',
                        data["coarse_labels"], dtype=np.uint8, fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'object_ids',
                        data["object_id_list"], dtype=np.int32, fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'object_fields',
                        data["object_fields"], dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'list_images_per_class',
                        data["list_images_per_class"], dtype=np.int32, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'list_images_per_superclass',
                        data["list_images_per_superclass"], dtype=np.int32, fillvalue=0)
