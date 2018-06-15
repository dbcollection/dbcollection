"""
Cifar100 classification process functions.
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
    """Cifar100 Classification preprocessing functions."""

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
        loader = DatasetAnnotationLoader(
            finer_classes=self.finer_classes,
            coarse_classes=self.coarse_classes,
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
        SuperClassLabelField(**args).process()
        image_ids = ImageField(**args).process()
        label_ids = LabelIdField(**args).process()
        super_label_ids = SuperLabelIdField(**args).process()
        ObjectFieldNamesField(**args).process()
        ObjectIdsField(**args).process(image_ids, label_ids, super_label_ids)

        # Lists
        if self.verbose:
            print('\n==> Setting up ordered lists:')
        ImagesPerClassList(**args).process()
        ImagesPerSuperClassList(**args).process()


# -----------------------------------------------------------
# Data load / set up
# -----------------------------------------------------------

class DatasetAnnotationLoader:
    """Annotation's data loader for the cifar10 dataset (train/test)."""

    def __init__(self, finer_classes, coarse_classes, data_files, data_path, cache_path, verbose):
        self.finer_classes = finer_classes
        self.coarse_classes = coarse_classes
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
        images, labels, coarse_labels = self.load_data_annotations(is_test)
        return {
            "images": images,
            "classes": self.finer_classes,
            "coarse_classes": self.coarse_classes,
            "labels": labels,
            "coarse_labels": coarse_labels
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


class SuperClassLabelField(BaseField):
    """Super class label names' field metadata process/save class."""

    @display_message_processing('super class labels')
    def process(self):
        """Processes and saves the super classes metadata to hdf5."""
        class_names = self.get_class_names()
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='superclasses',
            data=str2ascii(class_names),
            dtype=np.uint8,
            fillvalue=0
        )

    def get_class_names(self):
        """Returns a list of super class names."""
        return self.data['coarse_classes']


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


class SuperLabelIdField(BaseField):
    """Super label id field metadata process/save class."""

    @display_message_processing('super labels')
    def process(self):
        """Processes and saves the super labels metadata to hdf5."""
        super_labels, super_label_ids = self.get_super_labels()
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='superlabels',
            data=super_labels,
            dtype=np.uint8,
            fillvalue=0
        )
        return super_label_ids

    def get_super_labels(self):
        """Returns a np.ndarray of super labels and a list
        of label ids for each row of 'object_ids' field."""
        super_labels = self.data['coarse_labels']
        super_label_ids = list(range(len(super_labels)))
        return super_labels, super_label_ids


class ObjectFieldNamesField(BaseField):
    """Object field names metadata process/save class."""

    def process(self):
        """Processes and saves the labels metadata to hdf5."""
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='object_fields',
            data=str2ascii(['images', 'labels', 'superlabels']),
            dtype=np.uint8,
            fillvalue=0
        )


class ObjectIdsField(BaseField):
    """Object ids' field metadata process/save class."""

    def process(self, image_ids, label_ids, super_label_ids):
        """Processes and saves the object ids metadata to hdf5."""
        # images, labels, superlabels
        object_ids = [[image_ids[i], label_ids[i], super_label_ids[i]] for i, _ in enumerate(label_ids)]
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
        """Pads a list of lists and converts it into a numpy.ndarray."""
        padded_list = pad_list(list_ids, val=-1)
        return np.array(padded_list, dtype=np.int32)


class ImagesPerSuperClassList(BaseField):
    """Images per super class list metadata process/save class."""

    @display_message_processing('images per super class list')
    def process(self):
        """Processes and saves the list ids metadata to hdf5."""
        images_per_super_class = self.get_image_ids_per_super_class()
        images_per_super_class_array = self.convert_list_to_array(images_per_super_class)
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='list_images_per_superclass',
            data=images_per_super_class_array,
            dtype=np.int32,
            fillvalue=-1
        )

    def get_image_ids_per_super_class(self):
        """Returns a list of lists of image filename ids per super class id."""
        images_per_super_class = []
        super_labels = self.data['coarse_labels']
        unique_super_labels = np.unique(super_labels)
        for label in unique_super_labels:
            images_idx = np.where(super_labels == label)[0].tolist()
            images_per_super_class.append(images_idx)
        return images_per_super_class

    def convert_list_to_array(self, list_ids):
        """Pads a list of lists and converts it into a numpy.ndarray."""
        padded_list = pad_list(list_ids, val=-1)
        return np.array(padded_list, dtype=np.int32)
