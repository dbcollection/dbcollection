"""
Test the base classes for managing datasets and tasks.

Dataset: Caltech Pedestrian

Tasks: Detection, Detection10x, Detection30x
"""


import os
import sys
import pytest
import numpy as np


from dbcollection.datasets.caltech.caltech_pedestrian import Detection


@pytest.fixture()
def mock_detection_class():
    return Detection(data_path='/some/path/data', cache_path='/some/path/cache')


class TestDetectionTask:
    """Unit tests for the caltech pedestrian Detection task."""

    def test_task_attributes(self, mocker, mock_detection_class):
        assert mock_detection_class.filename_h5 == 'detection'
        assert mock_detection_class.skip_step == 30
        assert mock_detection_class.classes == ('person', 'person-fa', 'people', 'person?')
        assert mock_detection_class.sets == {
            "train": ('set00', 'set01', 'set02', 'set03', 'set04', 'set05'),
            "test": ('set06', 'set07', 'set08', 'set09', 'set10')
        }

