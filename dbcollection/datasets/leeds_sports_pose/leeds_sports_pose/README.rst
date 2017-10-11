.. _lsp_readme:

=======================
LSP - Leeds Sports Pose
=======================

The **Leeds Sports Pose** dataset contains 2000 pose annotated images of mostly sports people gathered from Flickr
using the tags shown above. The images have been scaled such that the most prominent person is
roughly 150 pixels in length. Each image has been annotated with 14 joint locations. Left and
right joints are consistently labelled from a person-centric viewpoint.


Use cases
=========

Human body joint detection.


Properties
==========

- ``name``: leeds_sports_pose
- ``keywords``: image_processing, detection, human_pose, keypoints
- ``dataset size``: 264,2 MB
- ``is downloadable``: **yes**
- ``tasks``:
    - keypoints: **(default)**
        - ``primary use``: human body joint detection
        - ``description``: Contains image files and body parts keypoint coordinates for detecting human body joints in images
        - ``sets``: train, test
        - ``metadata file size in disk``: 473,7 kB
        - ``has annotations``: **yes**
            - ``which``:
                - body joint keypoints
    - keypoints_original:
        - ``primary use``: human body joint detection
        - ``description``: Contains image files and body parts keypoint coordinates for detecting human body joints in images
        - ``sets``: train, test
        - ``metadata file size in disk``: 396,0 kB
        - ``has annotations``: **yes**
            - ``which``:
                - body joint keypoints

.. note::
    The ``keypoints_original`` task is essentially the same as ``keypoints``,
    but contains full size images instead of crops of persons.


Metadata structure (HDF5)
=========================

Task: keypoints
---------------

::

    /
    ├── train/
    │   ├── image_filenames   # dtype=np.uint8, shape=(1000,83)  (note: string in ASCII format)
    │   ├── keypoint_names    # dtype=np.uint8, shape=(14,15)    (note: string in ASCII format)
    │   ├── keypoints         # dtype=np.float, shape=(1000,14,3)
    │   ├── object_fields     # dtype=np.uint8, shape=(2,16)     (note: string in ASCII format)
    │   └── object_ids        # dtype=np.int32, shape=(1000,2)
    │
    └── test/
        ├── image_filenames   # dtype=np.uint8, shape=(1000,83)  (note: string in ASCII format)
        ├── keypoint_names    # dtype=np.uint8, shape=(14,15)    (note: string in ASCII format)
        ├── keypoints         # dtype=np.float, shape=(1000,14,3)
        ├── object_fields     # dtype=np.uint8, shape=(2,16)     (note: string in ASCII format)
        └── object_ids        # dtype=np.int32, shape=(1000,2)


Fields
^^^^^^

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
- ``keypoints``: keypoint coordinates
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: keypoint format [x1,y1,is_visible]
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


Task: keypoints_original
------------------------

::

    /
    ├── train/
    │   ├── image_filenames   # dtype=np.uint8, shape=(1000,83)  (note: string in ASCII format)
    │   ├── keypoint_names    # dtype=np.uint8, shape=(14,15)    (note: string in ASCII format)
    │   ├── keypoints         # dtype=np.float, shape=(1000,14,3)
    │   ├── object_fields     # dtype=np.uint8, shape=(2,16)     (note: string in ASCII format)
    │   └── object_ids        # dtype=np.int32, shape=(1000,2)
    │
    └── test/
        ├── image_filenames   # dtype=np.uint8, shape=(1000,83)  (note: string in ASCII format)
        ├── keypoint_names    # dtype=np.uint8, shape=(14,15)    (note: string in ASCII format)
        ├── keypoints         # dtype=np.float, shape=(1000,14,3)
        ├── object_fields     # dtype=np.uint8, shape=(2,16)     (note: string in ASCII format)
        └── object_ids        # dtype=np.int32, shape=(1000,2)


Fields
^^^^^^

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
- ``keypoints``: keypoint coordinates
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: keypoint format [x1,y1,is_visible]
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

All rights reserved to the original creators of **Leeds Sports Pose**.

For information about the dataset and its terms of use, please see this `link <http://sam.johnson.io/research/lsp.html>`_.