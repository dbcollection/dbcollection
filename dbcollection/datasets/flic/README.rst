.. _flic_readme:

===============================
FLIC - Frames Labeled In Cinema
===============================

Collection of 5003 images automatically from popular Hollywood movies.
It contains annotations of upper body joints only.
It has 3987 images for training and 1016 for testing.


Use cases
=========

Human body joint detection.


Properties
==========

- ``name``: flic
- ``keywords``: image_processing, detection, human_pose, keypoints
- ``dataset size``: 300,3 MB
- ``is downloadable``: **yes**
- ``tasks``:
    - keypoints: **(default)**
        - ``primary use``: image classification
        - ``description``: Contains keypoint coordinates (upper body joints only) and bounding boxes of the torso for body joint detection.
        - ``sets``: train, test
        - ``metadata file size``: 582,0 kB
        - ``has annotations``: **yes**
            - ``which``:
                - image filenames
                - upper body joint coordinates
                - torso bounding box


Metadata structure (HDF5)
=========================

Task: classification
--------------------

::

    /
    ├── train/
    │   ├── image_filenames   # dtype=np.uint8, shape=(3987,108)  (note: string in ASCII format)
    │   ├── movienames        # dtype=np.uint8, shape=(3987,31)   (note: string in ASCII format)
    │   ├── width             # dtype=np.int32, shape=(3987,)
    │   ├── height            # dtype=np.int32, shape=(3987,)
    │   ├── torso_boxes       # dtype=np.float, shape=(3987,4)
    │   ├── keypoints         # dtype=np.float, shape=(3987,11,3)
    │   ├── keypoint_names    # dtype=np.uint8, shape=(11,15)    (note: string in ASCII format)
    │   ├── object_fields     # dtype=np.uint8, shape=(5,16)     (note: string in ASCII format)
    │   └── object_ids        # dtype=np.int32, shape=(3987,5)
    │
    └── test/
        ├── image_filenames   # dtype=np.uint8, shape=(1016,108)  (note: string in ASCII format)
        ├── movienames        # dtype=np.uint8, shape=(1016,31)   (note: string in ASCII format)
        ├── width             # dtype=np.int32, shape=(1016,)
        ├── height            # dtype=np.int32, shape=(1016,)
        ├── torso_boxes       # dtype=np.float, shape=(1016,4)
        ├── keypoints         # dtype=np.float, shape=(1016,11,3)
        ├── keypoint_names    # dtype=np.uint8, shape=(11,15)    (note: string in ASCII format)
        ├── object_fields     # dtype=np.uint8, shape=(5,16)     (note: string in ASCII format)
        └── object_ids        # dtype=np.int32, shape=(1016,5)


Fields
^^^^^^

- ``image_filenames``: image file path + name
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``movienames``: name of the movie where the image was taken from
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``width``: image width
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``height``: image height
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``torso_boxes``: torso bounding box
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format [x1,y1,x2,y2]
- ``keypoints``: body joint coordinates
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: keypoint format [x1,y1,is_visible]
- ``keypoint_names``: body joint name
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


Disclaimer
==========

All rights reserved to the original creators of **Frames Labeled In Cinema**.

For information about the dataset and its terms of use, please see this `link <http://bensapp.github.io/flic-dataset.html>`_.