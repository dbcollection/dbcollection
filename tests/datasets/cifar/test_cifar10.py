"""
Test the base classes for managing datasets and tasks.
"""


import os
import pytest
import numpy as np

from dbcollection.datasets.cifar.cifar10 import Classification


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
