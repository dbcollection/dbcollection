.. _mpii_pose_readme:

===============
MPII Human Pose
===============

**MPII Human Pose** dataset is a state of the art benchmark for evaluation of articulated human pose
estimation. The dataset includes around 25K images containing over 40K people with annotated body joints.
The images were systematically collected using an established taxonomy of every day human activities.
Overall the dataset covers 410 human activities and each image is provided with an activity label.



Use cases
=========

Human body joint detection.


Properties
==========

- ``name``: mpii_pose
- ``keywords``: image_processing, detection, human_pose, keypoints
- ``dataset size``: 12,1 GB
- ``is downloadable``: **yes**
- ``tasks``:
    - keypoints: **(default)**
        - ``primary use``: image classification
        - ``description``: Contains image tensors and label annotations for image classification.
        - ``sets``: train, test
        - ``metadata file size in disk``: 3,9 MB
        - ``has annotations``: **yes**
            - ``which``:
                - labels for each activity.
                - frame position of an image from the original video
                - head bounding box coordinates
                - body part coordinates
                - center coordinates of a person detection
                - scale of the person
        - ``note``: this task was manually cleaned/parsed in order to remove bad annotations.
    - keypoints_full:
        - ``primary use``: image classification
        - ``description``: Contains image tensors and label annotations for image classification.
        - ``sets``: train, test
        - ``metadata file size in disk``: 3,9 MB
        - ``has annotations``: **yes**
            - ``which``:
                - labels for each activity.
                - frame position of an image from the original video
                - head bounding box coordinates
                - body part coordinates
                - center coordinates of a person detection
                - scale of the person


Metadata structure (HDF5)
=========================


Task: keypoints
---------------

::

    /
    ├── train/
    │   ├── activity_id       # dtype=np.int32, shape=(18079,)
    │   ├── activity_name     # dtype=np.uint8, shape=(18079,101)  (note: string in ASCII format)
    │   ├── category_name     # dtype=np.uint8, shape=(18079,23)   (note: string in ASCII format)
    │   ├── frame_sec         # dtype=np.int32, shape=(18079,)
    │   ├── head_bbox         # dtype=np.float, shape=(28883,4)    (note: string in ASCII format)
    │   ├── image_filenames   # dtype=np.uint8, shape=(18079,58)   (note: string in ASCII format)
    │   ├── keypoint_names    # dtype=np.uint8, shape=(16,15)      (note: string in ASCII format)
    │   ├── keypoints         # dtype=np.float, shape=(28883,16,3)
    │   ├── objpos            # dtype=np.float, shape=(28883,2)
    │   ├── scale             # dtype=np.float, shape=(28883,)
    │   ├── video_idx         # dtype=np.int32, shape=(18079,)
    │   ├── video_names       # dtype=np.uint8, shape=(2821,12)    (note: string in ASCII format)
    │   ├── object_fields     # dtype=np.uint8, shape=(7,16)       (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(28883,7)
    │   ├── list_keypoints_per_image       # dtype=np.int32, shape=(18079,17)
    │   ├── list_object_ids_per_image      # dtype=np.int32, shape=(18079,17)
    │   └── list_single_person_per_image   # dtype=np.int32, shape=(18079,7))
    │
    └── test/
        ├── image_filenames   # dtype=np.uint8, shape=(6908,58)  (note: string in ASCII format)
        ├── keypoint_names    # dtype=np.uint8, shape=(16,15)    (note: string in ASCII format)
        ├── objpos            # dtype=np.float, shape=(11823,2)
        ├── scale             # dtype=np.float, shape=(11823,)
        ├── video_names       # dtype=np.uint8, shape=(2821,12)  (note: string in ASCII format)
        ├── object_fields     # dtype=np.uint8, shape=(3,16)     (note: string in ASCII format)
        ├── object_ids        # dtype=np.int32, shape=(12067,3)
        ├── list_object_ids_per_image      # dtype=np.int32, shape=(6908,17)
        └── list_single_person_per_image   # dtype=np.int32, shape=(6908,8))


Fields
^^^^^^

- ``activity_id``: activity ids
    - ``available in``: train
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``activity_name``: activity names
    - ``available in``: train
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``category_name``: category names
    - ``available in``: train
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``frame_sec``: image position in video, in seconds
    - ``available in``: train
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``head_bbox``: head bounding box coordinates
    - ``available in``: train
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format [x1,y1,x2,y2]
- ``image_filenames``: image file path+name
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``keypoint_names``: body joint names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``keypoints``: body part keypoit coordinates
    - ``available in``: train
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: keypoint format [x1,y1,is_visible]
- ``objpos``: object/person center coordinates
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: position format [x,y]
- ``scale``: person scale w.r.t. 200px height
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
- ``video_names``: video names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``object_fields``: list of field names of the object id list
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
    - ``note``: key field (*field name* aggregator)
- ``object_ids``: list of field ids
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: key field (*field id* aggregator)
- ``list_keypoints_per_image``: list of available body joints ids per image
    - ``available in``: train
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_object_ids_per_image``: list of object ids per image
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_single_person_per_image``: list of single person detection ids per image
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list


Task: keypoints_full
--------------------

::

    /
    ├── train/
    │   ├── activity_id       # dtype=np.int32, shape=(18079,)
    │   ├── activity_name     # dtype=np.uint8, shape=(18079,101)  (note: string in ASCII format)
    │   ├── category_name     # dtype=np.uint8, shape=(18079,23)   (note: string in ASCII format)
    │   ├── frame_sec         # dtype=np.int32, shape=(18079,)
    │   ├── head_bbox         # dtype=np.float, shape=(29116,4)    (note: string in ASCII format)
    │   ├── image_filenames   # dtype=np.uint8, shape=(18079,58)   (note: string in ASCII format)
    │   ├── keypoint_names    # dtype=np.uint8, shape=(16,15)      (note: string in ASCII format)
    │   ├── keypoints         # dtype=np.float, shape=(29116,16,3)
    │   ├── objpos            # dtype=np.float, shape=(29116,2)
    │   ├── scale             # dtype=np.float, shape=(29116,)
    │   ├── video_idx         # dtype=np.int32, shape=(18079,)
    │   ├── video_names       # dtype=np.uint8, shape=(2821,12)    (note: string in ASCII format)
    │   ├── object_fields     # dtype=np.uint8, shape=(7,16)       (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(29692,7)
    │   ├── list_keypoints_per_image       # dtype=np.int32, shape=(18079,17)
    │   ├── list_object_ids_per_image      # dtype=np.int32, shape=(18079,17)
    │   └── list_single_person_per_image   # dtype=np.int32, shape=(18079,7))
    │
    └── test/
        ├── image_filenames   # dtype=np.uint8, shape=(6908,11)  (note: string in ASCII format)
        ├── keypoint_names    # dtype=np.uint8, shape=(16,15)    (note: string in ASCII format)
        ├── objpos            # dtype=np.float, shape=(11823,2)
        ├── scale             # dtype=np.float, shape=(11823,)
        ├── video_names       # dtype=np.uint8, shape=(2821,12)  (note: string in ASCII format)
        ├── object_fields     # dtype=np.uint8, shape=(3,16)     (note: string in ASCII format)
        ├── object_ids        # dtype=np.int32, shape=(12067,3)
        ├── list_object_ids_per_image      # dtype=np.int32, shape=(6908,17)
        └── list_single_person_per_image   # dtype=np.int32, shape=(6908,8))


Fields
^^^^^^

- ``activity_id``: activity ids
    - ``available in``: train
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``activity_name``: activity names
    - ``available in``: train
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``category_name``: category names
    - ``available in``: train
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``frame_sec``: image position in video, in seconds
    - ``available in``: train
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``head_bbox``: head bounding box coordinates
    - ``available in``: train
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format [x1,y1,x2,y2]
- ``image_filenames``: image file path+name
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``keypoint_names``: body joint names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``keypoints``: body part keypoit coordinates
    - ``available in``: train
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: keypoint format [x1,y1,is_visible]
- ``objpos``: object/person center coordinates
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: position format [x,y]
- ``scale``: person scale w.r.t. 200px height
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
- ``video_names``: video names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``object_fields``: list of field names of the object id list
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
    - ``note``: key field (*field name* aggregator)
- ``object_ids``: list of field ids
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: key field (*field id* aggregator)
- ``list_keypoints_per_image``: list of available body joints ids per image
    - ``available in``: train
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_object_ids_per_image``: list of object ids per image
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_single_person_per_image``: list of single person detection ids per image
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list


Disclaimer
==========

All rights reserved to the original creators of **MPII Human Pose**.

For information about the dataset and its terms of use, please see this `link <http://human-pose.mpi-inf.mpg.de/>`_.