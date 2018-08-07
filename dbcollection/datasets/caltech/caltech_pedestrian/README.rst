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
    - :ref:`detection_clean <caltech_pedestrian_readme_detection_clean>`
    - :ref:`detection_10x <caltech_pedestrian_readme_detection_10x>`
    - :ref:`detection_10x_clean <caltech_pedestrian_readme_detection_10x_clean>`
    - :ref:`detection_30x <caltech_pedestrian_readme_detection_30x>`
    - :ref:`detection_30x_clean <caltech_pedestrian_readme_detection_30x_clean>`

.. note::
    The ``detection`` tasks contains 1/30 of all frames of each video.

    The ``detection_10x`` tasks contains 1/3 of all frames of each video.

    The ``detection_30x`` tasks has all the frames of each video.

    Tasks ending with ``_clean`` have bounding boxes with small area (less than 5px width/height) discarded.
    These are mostly due to bad annotations and are kept from these tasks.


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
- ``metadata file size in disk``: 524,0 kB
- ``has annotations``: **yes**
    - ``which``:
        - labels for each class/category.
        - bounding box of pedestrians.
        - occlusion % of pedestrian detections.
- ``available fields``:
    - :ref:`boxes <caltech_pedestrian_detection_fields_boxes>`
    - :ref:`boxesv <caltech_pedestrian_detection_fields_boxesv>`
    - :ref:`classes <caltech_pedestrian_detection_fields_classes>`
    - :ref:`classes_unique <caltech_pedestrian_detection_fields_classes_unique>`
    - :ref:`id <caltech_pedestrian_detection_fields_id>`
    - :ref:`image_filenames <caltech_pedestrian_detection_fields_image_filenames>`
    - :ref:`image_filenames_unique <caltech_pedestrian_detection_fields_image_filenames_unique>`
    - :ref:`object_fields <caltech_pedestrian_detection_fields_object_fields>`
    - :ref:`object_ids <caltech_pedestrian_detection_fields_object_ids>`
    - :ref:`occlusion <caltech_pedestrian_detection_fields_occlusion>`
    - :ref:`list_boxes_per_image <caltech_pedestrian_detection_fields_list_boxes_per_image>`
    - :ref:`list_boxesv_per_image <caltech_pedestrian_detection_fields_list_boxesv_per_image>`
    - :ref:`list_image_filenames_per_class <caltech_pedestrian_detection_fields_list_image_filenames_per_class>`
    - :ref:`list_object_ids_per_image <caltech_pedestrian_detection_fields_list_object_ids_per_image>`
    - :ref:`list_objects_ids_per_class <caltech_pedestrian_detection_fields_list_objects_ids_per_class>`


.. _caltech_pedestrian_detection_hdf5_file_structure:

HDF5 file structure
^^^^^^^^^^^^^^^^^^^

::

    /
    ├── train/
    │   ├── boxes                    # dtype=np.float, shape=(6365,4)
    │   ├── boxesv                   # dtype=np.float, shape=(6365,4)
    │   ├── classes                  # dtype=np.uint8, shape=(6365,10)  (note: string in ASCII format)
    │   ├── classes_unique           # dtype=np.uint8, shape=(4,10)     (note: string in ASCII format)
    │   ├── id                       # dtype=np.int32, shape=(6365,)
    │   ├── image_filenames          # dtype=np.uint8, shape=(6365,90)  (note: string in ASCII format)
    │   ├── image_filenames_unique   # dtype=np.uint8, shape=(4250,90)  (note: string in ASCII format)
    │   ├── object_fields            # dtype=np.uint8, shape=(6,16)     (note: string in ASCII format)
    │   ├── object_ids               # dtype=np.int32, shape=(6365,6)
    │   ├── occlusion                # dtype=np.float, shape=(6365,)
    │   ├── list_boxes_per_image             # dtype=np.int32, shape=(2223,22)
    │   ├── list_boxesv_per_image            # dtype=np.int32, shape=(2223,22)
    │   ├── list_image_filenames_per_class   # dtype=np.int32, shape=(4,2033)
    │   ├── list_object_ids_per_image        # dtype=np.int32, shape=(2223,22)
    │   └── list_objects_ids_per_class       # dtype=np.int32, shape=(4,5081)
    │
    └── test/
        ├── boxes                    # dtype=np.float, shape=(5142,4)
        ├── boxesv                   # dtype=np.float, shape=(5142,4)
        ├── classes                  # dtype=np.uint8, shape=(5142,10)  (note: string in ASCII format)
        ├── classes_unique           # dtype=np.uint8, shape=(4,10)     (note: string in ASCII format)
        ├── id                       # dtype=np.int32, shape=(5142,)
        ├── image_filenames          # dtype=np.uint8, shape=(5142,90)  (note: string in ASCII format)
        ├── image_filenames_unique   # dtype=np.uint8, shape=(4024,90)  (note: string in ASCII format)
        ├── object_fields            # dtype=np.uint8, shape=(6,16)     (note: string in ASCII format)
        ├── object_ids               # dtype=np.int32, shape=(5142,6)
        ├── occlusion                # dtype=np.float, shape=(5142,)
        ├── list_boxes_per_image             # dtype=np.int32, shape=(2152,13)
        ├── list_boxesv_per_image            # dtype=np.int32, shape=(2152,13)
        ├── list_image_filenames_per_class   # dtype=np.int32, shape=(4,2014)
        ├── list_object_ids_per_image        # dtype=np.int32, shape=(2152,13)
        └── list_objects_ids_per_class       # dtype=np.int32, shape=(4,4401)


.. _caltech_pedestrian_detection_fields:

Fields
^^^^^^

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

.. _caltech_pedestrian_detection_fields_classes:

- ``classes``: class names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_fields_classes_unique:

- ``classes``: unique class names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_fields_id:

- ``id``: label ids
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1

.. _caltech_pedestrian_detection_fields_image_filenames:

- ``image_filenames``: image file path + names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_fields_image_filenames_unique:

- ``image_filenames``: unique image file path + names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

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

.. _caltech_pedestrian_detection_fields_occlusion:

- ``occlusion``: occlusion percentage
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1

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

.. _caltech_pedestrian_detection_fields_list_image_filenames_per_class:

- ``list_image_filenames_per_class``: list of image per class
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


.. _caltech_pedestrian_readme_detection_clean:

detection_clean
------------------------

- :ref:`How to use <caltech_pedestrian_detection_clean_how_to_use>`
- :ref:`Properties <caltech_pedestrian_detection_clean_properties>`
- :ref:`HDF5 file structure <caltech_pedestrian_detection_clean_hdf5_file_structure>`
- :ref:`Fields <caltech_pedestrian_detection_clean_fields>`

.. _caltech_pedestrian_detection_clean_how_to_use:

How to use
^^^^^^^^^^

.. code-block:: python

    >>> # import the package
    >>> import dbcollection as dbc
    >>>
    >>> # load the dataset
    >>> caltech_ped_clean = dbc.load('caltech_pedestrian', 'detection_clean')
    >>> caltech_ped_clean
    DataLoader: "caltech_pedestrian" (detection_clean task)


.. _caltech_pedestrian_detection_clean_properties:

Properties
^^^^^^^^^^

- ``primary use``: object detection
- ``description``: Contains image filenames, classes and bounding box annotations for pedestrian detection in images/videos. Very small annotations (<5px height/width) have been discarded.
- ``sets``: train, test
- ``metadata file size in disk``: 728,4 kB
- ``has annotations``: **yes**
    - ``which``:
        - labels for each class/category.
        - bounding box of pedestrians.
        - occlusion % of pedestrian detections.
- ``available fields``:
    - :ref:`boxes <caltech_pedestrian_detection_clean_fields_boxes>`
    - :ref:`boxesv <caltech_pedestrian_detection_clean_fields_boxesv>`
    - :ref:`classes <caltech_pedestrian_detection_clean_fields_classes>`
    - :ref:`classes_unique <caltech_pedestrian_detection_clean_fields_classes_unique>`
    - :ref:`id <caltech_pedestrian_detection_clean_fields_id>`
    - :ref:`image_filenames <caltech_pedestrian_detection_clean_fields_image_filenames>`
    - :ref:`image_filenames_unique <caltech_pedestrian_detection_clean_fields_image_filenames_unique>`
    - :ref:`object_fields <caltech_pedestrian_detection_clean_fields_object_fields>`
    - :ref:`object_ids <caltech_pedestrian_detection_clean_fields_object_ids>`
    - :ref:`occlusion <caltech_pedestrian_detection_clean_fields_occlusion>`
    - :ref:`list_boxes_per_image <caltech_pedestrian_detection_clean_fields_list_boxes_per_image>`
    - :ref:`list_boxesv_per_image <caltech_pedestrian_detection_clean_fields_list_boxesv_per_image>`
    - :ref:`list_image_filenames_per_class <caltech_pedestrian_detection_clean_fields_list_image_filenames_per_class>`
    - :ref:`list_object_ids_per_image <caltech_pedestrian_detection_clean_fields_list_object_ids_per_image>`
    - :ref:`list_objects_ids_per_class <caltech_pedestrian_detection_clean_fields_list_objects_ids_per_class>`


.. _caltech_pedestrian_detection_clean_hdf5_file_structure:

HDF5 file structure
^^^^^^^^^^^^^^^^^^^

::

    /
    ├── train/
    │   ├── boxes                    # dtype=np.float, shape=(6313,4)
    │   ├── boxesv                   # dtype=np.float, shape=(6313,4)
    │   ├── classes                  # dtype=np.uint8, shape=(6313,10)  (note: string in ASCII format)
    │   ├── classes_unique           # dtype=np.uint8, shape=(4,10)     (note: string in ASCII format)
    │   ├── id                       # dtype=np.int32, shape=(6313,)
    │   ├── image_filenames          # dtype=np.uint8, shape=(6313,90)  (note: string in ASCII format)
    │   ├── image_filenames_unique   # dtype=np.uint8, shape=(4250,90)  (note: string in ASCII format)
    │   ├── object_fields            # dtype=np.uint8, shape=(6,16)     (note: string in ASCII format)
    │   ├── object_ids               # dtype=np.int32, shape=(6313,6)
    │   ├── occlusion                # dtype=np.float, shape=(6313,)
    │   ├── list_boxes_per_image             # dtype=np.int32, shape=(2218,22)
    │   ├── list_boxesv_per_image            # dtype=np.int32, shape=(2218,22)
    │   ├── list_image_filenames_per_class   # dtype=np.int32, shape=(4,2027)
    │   ├── list_object_ids_per_image        # dtype=np.int32, shape=(2218,22)
    │   └── list_objects_ids_per_class       # dtype=np.int32, shape=(4,5033)
    │
    └── test/
        ├── boxes                    # dtype=np.float, shape=(5109,4)
        ├── boxesv                   # dtype=np.float, shape=(5109,4)
        ├── classes                  # dtype=np.uint8, shape=(5109,10)  (note: string in ASCII format)
        ├── classes_unique           # dtype=np.uint8, shape=(4,10)     (note: string in ASCII format)
        ├── id                       # dtype=np.int32, shape=(5109,)
        ├── image_filenames          # dtype=np.uint8, shape=(5109,90)  (note: string in ASCII format)
        ├── image_filenames_unique   # dtype=np.uint8, shape=(4024,90)  (note: string in ASCII format)
        ├── object_fields            # dtype=np.uint8, shape=(6,16)     (note: string in ASCII format)
        ├── object_ids               # dtype=np.int32, shape=(5109,6)
        ├── occlusion                # dtype=np.float, shape=(5109,)
        ├── list_boxes_per_image             # dtype=np.int32, shape=(2148,13)
        ├── list_boxesv_per_image            # dtype=np.int32, shape=(2148,13)
        ├── list_image_filenames_per_class   # dtype=np.int32, shape=(4,2010)
        ├── list_object_ids_per_image        # dtype=np.int32, shape=(2148,13)
        └── list_objects_ids_per_class       # dtype=np.int32, shape=(4,4371)

.. _caltech_pedestrian_detection_clean_fields:

Fields
^^^^^^

.. _caltech_pedestrian_detection_clean_fields_boxes:

- ``boxes``: bounding boxes
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format (x1,y1,x2,y2)

.. _caltech_pedestrian_detection_clean_fields_boxesv:

- ``boxesv``: bounding boxes (visible)
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format (x1,y1,x2,y2)

.. _caltech_pedestrian_detection_clean_fields_classes:

- ``classes``: class names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_clean_fields_classes_unique:

- ``classes``: unique class names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_clean_fields_id:

- ``id``: label ids
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1

.. _caltech_pedestrian_detection_clean_fields_image_filenames:

- ``image_filenames``: image file path + names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_clean_fields_image_filenames_unique:

- ``image_filenames``: unique image file path + names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_clean_fields_object_fields:

- ``object_fields``: list of field names of the object id list
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
    - ``note``: key field (*field name* aggregator)

.. _caltech_pedestrian_detection_clean_fields_object_ids:

- ``object_ids``: list of field ids
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: key field (*field id* aggregator)

.. _caltech_pedestrian_detection_clean_fields_occlusion:

- ``occlusion``: occlusion percentage
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1

.. _caltech_pedestrian_detection_clean_fields_list_boxes_per_image:

- ``list_boxes_per_image``: list of bounding boxes per image
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_clean_fields_list_boxesv_per_image:

- ``list_boxesv_per_image``: list of (visible) bounding boxes per image
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_clean_fields_list_image_filenames_per_class:

- ``list_image_filenames_per_class``: list of image per class
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_clean_fields_list_object_ids_per_image:

- ``list_object_ids_per_image``: list of object ids per image
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_clean_fields_list_objects_ids_per_class:

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
- ``metadata file size in disk``: 4,3 MB
- ``has annotations``: **yes**
    - ``which``:
        - labels for each class/category.
        - bounding box of pedestrians.
        - occlusion % of pedestrian detections.
- ``available fields``:
    - :ref:`boxes <caltech_pedestrian_detection_10x_fields_boxes>`
    - :ref:`boxesv <caltech_pedestrian_detection_10x_fields_boxesv>`
    - :ref:`classes <caltech_pedestrian_detection_10x_fields_classes>`
    - :ref:`classes_unique <caltech_pedestrian_detection_10x_fields_classes_unique>`
    - :ref:`id <caltech_pedestrian_detection_10x_fields_id>`
    - :ref:`image_filenames <caltech_pedestrian_detection_10x_fields_image_filenames>`
    - :ref:`image_filenames_unique <caltech_pedestrian_detection_10x_fields_image_filenames_unique>`
    - :ref:`object_fields <caltech_pedestrian_detection_10x_fields_object_fields>`
    - :ref:`object_ids <caltech_pedestrian_detection_10x_fields_object_ids>`
    - :ref:`occlusion <caltech_pedestrian_detection_10x_fields_occlusion>`
    - :ref:`list_boxes_per_image <caltech_pedestrian_detection_10x_fields_list_boxes_per_image>`
    - :ref:`list_boxesv_per_image <caltech_pedestrian_detection_10x_fields_list_boxesv_per_image>`
    - :ref:`list_image_filenames_per_class <caltech_pedestrian_detection_10x_fields_list_image_filenames_per_class>`
    - :ref:`list_object_ids_per_image <caltech_pedestrian_detection_10x_fields_list_object_ids_per_image>`
    - :ref:`list_objects_ids_per_class <caltech_pedestrian_detection_10x_fields_list_objects_ids_per_class>`


.. _caltech_pedestrian_detection_10x_hdf5_file_structure:

HDF5 file structure
^^^^^^^^^^^^^^^^^^^

::

    /
    ├── train/
    │   ├── boxes                    # dtype=np.float, shape=(64063,4)
    │   ├── boxesv                   # dtype=np.float, shape=(64063,4)
    │   ├── classes                  # dtype=np.uint8, shape=(64063,10)  (note: string in ASCII format)
    │   ├── classes_unique           # dtype=np.uint8, shape=(4,10)      (note: string in ASCII format)
    │   ├── id                       # dtype=np.int32, shape=(64063,)
    │   ├── image_filenames          # dtype=np.uint8, shape=(64063,90)  (note: string in ASCII format)
    │   ├── image_filenames_unique   # dtype=np.uint8, shape=(42782,90)  (note: string in ASCII format)
    │   ├── object_fields            # dtype=np.uint8, shape=(6,16)      (note: string in ASCII format)
    │   ├── object_ids               # dtype=np.int32, shape=(64063,6)
    │   ├── occlusion                # dtype=np.float, shape=(64063,)
    │   ├── list_boxes_per_image             # dtype=np.int32, shape=(22356,22)
    │   ├── list_boxesv_per_image            # dtype=np.int32, shape=(22356,22)
    │   ├── list_image_filenames_per_class   # dtype=np.int32, shape=(4,20480)
    │   ├── list_object_ids_per_image        # dtype=np.int32, shape=(22356,22)
    │   └── list_objects_ids_per_class       # dtype=np.int32, shape=(4,51092)
    │
    └── test/
        ├── boxes                    # dtype=np.float, shape=(51451,4)
        ├── boxesv                   # dtype=np.float, shape=(51451,4)
        ├── classes                  # dtype=np.uint8, shape=(51451,10)  (note: string in ASCII format)
        ├── classes_unique           # dtype=np.uint8, shape=(4,10)      (note: string in ASCII format)
        ├── id                       # dtype=np.int32, shape=(51451,)
        ├── image_filenames          # dtype=np.uint8, shape=(51451,90)  (note: string in ASCII format)
        ├── image_filenames_unique   # dtype=np.uint8, shape=(40465,90)  (note: string in ASCII format)
        ├── object_fields            # dtype=np.uint8, shape=(6,16)      (note: string in ASCII format)
        ├── object_ids               # dtype=np.int32, shape=(51451,6)
        ├── occlusion                # dtype=np.float, shape=(51451,)
        ├── list_boxes_per_image             # dtype=np.int32, shape=(21653,14)
        ├── list_boxesv_per_image            # dtype=np.int32, shape=(21653,14)
        ├── list_image_filenames_per_class   # dtype=np.int32, shape=(4,20239)
        ├── list_object_ids_per_image        # dtype=np.int32, shape=(21653,14)
        └── list_objects_ids_per_class       # dtype=np.int32, shape=(4,44095)


.. _caltech_pedestrian_detection_10x_fields:

Fields
^^^^^^

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

.. _caltech_pedestrian_detection_10x_fields_classes:

- ``classes``: class names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_10x_fields_classes_unique:

- ``classes``: unique class names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_10x_fields_id:

- ``id``: label ids
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1

.. _caltech_pedestrian_detection_10x_fields_image_filenames:

- ``image_filenames``: image file path + names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_10x_fields_image_filenames_unique:

- ``image_filenames``: unique image file path + names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

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

.. _caltech_pedestrian_detection_10x_fields_occlusion:

- ``occlusion``: occlusion percentage
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1

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

.. _caltech_pedestrian_detection_10x_fields_list_image_filenames_per_class:

- ``list_image_filenames_per_class``: list of image per class
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


.. _caltech_pedestrian_readme_detection_10x_clean:

detection_10x_clean
------------------------

- :ref:`How to use <caltech_pedestrian_detection_10x_clean_how_to_use>`
- :ref:`Properties <caltech_pedestrian_detection_10x_clean_properties>`
- :ref:`HDF5 file structure <caltech_pedestrian_detection_10x_clean_hdf5_file_structure>`
- :ref:`Fields <caltech_pedestrian_detection_10x_clean_fields>`

.. _caltech_pedestrian_detection_10x_clean_how_to_use:

How to use
^^^^^^^^^^

.. code-block:: python

    >>> # import the package
    >>> import dbcollection as dbc
    >>>
    >>> # load the dataset
    >>> caltech_ped_10x_clean = dbc.load('caltech_pedestrian', 'detection_10x_clean')
    >>> caltech_ped_10x_clean
    DataLoader: "caltech_pedestrian" (detection_10x_clean task)


.. _caltech_pedestrian_detection_10x_clean_properties:

Properties
^^^^^^^^^^

- ``primary use``: object detection
- ``description``: Contains image filenames, classes and bounding box annotations for pedestrian detection in images/videos. It contains 10x more annotations than the default task ('detection'). Very small annotations (<5px height/width) have been discarded.
- ``sets``: train, test
- ``metadata file size in disk``: 4,3 MB
- ``has annotations``: **yes**
    - ``which``:
        - labels for each class/category.
        - bounding box of pedestrians.
        - occlusion % of pedestrian detections.
- ``available fields``:
    - :ref:`boxes <caltech_pedestrian_detection_10x_clean_fields_boxes>`
    - :ref:`boxesv <caltech_pedestrian_detection_10x_clean_fields_boxesv>`
    - :ref:`classes <caltech_pedestrian_detection_10x_clean_fields_classes>`
    - :ref:`classes_unique <caltech_pedestrian_detection_10x_clean_fields_classes_unique>`
    - :ref:`id <caltech_pedestrian_detection_10x_clean_fields_id>`
    - :ref:`image_filenames <caltech_pedestrian_detection_10x_clean_fields_image_filenames>`
    - :ref:`image_filenames_unique <caltech_pedestrian_detection_10x_clean_fields_image_filenames_unique>`
    - :ref:`object_fields <caltech_pedestrian_detection_10x_clean_fields_object_fields>`
    - :ref:`object_ids <caltech_pedestrian_detection_10x_clean_fields_object_ids>`
    - :ref:`occlusion <caltech_pedestrian_detection_10x_clean_fields_occlusion>`
    - :ref:`list_boxes_per_image <caltech_pedestrian_detection_10x_clean_fields_list_boxes_per_image>`
    - :ref:`list_boxesv_per_image <caltech_pedestrian_detection_10x_clean_fields_list_boxesv_per_image>`
    - :ref:`list_image_filenames_per_class <caltech_pedestrian_detection_10x_clean_fields_list_image_filenames_per_class>`
    - :ref:`list_object_ids_per_image <caltech_pedestrian_detection_10x_clean_fields_list_object_ids_per_image>`
    - :ref:`list_objects_ids_per_class <caltech_pedestrian_detection_10x_clean_fields_list_objects_ids_per_class>`


.. _caltech_pedestrian_detection_10x_clean_hdf5_file_structure:

HDF5 file structure
^^^^^^^^^^^^^^^^^^^

::

    /
    ├── train/
    │   ├── boxes                    # dtype=np.float, shape=(63538,4)
    │   ├── boxesv                   # dtype=np.float, shape=(63538,4)
    │   ├── classes                  # dtype=np.uint8, shape=(63538,10)  (note: string in ASCII format)
    │   ├── classes_unique           # dtype=np.uint8, shape=(4,10)      (note: string in ASCII format)
    │   ├── id                       # dtype=np.int32, shape=(63538,)
    │   ├── image_filenames          # dtype=np.uint8, shape=(63538,90)  (note: string in ASCII format)
    │   ├── image_filenames_unique   # dtype=np.uint8, shape=(42782,90)  (note: string in ASCII format)
    │   ├── object_fields            # dtype=np.uint8, shape=(6,16)      (note: string in ASCII format)
    │   ├── object_ids               # dtype=np.int32, shape=(63538,6)
    │   ├── occlusion                # dtype=np.float, shape=(63538,)
    │   ├── list_boxes_per_image             # dtype=np.int32, shape=(22303,22)
    │   ├── list_boxesv_per_image            # dtype=np.int32, shape=(22303,22)
    │   ├── list_image_filenames_per_class   # dtype=np.int32, shape=(4,20422)
    │   ├── list_object_ids_per_image        # dtype=np.int32, shape=(22303,22)
    │   └── list_objects_ids_per_class       # dtype=np.int32, shape=(4,50605)
    │
    └── test/
        ├── boxes                    # dtype=np.float, shape=(51079,4)
        ├── boxesv                   # dtype=np.float, shape=(51079,4)
        ├── classes                  # dtype=np.uint8, shape=(51079,10)  (note: string in ASCII format)
        ├── classes_unique           # dtype=np.uint8, shape=(4,10)      (note: string in ASCII format)
        ├── id                       # dtype=np.int32, shape=(51079,)
        ├── image_filenames          # dtype=np.uint8, shape=(51079,90)  (note: string in ASCII format)
        ├── image_filenames_unique   # dtype=np.uint8, shape=(40465,90)  (note: string in ASCII format)
        ├── object_fields            # dtype=np.uint8, shape=(6,16)      (note: string in ASCII format)
        ├── object_ids               # dtype=np.int32, shape=(51079,6)
        ├── occlusion                # dtype=np.float, shape=(51079,)
        ├── list_boxes_per_image             # dtype=np.int32, shape=(21590,14)
        ├── list_boxesv_per_image            # dtype=np.int32, shape=(21590,14)
        ├── list_image_filenames_per_class   # dtype=np.int32, shape=(4,20173)
        ├── list_object_ids_per_image        # dtype=np.int32, shape=(21590,14)
        └── list_objects_ids_per_class       # dtype=np.int32, shape=(4,43748)

.. _caltech_pedestrian_detection_10x_clean_fields:

Fields
^^^^^^

.. _caltech_pedestrian_detection_10x_clean_fields_boxes:

- ``boxes``: bounding boxes
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format (x1,y1,x2,y2)

.. _caltech_pedestrian_detection_10x_clean_fields_boxesv:

- ``boxesv``: bounding boxes (visible)
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format (x1,y1,x2,y2)

.. _caltech_pedestrian_detection_10x_clean_fields_classes:

- ``classes``: class names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_10x_clean_fields_classes_unique:

- ``classes``: unique class names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_10x_clean_fields_id:

- ``id``: label ids
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1

.. _caltech_pedestrian_detection_10x_clean_fields_image_filenames:

- ``image_filenames``: image file path + names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_10x_clean_fields_image_filenames_unique:

- ``image_filenames``: unique image file path + names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_10x_clean_fields_object_fields:

- ``object_fields``: list of field names of the object id list
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
    - ``note``: key field (*field name* aggregator)

.. _caltech_pedestrian_detection_10x_clean_fields_object_ids:

- ``object_ids``: list of field ids
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: key field (*field id* aggregator)

.. _caltech_pedestrian_detection_10x_clean_fields_occlusion:

- ``occlusion``: occlusion percentage
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1

.. _caltech_pedestrian_detection_10x_clean_fields_list_boxes_per_image:

- ``list_boxes_per_image``: list of bounding boxes per image
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_10x_clean_fields_list_boxesv_per_image:

- ``list_boxesv_per_image``: list of (visible) bounding boxes per image
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_10x_clean_fields_list_image_filenames_per_class:

- ``list_image_filenames_per_class``: list of image per class
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_10x_clean_fields_list_object_ids_per_image:

- ``list_object_ids_per_image``: list of object ids per image
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_10x_clean_fields_list_objects_ids_per_class:

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
- ``metadata file size in disk``: 12,0 MB
- ``has annotations``: **yes**
    - ``which``:
        - labels for each class/category.
        - bounding box of pedestrians.
        - occlusion % of pedestrian detections.
- ``available fields``:
    - :ref:`boxes <caltech_pedestrian_detection_30x_fields_boxes>`
    - :ref:`boxesv <caltech_pedestrian_detection_30x_fields_boxesv>`
    - :ref:`classes <caltech_pedestrian_detection_30x_fields_classes>`
    - :ref:`classes_unique <caltech_pedestrian_detection_30x_fields_classes_unique>`
    - :ref:`id <caltech_pedestrian_detection_30x_fields_id>`
    - :ref:`image_filenames <caltech_pedestrian_detection_30x_fields_image_filenames>`
    - :ref:`image_filenames_unique <caltech_pedestrian_detection_30x_fields_image_filenames_unique>`
    - :ref:`object_fields <caltech_pedestrian_detection_30x_fields_object_fields>`
    - :ref:`object_ids <caltech_pedestrian_detection_30x_fields_object_ids>`
    - :ref:`occlusion <caltech_pedestrian_detection_30x_fields_occlusion>`
    - :ref:`list_boxes_per_image <caltech_pedestrian_detection_30x_fields_list_boxes_per_image>`
    - :ref:`list_boxesv_per_image <caltech_pedestrian_detection_30x_fields_list_boxesv_per_image>`
    - :ref:`list_image_filenames_per_class <caltech_pedestrian_detection_30x_fields_list_image_filenames_per_class>`
    - :ref:`list_object_ids_per_image <caltech_pedestrian_detection_30x_fields_list_object_ids_per_image>`
    - :ref:`list_objects_ids_per_class <caltech_pedestrian_detection_30x_fields_list_objects_ids_per_class>`


.. _caltech_pedestrian_detection_30x_hdf5_file_structure:

HDF5 file structure
^^^^^^^^^^^^^^^^^^^

::

    /
    ├── train/
    │   ├── boxes                    # dtype=np.float, shape=(192185,4)
    │   ├── boxesv                   # dtype=np.float, shape=(192185,4)
    │   ├── classes                  # dtype=np.uint8, shape=(192185,10)  (note: string in ASCII format)
    │   ├── classes_unique           # dtype=np.uint8, shape=(4,10)       (note: string in ASCII format)
    │   ├── id                       # dtype=np.int32, shape=(192185,)
    │   ├── image_filenames          # dtype=np.uint8, shape=(192185,90)  (note: string in ASCII format)
    │   ├── image_filenames_unique   # dtype=np.uint8, shape=(128419,90)  (note: string in ASCII format)
    │   ├── object_fields            # dtype=np.uint8, shape=(6,16)       (note: string in ASCII format)
    │   ├── object_ids               # dtype=np.int32, shape=(192185,6)
    │   ├── occlusion                # dtype=np.float, shape=(192185,)
    │   ├── list_boxes_per_image             # dtype=np.int32, shape=(67083,22)
    │   ├── list_boxesv_per_image            # dtype=np.int32, shape=(67083,22)
    │   ├── list_image_filenames_per_class   # dtype=np.int32, shape=(4,61439)
    │   ├── list_object_ids_per_image        # dtype=np.int32, shape=(67083,22)
    │   └── list_objects_ids_per_class       # dtype=np.int32, shape=(4,153234)
    │
    └── test/
        ├── boxes                    # dtype=np.float, shape=(154436,4)
        ├── boxesv                   # dtype=np.float, shape=(154436,4)
        ├── classes                  # dtype=np.uint8, shape=(154436,10)  (note: string in ASCII format)
        ├── classes_unique           # dtype=np.uint8, shape=(4,10)       (note: string in ASCII format)
        ├── id                       # dtype=np.int32, shape=(154436,)
        ├── image_filenames          # dtype=np.uint8, shape=(154436,90)  (note: string in ASCII format)
        ├── image_filenames_unique   # dtype=np.uint8, shape=(121465,90)  (note: string in ASCII format)
        ├── object_fields            # dtype=np.uint8, shape=(6,16)       (note: string in ASCII format)
        ├── object_ids               # dtype=np.int32, shape=(154436,6)
        ├── occlusion                # dtype=np.float, shape=(154436,)
        ├── list_boxes_per_image             # dtype=np.int32, shape=(64999,14)
        ├── list_boxesv_per_image            # dtype=np.int32, shape=(64999,14)
        ├── list_image_filenames_per_class   # dtype=np.int32, shape=(4,60748)
        ├── list_object_ids_per_image        # dtype=np.int32, shape=(64999,14)
        └── list_objects_ids_per_class       # dtype=np.int32, shape=(4,132324)


.. _caltech_pedestrian_detection_30x_fields:

Fields
^^^^^^

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

.. _caltech_pedestrian_detection_30x_fields_classes:

- ``classes``: class names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_30x_fields_classes_unique:

- ``classes``: unique class names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_30x_fields_id:

- ``id``: label ids
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1

.. _caltech_pedestrian_detection_30x_fields_image_filenames:

- ``image_filenames``: image file path + names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_30x_fields_image_filenames_unique:

- ``image_filenames``: unique image file path + names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

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

.. _caltech_pedestrian_detection_30x_fields_occlusion:

- ``occlusion``: occlusion percentage
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1

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

.. _caltech_pedestrian_detection_30x_fields_list_image_filenames_per_class:

- ``list_image_filenames_per_class``: list of image per class
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


.. _caltech_pedestrian_readme_detection_30x_clean:

detection_30x_clean
------------------------

- :ref:`How to use <caltech_pedestrian_detection_30x_clean_how_to_use>`
- :ref:`Properties <caltech_pedestrian_detection_30x_clean_properties>`
- :ref:`HDF5 file structure <caltech_pedestrian_detection_30x_clean_hdf5_file_structure>`
- :ref:`Fields <caltech_pedestrian_detection_30x_clean_fields>`

.. _caltech_pedestrian_detection_30x_clean_how_to_use:

How to use
^^^^^^^^^^

.. code-block:: python

    >>> # import the package
    >>> import dbcollection as dbc
    >>>
    >>> # load the dataset
    >>> caltech_ped_30x_clean = dbc.load('caltech_pedestrian', 'detection_30x_clean')
    >>> caltech_ped_30x_clean
    DataLoader: "caltech_pedestrian" (detection_30x_clean task)


.. _caltech_pedestrian_detection_30x_clean_properties:

Properties
^^^^^^^^^^

- ``primary use``: object detection
- ``description``: Contains image filenames, classes and bounding box annotations for pedestrian detection in images/videos. It contains 10x more annotations than the default task ('detection'). Very small annotations (<5px height/width) have been discarded.
- ``sets``: train, test
- ``metadata file size in disk``: 11,9 MB
- ``has annotations``: **yes**
    - ``which``:
        - labels for each class/category.
        - bounding box of pedestrians.
        - occlusion % of pedestrian detections.
- ``available fields``:
    - :ref:`boxes <caltech_pedestrian_detection_30x_clean_fields_boxes>`
    - :ref:`boxesv <caltech_pedestrian_detection_30x_clean_fields_boxesv>`
    - :ref:`classes <caltech_pedestrian_detection_30x_clean_fields_classes>`
    - :ref:`classes_unique <caltech_pedestrian_detection_30x_clean_fields_classes_unique>`
    - :ref:`id <caltech_pedestrian_detection_30x_clean_fields_id>`
    - :ref:`image_filenames <caltech_pedestrian_detection_30x_clean_fields_image_filenames>`
    - :ref:`image_filenames_unique <caltech_pedestrian_detection_30x_clean_fields_image_filenames_unique>`
    - :ref:`object_fields <caltech_pedestrian_detection_30x_clean_fields_object_fields>`
    - :ref:`object_ids <caltech_pedestrian_detection_30x_clean_fields_object_ids>`
    - :ref:`occlusion <caltech_pedestrian_detection_30x_clean_fields_occlusion>`
    - :ref:`list_boxes_per_image <caltech_pedestrian_detection_30x_clean_fields_list_boxes_per_image>`
    - :ref:`list_boxesv_per_image <caltech_pedestrian_detection_30x_clean_fields_list_boxesv_per_image>`
    - :ref:`list_image_filenames_per_class <caltech_pedestrian_detection_30x_clean_fields_list_image_filenames_per_class>`
    - :ref:`list_object_ids_per_image <caltech_pedestrian_detection_30x_clean_fields_list_object_ids_per_image>`
    - :ref:`list_objects_ids_per_class <caltech_pedestrian_detection_30x_clean_fields_list_objects_ids_per_class>`


.. _caltech_pedestrian_detection_30x_clean_hdf5_file_structure:

HDF5 file structure
^^^^^^^^^^^^^^^^^^^

::

    /
    ├── train/
    │   ├── boxes                    # dtype=np.float, shape=(190598,4)
    │   ├── boxesv                   # dtype=np.float, shape=(190598,4)
    │   ├── classes                  # dtype=np.uint8, shape=(190598,10)  (note: string in ASCII format)
    │   ├── classes_unique           # dtype=np.uint8, shape=(4,10)       (note: string in ASCII format)
    │   ├── id                       # dtype=np.int32, shape=(190598,)
    │   ├── image_filenames          # dtype=np.uint8, shape=(190598,90)  (note: string in ASCII format)
    │   ├── image_filenames_unique   # dtype=np.uint8, shape=(128419,90)  (note: string in ASCII format)
    │   ├── object_fields            # dtype=np.uint8, shape=(6,16)       (note: string in ASCII format)
    │   ├── object_ids               # dtype=np.int32, shape=(190598,6)
    │   ├── occlusion                # dtype=np.float, shape=(190598,)
    │   ├── list_boxes_per_image             # dtype=np.int32, shape=(66923,22)
    │   ├── list_boxesv_per_image            # dtype=np.int32, shape=(66923,22)
    │   ├── list_image_filenames_per_class   # dtype=np.int32, shape=(4,61274)
    │   ├── list_object_ids_per_image        # dtype=np.int32, shape=(66923,22)
    │   └── list_objects_ids_per_class       # dtype=np.int32, shape=(4,151768)
    │
    └── test/
        ├── boxes                    # dtype=np.float, shape=(153305,4)
        ├── boxesv                   # dtype=np.float, shape=(153305,4)
        ├── classes                  # dtype=np.uint8, shape=(153305,10)  (note: string in ASCII format)
        ├── classes_unique           # dtype=np.uint8, shape=(4,10)       (note: string in ASCII format)
        ├── id                       # dtype=np.int32, shape=(153305,)
        ├── image_filenames          # dtype=np.uint8, shape=(153305,90)  (note: string in ASCII format)
        ├── image_filenames_unique   # dtype=np.uint8, shape=(121465,90)  (note: string in ASCII format)
        ├── object_fields            # dtype=np.uint8, shape=(6,16)       (note: string in ASCII format)
        ├── object_ids               # dtype=np.int32, shape=(153305,6)
        ├── occlusion                # dtype=np.float, shape=(153305,)
        ├── list_boxes_per_image             # dtype=np.int32, shape=(64801,14)
        ├── list_boxesv_per_image            # dtype=np.int32, shape=(64801,14)
        ├── list_image_filenames_per_class   # dtype=np.int32, shape=(4,60537)
        ├── list_object_ids_per_image        # dtype=np.int32, shape=(64801,14)
        └── list_objects_ids_per_class       # dtype=np.int32, shape=(4,131273)


.. _caltech_pedestrian_detection_30x_clean_fields:

Fields
^^^^^^

.. _caltech_pedestrian_detection_30x_clean_fields_boxes:

- ``boxes``: bounding boxes
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format (x1,y1,x2,y2)

.. _caltech_pedestrian_detection_30x_clean_fields_boxesv:

- ``boxesv``: bounding boxes (visible)
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format (x1,y1,x2,y2)

.. _caltech_pedestrian_detection_30x_clean_fields_classes:

- ``classes``: class names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_30x_clean_fields_classes_unique:

- ``classes``: unique class names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_30x_clean_fields_id:

- ``id``: label ids
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1

.. _caltech_pedestrian_detection_30x_clean_fields_image_filenames:

- ``image_filenames``: image file path + names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_30x_clean_fields_image_filenames_unique:

- ``image_filenames``: unique image file path + names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _caltech_pedestrian_detection_30x_clean_fields_object_fields:

- ``object_fields``: list of field names of the object id list
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
    - ``note``: key field (*field name* aggregator)

.. _caltech_pedestrian_detection_30x_clean_fields_object_ids:

- ``object_ids``: list of field ids
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: key field (*field id* aggregator)

.. _caltech_pedestrian_detection_30x_clean_fields_occlusion:

- ``occlusion``: occlusion percentage
    - ``available in``: train, test
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1

.. _caltech_pedestrian_detection_30x_clean_fields_list_boxes_per_image:

- ``list_boxes_per_image``: list of bounding boxes per image
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_30x_clean_fields_list_boxesv_per_image:

- ``list_boxesv_per_image``: list of (visible) bounding boxes per image
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_30x_clean_fields_list_image_filenames_per_class:

- ``list_image_filenames_per_class``: list of image per class
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_30x_clean_fields_list_object_ids_per_image:

- ``list_object_ids_per_image``: list of object ids per image
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list

.. _caltech_pedestrian_detection_30x_clean_fields_list_objects_ids_per_class:

- ``list_objects_ids_per_class``: list of object ids per class
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list


Disclaimer
==========

All rights reserved to the original creators of **Caltech Pedestrian Dataset**.

For information about the dataset and its terms of use, please see this `link <http://www.vision.caltech.edu/Image_Datasets/CaltechPedestrians>`_.
