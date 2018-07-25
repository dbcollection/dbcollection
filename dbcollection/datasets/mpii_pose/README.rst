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
    - :ref:`keypoints (default) <mpii_readme_keypoints>`
    - :ref:`keypoints_full <mpii_readme_keypoints_full>`


Tasks
=====

.. mpii_readme_keypoints:

keypoints (default)
------------------------

- :ref:`How to use <keypoints_how_to_use>`
- :ref:`Properties <keypoints_properties>`
- :ref:`HDF5 file structure <keypoints_hdf5_file_structure>`
- :ref:`Fields <keypoints_fields>`

.. _keypoints_how_to_use:

How to use
^^^^^^^^^^

.. code-block:: python

    >>> # import the package
    >>> import dbcollection as dbc
    >>>
    >>> # load the dataset
    >>> mnist = dbc.load('mpii_pose', 'keypoints')
    >>> mnist
    DataLoader: "mpii_pose" (keypoints task)


.. _keypoints_properties:

Properties
^^^^^^^^^^

- ``primary use``: body joint prediction / classification
- ``description``: Contains single human body pose annotations for body joint prediction / classification.
- ``sets``: train, train01, val01, test
- ``metadata file size in disk``: 7 MB
- ``has annotations``: **yes**
    - ``which``:
        - labels for each activity.
        - frame position of an image from the original video
        - head bounding box coordinates
        - body joint coordinates (x, y) and visibility
        - center coordinates (x, y) of a single person detection
        - scale of the person detection w.r.t. 200px height detections
        - is detection of sufficiently separated individuals?
        - acivities
        - category names
        - keypoint labels
        - video names / ids
- ``available fields``:
    - :ref:`activity_id <keypoints_fields_activity_id>`
    - :ref:`activity_name <keypoints_fields_activity_name>`
    - :ref:`category_name <keypoints_fields_category_name>`
    - :ref:`frame_sec <keypoints_fields_frame_sec>`
    - :ref:`head_bbox <keypoints_fields_head_bbox>`
    - :ref:`image_filenames <keypoints_fields_image_filenames>`
    - :ref:`keypoint_labels <keypoints_fields_keypoint_labels>`
    - :ref:`keypoints <keypoints_fields_keypoint>`
    - :ref:`object_fields <keypoints_fields_object_fields>`
    - :ref:`object_ids <keypoints_fields_object_ids>`
    - :ref:`objpos <keypoints_fields_objpos>`
    - :ref:`scale <keypoints_fields_scale>`
    - :ref:`video_id <keypoints_fields_video_id>`
    - :ref:`video_name <keypoints_fields_video_name>`
    - :ref:`list_keypoints_per_image <keypoints_fields_list_keypoints_per_image>`
    - :ref:`list_single_person_per_image <keypoints_fields_list_single_person_per_image>`


.. _classification_hdf5_file_structure:

HDF5 file structure
^^^^^^^^^^^^^^^^^^^

::

    /
    ├── train/
    │   ├── activity_id       # dtype=np.int32, shape=(29116,),
    │   ├── activity_name     # dtype=np.uint8, shape=(29116,101)  (note: string in ASCII format)
    │   ├── category_name     # dtype=np.uint8, shape=(29116,23)   (note: string in ASCII format)
    │   ├── frame_sec         # dtype=np.int32, shape=(29116,)
    │   ├── head_bbox         # dtype=np.float, shape=(29116,4)
    │   ├── image_filenames   # dtype=np.uint8, shape=(29116,21)   (note: string in ASCII format)
    │   ├── keypoint_labels   # dtype=np.uint8, shape=(16,15)      (note: string in ASCII format)
    │   ├── keypoints         # dtype=np.float, shape=(29116,16,3)
    │   ├── object_fields     # dtype=np.uint8, shape=(13,16)       (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(29116,13)
    │   ├── objpos            # dtype=np.float, shape=(29116,2)
    │   ├── scales            # dtype=np.float, shape=(29116,)
    │   ├── video_ids         # dtype=np.int32, shape=(29116,)
    │   ├── video_names       # dtype=np.uint8, shape=(29116,12)    (note: string in ASCII format)
    │   ├── list_keypoints_per_image       # dtype=np.int32, shape=(18079,17)
    │   └── list_single_person_per_image   # dtype=np.int32, shape=(18079,1))
    │
    ├── train01/
    │   ├── activity_id       # dtype=np.int32, shape=(20310,),
    │   ├── activity_name     # dtype=np.uint8, shape=(20310,101)  (note: string in ASCII format)
    │   ├── category_name     # dtype=np.uint8, shape=(20310,23)   (note: string in ASCII format)
    │   ├── frame_sec         # dtype=np.int32, shape=(20310,)
    │   ├── head_bbox         # dtype=np.float, shape=(20310,4)
    │   ├── image_filenames   # dtype=np.uint8, shape=(20310,21)   (note: string in ASCII format)
    │   ├── keypoint_labels   # dtype=np.uint8, shape=(16,15)      (note: string in ASCII format)
    │   ├── keypoints         # dtype=np.float, shape=(20310,16,3)
    │   ├── object_fields     # dtype=np.uint8, shape=(13,16)       (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(20310,13)
    │   ├── objpos            # dtype=np.float, shape=(20310,2)
    │   ├── scales            # dtype=np.float, shape=(20310,)
    │   ├── video_ids         # dtype=np.int32, shape=(20310,)
    │   ├── video_names       # dtype=np.uint8, shape=(20310,12)    (note: string in ASCII format)
    │   ├── list_keypoints_per_image       # dtype=np.int32, shape=(12656,17)
    │   └── list_single_person_per_image   # dtype=np.int32, shape=(12656,1))
    │
    ├── val01/
    │   ├── activity_id       # dtype=np.int32, shape=(8806,),
    │   ├── activity_name     # dtype=np.uint8, shape=(8806,101)  (note: string in ASCII format)
    │   ├── category_name     # dtype=np.uint8, shape=(8806,23)   (note: string in ASCII format)
    │   ├── frame_sec         # dtype=np.int32, shape=(8806,)
    │   ├── head_bbox         # dtype=np.float, shape=(8806,4)
    │   ├── image_filenames   # dtype=np.uint8, shape=(8806,21)   (note: string in ASCII format)
    │   ├── keypoint_labels   # dtype=np.uint8, shape=(16,15)      (note: string in ASCII format)
    │   ├── keypoints         # dtype=np.float, shape=(8806,16,3)
    │   ├── object_fields     # dtype=np.uint8, shape=(13,16)       (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(8806,13)
    │   ├── objpos            # dtype=np.float, shape=(8806,2)
    │   ├── scales            # dtype=np.float, shape=(8806,)
    │   ├── video_ids         # dtype=np.int32, shape=(8806,)
    │   ├── video_names       # dtype=np.uint8, shape=(8806,12)    (note: string in ASCII format)
    │   ├── list_keypoints_per_image       # dtype=np.int32, shape=(5423,17)
    │   └── list_single_person_per_image   # dtype=np.int32, shape=(5423,7))
    │
    └── test/
        ├── activity_id       # dtype=np.int32, shape=(11776,),
        ├── activity_name     # dtype=np.uint8, shape=(11776,101)  (note: string in ASCII format)
        ├── category_name     # dtype=np.uint8, shape=(11776,23)   (note: string in ASCII format)
        ├── frame_sec         # dtype=np.int32, shape=(11776,)
        ├── image_filenames   # dtype=np.uint8, shape=(11776,21)   (note: string in ASCII format)
        ├── keypoint_labels   # dtype=np.uint8, shape=(16,15)      (note: string in ASCII format)
        ├── object_fields     # dtype=np.uint8, shape=(13,16)       (note: string in ASCII format)
        ├── object_ids        # dtype=np.int32, shape=(11776,13)
        ├── objpos            # dtype=np.float, shape=(11776,2)
        ├── scales            # dtype=np.float, shape=(11776,)
        ├── video_ids         # dtype=np.int32, shape=(11776,)
        ├── video_names       # dtype=np.uint8, shape=(11776,12)    (note: string in ASCII format)
        └── list_single_person_per_image   # dtype=np.int32, shape=(6908,7))


.. _keypoints_fields:

Fields
^^^^^^

.. _keypoints_fields_activity_id:

- ``activity_id``: activity ids
    - ``available in``: train, train01, val01, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1

.. _keypoints_fields_activity_name:

- ``activity_name``: activity names
    - ``available in``: train, train01, val01, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _keypoints_fields_category_name:

- ``category_name``: category names
    - ``available in``: train, train01, val01, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _keypoints_fields_frame_sec:

- ``frame_sec``: image position in video, in seconds
    - ``available in``: train, train01, val01, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1

.. _keypoints_fields_head_bbox:

- ``head_bbox``: head bounding box coordinates
    - ``available in``: train, train01, val01
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format [x1,y1,x2,y2]

.. _keypoints_fields_image_filenames:

- ``image_filenames``: image file name + path
    - ``available in``: train, train01, val01, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _keypoints_fields_keypoint_labels:

- ``keypoint_labels``: body joint names
    - ``available in``: train, train01, val01, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _keypoints_fields_keypoint:

- ``keypoints``: body joint coordinates (x, y)
    - ``available in``: train, train01, val01
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: keypoint format [x1, y1, is_visible]

.. _keypoints_fields_object_fields:

- ``object_fields``: list of field names of the object id list
    - ``available in``: train, train01, val01, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
    - ``note``: key field (*field name* aggregator)

.. _keypoints_fields_object_ids:

- ``object_ids``: list of field ids
    - ``available in``: train, train01, val01, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: key field (*field id* aggregator)

.. _keypoints_fields_objpos:

- ``objpos``: person / detection center coordinates
    - ``available in``: train, train01, val01, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: position format [x, y]

.. _keypoints_fields_scale:

- ``scale``: person scale w.r.t. 200px height
    - ``available in``: train, train01, val01, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1

.. _keypoints_fields_video_id:

- ``video_id``: video index
    - ``available in``: train, train01, val01, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1

.. _keypoints_fields_video_name:

- ``video_name``: video name
    - ``available in``: train, train01, val01, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _keypoints_fields_list_keypoints_per_image:

- ``list_keypoints_per_image``: list of available body joints ids per image
    - ``available in``: train, train01, val01
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _keypoints_fields_list_single_person_per_image:

- ``list_single_person_per_image``: list of single person detection ids per image
    - ``available in``: train, train01, val01, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
