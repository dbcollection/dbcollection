"""
Test the base classes for managing datasets and tasks.
"""


import os
import sys
import pytest
import numpy as np

from dbcollection.datasets.mnist import Classification


@pytest.fixture()
def mock_classification_class():
    return Classification(data_path='/some/path/data', cache_path='/some/path/cache')


class TestClassificationTask:
    """Unit tests for the mnist Classification task."""

    def test_task_attributes(self, mocker, mock_classification_class):
        assert mock_classification_class.filename_h5 == 'classification'
        classes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        assert mock_classification_class.classes == classes

    def test_load_data(self, mocker, mock_classification_class):
        mock_load_data_train = mocker.patch.object(Classification, "load_data_train", return_value=['some_train_data'])
        mock_load_data_test = mocker.patch.object(Classification, "load_data_test", return_value=['some_test_data'])

        load_data_generator = mock_classification_class.load_data()
        if sys.version[0] == '3':
            train_data = load_data_generator.__next__()
            test_data = load_data_generator.__next__()
        else:
            train_data = load_data_generator.next()
            test_data = load_data_generator.next()

        mock_load_data_train.assert_called_once_with()
        mock_load_data_test.assert_called_once_with()
        assert train_data == {"train": ['some_train_data']}
        assert test_data == {"test": ['some_test_data']}
