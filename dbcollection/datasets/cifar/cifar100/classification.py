"""
Cifar100 classification process functions.
"""


from __future__ import print_function, division
import os
import numpy as np

from dbcollection.datasets.dbclass import BaseTask

from dbcollection.utils.file_load import load_pickle
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list


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
        'beaver', 'dolphin', 'otter', 'seal', 'whale', \
        'aquarium fish', 'flatfish', 'ray', 'shark', 'trout', \
        'orchids', 'poppies', 'roses', 'sunflowers', 'tulips', \
        'bottles', 'bowls', 'cans', 'cups', 'plates', \
        'apples', 'mushrooms', 'oranges', 'pears', 'sweet peppers', \
        'clock', 'computer keyboard', 'lamp', 'telephone', 'television', \
        'bed', 'chair', 'couch', 'table', 'wardrobe', \
        'bee', 'beetle', 'butterfly', 'caterpillar', 'cockroach', \
        'bear', 'leopard', 'lion', 'tiger', 'wolf', \
        'bridge', 'castle', 'house', 'road', 'skyscraper', \
        'cloud', 'forest', 'mountain', 'plain', 'sea', \
        'camel', 'cattle', 'chimpanzee', 'elephant', 'kangaroo', \
        'fox', 'porcupine', 'possum', 'raccoon', 'skunk', \
        'crab', 'lobster', 'snail', 'spider', 'worm', \
        'baby', 'boy', 'girl', 'man', 'woman', \
        'crocodile', 'dinosaur', 'lizard', 'snake', 'turtle', \
        'hamster', 'mouse', 'rabbit', 'shrew', 'squirrel', \
        'maple', 'oak', 'palm', 'pine', 'willow', \
        'bicycle', 'bus', 'motorcycle', 'pickup truck', 'train', \
        'lawn-mower', 'rocket', 'streetcar', 'tank', 'tractor' \
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


    def load_data_train(self):
        """
        Load train data.
        """
        # merge the path with the extracted folder name
        data_path_ = os.path.join(self.data_path, 'cifar-100-python')

        # load classes name file
        class_names = self.get_class_names(data_path_)

        # load train data files
        train_batch = load_pickle(os.path.join(data_path_, self.data_files[1]))

        train_data = train_batch['data'].reshape((50000, 3, 32, 32))
        train_data = np.transpose(train_data, (0, 2, 3, 1)) # NxHxWxC
        train_labels = np.array(train_batch['fine_labels'], dtype=np.uint8)
        train_coarse_labels = np.array(train_batch['coarse_labels'], dtype=np.uint8)
        train_object_list = self.get_object_list(train_data, train_labels, train_coarse_labels)

        # organize list of image indexes per class
        train_images_per_class = []
        labels = np.unique(train_labels)
        for label in labels:
            images_idx = np.where(train_labels == label)[0].tolist()
            train_images_per_class.append(images_idx)

        return {
            "object_fields": str2ascii(['images', 'classes', 'superclasses']),
            "data": train_data,
            "class_name": str2ascii(self.finer_classes),
            "coarse_class_name": str2ascii(self.coarse_classes),
            "labels": train_labels,
            "coarse_labels": train_coarse_labels,
            "object_id_list": train_object_list,
            "list_images_per_class": np.array(pad_list(train_images_per_class, 1), dtype=np.int32)
        }


    def load_data_test(self):
        """
        Load test data.
        """
        # merge the path with the extracted folder name
        data_path_ = os.path.join(self.data_path, 'cifar-100-python')

        # load classes name file
        class_names = self.get_class_names(data_path_)

        # load test data file
        test_batch = load_pickle(os.path.join(data_path_, self.data_files[2]))

        test_data = test_batch['data'].reshape(10000, 3, 32, 32)
        test_data = np.transpose(test_data, (0, 2, 3, 1)) # NxHxWxC
        test_labels = np.array(test_batch['fine_labels'], dtype=np.uint8)
        test_coarse_labels = np.array(test_batch['coarse_labels'], dtype=np.uint8)
        test_object_list = self.get_object_list(test_data, test_labels, test_coarse_labels)

        # organize list of image indexes per class
        test_images_per_class = []
        labels = np.unique(test_labels)
        for label in labels:
            images_idx = np.where(test_labels == label)[0].tolist()
            test_images_per_class.append(images_idx)

        return {
            "object_fields": str2ascii(['images', 'classes', 'superclasses']),
            "data": test_data,
            "class_name": str2ascii(self.finer_classes),
            "coarse_class_name": str2ascii(self.coarse_classes),
            "labels": test_labels,
            "coarse_labels": test_coarse_labels,
            "object_id_list": test_object_list,
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
        handler.create_dataset('superclasses', data=data["coarse_class_name"], dtype=np.uint8)
        handler.create_dataset('images', data=data["data"], dtype=np.uint8)
        handler.create_dataset('labels', data=data["labels"], dtype=np.uint8)
        handler.create_dataset('coarse_labels', data=data["coarse_labels"], dtype=np.uint8)


    def add_data_to_default(self, handler, data, set_name=None):
        """
        Add data of a set to the default group.

        For each field, the data is organized into a single big matrix.
        """
        handler.create_dataset('classes', data=data["class_name"], dtype=np.uint8)
        handler.create_dataset('superclasses', data=data["coarse_class_name"], dtype=np.uint8)
        handler.create_dataset('images', data=data["data"], dtype=np.uint8)
        handler.create_dataset('object_ids', data=data["object_id_list"], dtype=np.int32)
        handler.create_dataset('object_fields', data=data["object_fields"], dtype=np.uint8)
        handler.create_dataset('list_images_per_class', data=data["list_images_per_class"], dtype=np.uint8)