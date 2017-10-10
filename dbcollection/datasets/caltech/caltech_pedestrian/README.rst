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
    - detection: **(default)**
        - ``primary use``: object detection
        - ``description``: Contains image filenames, classes and bounding box annotations for pedestrian detection in images/videos.
        - ``sets``: train, test
        - ``metadata file size``: 728,4 kB
        - ``has annotations``: **yes**
            - ``which``:
                - labels for each class/category.
                - bounding box of pedestrians.
                - occlusion % of annotated pedestrians.
    - detection_10x:
        - ``primary use``: object detection
        - ``description``: Contains image filenames, classes and bounding box annotations for pedestrian detection in images/videos.
        - ``sets``: train, test
        - ``metadata file size``: 6,2 MB
        - ``has annotations``: **yes**
            - ``which``:
                - labels for each class/category.
                - bounding box of pedestrians.
                - occlusion % of annotated pedestrians.
    - detection_30x:
        - ``primary use``: object detection
        - ``description``: Contains image filenames, classes and bounding box annotations for pedestrian detection in images/videos.
        - ``sets``: train, test
        - ``metadata file size``: 17,4 MB
        - ``has annotations``: **yes**
            - ``which``:
                - labels for each class/category.
                - bounding box of pedestrians.
                - occlusion % of annotated pedestrians.


.. note:
    The **detection** task contains 1/30 of all frames+annotations from each video.
    The **detection_10x** task contains 1/3 of all frames+annotations from each video.
    The **detection_30x** task has all the frames+annotations for each video.


Metadata structure (HDF5)
=========================

Task: detection
---------------

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


Fields
^^^^^^

- ``image_filenames``: image file path+names.
- ``classes``: class names.
- ``boxes``: bounding boxes in the format (x1,y1,x2,y2).
- ``boxesv``: (valid) bounding boxes in the format (x1,y1,x2,y2).
- ``id``: label ids.
- ``occlusion``: occlusion percentage.
- ``object_fields``: array of fields composing the object id list.
- ``object_ids``: array of field ids.
- ``list_image_filenames_per_class``: list of image per class.
- ``list_boxes_per_image``: list of bounding boxes per image.
- ``list_boxesv_per_image``: list of (valid) bounding boxes per image.
- ``list_object_ids_per_image``: list of object ids per image.
- ``list_objects_ids_per_class``: list of object ids per class.


Task: detection_10x
-------------------

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


Fields
^^^^^^

- ``image_filenames``: image file path+names.
- ``classes``: class names.
- ``boxes``: bounding boxes in the format (x1,y1,x2,y2).
- ``boxesv``: (valid) bounding boxes in the format (x1,y1,x2,y2).
- ``id``: label ids.
- ``occlusion``: occlusion percentage.
- ``object_fields``: array of fields composing the object id list.
- ``object_ids``: array of field ids.
- ``list_image_filenames_per_class``: list of image per class.
- ``list_boxes_per_image``: list of bounding boxes per image.
- ``list_boxesv_per_image``: list of (valid) bounding boxes per image.
- ``list_object_ids_per_image``: list of object ids per image.
- ``list_objects_ids_per_class``: list of object ids per class.


Task: detection_30x
-------------------

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


Fields
^^^^^^

- ``image_filenames``: image file path+names.
- ``classes``: class names.
- ``boxes``: bounding boxes in the format (x1,y1,x2,y2).
- ``boxesv``: (valid) bounding boxes in the format (x1,y1,x2,y2).
- ``id``: label ids.
- ``occlusion``: occlusion percentage.
- ``object_fields``: array of fields composing the object id list.
- ``object_ids``: array of field ids.
- ``list_image_filenames_per_class``: list of image per class.
- ``list_boxes_per_image``: list of bounding boxes per image.
- ``list_boxesv_per_image``: list of (valid) bounding boxes per image.
- ``list_object_ids_per_image``: list of object ids per image.
- ``list_objects_ids_per_class``: list of object ids per class.


Disclaimer
==========

All rights reserved to the original creators of **Caltech Pedestrian Dataset**.

For information about the dataset and its terms of use, please see this `link <http://www.vision.caltech.edu/Image_Datasets/CaltechPedestrians>`_.