"""
Test the base classes for managing datasets and tasks.
"""


import os
import sys
import pytest
import numpy as np
from numpy.testing import assert_array_equal

from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.datasets.mnist.classification import (
    Classification,
    DatasetAnnotationLoader
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
        mock_load_data = mocker.patch.object(Classification, "load_data_set", return_value=['some_data'])

        load_data_generator = mock_classification_class.load_data()
        if sys.version[0] == '3':
            train_data = load_data_generator.__next__()
            test_data = load_data_generator.__next__()
        else:
            train_data = load_data_generator.next()
            test_data = load_data_generator.next()

        assert mock_load_data.called
        assert train_data == {"train": ['some_data']}
        assert test_data == {"test": ['some_data']}

    @pytest.mark.parametrize('is_test', [False, True])
    def test_load_data_set(self, mocker, mock_classification_class, classes_classification, is_test):
        images, labels, size_set = (np.random.rand(10, 784), np.array(range(10)), 10)
        mock_get_data_train= mocker.patch.object(Classification, "get_train_data", return_value=(images, labels, size_set))
        mock_get_data_test= mocker.patch.object(Classification, "get_test_data", return_value=(images, labels, size_set))
        mock_get_list = mocker.patch.object(Classification, "get_list_images_per_class", return_value=list(range(10)))

        set_data = mock_classification_class.load_data_set(is_test=is_test)

        if is_test:
            mock_get_data_test.assert_called_once_with()
            assert not mock_get_data_train.called
        else:
            mock_get_data_train.assert_called_once_with()
            assert not mock_get_data_test.called
        mock_get_list.assert_called_once_with(labels)
        assert_array_equal(set_data['classes'], str2ascii(classes_classification))
        assert_array_equal(set_data['images'], images.reshape(size_set, 28, 28))
        assert_array_equal(set_data['labels'], labels)
        assert_array_equal(set_data['object_fields'], str2ascii(['images', 'labels']))
        assert_array_equal(set_data['object_ids'], np.array([[i, labels[i]] for i in range(size_set)]))
        assert set_data['list_images_per_class'] == list(range(10))

    def test_get_train_data(self, mocker, mock_classification_class):
        mock_load_images = mocker.patch.object(Classification, "load_images_numpy", return_value=np.zeros((5,768)))
        mock_load_labels = mocker.patch.object(Classification, "load_labels_numpy", return_value=np.ones(5))

        train_images, train_labels, size_train = mock_classification_class.get_train_data()

        mock_load_images.assert_called_once_with(os.path.join('/some/path/data', 'train-images.idx3-ubyte'))
        mock_load_labels.assert_called_once_with(os.path.join('/some/path/data', 'train-labels.idx1-ubyte'))
        assert_array_equal(train_images, np.zeros((5,768)))
        assert_array_equal(train_labels, np.ones(5))
        assert size_train == 60000

    def test_get_list_images_per_class(self, mocker, mock_classification_class):
        labels = np.array([1,1,1,1,0,1,1,0])

        images_per_class = mock_classification_class.get_list_images_per_class(labels)

        expected = np.array([[4, 7, -1, -1, -1, -1],
                             [0, 1, 2, 3, 5, 6]],
                             dtype=np.int32)
        assert_array_equal(images_per_class, expected)

    def test_get_test_data(self, mocker, mock_classification_class):
        mock_load_images = mocker.patch.object(Classification, "load_images_numpy", return_value=np.zeros((5,768)))
        mock_load_labels = mocker.patch.object(Classification, "load_labels_numpy", return_value=np.ones(5))

        test_images, test_labels, size_test = mock_classification_class.get_test_data()

        mock_load_images.assert_called_once_with(os.path.join('/some/path/data', 't10k-images.idx3-ubyte'))
        mock_load_labels.assert_called_once_with(os.path.join('/some/path/data', 't10k-labels.idx1-ubyte'))
        assert_array_equal(test_images, np.zeros((5,768)))
        assert_array_equal(test_labels, np.ones(5))
        assert size_test == 10000

    def test_process_set_metadata(self, mocker, mock_classification_class):
        mock_save_hdf5 = mocker.patch.object(Classification, "save_field_to_hdf5")

        data = {"classes": 1, "images": 1, "labels": 1,
                "object_fields": 1, "object_ids": 1, "list_images_per_class": 1}
        mock_classification_class.process_set_metadata(data, 'train')

        assert mock_save_hdf5.called
        assert mock_save_hdf5.call_count == 6


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
