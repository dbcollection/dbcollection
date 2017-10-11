.. _pascal_voc2007_readme:

================================================================
PASCAL VOC2007 - The PASCAL Visual Object Classes Challenge 2007
================================================================

The **PASCAL Visual Object Classes Challenge 2007** goal is to recognize objects from a number of visual object
classes in realistic scenes (i.e. not pre-segmented objects). There are two main tasks (classification and detection)
and two additional competitions (segmentation and person layout).

.. note::
    For now, only the detection task is implemented. Submittions of the remaining
    tasks are highly appreciated if you are considering contributing to this project.


Use cases
=========

Image classification, detection, segmentation and person pose detection.


Properties
==========

- ``name``: pascal_voc_2007
- ``keywords``: image_processing, object_detection
- ``dataset size``: 911,1 MB
- ``is downloadable``: **yes**
- ``tasks``:
    - detection: **(default)**
        - ``primary use``: image classification
        - ``description``: Contains image filenames, label and bounding box coordinates annotations for object detection.
        - ``sets``: train, val, trainval, test
        - ``metadata file size in disk``: 1,4 MB
        - ``has annotations``: **yes**
            - ``which``:
                - labels for each image class/category.
                - bounding box coordinates


Metadata structure (HDF5)
=========================

Task: detection
---------------

::

    /
    ├── train/
    │   ├── boxes             # dtype=np.float, shape=(7844,4)
    │   ├── category_id       # dtype=np.int32, shape=(20,)
    │   ├── classes           # dtype=np.uint8, shape=(20,12)     (note: string in ASCII format)
    │   ├── difficult         # dtype=np.int32, shape=(2,)
    │   ├── id                # dtype=np.int32, shape=(7844,)
    │   ├── image_filenames   # dtype=np.uint8, shape=(2501,83)   (note: string in ASCII format)
    │   ├── image_id          # dtype=np.int32, shape=(2501,)
    │   ├── sizes             # dtype=np.int32, shape=(2501,3)
    │   ├── truncated         # dtype=np.int32, shape=(2,)
    │   ├── object_fields     # dtype=np.uint8, shape=(6,16)      (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(7844,6)
    │   ├── list_boxes_per_image             # dtype=np.int32, shape=(2501,37)
    │   ├── list_image_filenames_per_class   # dtype=np.int32, shape=(20,1070)
    │   ├── list_object_ids_per_image        # dtype=np.int32, shape=(2501,37)
    │   ├── list_object_ids_difficult        # dtype=np.int32, shape=(1543,)
    │   ├── list_object_ids_no_difficult     # dtype=np.int32, shape=(6301,)
    │   ├── list_object_ids_truncated        # dtype=np.int32, shape=(4108,)
    │   ├── list_object_ids_no_truncated     # dtype=np.int32, shape=(3736,)
    │   └── list_object_ids_per_class        # dtype=np.int32, shape=(20,2705)
    │
    ├── val/
    │   ├── boxes             # dtype=np.float, shape=(7818,4)
    │   ├── category_id       # dtype=np.int32, shape=(20,)
    │   ├── classes           # dtype=np.uint8, shape=(20,12)     (note: string in ASCII format)
    │   ├── difficult         # dtype=np.int32, shape=(2,)
    │   ├── id                # dtype=np.int32, shape=(7818,)
    │   ├── image_filenames   # dtype=np.uint8, shape=(2510,83)   (note: string in ASCII format)
    │   ├── image_id          # dtype=np.int32, shape=(2510,)
    │   ├── sizes             # dtype=np.int32, shape=(2510,3)
    │   ├── truncated         # dtype=np.int32, shape=(2,)
    │   ├── object_fields     # dtype=np.uint8, shape=(6,16)      (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(7818,6)
    │   ├── list_boxes_per_image             # dtype=np.int32, shape=(2510,42)
    │   ├── list_image_filenames_per_class   # dtype=np.int32, shape=(20,1025)
    │   ├── list_object_ids_per_image        # dtype=np.int32, shape=(2510,42)
    │   ├── list_object_ids_difficult        # dtype=np.int32, shape=(1511,)
    │   ├── list_object_ids_no_difficult     # dtype=np.int32, shape=(6307,)
    │   ├── list_object_ids_truncated        # dtype=np.int32, shape=(4036,)
    │   ├── list_object_ids_no_truncated     # dtype=np.int32, shape=(3782,)
    │   └── list_object_ids_per_class        # dtype=np.int32, shape=(20,2742)
    │
    ├── trainval/
    │   ├── boxes             # dtype=np.float, shape=(15662,4)
    │   ├── category_id       # dtype=np.int32, shape=(20,)
    │   ├── classes           # dtype=np.uint8, shape=(20,12)     (note: string in ASCII format)
    │   ├── difficult         # dtype=np.int32, shape=(2,)
    │   ├── id                # dtype=np.int32, shape=(15662,)
    │   ├── image_filenames   # dtype=np.uint8, shape=(5011,83)   (note: string in ASCII format)
    │   ├── image_id          # dtype=np.int32, shape=(5011,)
    │   ├── sizes             # dtype=np.int32, shape=(5011,3)
    │   ├── truncated         # dtype=np.int32, shape=(2,)
    │   ├── object_fields     # dtype=np.uint8, shape=(6,16)      (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(15662,6)
    │   ├── list_boxes_per_image             # dtype=np.int32, shape=(5011,42)
    │   ├── list_image_filenames_per_class   # dtype=np.int32, shape=(20,2095)
    │   ├── list_object_ids_per_image        # dtype=np.int32, shape=(5011,42)
    │   ├── list_object_ids_difficult        # dtype=np.int32, shape=(3054,)
    │   ├── list_object_ids_no_difficult     # dtype=np.int32, shape=(12608,)
    │   ├── list_object_ids_truncated        # dtype=np.int32, shape=(8144,)
    │   ├── list_object_ids_no_truncated     # dtype=np.int32, shape=(7518,)
    │   └── list_object_ids_per_class        # dtype=np.int32, shape=(20,5447)
    │
    └── test/
        ├── boxes             # dtype=np.float, shape=(14976,4)
        ├── category_id       # dtype=np.int32, shape=(20,)
        ├── classes           # dtype=np.uint8, shape=(20,12)     (note: string in ASCII format)
        ├── difficult         # dtype=np.int32, shape=(2,)
        ├── id                # dtype=np.int32, shape=(14976,)
        ├── image_filenames   # dtype=np.uint8, shape=(4952,83)   (note: string in ASCII format)
        ├── image_id          # dtype=np.int32, shape=(4952,)
        ├── sizes             # dtype=np.int32, shape=(4952,3)
        ├── truncated         # dtype=np.int32, shape=(2,)
        ├── object_fields     # dtype=np.uint8, shape=(6,16)      (note: string in ASCII format)
        ├── object_ids        # dtype=np.int32, shape=(14976,6)
        ├── list_boxes_per_image             # dtype=np.int32, shape=(4952,41)
        ├── list_image_filenames_per_class   # dtype=np.int32, shape=(20,2097)
        ├── list_object_ids_per_image        # dtype=np.int32, shape=(4952,41)
        ├── list_object_ids_difficult        # dtype=np.int32, shape=(2944,)
        ├── list_object_ids_no_difficult     # dtype=np.int32, shape=(12032,)
        ├── list_object_ids_truncated        # dtype=np.int32, shape=(1824,)
        ├── list_object_ids_no_truncated     # dtype=np.int32, shape=(7152,)
        └── list_object_ids_per_class        # dtype=np.int32, shape=(20,5227)


Fields
^^^^^^

- ``boxes``: bounding box coordinates
    - ``available in``: train, val, trainval, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format [x1,y1,x2,y2]
- ``category_id``: category id
    - ``available in``: train, val, trainval, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``classes``: class names
    - ``available in``: train, val, trainval, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``difficult``: is difficult
    - ``available in``: train, val, trainval, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``id``: object id
    - ``available in``: train, val, trainval, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``image_filenames``: image file path+name
    - ``available in``: train, val, trainval, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``image_id``: image id
    - ``available in``: train, val, trainval, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``sizes``: image size
    - ``available in``: train, val, trainval, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: size format [width, height, depth]
- ``truncated``: is truncated
    - ``available in``: train, val, trainval, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``object_fields``: list of field names of the object id list
    - ``available in``: train, val, trainval, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
    - ``note``: key field (*field name* aggregator)
- ``object_ids``: list of field ids
    - ``available in``: train, val, trainval, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: key field (*field id* aggregator)
- ``list_boxes_per_image``: list of bounding boxes per image
    - ``available in``: train, val, trainval, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_image_filenames_per_class``: list of image filenames ids per class
    - ``available in``: train, val, trainval, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_object_ids_per_image``: list of object ids per image
    - ``available in``: train, val, trainval, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_object_ids_difficult``: list of object ids for difficult objects
    - ``available in``: train, val, trainval, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_object_ids_no_difficult``: list of object ids for not difficult objects
    - ``available in``: train, val, trainval, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_object_ids_truncated``: list of object ids for truncated objects
    - ``available in``: train, val, trainval, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_object_ids_no_truncated``: list of object ids for not truncated objects
    - ``available in``: train, val, trainval, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_object_ids_per_class``: list of object ids per class
    - ``available in``: train, val, trainval, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list


Disclaimer
==========

All rights reserved to the original creators of **PASCAL VOC2007**.

For information about the dataset and its terms of use, please see this `link <http://host.robots.ox.ac.uk/pascal/VOC/voc2007/>`_.