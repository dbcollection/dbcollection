"""
Test ucf101 hdf5 file contents.
"""


import pytest
import dbcollection.manager as dbc
from dbcollection.utils.cache import CacheManager
from dbcollection.utils.string_ascii import convert_ascii_to_str as ascii2str

name = 'ucf101'
cache_manager = CacheManager(is_test=True)


@pytest.mark.skiptif(not cache_manager.is_task(name, 'recognition'),
                     reason='Dataset is not available for testing: {}'.format(name))
def test_ucf101__task_recognition():
    ucf101 = dbc.load(name=name, task='recognition')

    assert set(ucf101.sets) == set(['train', 'test'])

    # check train01 values
    assert ascii2str(ucf101.get('train01', 'activities', 0)) == 'ApplyEyeMakeup'
    assert ascii2str(ucf101.get('train01', 'videos', 0)) == 'v_ApplyEyeMakeup_g08_c01'
    assert set(ucf101.list('train01')) == set(['videos', 'video_filenames',
                                               'list_image_filenames_per_video',
                                               'activities', 'total_frames'])

    # check test01 values
    assert ascii2str(ucf101.get('test01', 'activities', 0)) == 'ApplyEyeMakeup'
    assert ascii2str(ucf101.get('test01', 'videos', 0)) == 'v_ApplyEyeMakeup_g01_c01'
    assert set(ucf101.list('test01')) == set(['videos', 'video_filenames',
                                              'list_image_filenames_per_video',
                                              'activities', 'total_frames'])

