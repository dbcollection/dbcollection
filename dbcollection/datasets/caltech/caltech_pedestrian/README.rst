.. _caltech_pedestrian_readme:

==================
Caltech Pedestrian
==================

The **Caltech Pedestrian Dataset consists** of approximately 10 hours of 640x480 30Hz video
taken from a vehicle driving through regular traffic in an urban environment. About 250,000
frames (in 137 approximately minute long segments) with a total of 350,000 bounding boxes and
2300 unique pedestrians were annotated.

The annotation includes temporal correspondence between bounding boxes and detailed occlusion
labels.


Use cases
=========

Pedestrian detection in images/videos.


Properties
==========

- ``name``: caltech_pedestrian
- ``keywords``: image_processing, detection, pedestrian
- ``dataset size``: 11,9 GB
- ``is downloadable``: **yes**
- ``tasks``:
    - :ref:`detection (default) <caltech_pedestrian_readme_detection>`
    - :ref:`detection_10x <caltech_pedestrian_readme_detection_10x>`
    - :ref:`detection_30x <caltech_pedestrian_readme_detection_30x>`


.. note:
    The **detection** task contains 1/30 of all frames of each video.
    The **detection_10x** task contains 1/3 of all frames of each video.
    The **detection_30x** task has all the frames of each video.


Tasks
=====

.. _caltech_pedestrian_readme_detection:

detection (default)
------------------------

- :ref:`How to use <caltech_pedestrian_detection_how_to_use>`
- :ref:`Properties <caltech_pedestrian_detection_properties>`
- :ref:`HDF5 file structure <caltech_pedestrian_detection_hdf5_file_structure>`
- :ref:`Fields <caltech_pedestrian_detection_fields>`

.. _caltech_pedestrian_detection_how_to_use:

How to use
^^^^^^^^^^

.. code-block:: python

    >>> # import the package
    >>> import dbcollection as dbc
    >>>
    >>> # load the dataset
    >>> caltech_ped = dbc.load('caltech_pedestrian')
    >>> caltech_ped
    DataLoader: "caltech_pedestrian" (detection task)


.. _caltech_pedestrian_detection_properties:

Properties
^^^^^^^^^^

- ``primary use``: object detection
- ``description``: Contains image filenames, classes and bounding box annotations for pedestrian detection in images/videos.
- ``sets``: train, test
- ``metadata file size in disk``: 728,4 kB
- ``has annotations``: **yes**
    - ``which``:
        - labels for each class/category.
        - bounding box of pedestrians.
        - occlusion % of pedestrian detections.
- ``available fields``:
    - :ref:`image_filenames <caltech_pedestrian_detection_fields_image_filenames>`
    - :ref:`classes <caltech_pedestrian_detection_fields_classes>`
    - :ref:`boxes <caltech_pedestrian_detection_fields_boxes>`
    - :ref:`boxesv <caltech_pedestrian_detection_fields_boxesv>`
    - :ref:`id <caltech_pedestrian_detection_fields_id>`
    - :ref:`occlusion <caltech_pedestrian_detection_fields_occlusion>`
    - :ref:`object_fields <caltech_pedestrian_detection_fields_object_fields>`
    - :ref:`object_ids <caltech_pedestrian_detection_fields_object_ids>`
    - :ref:`list_image_filenames_per_class <caltech_pedestrian_detection_fields_list_image_filenames_per_class>`
    - :ref:`list_boxes_per_image <caltech_pedestrian_detection_fields_list_boxes_per_image>`
    - :ref:`list_boxesv_per_image <caltech_pedestrian_detection_fields_list_boxesv_per_image>`
    - :ref:`list_object_ids_per_image <caltech_pedestrian_detection_fields_list_object_ids_per_image>`
    - :ref:`list_objects_ids_per_class <caltech_pedestrian_detection_fields_list_objects_ids_per_class>`


.. _caltech_pedestrian_detection_hdf5_file_structure:

HDF5 file structure
^^^^^^^^^^^^^^^^^^^

::

    /
    ├── train/
    │   ├── image_filenames   # dtype=np.uint8, shape=(4250,90)  (note: string in ASCII format)
    │   ├── classes           # dtype=np.uint8, shape=(4,10)     (note: string in ASCII format)
    │   ├── boxes             # dtype=np.float, shape=(6313,4)
    │   ├── boxesv            # dtype=np.float, shape=(6313,4)
    │   ├── id                # dtype=np.int32, shape=(6313,)
    │   ├── occlusion         # dtype=np.float, shape=(6313,)
    │   ├── object_fields     # dtype=np.uint8, shape=(6,16)     (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(6313,6)
    │   ├── list_image_filenames_per_class   # dtype=np.int32, shape=(4,5033))
    │   ├── list_boxes_per_image             # dtype=np.int32, shape=(4250,22))
    │   ├── list_boxesv_per_image            # dtype=np.int32, shape=(4250,22))
    │   ├── list_object_ids_per_image        # dtype=np.int32, shape=(4250,22))
    │   └── list_objects_ids_per_class       # dtype=np.int32, shape=(4,5033))
    │
    └── test/
        ├── image_filenames   # dtype=np.uint8, shape=(4024,90)  (note: string in ASCII format)
        ├── classes           # dtype=np.uint8, shape=(4,10)     (note: string in ASCII format)
        ├── boxes             # dtype=np.float, shape=(5109,4)
        ├── boxesv            # dtype=np.float, shape=(5109,4)
        ├── id                # dtype=np.int32, shape=(5109,)
        ├── occlusion         # dtype=np.float, shape=(5109,)
        ├── object_fields     # dtype=np.uint8, shape=(6,16)     (note: string in ASCII format)
        ├── object_ids        # dtype=np.int32, shape=(5109,6)
        ├── list_image_filenames_per_class   # dtype=np.int32, shape=(4,2010))
        ├── list_boxes_per_image             # dtype=np.int32, shape=(4024,13))
        ├── list_boxesv_per_image            # dtype=np.int32, shape=(4024,13))
        ├── list_object_ids_per_image        # dtype=np.int32, shape=(4024,13))
        └── list_objects_ids_per_class       # dtype=np.int32, shape=(4,4371))


.. _caltech_pedestrian_detection_fields:

Fields
^^^^^^

.. _caltech_pedestrian_detection_fields_image_filenames:

- ``image_filenames``: image file path + names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_fields_classes:

- ``classes``: class names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_fields_boxes:

- ``boxes``: bounding boxes
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format (x1,y1,x2,y2)

.. _caltech_pedestrian_detection_fields_boxesv:

- ``boxesv``: bounding boxes (visible)
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format (x1,y1,x2,y2)

.. _caltech_pedestrian_detection_fields_id:

- ``id``: label ids
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1

.. _caltech_pedestrian_detection_fields_occlusion:

- ``occlusion``: occlusion percentage
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1

.. _caltech_pedestrian_detection_fields_object_fields:

- ``object_fields``: list of field names of the object id list
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
    - ``note``: key field (*field name* aggregator)

.. _caltech_pedestrian_detection_fields_object_ids:

- ``object_ids``: list of field ids
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: key field (*field id* aggregator)

.. _caltech_pedestrian_detection_fields_list_image_filenames_per_class:

- ``list_image_filenames_per_class``: list of image per class
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_fields_list_boxes_per_image:

- ``list_boxes_per_image``: list of bounding boxes per image
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_fields_list_boxesv_per_image:

- ``list_boxesv_per_image``: list of (visible) bounding boxes per image
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_fields_list_object_ids_per_image:

- ``list_object_ids_per_image``: list of object ids per image
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_fields_list_objects_ids_per_class:

- ``list_objects_ids_per_class``: list of object ids per class
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list


.. _caltech_pedestrian_readme_detection_10x:

detection_10x
------------------------

- :ref:`How to use <caltech_pedestrian_detection_10x_how_to_use>`
- :ref:`Properties <caltech_pedestrian_detection_10x_properties>`
- :ref:`HDF5 file structure <caltech_pedestrian_detection_10x_hdf5_file_structure>`
- :ref:`Fields <caltech_pedestrian_detection_10x_fields>`

.. _caltech_pedestrian_detection_10x_how_to_use:

How to use
^^^^^^^^^^

.. code-block:: python

    >>> # import the package
    >>> import dbcollection as dbc
    >>>
    >>> # load the dataset
    >>> caltech_ped_10x = dbc.load('caltech_pedestrian', 'detection_10x')
    >>> caltech_ped_10x
    DataLoader: "caltech_pedestrian" (detection_10x task)


.. _caltech_pedestrian_detection_10x_properties:

Properties
^^^^^^^^^^

- ``primary use``: object detection
- ``description``: Contains image filenames, classes and bounding box annotations for pedestrian detection in images/videos. It contains 10x more annotations than the default task ('detection').
- ``sets``: train, test
- ``metadata file size in disk``: 6,2 MB
- ``has annotations``: **yes**
    - ``which``:
        - labels for each class/category.
        - bounding box of pedestrians.
        - occlusion % of pedestrian detections.
- ``available fields``:
    - :ref:`image_filenames <caltech_pedestrian_detection_10x_fields_image_filenames>`
    - :ref:`classes <caltech_pedestrian_detection_10x_fields_classes>`
    - :ref:`boxes <caltech_pedestrian_detection_10x_fields_boxes>`
    - :ref:`boxesv <caltech_pedestrian_detection_10x_fields_boxesv>`
    - :ref:`id <caltech_pedestrian_detection_10x_fields_id>`
    - :ref:`occlusion <caltech_pedestrian_detection_10x_fields_occlusion>`
    - :ref:`object_fields <caltech_pedestrian_detection_10x_fields_object_fields>`
    - :ref:`object_ids <caltech_pedestrian_detection_10x_fields_object_ids>`
    - :ref:`list_image_filenames_per_class <caltech_pedestrian_detection_10x_fields_list_image_filenames_per_class>`
    - :ref:`list_boxes_per_image <caltech_pedestrian_detection_10x_fields_list_boxes_per_image>`
    - :ref:`list_boxesv_per_image <caltech_pedestrian_detection_10x_fields_list_boxesv_per_image>`
    - :ref:`list_object_ids_per_image <caltech_pedestrian_detection_10x_fields_list_object_ids_per_image>`
    - :ref:`list_objects_ids_per_class <caltech_pedestrian_detection_10x_fields_list_objects_ids_per_class>`


.. _caltech_pedestrian_detection_10x_hdf5_file_structure:

HDF5 file structure
^^^^^^^^^^^^^^^^^^^

::

    /
    ├── train/
    │   ├── image_filenames   # dtype=np.uint8, shape=(42782,90)  (note: string in ASCII format)
    │   ├── classes           # dtype=np.uint8, shape=(4,10)     (note: string in ASCII format)
    │   ├── boxes             # dtype=np.float, shape=(63538,4)
    │   ├── boxesv            # dtype=np.float, shape=(63538,4)
    │   ├── id                # dtype=np.int32, shape=(63538,)
    │   ├── occlusion         # dtype=np.float, shape=(63538,)
    │   ├── object_fields     # dtype=np.uint8, shape=(6,16)     (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(63538,6)
    │   ├── list_image_filenames_per_class   # dtype=np.int32, shape=(4,20422))
    │   ├── list_boxes_per_image             # dtype=np.int32, shape=(42782,22))
    │   ├── list_boxesv_per_image            # dtype=np.int32, shape=(42782,22))
    │   ├── list_object_ids_per_image        # dtype=np.int32, shape=(42782,22))
    │   └── list_objects_ids_per_class       # dtype=np.int32, shape=(4,50605))
    │
    └── test/
        ├── image_filenames   # dtype=np.uint8, shape=(40465,90)  (note: string in ASCII format)
        ├── classes           # dtype=np.uint8, shape=(4,10)     (note: string in ASCII format)
        ├── boxes             # dtype=np.float, shape=(51079,4)
        ├── boxesv            # dtype=np.float, shape=(51079,4)
        ├── id                # dtype=np.int32, shape=(51079,)
        ├── occlusion         # dtype=np.float, shape=(51079,)
        ├── object_fields     # dtype=np.uint8, shape=(6,16)     (note: string in ASCII format)
        ├── object_ids        # dtype=np.int32, shape=(51079,6)
        ├── list_image_filenames_per_class   # dtype=np.int32, shape=(4,20173))
        ├── list_boxes_per_image             # dtype=np.int32, shape=(40465,14))
        ├── list_boxesv_per_image            # dtype=np.int32, shape=(40465,14))
        ├── list_object_ids_per_image        # dtype=np.int32, shape=(40465,14))
        └── list_objects_ids_per_class       # dtype=np.int32, shape=(4,43748))


.. _caltech_pedestrian_detection_10x_fields:

Fields
^^^^^^

.. _caltech_pedestrian_detection_10x_fields_image_filenames:

- ``image_filenames``: image file path + names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_10x_fields_classes:

- ``classes``: class names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_10x_fields_boxes:

- ``boxes``: bounding boxes
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format (x1,y1,x2,y2)

.. _caltech_pedestrian_detection_10x_fields_boxesv:

- ``boxesv``: bounding boxes (visible)
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format (x1,y1,x2,y2)

.. _caltech_pedestrian_detection_10x_fields_id:

- ``id``: label ids
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1

.. _caltech_pedestrian_detection_10x_fields_occlusion:

- ``occlusion``: occlusion percentage
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1

.. _caltech_pedestrian_detection_10x_fields_object_fields:

- ``object_fields``: list of field names of the object id list
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
    - ``note``: key field (*field name* aggregator)

.. _caltech_pedestrian_detection_10x_fields_object_ids:

- ``object_ids``: list of field ids
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: key field (*field id* aggregator)

.. _caltech_pedestrian_detection_10x_fields_list_image_filenames_per_class:

- ``list_image_filenames_per_class``: list of image per class
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_10x_fields_list_boxes_per_image:

- ``list_boxes_per_image``: list of bounding boxes per image
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_10x_fields_list_boxesv_per_image:

- ``list_boxesv_per_image``: list of (visible) bounding boxes per image
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_10x_fields_list_object_ids_per_image:

- ``list_object_ids_per_image``: list of object ids per image
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_10x_fields_list_objects_ids_per_class:

- ``list_objects_ids_per_class``: list of object ids per class
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list


.. _caltech_pedestrian_readme_detection_30x:

detection_30x
------------------------

- :ref:`How to use <caltech_pedestrian_detection_30x_how_to_use>`
- :ref:`Properties <caltech_pedestrian_detection_30x_properties>`
- :ref:`HDF5 file structure <caltech_pedestrian_detection_30x_hdf5_file_structure>`
- :ref:`Fields <caltech_pedestrian_detection_30x_fields>`

.. _caltech_pedestrian_detection_30x_how_to_use:

How to use
^^^^^^^^^^

.. code-block:: python

    >>> # import the package
    >>> import dbcollection as dbc
    >>>
    >>> # load the dataset
    >>> caltech_ped_30x = dbc.load('caltech_pedestrian', 'detection_30x')
    >>> caltech_ped_30x
    DataLoader: "caltech_pedestrian" (detection_30x task)


.. _caltech_pedestrian_detection_30x_properties:

Properties
^^^^^^^^^^

- ``primary use``: object detection
- ``description``: Contains image filenames, classes and bounding box annotations for pedestrian detection in images/videos. It contains 10x more annotations than the default task ('detection').
- ``sets``: train, test
- ``metadata file size in disk``: 17,4 MB
- ``has annotations``: **yes**
    - ``which``:
        - labels for each class/category.
        - bounding box of pedestrians.
        - occlusion % of pedestrian detections.
- ``available fields``:
    - :ref:`image_filenames <caltech_pedestrian_detection_30x_fields_image_filenames>`
    - :ref:`classes <caltech_pedestrian_detection_30x_fields_classes>`
    - :ref:`boxes <caltech_pedestrian_detection_30x_fields_boxes>`
    - :ref:`boxesv <caltech_pedestrian_detection_30x_fields_boxesv>`
    - :ref:`id <caltech_pedestrian_detection_30x_fields_id>`
    - :ref:`occlusion <caltech_pedestrian_detection_30x_fields_occlusion>`
    - :ref:`object_fields <caltech_pedestrian_detection_30x_fields_object_fields>`
    - :ref:`object_ids <caltech_pedestrian_detection_30x_fields_object_ids>`
    - :ref:`list_image_filenames_per_class <caltech_pedestrian_detection_30x_fields_list_image_filenames_per_class>`
    - :ref:`list_boxes_per_image <caltech_pedestrian_detection_30x_fields_list_boxes_per_image>`
    - :ref:`list_boxesv_per_image <caltech_pedestrian_detection_30x_fields_list_boxesv_per_image>`
    - :ref:`list_object_ids_per_image <caltech_pedestrian_detection_30x_fields_list_object_ids_per_image>`
    - :ref:`list_objects_ids_per_class <caltech_pedestrian_detection_30x_fields_list_objects_ids_per_class>`


.. _caltech_pedestrian_detection_30x_hdf5_file_structure:

HDF5 file structure
^^^^^^^^^^^^^^^^^^^

::

    /
    ├── train/
    │   ├── image_filenames   # dtype=np.uint8, shape=(128419,90)  (note: string in ASCII format)
    │   ├── classes           # dtype=np.uint8, shape=(4,10)       (note: string in ASCII format)
    │   ├── boxes             # dtype=np.float, shape=(190598,4)
    │   ├── boxesv            # dtype=np.float, shape=(190598,4)
    │   ├── id                # dtype=np.int32, shape=(190598,)
    │   ├── occlusion         # dtype=np.float, shape=(190598,)
    │   ├── object_fields     # dtype=np.uint8, shape=(6,16)       (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(190598,6)
    │   ├── list_image_filenames_per_class   # dtype=np.int32, shape=(4,61274))
    │   ├── list_boxes_per_image             # dtype=np.int32, shape=(128419,22))
    │   ├── list_boxesv_per_image            # dtype=np.int32, shape=(128419,22))
    │   ├── list_object_ids_per_image        # dtype=np.int32, shape=(128419,22))
    │   └── list_objects_ids_per_class       # dtype=np.int32, shape=(4,151768))
    │
    └── test/
        ├── image_filenames   # dtype=np.uint8, shape=(121465,90)  (note: string in ASCII format)
        ├── classes           # dtype=np.uint8, shape=(4,10)       (note: string in ASCII format)
        ├── boxes             # dtype=np.float, shape=(153305,4)
        ├── boxesv            # dtype=np.float, shape=(153305,4)
        ├── id                # dtype=np.int32, shape=(153305,)
        ├── occlusion         # dtype=np.float, shape=(153305,)
        ├── object_fields     # dtype=np.uint8, shape=(6,16)       (note: string in ASCII format)
        ├── object_ids        # dtype=np.int32, shape=(153305,6)
        ├── list_image_filenames_per_class   # dtype=np.int32, shape=(4,60537))
        ├── list_boxes_per_image             # dtype=np.int32, shape=(121465,14))
        ├── list_boxesv_per_image            # dtype=np.int32, shape=(121465,14))
        ├── list_object_ids_per_image        # dtype=np.int32, shape=(121465,14))
        └── list_objects_ids_per_class       # dtype=np.int32, shape=(4,131273))


.. _caltech_pedestrian_detection_30x_fields:

Fields
^^^^^^

.. _caltech_pedestrian_detection_30x_fields_image_filenames:

- ``image_filenames``: image file path + names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_30x_fields_classes:

- ``classes``: class names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_30x_fields_boxes:

- ``boxes``: bounding boxes
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format (x1,y1,x2,y2)

.. _caltech_pedestrian_detection_30x_fields_boxesv:

- ``boxesv``: bounding boxes (visible)
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format (x1,y1,x2,y2)

.. _caltech_pedestrian_detection_30x_fields_id:

- ``id``: label ids
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1

.. _caltech_pedestrian_detection_30x_fields_occlusion:

- ``occlusion``: occlusion percentage
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1

.. _caltech_pedestrian_detection_30x_fields_object_fields:

- ``object_fields``: list of field names of the object id list
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
    - ``note``: key field (*field name* aggregator)

.. _caltech_pedestrian_detection_30x_fields_object_ids:

- ``object_ids``: list of field ids
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: key field (*field id* aggregator)

.. _caltech_pedestrian_detection_30x_fields_list_image_filenames_per_class:

- ``list_image_filenames_per_class``: list of image per class
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_30x_fields_list_boxes_per_image:

- ``list_boxes_per_image``: list of bounding boxes per image
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_30x_fields_list_boxesv_per_image:

- ``list_boxesv_per_image``: list of (visible) bounding boxes per image
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_30x_fields_list_object_ids_per_image:

- ``list_object_ids_per_image``: list of object ids per image
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_30x_fields_list_objects_ids_per_class:

- ``list_objects_ids_per_class``: list of object ids per class
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
