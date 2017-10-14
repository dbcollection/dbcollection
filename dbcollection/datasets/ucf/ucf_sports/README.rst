.. _ucf_sports_readme:

=================
UCF Sports Action
=================

**UCF Sports** dataset consists of a set of actions collected from various sports
which are typically featured on broadcast television channels such as the BBC and
ESPN. The video sequences were obtained from a wide range of stock footage websites
including BBC Motion gallery and GettyImages.

The dataset includes a total of 150 sequences with the resolution of 720 x 480.
The collection represents a natural pool of actions featured in a wide range of
scenes and viewpoints.


Use cases
=========

Human action recognition in videos.


Properties
==========

- ``name``: ucf_sports
- ``keywords``: image_processing, recognition, detection, activity, human, single_person
- ``dataset size``: 1,8 GB
- ``is downloadable``: **yes**
- ``tasks``:
    - recognition: **(default)**
        - ``primary use``: action recognition in videos
        - ``description``: Contains videos and action label annotations for action recognition
        - ``sets``: train01, train02, train03, train04, train05, test01, test02, test03, test04, test05
        - ``metadata file size in disk``: 1,0 MB
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
    │   ├── activities        # dtype=np.uint8, shape=(10,14)     (note: string in ASCII format)
    │   ├── boxes             # dtype=np.int32, shape=(6548,4)
    │   ├── image_filenames   # dtype=np.uint8, shape=(6548,74)   (note: string in ASCII format)
    │   ├── videos            # dtype=np.uint8, shape=(103,24)    (note: string in ASCII format)
    │   ├── object_fields     # dtype=np.uint8, shape=(4,16)      (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(6548,4)
    │   ├── list_boxes_per_video        # dtype=np.int32, shape=(103,127)
    │   ├── list_filenames_per_video    # dtype=np.int32, shape=(103,127)
    │   ├── list_object_ids_per_video   # dtype=np.int32, shape=(103,127)
    │   └── list_videos_per_activity    # dtype=np.int32, shape=(10,15)
    │
    ├── test01/
    │   ├── activities        # dtype=np.uint8, shape=(10,14)     (note: string in ASCII format)
    │   ├── boxes             # dtype=np.int32, shape=(3032,4)
    │   ├── image_filenames   # dtype=np.uint8, shape=(3032,76)   (note: string in ASCII format)
    │   ├── videos            # dtype=np.uint8, shape=(47,24)     (note: string in ASCII format)
    │   ├── object_fields     # dtype=np.uint8, shape=(4,16)      (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(3032,4)
    │   ├── list_boxes_per_video        # dtype=np.int32, shape=(47,144)
    │   ├── list_filenames_per_video    # dtype=np.int32, shape=(47,144)
    │   ├── list_object_ids_per_video   # dtype=np.int32, shape=(47,144)
    │   └── list_videos_per_activity    # dtype=np.int32, shape=(10,7)
    │
    ├── train02/
    │   ├── activities        # dtype=np.uint8, shape=(10,14)     (note: string in ASCII format)
    │   ├── boxes             # dtype=np.int32, shape=(6529,4)
    │   ├── image_filenames   # dtype=np.uint8, shape=(6529,76)   (note: string in ASCII format)
    │   ├── videos            # dtype=np.uint8, shape=(103,24)    (note: string in ASCII format)
    │   ├── object_fields     # dtype=np.uint8, shape=(4,16)      (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(6529,4)
    │   ├── list_boxes_per_video        # dtype=np.int32, shape=(103,144)
    │   ├── list_filenames_per_video    # dtype=np.int32, shape=(103,144)
    │   ├── list_object_ids_per_video   # dtype=np.int32, shape=(103,144)
    │   └── list_videos_per_activity    # dtype=np.int32, shape=(10,15)
    │
    ├── test02/
    │   ├── activities        # dtype=np.uint8, shape=(10,14)     (note: string in ASCII format)
    │   ├── boxes             # dtype=np.int32, shape=(3051,4)
    │   ├── image_filenames   # dtype=np.uint8, shape=(3051,74)   (note: string in ASCII format)
    │   ├── videos            # dtype=np.uint8, shape=(47,24)     (note: string in ASCII format)
    │   ├── object_fields     # dtype=np.uint8, shape=(4,16)      (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(3051,4)
    │   ├── list_boxes_per_video        # dtype=np.int32, shape=(47,123)
    │   ├── list_filenames_per_video    # dtype=np.int32, shape=(47,123)
    │   ├── list_object_ids_per_video   # dtype=np.int32, shape=(47,123)
    │   └── list_videos_per_activity    # dtype=np.int32, shape=(10,7)
    │
    ├── train03/
    │   ├── activities        # dtype=np.uint8, shape=(10,14)     (note: string in ASCII format)
    │   ├── boxes             # dtype=np.int32, shape=(6537,4)
    │   ├── image_filenames   # dtype=np.uint8, shape=(6537,74)   (note: string in ASCII format)
    │   ├── videos            # dtype=np.uint8, shape=(103,24)    (note: string in ASCII format)
    │   ├── object_fields     # dtype=np.uint8, shape=(4,16)      (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(6537,4)
    │   ├── list_boxes_per_video        # dtype=np.int32, shape=(103,144)
    │   ├── list_filenames_per_video    # dtype=np.int32, shape=(103,144)
    │   ├── list_object_ids_per_video   # dtype=np.int32, shape=(103,144)
    │   └── list_videos_per_activity    # dtype=np.int32, shape=(10,15)
    │
    ├── test03/
    │   ├── activities        # dtype=np.uint8, shape=(10,14)     (note: string in ASCII format)
    │   ├── boxes             # dtype=np.int32, shape=(3034,4)
    │   ├── image_filenames   # dtype=np.uint8, shape=(3034,76)   (note: string in ASCII format)
    │   ├── videos            # dtype=np.uint8, shape=(47,24)     (note: string in ASCII format)
    │   ├── object_fields     # dtype=np.uint8, shape=(4,16)      (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(3034,4)
    │   ├── list_boxes_per_video        # dtype=np.int32, shape=(47,127)
    │   ├── list_filenames_per_video    # dtype=np.int32, shape=(47,127)
    │   ├── list_object_ids_per_video   # dtype=np.int32, shape=(47,127)
    │   └── list_videos_per_activity    # dtype=np.int32, shape=(10,7)
    │
    ├── train04/
    │   ├── activities        # dtype=np.uint8, shape=(10,14)     (note: string in ASCII format)
    │   ├── boxes             # dtype=np.int32, shape=(6520,4)
    │   ├── image_filenames   # dtype=np.uint8, shape=(6520,74)   (note: string in ASCII format)
    │   ├── videos            # dtype=np.uint8, shape=(103,24)    (note: string in ASCII format)
    │   ├── object_fields     # dtype=np.uint8, shape=(4,16)      (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(6520,4)
    │   ├── list_boxes_per_video        # dtype=np.int32, shape=(103,127)
    │   ├── list_filenames_per_video    # dtype=np.int32, shape=(103,127)
    │   ├── list_object_ids_per_video   # dtype=np.int32, shape=(103,127)
    │   └── list_videos_per_activity    # dtype=np.int32, shape=(10,15)
    │
    ├── test04/
    │   ├── activities        # dtype=np.uint8, shape=(10,14)     (note: string in ASCII format)
    │   ├── boxes             # dtype=np.int32, shape=(3060,4)
    │   ├── image_filenames   # dtype=np.uint8, shape=(3060,73)   (note: string in ASCII format)
    │   ├── videos            # dtype=np.uint8, shape=(47,24)     (note: string in ASCII format)
    │   ├── object_fields     # dtype=np.uint8, shape=(4,16)      (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(3060,4)
    │   ├── list_boxes_per_video        # dtype=np.int32, shape=(47,144)
    │   ├── list_filenames_per_video    # dtype=np.int32, shape=(47,144)
    │   ├── list_object_ids_per_video   # dtype=np.int32, shape=(47,144)
    │   └── list_videos_per_activity    # dtype=np.int32, shape=(10,7)
    │
    ├── train05/
    │   ├── activities        # dtype=np.uint8, shape=(10,14)     (note: string in ASCII format)
    │   ├── boxes             # dtype=np.int32, shape=(6542,4)
    │   ├── image_filenames   # dtype=np.uint8, shape=(6542,76)   (note: string in ASCII format)
    │   ├── videos            # dtype=np.uint8, shape=(103,24)    (note: string in ASCII format)
    │   ├── object_fields     # dtype=np.uint8, shape=(4,16)      (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(6542,4)
    │   ├── list_boxes_per_video        # dtype=np.int32, shape=(103,144)
    │   ├── list_filenames_per_video    # dtype=np.int32, shape=(103,144)
    │   ├── list_object_ids_per_video   # dtype=np.int32, shape=(103,144)
    │   └── list_videos_per_activity    # dtype=np.int32, shape=(10,15)
    │
    └── test05/
        ├── activities        # dtype=np.uint8, shape=(10,14)     (note: string in ASCII format)
        ├── boxes             # dtype=np.int32, shape=(3038,4)
        ├── image_filenames   # dtype=np.uint8, shape=(3038,75)   (note: string in ASCII format)
        ├── videos            # dtype=np.uint8, shape=(47,24)     (note: string in ASCII format)
        ├── object_fields     # dtype=np.uint8, shape=(4,16)      (note: string in ASCII format)
        ├── object_ids        # dtype=np.int32, shape=(3038,4)
        ├── list_boxes_per_video        # dtype=np.int32, shape=(47,127)
        ├── list_filenames_per_video    # dtype=np.int32, shape=(47,127)
        ├── list_object_ids_per_video   # dtype=np.int32, shape=(47,127)
        └── list_videos_per_activity    # dtype=np.int32, shape=(10,7)


Fields
^^^^^^

- ``activities``: activity names
    - ``available in``: train01, train02, train03, train04, train05, test01, test02, test03, test04, test05
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``image_filenames``: image file path+name
    - ``available in``: train01, train02, train03, train04, train05, test01, test02, test03, test04, test05
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``boxes``: bounding box coordinates
    - ``available in``: train01, train02, train03, train04, train05, test01, test02, test03, test04, test05
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format [x1,y1,x2,y2]
- ``videos``: video name
    - ``available in``: train01, train02, train03, train04, train05, test01, test02, test03, test04, test05
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``object_fields``: list of field names of the object id list
    - ``available in``: train01, train02, train03, train04, train05, test01, test02, test03, test04, test05
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
    - ``note``: key field (*field name* aggregator)
- ``object_ids``: list of field ids
    - ``available in``: train01, train02, train03, train04, train05, test01, test02, test03, test04, test05
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: key field (*field id* aggregator)
- ``list_boxes_per_video``: list of bounding box ids per video
    - ``available in``: train01, train02, train03, train04, train05, test01, test02, test03, test04, test05
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_filenames_per_video``: list of image ids per video
    - ``available in``: train01, train02, train03, train04, train05, test01, test02, test03, test04, test05
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_object_ids_per_video``: list of object ids per video
    - ``available in``: train01, train02, train03, train04, train05, test01, test02, test03, test04, test05
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_videos_per_activity``: list of video ids per activity
    - ``available in``: train01, train02, train03, train04, train05, test01, test02, test03, test04, test05
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list


Disclaimer
==========

All rights reserved to the original creators of **UCF-Sports**.

For information about the dataset and its terms of use, please see this `link <http://crcv.ucf.edu/data/UCF_Sports_Action.php>`_.