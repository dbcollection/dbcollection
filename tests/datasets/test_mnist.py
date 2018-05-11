"""
Test the base classes for managing datasets and tasks.
"""


import os
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
