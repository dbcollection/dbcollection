.. _ucf_101_readme:

===========================
UCF101 - Action Recognition
===========================

**UCF101** is an action recognition data set of realistic action videos, collected from YouTube,
having 101 action categories. This data set is an extension of **UCF50** data set which has 50 action
categories.

With 13320 videos from 101 action categories, **UCF101** gives the largest diversity in terms of
actions and with the presence of large variations in camera motion, object appearance and pose,
object scale, viewpoint, cluttered background, illumination conditions, etc, it is the most
challenging data set to date.

The videos in 101 action categories are grouped into 25 groups, where each group can consist of
4-7 videos of an action.

Use cases
=========

Human action recognition in videos.


Properties
==========

- ``name``: ucf_101
- ``keywords``: image_processing, recognition, activity, human, single_person
- ``dataset size``: 6,9 GB
- ``is downloadable``: **yes**
- ``tasks``:
    - recognition: **(default)**
        - ``primary use``: action recognition in videos
        - ``description``: Contains videos and action label annotations for action recognition
        - ``sets``: train01, train02, train03, test01, test02, test03
        - ``metadata file size in disk``: 14,5 MB
        - ``has annotations``: **yes**
            - ``which``:
                - activity labels for each video.


Metadata structure (HDF5)
=========================

Task: recognition
-----------------

::

    /
    ├── train01/
    │   ├── activities        # dtype=np.uint8, shape=(101,19)        (note: string in ASCII format)
    │   ├── image_filenames   # dtype=np.uint8, shape=(1788425,113)   (note: string in ASCII format)
    │   ├── total_frames      # dtype=np.int32, shape=(9537,)
    │   ├── video_filenames   # dtype=np.uint8, shape=(9537,60)
    │   ├── videos            # dtype=np.uint8, shape=(9537,29)       (note: string in ASCII format)
    │   ├── object_fields     # dtype=np.uint8, shape=(5,31)          (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(9537,5)
    │   ├── list_image_filenames_per_video   # dtype=np.int32, shape=(9537,1776)
    │   └── list_videos_per_activity         # dtype=np.int32, shape=(101,121)
    │
    ├── test01/
    │   ├── activities        # dtype=np.uint8, shape=(101,19)       (note: string in ASCII format)
    │   ├── image_filenames   # dtype=np.uint8, shape=(697865,113)   (note: string in ASCII format)
    │   ├── total_frames      # dtype=np.int32, shape=(3783,)
    │   ├── video_filenames   # dtype=np.uint8, shape=(3783,60)
    │   ├── videos            # dtype=np.uint8, shape=(3783,29)      (note: string in ASCII format)
    │   ├── object_fields     # dtype=np.uint8, shape=(5,31)         (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(3783,5)
    │   ├── list_image_filenames_per_video   # dtype=np.int32, shape=(3783,900)
    │   └── list_videos_per_activity         # dtype=np.int32, shape=(101,49)
    │
    ├── train02/
    │   ├── activities        # dtype=np.uint8, shape=(101,19)        (note: string in ASCII format)
    │   ├── image_filenames   # dtype=np.uint8, shape=(1791290,113)   (note: string in ASCII format)
    │   ├── total_frames      # dtype=np.int32, shape=(9586,)
    │   ├── video_filenames   # dtype=np.uint8, shape=(9586,60)
    │   ├── videos            # dtype=np.uint8, shape=(9586,29)       (note: string in ASCII format)
    │   ├── object_fields     # dtype=np.uint8, shape=(5,31)          (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(9586,5)
    │   ├── list_image_filenames_per_video   # dtype=np.int32, shape=(9586,1776)
    │   └── list_videos_per_activity         # dtype=np.int32, shape=(101,122)
    │
    ├── test02/
    │   ├── activities        # dtype=np.uint8, shape=(101,19)       (note: string in ASCII format)
    │   ├── image_filenames   # dtype=np.uint8, shape=(695000,113)   (note: string in ASCII format)
    │   ├── total_frames      # dtype=np.int32, shape=(3734,)
    │   ├── video_filenames   # dtype=np.uint8, shape=(3734,60)
    │   ├── videos            # dtype=np.uint8, shape=(3734,29)      (note: string in ASCII format)
    │   ├── object_fields     # dtype=np.uint8, shape=(5,31)         (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(3734,5)
    │   ├── list_image_filenames_per_video   # dtype=np.int32, shape=(3734,833)
    │   └── list_videos_per_activity         # dtype=np.int32, shape=(101,49)
    │
    ├── train03/
    │   ├── activities        # dtype=np.uint8, shape=(101,19)        (note: string in ASCII format)
    │   ├── image_filenames   # dtype=np.uint8, shape=(1786111,113)   (note: string in ASCII format)
    │   ├── total_frames      # dtype=np.int32, shape=(9624,)
    │   ├── video_filenames   # dtype=np.uint8, shape=(9624,60)
    │   ├── videos            # dtype=np.uint8, shape=(9624,29)       (note: string in ASCII format)
    │   ├── object_fields     # dtype=np.uint8, shape=(5,31)          (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(9624,5)
    │   ├── list_image_filenames_per_video   # dtype=np.int32, shape=(9624,900)
    │   └── list_videos_per_activity         # dtype=np.int32, shape=(101,124)
    │
    └── test03/
        ├── activities        # dtype=np.uint8, shape=(101,19)       (note: string in ASCII format)
        ├── image_filenames   # dtype=np.uint8, shape=(700157,113)   (note: string in ASCII format)
        ├── total_frames      # dtype=np.int32, shape=(3696,)
        ├── video_filenames   # dtype=np.uint8, shape=(3696,60)
        ├── videos            # dtype=np.uint8, shape=(3696,29)      (note: string in ASCII format)
        ├── object_fields     # dtype=np.uint8, shape=(5,31)         (note: string in ASCII format)
        ├── object_ids        # dtype=np.int32, shape=(3696,5)
        ├── list_image_filenames_per_video   # dtype=np.int32, shape=(3696,1776)
        └── list_videos_per_activity         # dtype=np.int32, shape=(101,48)


Fields
^^^^^^

- ``activities``: activity names
    - ``available in``: train01,  train02,  train03,  test01,  test02,  test03
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``image_filenames``: image file path+name
    - ``available in``: train01,  train02,  train03,  test01,  test02,  test03
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``total_frames``: number of frames per video
    - ``available in``: train01,  train02,  train03,  test01,  test02,  test03
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``videos``: video name
    - ``available in``: train01,  train02,  train03,  test01,  test02,  test03
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``video_filenames``: video file path+name
    - ``available in``: train01,  train02,  train03,  test01,  test02,  test03
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``object_fields``: list of field names of the object id list
    - ``available in``: train01,  train02,  train03,  test01,  test02,  test03
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
    - ``note``: key field (*field name* aggregator)
- ``object_ids``: list of field ids
    - ``available in``: train01,  train02,  train03,  test01,  test02,  test03
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: key field (*field id* aggregator)
- ``list_image_filenames_per_video``: list of image ids per video
    - ``available in``: train01,  train02,  train03,  test01,  test02,  test03
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_videos_per_activity``: list of video ids per activity
    - ``available in``: train01,  train02,  train03,  test01,  test02,  test03
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list


Disclaimer
==========

All rights reserved to the original creators of **UCF101**.

For information about the dataset and its terms of use, please see this `link <http://crcv.ucf.edu/data/UCF101.php>`_.