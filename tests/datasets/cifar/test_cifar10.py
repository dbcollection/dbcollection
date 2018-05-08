"""
Test the base classes for managing datasets and tasks.
"""


import os
import pytest
import numpy as np
from numpy.testing import assert_array_equal

from dbcollection.datasets.cifar.cifar10 import Classification
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii


@pytest.fixture()
def mock_classification_class():
    return Classification(data_path='/some/path/data', cache_path='/some/path/cache')


class TestClassification:
    """Unit tests for the BaseDatasetNew class."""

    def test_load_data(self, mocker, mock_classification_class):
        mock_load_data = mocker.patch.object(Classification, "load_data_set", return_value=['some_data'])

        load_data_generator = mock_classification_class.load_data()
        train_data = load_data_generator.__next__()
        test_data = load_data_generator.__next__()

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
        assert_array_equal(set_data['class_name'], str2ascii(['some_class']))
        assert set_data['data'] == 'data'
        assert set_data['labels'] == 'labels'
        assert set_data['object_ids'] == list(range(10))
        assert set_data['list_images_per_class'] == list(range(5))
