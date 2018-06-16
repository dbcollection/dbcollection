"""
Test the base classes for managing datasets and tasks.
"""


import os
import sys
import pytest
import numpy as np
from numpy.testing import assert_array_equal

from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list
from dbcollection.datasets.mnist.classification import (
    Classification,
    DatasetAnnotationLoader,
    ClassLabelField,
    ImageField,
    LabelIdField,
    ObjectFieldNamesField,
    ObjectIdsField,
    ImagesPerClassList
)


@pytest.fixture()
def mock_classification_class():
    return Classification(data_path='/some/path/data', cache_path='/some/path/cache')


@pytest.fixture()
def classes_classification():
    return ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


class TestClassificationTask:
    """Unit tests for the mnist Classification task."""

    def test_task_attributes(self, mocker, mock_classification_class, classes_classification):
        assert mock_classification_class.filename_h5 == 'classification'
        assert mock_classification_class.classes == classes_classification

    def test_load_data(self, mocker, mock_classification_class):
        dummy_data = ['some_data']
        mock_load_train = mocker.patch.object(DatasetAnnotationLoader, "load_train_data", return_value=dummy_data)
        mock_load_test = mocker.patch.object(DatasetAnnotationLoader, "load_test_data", return_value=dummy_data)

        load_data_generator = mock_classification_class.load_data()

        if sys.version[0] == '3':
            train_data = load_data_generator.__next__()
            test_data = load_data_generator.__next__()
        else:
            train_data = load_data_generator.next()
            test_data = load_data_generator.next()

        mock_load_train.assert_called_once_with()
        mock_load_test.assert_called_once_with()
        assert train_data == {"train": ['some_data']}
        assert test_data == {"test": ['some_data']}

    def test_process_set_metadata(self, mocker, mock_classification_class):
        dummy_ids = [0, 1, 2, 3, 4, 5]
        mock_class_field = mocker.patch.object(ClassLabelField, "process")
        mock_image_field = mocker.patch.object(ImageField, "process", return_value=dummy_ids)
        mock_label_field = mocker.patch.object(LabelIdField, "process", return_value=dummy_ids)
        mock_objfield_field = mocker.patch.object(ObjectFieldNamesField, "process")
        mock_objids_field = mocker.patch.object(ObjectIdsField, "process")
        mock_images_per_class_list = mocker.patch.object(ImagesPerClassList, "process")

        data = {"classes": 1, "images": 1, "labels": 1,
                "object_fields": 1, "object_ids": 1, "list_images_per_class": 1}
        mock_classification_class.process_set_metadata(data, 'train')

        mock_class_field.assert_called_once_with()
        mock_image_field.assert_called_once_with()
        mock_label_field.assert_called_once_with()
        mock_objfield_field.assert_called_once_with()
        mock_objids_field.assert_called_once_with(dummy_ids, dummy_ids)
        mock_images_per_class_list.assert_called_once_with()


class TestDatasetAnnotationLoader:
    """Unit tests for the DatasetAnnotationLoader class."""

    @staticmethod
    @pytest.fixture()
    def mock_loader_class():
        return DatasetAnnotationLoader(
            classes=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
            data_path='/some/path/data',
            cache_path='/some/path/cache',
            verbose=True
        )

    def test_task_attributes(self, mocker, mock_loader_class):
        assert mock_loader_class.classes == ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        assert mock_loader_class.data_path == '/some/path/data'
        assert mock_loader_class.cache_path == '/some/path/cache'
        assert mock_loader_class.verbose == True

    def test_load_train_data(self, mocker, mock_loader_class):
        dummy_data = {"dummy": 'data'}
        mock_load_data = mocker.patch.object(DatasetAnnotationLoader, 'load_data_set', return_value=dummy_data)

        data = mock_loader_class.load_train_data()

        mock_load_data.assert_called_once_with(is_test=False)
        assert data == dummy_data

    def test_load_test_data(self, mocker, mock_loader_class):
        dummy_data = {"dummy": 'data'}
        mock_load_data = mocker.patch.object(DatasetAnnotationLoader, 'load_data_set', return_value=dummy_data)

        data = mock_loader_class.load_test_data()

        mock_load_data.assert_called_once_with(is_test=True)
        assert data == dummy_data

    def test_load_data_set(self, mocker, mock_loader_class):
        dummy_images = np.random.rand(10,28,28)
        dummy_labels = np.random.randint(0, 9, 10)
        mock_load_data = mocker.patch.object(DatasetAnnotationLoader, "load_data_annotations", return_value=(dummy_images, dummy_labels))

        set_data = mock_loader_class.load_data_set(is_test=True)

        mock_load_data.assert_called_once_with(True)
        assert set_data['classes'] == ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        assert_array_equal(set_data['images'], dummy_images)
        assert_array_equal(set_data['labels'], dummy_labels)

    @pytest.mark.parametrize('is_test', [False, True])
    def test_load_data_annotations(self, mocker, mock_loader_class, is_test):
        dummy_images = np.random.rand(10*28*28)
        dummy_labels = np.random.randint(0,9,10)
        dummy_set_size = 10
        mock_get_data_test = mocker.patch.object(DatasetAnnotationLoader, "get_data_test", return_value=(dummy_images, dummy_labels, dummy_set_size))
        mock_get_data_train = mocker.patch.object(DatasetAnnotationLoader, "get_data_train", return_value=(dummy_images, dummy_labels, dummy_set_size))

        images, labels = mock_loader_class.load_data_annotations(is_test=is_test)

        if is_test:
            mock_get_data_test.assert_called_once_with()
            mock_get_data_train.assert_not_called()
        else:
            mock_get_data_test.assert_not_called()
            mock_get_data_train.assert_called_once_with()
        assert_array_equal(images, dummy_images.reshape(dummy_set_size, 28, 28))
        assert_array_equal(labels, dummy_labels)

    def test_get_data_test(self, mocker, mock_loader_class):
        dummy_images = np.zeros((5,28*28))
        dummy_labels = np.random.randint(0,9,5)
        mock_load_images = mocker.patch.object(DatasetAnnotationLoader, "load_images_numpy", return_value=dummy_images)
        mock_load_labels = mocker.patch.object(DatasetAnnotationLoader, "load_labels_numpy", return_value=dummy_labels)

        test_images, test_labels, size_test = mock_loader_class.get_data_test()

        mock_load_images.assert_called_once_with(os.path.join('/some/path/data', 't10k-images.idx3-ubyte'))
        mock_load_labels.assert_called_once_with(os.path.join('/some/path/data', 't10k-labels.idx1-ubyte'))
        assert_array_equal(test_images, dummy_images)
        assert_array_equal(test_labels, dummy_labels)
        assert size_test == 10000

    def test_get_data_train(self, mocker, mock_loader_class):
        dummy_images = np.zeros((5,28*28))
        dummy_labels = np.random.randint(0,9,5)
        mock_load_images = mocker.patch.object(DatasetAnnotationLoader, "load_images_numpy", return_value=dummy_images)
        mock_load_labels = mocker.patch.object(DatasetAnnotationLoader, "load_labels_numpy", return_value=dummy_labels)

        train_images, train_labels, size_train = mock_loader_class.get_data_train()

        mock_load_images.assert_called_once_with(os.path.join('/some/path/data', 'train-images.idx3-ubyte'))
        mock_load_labels.assert_called_once_with(os.path.join('/some/path/data', 'train-labels.idx1-ubyte'))
        assert_array_equal(train_images, dummy_images)
        assert_array_equal(train_labels, dummy_labels)
        assert size_train == 60000


@pytest.fixture()
def test_data_loaded():
    classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    images = np.random.rand(10,28, 28)
    labels = np.array(range(10))
    return {
            "classes": classes,
            "images": images,
            "labels": labels
        }


@pytest.fixture()
def field_kwargs(test_data_loaded):
    return {
        "data": test_data_loaded,
        "set_name": 'train',
        "hdf5_manager": {'dummy': 'object'},
        "verbose": True
    }


class TestClassLabelField:
    """Unit tests for the ClassLabelField class."""

    @staticmethod
    @pytest.fixture()
    def mock_classlabel_class(field_kwargs):
        return ClassLabelField(**field_kwargs)

    def test_process(self, mocker, mock_classlabel_class):
        dummy_names = ['car']*10
        mock_get_class = mocker.patch.object(ClassLabelField, "get_class_names", return_value=dummy_names)
        mock_save_hdf5 = mocker.patch.object(ClassLabelField, "save_field_to_hdf5")

        mock_classlabel_class.process()

        mock_get_class.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='classes',
        #     data=str2ascii(dummy_names),
        #     dtype=np.uint8,
        #     fillvalue=-1
        # )

    def test_get_class_names(self, mocker, mock_classlabel_class, test_data_loaded):
        class_names = mock_classlabel_class.get_class_names()

        assert class_names == test_data_loaded['classes']


class TestImageField:
    """Unit tests for the ImageField class."""

    @staticmethod
    @pytest.fixture()
    def mock_image_class(field_kwargs):
        return ImageField(**field_kwargs)

    def test_process(self, mocker, mock_image_class):
        dummy_images = np.random.rand(5, 28, 28)
        dummy_ids = list(range(5))
        mock_get_images = mocker.patch.object(ImageField, "get_images", return_value=(dummy_images, dummy_ids))
        mock_save_hdf5 = mocker.patch.object(ImageField, "save_field_to_hdf5")

        image_ids = mock_image_class.process()

        assert image_ids == dummy_ids
        mock_get_images.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='images',
        #     data=dummy_images,
        #     dtype=np.uint8,
        #     fillvalue=-1
        # )

    def test_get_images(self, mocker, mock_image_class, test_data_loaded):
        images, image_ids = mock_image_class.get_images()

        assert_array_equal(images, test_data_loaded['images'])
        assert image_ids == list(range(len(images)))


class TestLabelIdField:
    """Unit tests for the LabelIdField class."""

    @staticmethod
    @pytest.fixture()
    def mock_label_class(field_kwargs):
        return LabelIdField(**field_kwargs)

    def test_process(self, mocker, mock_label_class):
        dummy_labels = np.array(range(10))
        dummy_ids = list(range(10))
        mock_get_labels = mocker.patch.object(LabelIdField, "get_labels", return_value=(dummy_labels, dummy_ids))
        mock_save_hdf5 = mocker.patch.object(LabelIdField, "save_field_to_hdf5")

        label_ids = mock_label_class.process()

        assert label_ids == dummy_ids
        mock_get_labels.assert_called_once_with()
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='labels',
        #     data=dummy_labels,
        #     dtype=np.uint8,
        #     fillvalue=0
        # )

    def test_get_images(self, mocker, mock_label_class, test_data_loaded):
        labels, label_ids = mock_label_class.get_labels()

        assert_array_equal(labels, test_data_loaded['labels'])
        assert label_ids == list(range(len(labels)))


class TestObjectFieldNamesField:
    """Unit tests for the ObjectFieldNamesField class."""

    @staticmethod
    @pytest.fixture()
    def mock_objfields_class(field_kwargs):
        return ObjectFieldNamesField(**field_kwargs)

    def test_process(self, mocker, mock_objfields_class):
        mock_save_hdf5 = mocker.patch.object(ObjectFieldNamesField, "save_field_to_hdf5")

        mock_objfields_class.process()

        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='object_fields',
        #     data=str2ascii(['images', 'labels']),
        #     dtype=np.uint8,
        #     fillvalue=0
        # )


class TestObjectIdsField:
    """Unit tests for the ObjectIdsField class."""

    @staticmethod
    @pytest.fixture()
    def mock_objfids_class(field_kwargs):
        return ObjectIdsField(**field_kwargs)

    def test_process(self, mocker, mock_objfids_class):
        mock_save_hdf5 = mocker.patch.object(ObjectIdsField, "save_field_to_hdf5")

        image_ids = [0, 1, 2, 3, 4, 5]
        label_ids = [1, 5, 9, 8, 3, 5]
        object_ids = mock_objfids_class.process(
            image_ids=image_ids,
            label_ids=label_ids
        )

        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='object_ids',
        #     data=np.array([[0, 1], [1, 5], [2, 9], [3, 8], [4, 3], [5, 5]], dtype=np.int32),
        #     dtype=np.int32,
        #     fillvalue=-1
        # )

  # )


class TestImagesPerClassList:
    """Unit tests for the ImagesPerClassList class."""

    @staticmethod
    @pytest.fixture()
    def mock_img_per_class_list(field_kwargs):
        return ImagesPerClassList(**field_kwargs)

    def test_process(self, mocker, mock_img_per_class_list):
        dummy_ids = [[0], [2, 3], [4, 5]]
        dummy_array = np.array([[0, -1], [2, 3], [4, 5]])
        mock_get_ids = mocker.patch.object(ImagesPerClassList, "get_image_ids_per_class", return_value=dummy_ids)
        mock_convert_array = mocker.patch.object(ImagesPerClassList, "convert_list_to_array", return_value=dummy_array)
        mock_save_hdf5 = mocker.patch.object(ImagesPerClassList, "save_field_to_hdf5")

        mock_img_per_class_list.process()

        mock_get_ids.assert_called_once_with()
        mock_convert_array.assert_called_once_with(dummy_ids)
        assert mock_save_hdf5.called
        # **disabled until I find a way to do assert calls with numpy arrays**
        # mock_save_hdf5.assert_called_once_with(
        #     set_name='train',
        #     field='list_images_per_class',
        #     data=dummy_array,
        #     dtype=np.int32,
        #     fillvalue=-1
        # )

    def test_get_image_ids_per_class(self, mocker, mock_img_per_class_list):
        images_per_class_ids = mock_img_per_class_list.get_image_ids_per_class()

        assert images_per_class_ids == [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]]

    def test_convert_list_to_array(self, mocker, mock_img_per_class_list):
        list_ids = [[0], [2, 3], [4, 5, 6]]
        images_per_class_array = mock_img_per_class_list.convert_list_to_array(list_ids)

        expected = np.array(pad_list([[0, -1, -1], [2, 3, -1], [4, 5, 6]], -1), dtype=np.int32)
        assert_array_equal(images_per_class_array, expected)
