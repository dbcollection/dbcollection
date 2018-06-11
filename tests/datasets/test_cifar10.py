"""
Test the base classes for managing datasets and tasks.
"""


import os
import sys
import pytest
import numpy as np
from numpy.testing import assert_array_equal

from dbcollection.datasets.cifar.cifar10 import Classification
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii


@pytest.fixture()
def mock_classification_class():
    return Classification(data_path='/some/path/data', cache_path='/some/path/cache')


class TestClassificationTask:
    """Unit tests for the cifar10 Classification task."""

    def test_task_attributes(self, mocker, mock_classification_class):
        assert mock_classification_class.filename_h5 == 'classification'
        assert mock_classification_class.data_files == ["batches.meta",
                                                        "data_batch_1",
                                                        "data_batch_2",
                                                        "data_batch_3",
                                                        "data_batch_4",
                                                        "data_batch_5",
                                                        "test_batch"]

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

    def test_load_data_set(self, mocker, mock_classification_class):
        mock_load_annotations = mocker.patch.object(Classification, "load_data_annotations", return_value=('data', 'labels', {"label_names": 'some_class'}))
        mock_get_object_list = mocker.patch.object(Classification, "get_object_list", return_value=list(range(10)))
        mock_get_list = mocker.patch.object(Classification, "get_images_per_class", return_value=list(range(5)))

        set_data = mock_classification_class.load_data_set(False)

        mock_load_annotations.assert_called_once_with(False)
        mock_get_object_list.assert_called_once_with('data', 'labels')
        mock_get_list.assert_called_once_with('labels')
        assert_array_equal(set_data['object_fields'], str2ascii(['images', 'classes']))
        assert_array_equal(set_data['classes'], str2ascii(['some_class']))
        assert set_data['images'] == 'data'
        assert set_data['labels'] == 'labels'
        assert set_data['object_ids'] == list(range(10))
        assert set_data['list_images_per_class'] == list(range(5))

    @pytest.mark.parametrize('is_test', [False, True])
    def test_load_data_annotations_for_train_set(self, mocker, mock_classification_class, is_test):
        random_data = np.random.rand(20,3,32,32)
        mock_get_names = mocker.patch.object(Classification, "get_class_names", return_value=['some', 'class', 'names'])
        mock_get_data_test = mocker.patch.object(Classification, "get_data_test", return_value=(random_data, np.array(range(10))))
        mock_get_data_train = mocker.patch.object(Classification, "get_data_train", return_value=(random_data, np.array(range(10))))

        data_path = os.path.join(mock_classification_class.data_path, 'cifar-10-batches-py')
        data, labels, class_names = mock_classification_class.load_data_annotations(is_test=is_test)

        mock_get_names.assert_called_once_with(data_path)
        if is_test:
            mock_get_data_test.assert_called_once_with(data_path)
            assert not mock_get_data_train.called
        else:
            assert not mock_get_data_test.called
            mock_get_data_train.assert_called_once_with(data_path)
        assert_array_equal(data, np.transpose(random_data, (0, 2, 3, 1)))
        assert_array_equal(labels, np.array(range(10)))
        assert class_names == ['some', 'class', 'names']

    def test_get_class_names(self, mocker, mock_classification_class):
        mock_load_annot_file = mocker.patch.object(Classification, "load_annotation_file", return_value='dummy_data')

        path = mock_classification_class.data_path
        result = mock_classification_class.get_class_names(path)

        filename = os.path.join(path, "batches.meta")
        mock_load_annot_file.assert_called_once_with(filename)
        assert result == 'dummy_data'

    def test_get_data_train(self, mocker, mock_classification_class):
        test_data = {
            "data": np.random.rand(10, 3*32*32),
            "labels": np.random.randint(0, 9, (10,))
        }
        test_data_concat = np.concatenate(
            (test_data['data'], test_data['data'], test_data['data'], test_data['data'], test_data['data']),
            axis=0
        )
        output_data = test_data_concat.reshape(50,3,32,32)
        mock_load_annot_file = mocker.patch.object(Classification, "load_annotation_file", return_value=test_data)
        mock_reshape_array = mocker.patch.object(Classification, "reshape_array", return_value=output_data)

        path = mock_classification_class.data_path
        data, labels = mock_classification_class.get_data_train(path)

        assert mock_load_annot_file.called
        assert mock_load_annot_file.call_count == 5
        #mock_reshape_array.assert_called_once_with(test_data_concat, 50000)
        assert mock_reshape_array.called
        assert_array_equal(data, output_data)
        assert_array_equal(labels, np.concatenate(
            (test_data['labels'], test_data['labels'], test_data['labels'], test_data['labels'], test_data['labels']),
            axis=0)
        )

    def test_reshape_array(self, mocker, mock_classification_class):
        data = np.random.rand(20, 3*32*32)

        result = mock_classification_class.reshape_array(data, 20)

        assert_array_equal(result, data.reshape(20, 3, 32, 32))

    def test_get_data_test(self, mocker, mock_classification_class):
        test_data = {
            "data": np.random.rand(10, 3*32*32),
            "labels": np.random.randint(0, 9, (10,))
        }
        mock_load_annot_file = mocker.patch.object(Classification, "load_annotation_file", return_value=test_data)
        mock_reshape_array = mocker.patch.object(Classification, "reshape_array", return_value=test_data['data'].reshape(10, 3, 32, 32))

        path = mock_classification_class.data_path
        data, labels = mock_classification_class.get_data_test(path)

        mock_load_annot_file.assert_called_once_with(os.path.join(path, 'test_batch'))
        mock_reshape_array.assert_called_once_with(test_data['data'], 10000)
        assert_array_equal(data, test_data['data'].reshape((10, 3, 32, 32)))
        assert_array_equal(labels, test_data['labels'])

    def test_get_object_list(self, mocker, mock_classification_class):
        data = np.random.rand(20,2,32,32)
        labels = np.array(range(20))

        object_ids = mock_classification_class.get_object_list(data, labels)

        assert_array_equal(object_ids, np.array([[i, labels[i]] for i in range(20)]))

    def test_get_images_per_class(self, mocker, mock_classification_class):
        labels = np.array([1,1,1,1,0,1,1,0])

        images_per_class = mock_classification_class.get_images_per_class(labels)

        expected = np.array([[4, 7, -1, -1, -1, -1],
                             [0, 1, 2, 3, 5, 6]],
                             dtype=np.int32)
        assert_array_equal(images_per_class, expected)

    def test_process_set_metadata(self, mocker, mock_classification_class):
        mock_save_hdf5 = mocker.patch.object(Classification, "save_field_to_hdf5")

        data = {"classes": 1, "images": 1, "labels": 1,
                "object_fields": 1, "object_ids": 1, "list_images_per_class": 1}
        mock_classification_class.process_set_metadata(data, 'train')

        assert mock_save_hdf5.called
        assert mock_save_hdf5.call_count == 6
