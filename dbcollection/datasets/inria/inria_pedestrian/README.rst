.. _inria_pedestrian_readme:

================
INRIA Pedestrian
================

The **INRIA person** dataset is popular in the Pedestrian Detection community, both for training detectors and reporting results.

It consists of 614 person detections for training and 288 for testing.

.. note::
    The data files available for download are the ones distributed in `here <http://www.vision.caltech.edu/Image_Datasets/CaltechPedestrians/datasets/INRIA/>`_.


Use cases
=========

Pedestrian detection in images.


Properties
==========

- ``name``: inria_pedestrian
- ``keywords``: image_processing, detection, pedestrian
- ``dataset size``: 1,1 GB
- ``is downloadable``: **yes**
- ``tasks``:
    - detection: **(default)**
        - ``primary use``: object detection
        - ``description``: Contains image filenames, classes and bounding box annotations for pedestrian detection in images/videos.
        - ``sets``: train, test
        - ``metadata file size in disk``: 139,1 kB
        - ``has annotations``: **yes**
            - ``which``:
                - labels for each class/category.
                - bounding box of pedestrians.
                - occlusion % of annotated pedestrians.


Metadata structure (HDF5)
=========================

Task: detection
---------------

::

    /
    ├── train/
    │   ├── image_filenames   # dtype=np.uint8, shape=(1832,88)  (note: string in ASCII format)
    │   ├── classes           # dtype=np.uint8, shape=(4,10)     (note: string in ASCII format)
    │   ├── boxes             # dtype=np.float, shape=(1237,4)
    │   ├── boxesv            # dtype=np.float, shape=(1237,4)
    │   ├── id                # dtype=np.int32, shape=(1237,)
    │   ├── occlusion         # dtype=np.float, shape=(1237,)
    │   ├── object_fields     # dtype=np.uint8, shape=(6,16)     (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(1237,6)
    │   ├── list_image_filenames_per_class   # dtype=np.int32, shape=(4,614))
    │   ├── list_boxes_per_image             # dtype=np.int32, shape=(1832,12))
    │   ├── list_boxesv_per_image            # dtype=np.int32, shape=(1832,12))
    │   ├── list_object_ids_per_image        # dtype=np.int32, shape=(1832,12))
    │   └── list_objects_ids_per_class       # dtype=np.int32, shape=(4,1237))
    │
    └── test/
        ├── image_filenames   # dtype=np.uint8, shape=(741,88)  (note: string in ASCII format)
        ├── classes           # dtype=np.uint8, shape=(4,10)     (note: string in ASCII format)
        ├── boxes             # dtype=np.float, shape=(589,4)
        ├── boxesv            # dtype=np.float, shape=(589,4)
        ├── id                # dtype=np.int32, shape=(589,)
        ├── occlusion         # dtype=np.float, shape=(589,)
        ├── object_fields     # dtype=np.uint8, shape=(6,16)     (note: string in ASCII format)
        ├── object_ids        # dtype=np.int32, shape=(589,6)
        ├── list_image_filenames_per_class   # dtype=np.int32, shape=(4,288))
        ├── list_boxes_per_image             # dtype=np.int32, shape=(741,16))
        ├── list_boxesv_per_image            # dtype=np.int32, shape=(741,16))
        ├── list_object_ids_per_image        # dtype=np.int32, shape=(741,16))
        └── list_objects_ids_per_class       # dtype=np.int32, shape=(4,589))


Fields
^^^^^^

- ``image_filenames``: image file path+names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``classes``: class names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``boxes``: bounding boxes
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format (x1,y1,x2,y2)
- ``boxesv``: bounding boxes (visible)
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format (x1,y1,x2,y2)
- ``id``: label ids
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``occlusion``: occlusion percentage
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
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
- ``list_image_filenames_per_class``: list of image per class
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_boxes_per_image``: list of bounding boxes per image
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_boxesv_per_image``: list of (visible) bounding boxes per image
    - ``available in``: train, test
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
- ``list_objects_ids_per_class``: list of object ids per class
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list


Disclaimer
==========

All rights reserved to the original creators of **INRIA Pedestrian Dataset**.

For information about the dataset and its terms of use, please see this 
`link <http://www.vision.caltech.edu/Image_Datasets/CaltechPedestrians/datasets/INRIA/>`_.