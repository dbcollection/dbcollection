"""
Test the base classes for managing datasets and tasks.
"""


import os
import sys
import pytest
import numpy as np
from numpy.testing import assert_array_equal

from dbcollection.datasets.mpii_pose.keypoints import Keypoints, DatasetAnnotationLoader


class TestKeypointsTask:
    """Unit tests for the mpii Keypoints task."""

    @staticmethod
    @pytest.fixture()
    def mock_keypoints_class():
        return Keypoints(data_path='/some/path/data', cache_path='/some/path/cache')

    def test_task_attributes(self, mocker, mock_keypoints_class):
        assert mock_keypoints_class.filename_h5 == 'keypoint'
        assert mock_keypoints_class.is_full == False
        assert mock_keypoints_class.keypoints_labels == [
            'right ankle',  # -- 1
            'right knee',  # -- 2
            'right hip',  # -- 3
            'left hip',  # -- 4
            'left knee',  # -- 5
            'left ankle',  # -- 6
            'pelvis',  # -- 7
            'thorax',  # -- 8
            'upper neck',  # -- 9
            'head top',  # -- 10
            'right wrist',  # -- 11
            'right elbow',  # -- 12
            'right shoulder',  # -- 13
            'left shoulder',  # -- 14
            'left elbow',  # -- 15
            'left wrist'  # -- 16
        ]


class TestDatasetAnnotationLoader:
    """Unit tests for DatasetAnnotationLoader class."""

    @staticmethod
    @pytest.fixture()
    def mock_loader_class():
        return DatasetAnnotationLoader(
            keypoints_labels=[
                'right ankle',
                'right knee',
                'right hip',
                'left hip',
                'left knee',
                'left ankle',
                'pelvis',
                'thorax',
                'upper neck',
                'head top',
                'right wrist',
                'right elbow',
                'right shoulder',
                'left shoulder',
                'left elbow',
                'left wrist'
            ],
            is_full=False,
            data_path='/some/path/data',
            cache_path='/some/path/cache',
            verbose=True
        )

    def test_task_attributes(self, mocker, mock_loader_class):
        assert mock_loader_class.keypoints_labels == [
            'right ankle',
            'right knee',
            'right hip',
            'left hip',
            'left knee',
            'left ankle',
            'pelvis',
            'thorax',
            'upper neck',
            'head top',
            'right wrist',
            'right elbow',
            'right shoulder',
            'left shoulder',
            'left elbow',
            'left wrist'
        ]
        assert mock_loader_class.is_full == False
        assert mock_loader_class.data_path=='/some/path/data'
        assert mock_loader_class.cache_path=='/some/path/cache'
        assert mock_loader_class.verbose==True

    def test_load_trainval_data(self, mocker, mock_loader_class):
        dummy_data = {"dummy": 'data'}
        mock_load_annotations = mocker.patch.object(DatasetAnnotationLoader, "load_annotations_set", return_value=dummy_data)

        annotations = mock_loader_class.load_trainval_data()

        assert annotations == dummy_data
        mock_load_annotations.assert_called_once_with(is_test=False)

    def test_load_train_data(self, mocker, mock_loader_class):
        dummy_data = {"dummy": 'data'}
        dummy_image_ids = [5,6,78,2,1,6,78,41,2]
        dummy_data_filtered = {"dummy": 'filtered'}
        mock_load_annotations = mocker.patch.object(DatasetAnnotationLoader, "load_annotations_set", return_value=dummy_data)
        mock_filter_annotations = mocker.patch.object(DatasetAnnotationLoader, "filter_annotations_by_ids", return_value=dummy_data_filtered)

        annotations = mock_loader_class.load_train_data(dummy_image_ids)

        assert annotations == dummy_data_filtered
        mock_load_annotations.assert_called_once_with(is_test=False)
        mock_filter_annotations.assert_called_once_with(dummy_data, dummy_image_ids)

    def test_load_val_data(self, mocker, mock_loader_class):
        dummy_data = {"dummy": 'data'}
        dummy_image_ids = [9,67,133,65]
        dummy_data_filtered = {"dummy": 'filtered'}
        mock_load_annotations = mocker.patch.object(DatasetAnnotationLoader, "load_annotations_set", return_value=dummy_data)
        mock_filter_annotations = mocker.patch.object(DatasetAnnotationLoader, "filter_annotations_by_ids", return_value=dummy_data_filtered)

        annotations = mock_loader_class.load_val_data(dummy_image_ids)

        assert annotations == dummy_data_filtered
        mock_load_annotations.assert_called_once_with(is_test=False)
        mock_filter_annotations.assert_called_once_with(dummy_data, dummy_image_ids)

    def test_load_test_data(self, mocker, mock_loader_class):
        dummy_data = {"dummy": 'data'}
        mock_load_annotations = mocker.patch.object(DatasetAnnotationLoader, "load_annotations_set", return_value=dummy_data)

        annotations = mock_loader_class.load_test_data()

        assert annotations == dummy_data
        mock_load_annotations.assert_called_once_with(is_test=True)
