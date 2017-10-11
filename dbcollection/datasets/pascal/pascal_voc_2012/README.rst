.. _pascal_voc2012_readme:

================================================================
PASCAL VOC2012 - The PASCAL Visual Object Classes Challenge 2012
================================================================

The **PASCAL Visual Object Classes Challenge 2012** goal is to recognize objects from a number of visual object
classes in realistic scenes (i.e. not pre-segmented objects). There are two main tasks (classification and detection)
and two additional competitions (segmentation and action classification).

.. note::
    For now, only the detection task is implemented. Submittions of the remaining
    tasks are highly appreciated if you are considering contributing to this project.


Use cases
=========

Image classification, detection, segmentation and action classification.


Properties
==========

- ``name``: pascal_voc_2012
- ``keywords``: image_processing, object_detection
- ``dataset size``: 2,0 GB + 1,9 GB
- ``is downloadable``: **partially**
    - ``data setup``: manually download and unpack the test set into a folder or symlink dir named ``pascal_voc_2012`` before loading the dataset.
- ``tasks``:
    - detection: **(default)**
        - ``primary use``: image classification
        - ``description``: Contains image filenames, label and bounding box coordinates annotations for object detection.
        - ``sets``: train, val, trainval, test
        - ``metadata file size in disk``: 1,9 MB
        - ``has annotations``: **yes**
            - ``which``:
                - labels for each image class/category.
                - bounding box coordinates


.. note::
    For the PASCAL VOC2012 dataset, contrary to VOC2007, the test set is only available
    for registered users in the dataset's `original website <http://host.robots.ox.ac.uk/pascal/VOC/voc2012/>`_.
    You can manually download it and add it along with the trainval data which is publicly available for download.
    The test set is **optional** if you cannot/do not want to download it from the source.
    Everything will work just fine, with the exception that you won't be able to access the test data.
    However, if you want to use it, this is the recommended way to do so:

    1. download the dataset using ``dbc.download('pascal_voc_2012', data_dir='some/path/dir/')``
    2. inside the created dir (it will have the same name as the dataset), put the test data file (zip) and unpack it.
    3. when loading the dataset's metadata with the ``load()`` method, during setup it will automatically detect if the test set is available or not.



Metadata structure (HDF5)
=========================

Task: detection
---------------

::

    /
    ├── train/
    │   ├── boxes             # dtype=np.float, shape=(15774,4)
    │   ├── category_id       # dtype=np.int32, shape=(20,)
    │   ├── classes           # dtype=np.uint8, shape=(20,12)     (note: string in ASCII format)
    │   ├── difficult         # dtype=np.int32, shape=(2,)
    │   ├── id                # dtype=np.int32, shape=(15774,)
    │   ├── image_filenames   # dtype=np.uint8, shape=(5717,88)   (note: string in ASCII format)
    │   ├── image_id          # dtype=np.int32, shape=(5717,)
    │   ├── sizes             # dtype=np.int32, shape=(5717,3)
    │   ├── truncated         # dtype=np.int32, shape=(2,)
    │   ├── object_fields     # dtype=np.uint8, shape=(6,16)      (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(15774,6)
    │   ├── list_boxes_per_image             # dtype=np.int32, shape=(5717,56)
    │   ├── list_image_filenames_per_class   # dtype=np.int32, shape=(20,2142)
    │   ├── list_object_ids_per_image        # dtype=np.int32, shape=(5717,56)
    │   ├── list_object_ids_difficult        # dtype=np.int32, shape=(2165,)
    │   ├── list_object_ids_no_difficult     # dtype=np.int32, shape=(13609,)
    │   ├── list_object_ids_truncated        # dtype=np.int32, shape=(8102,)
    │   ├── list_object_ids_no_truncated     # dtype=np.int32, shape=(7672,)
    │   └── list_object_ids_per_class        # dtype=np.int32, shape=(20,5019)
    │
    ├── val/
    │   ├── boxes             # dtype=np.float, shape=(15787,4)
    │   ├── category_id       # dtype=np.int32, shape=(20,)
    │   ├── classes           # dtype=np.uint8, shape=(20,12)     (note: string in ASCII format)
    │   ├── difficult         # dtype=np.int32, shape=(2,)
    │   ├── id                # dtype=np.int32, shape=(15787,)
    │   ├── image_filenames   # dtype=np.uint8, shape=(5823,88)   (note: string in ASCII format)
    │   ├── image_id          # dtype=np.int32, shape=(5823,)
    │   ├── sizes             # dtype=np.int32, shape=(5823,3)
    │   ├── truncated         # dtype=np.int32, shape=(2,)
    │   ├── object_fields     # dtype=np.uint8, shape=(6,16)      (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(15787,6)
    │   ├── list_boxes_per_image             # dtype=np.int32, shape=(5823,42)
    │   ├── list_image_filenames_per_class   # dtype=np.int32, shape=(20,2232)
    │   ├── list_object_ids_per_image        # dtype=np.int32, shape=(5823,42)
    │   ├── list_object_ids_difficult        # dtype=np.int32, shape=(1946,)
    │   ├── list_object_ids_no_difficult     # dtype=np.int32, shape=(13841,)
    │   ├── list_object_ids_truncated        # dtype=np.int32, shape=(8288,)
    │   ├── list_object_ids_no_truncated     # dtype=np.int32, shape=(7499,)
    │   └── list_object_ids_per_class        # dtype=np.int32, shape=(20,5110)
    │
    ├── trainval/
    │   ├── boxes             # dtype=np.float, shape=(31561,4)
    │   ├── category_id       # dtype=np.int32, shape=(20,)
    │   ├── classes           # dtype=np.uint8, shape=(20,12)     (note: string in ASCII format)
    │   ├── difficult         # dtype=np.int32, shape=(2,)
    │   ├── id                # dtype=np.int32, shape=(34561,)
    │   ├── image_filenames   # dtype=np.uint8, shape=(11540,88)   (note: string in ASCII format)
    │   ├── image_id          # dtype=np.int32, shape=(11540,)
    │   ├── sizes             # dtype=np.int32, shape=(11540,3)
    │   ├── truncated         # dtype=np.int32, shape=(2,)
    │   ├── object_fields     # dtype=np.uint8, shape=(6,16)      (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(31561,6)
    │   ├── list_boxes_per_image             # dtype=np.int32, shape=(11540,56)
    │   ├── list_image_filenames_per_class   # dtype=np.int32, shape=(20,4374)
    │   ├── list_object_ids_per_image        # dtype=np.int32, shape=(11540,56)
    │   ├── list_object_ids_difficult        # dtype=np.int32, shape=(4111,)
    │   ├── list_object_ids_no_difficult     # dtype=np.int32, shape=(27450,)
    │   ├── list_object_ids_truncated        # dtype=np.int32, shape=(16390,)
    │   ├── list_object_ids_no_truncated     # dtype=np.int32, shape=(15171,)
    │   └── list_object_ids_per_class        # dtype=np.int32, shape=(20,10129)
    │
    └── test/
        ├── id                # dtype=np.int32, shape=(10991,)
        ├── image_filenames   # dtype=np.uint8, shape=(10991,88)   (note: string in ASCII format)
        ├── object_fields     # dtype=np.uint8, shape=(16,)        (note: string in ASCII format)
        └── object_ids        # dtype=np.int32, shape=(10991,1)


Fields
^^^^^^

- ``boxes``: bounding box coordinates
    - ``available in``: train, val, trainval
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format [x1,y1,x2,y2]
- ``category_id``: category id
    - ``available in``: train, val, trainval
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``classes``: class names
    - ``available in``: train, val, trainval
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``difficult``: is difficult
    - ``available in``: train, val, trainval
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
    - ``available in``: train, val, trainval
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``sizes``: image size
    - ``available in``: train, val, trainval
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: size format [width, height, depth]
- ``truncated``: is truncated
    - ``available in``: train, val, trainval
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
    - ``available in``: train, val, trainval
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_image_filenames_per_class``: list of image filenames ids per class
    - ``available in``: train, val, trainval
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_object_ids_per_image``: list of object ids per image
    - ``available in``: train, val, trainval
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_object_ids_difficult``: list of object ids for difficult objects
    - ``available in``: train, val, trainval
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_object_ids_no_difficult``: list of object ids for not difficult objects
    - ``available in``: train, val, trainval
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_object_ids_truncated``: list of object ids for truncated objects
    - ``available in``: train, val, trainval
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_object_ids_no_truncated``: list of object ids for not truncated objects
    - ``available in``: train, val, trainval
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_object_ids_per_class``: list of object ids per class
    - ``available in``: train, val, trainval
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list


Disclaimer
==========

All rights reserved to the original creators of **PASCAL VOC2012**.

For information about the dataset and its terms of use, please see this `link <http://host.robots.ox.ac.uk/pascal/VOC/voc2012/>`_.