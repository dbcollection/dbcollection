.. _coco_readme:

================================
COCO - Common Objects in Context
================================

The   Microsoft   Common   Objects   in   COntext   (MS COCO)  dataset  contains  91  common  object  categories
with  82  of  them  having  more  than  5,000  labeled  instances. In total the dataset has 2,500,000 labeled
instances  in  328,000  images.


Use cases
=========

Object detection, segmentation, captioning and human body joint detection.


Properties
==========

- ``name``: coco
- ``keywords``: image_processing, detection, keypoint, captions, human, pose
- ``dataset size``: 40,3 GB
- ``is downloadable``: **yes**
- ``tasks``:
    - detection_2015: **(default)**
        - ``primary use``: object detection
        - ``description``: Contains image filenames, classes, bounding box and segmentation mask annotations for object detection in images.
        - ``sets``: train, val, test
        - ``metadata file size in disk``: 243,6 MB
        - ``has annotations``: **yes**
            - ``which``:
                - image filenames
                - object categories and supercategories
                - bounding box of pedestrians.
                - occlusion % of annotated pedestrians.
                - segmentation masks
    - detection_2016:
        - ``primary use``: object detection
        - ``description``: Contains image filenames, classes, bounding box and segmentation mask annotations for object detection in images.
        - ``sets``: train, val, test, test_dev
        - ``metadata file size in disk``: 244,7 MB
        - ``has annotations``: **yes**
            - ``which``:
                - image filenames
                - object categories and supercategories
                - bounding box of pedestrians.
                - occlusion % of annotated pedestrians.
                - segmentation masks
    - caption_2015:
        - ``primary use``: image captioning
        - ``description``: Contains image filenames and captions for image captioning.
        - ``sets``: train, val, test
        - ``metadata file size in disk``: 21,9 MB
        - ``has annotations``: **yes**
            - ``which``:
                - image filenames
                - captions
    - caption_2016:
        - ``primary use``: image captioning
        - ``description``: Contains image filenames and captions for image captioning.
        - ``sets``: train, val, test, test_dev
        - ``metadata file size in disk``: 23,0 MB
        - ``has annotations``: **yes**
            - ``which``:
                - image filenames
                - captions
    - keypoints_2016:
        - ``primary use``: human body joint detection
        - ``description``: Contains image filenames, classes, bounding box and segmentation mask annotations for object detection in images.
        - ``sets``: train, val, test, test_dev
        - ``metadata file size in disk``: 106,6 MB
        - ``has annotations``: **yes**
            - ``which``:
                - image filenames
                - object categories and supercategories
                - bounding box of pedestrians.
                - occlusion % of annotated pedestrians.
                - segmentation masks
                - body joint keypoints
                - skeleton


.. note:
    The test and test_dev sets do not have the all annotations like the train and validation sets.


Metadata structure (HDF5)
=========================

Task: detection_2015
--------------------

::

    /
    ├── train/
    │   ├── image_filenames       # dtype=np.uint8, shape=(82783,74)   (note: string in ASCII format)
    │   ├── category              # dtype=np.uint8, shape=(80,15)      (note: string in ASCII format)
    │   ├── supercategory         # dtype=np.uint8, shape=(12,11)      (note: string in ASCII format)
    │   ├── coco_annotations_ids  # dtype=np.int32, shape=(604907,)
    │   ├── coco_categories_ids   # dtype=np.int32, shape=(80,)
    │   ├── coco_images_ids       # dtype=np.int32, shape=(82783,)
    │   ├── coco_urls             # dtype=np.uint8, shape=(82783,32)   (note: string in ASCII format)
    │   ├── image_id              # dtype=np.int32, shape=(82783,)
    │   ├── category_id           # dtype=np.int32, shape=(80,)
    │   ├── annotation_id         # dtype=np.int32, shape=(604907,)
    │   ├── width                 # dtype=np.int32, shape=(82783,)
    │   ├── height                # dtype=np.int32, shape=(82783,)
    │   ├── boxes                 # dtype=np.float, shape=(604907,4)
    │   ├── iscrowd               # dtype=np.uint8, shape=(2,)
    │   ├── segmentation          # dtype=np.float, shape=(604907,10043)
    │   ├── area                  # dtype=np.int32, shape=(604907,)
    │   ├── object_fields         # dtype=np.uint8, shape=(13,16)      (note: string in ASCII format)
    │   ├── object_ids            # dtype=np.int32, shape=(604907,13)
    │   ├── list_boxes_per_image                    # dtype=np.int32, shape=(82783,93))
    │   ├── list_image_filenames_per_category       # dtype=np.int32, shape=(80,45174))
    │   ├── list_image_filenames_per_supercategory  # dtype=np.int32, shape=(12,45174))
    │   ├── list_object_ids_per_image               # dtype=np.int32, shape=(82783,93))
    │   ├── list_objects_ids_per_category           # dtype=np.int32, shape=(80,185316))
    │   └── list_objects_ids_per_supercategory      # dtype=np.int32, shape=(12,185316))
    │
    ├── val/
    │   ├── image_filenames       # dtype=np.uint8, shape=(40504,74)   (note: string in ASCII format)
    │   ├── category              # dtype=np.uint8, shape=(80,15)      (note: string in ASCII format)
    │   ├── supercategory         # dtype=np.uint8, shape=(12,11)      (note: string in ASCII format)
    │   ├── coco_annotations_ids  # dtype=np.int32, shape=(291875,)
    │   ├── coco_categories_ids   # dtype=np.int32, shape=(80,)
    │   ├── coco_images_ids       # dtype=np.int32, shape=(40504,)
    │   ├── coco_urls             # dtype=np.uint8, shape=(40504,32)   (note: string in ASCII format)
    │   ├── image_id              # dtype=np.int32, shape=(40504,)
    │   ├── category_id           # dtype=np.int32, shape=(80,)
    │   ├── annotation_id         # dtype=np.int32, shape=(291875,)
    │   ├── width                 # dtype=np.int32, shape=(40504,)
    │   ├── height                # dtype=np.int32, shape=(40504,)
    │   ├── boxes                 # dtype=np.float, shape=(291875,4)
    │   ├── iscrowd               # dtype=np.uint8, shape=(2,)
    │   ├── segmentation          # dtype=np.float, shape=(291875,7237)
    │   ├── area                  # dtype=np.int32, shape=(291875,)
    │   ├── object_fields         # dtype=np.uint8, shape=(13,16)      (note: string in ASCII format)
    │   ├── object_ids            # dtype=np.int32, shape=(291875,13)
    │   ├── list_boxes_per_image                    # dtype=np.int32, shape=(40504,93))
    │   ├── list_image_filenames_per_category       # dtype=np.int32, shape=(80,21634))
    │   ├── list_image_filenames_per_supercategory  # dtype=np.int32, shape=(12,21634))
    │   ├── list_object_ids_per_image               # dtype=np.int32, shape=(40504,93))
    │   ├── list_objects_ids_per_category           # dtype=np.int32, shape=(80,88153))
    │   └── list_objects_ids_per_supercategory      # dtype=np.int32, shape=(12,88153))
    │
    └── test/
        ├── image_filenames       # dtype=np.uint8, shape=(40775,72)   (note: string in ASCII format)
        ├── category              # dtype=np.uint8, shape=(80,15)      (note: string in ASCII format)
        ├── supercategory         # dtype=np.uint8, shape=(12,11)      (note: string in ASCII format)
        ├── coco_categories_ids   # dtype=np.int32, shape=(80,)
        ├── coco_images_ids       # dtype=np.int32, shape=(40775,)
        ├── coco_urls             # dtype=np.uint8, shape=(40775,32)   (note: string in ASCII format)
        ├── image_id              # dtype=np.int32, shape=(40775,)
        ├── category_id           # dtype=np.int32, shape=(80,)
        ├── width                 # dtype=np.int32, shape=(40775,)
        ├── height                # dtype=np.int32, shape=(40775,)
        ├── object_fields         # dtype=np.uint8, shape=(4,16)      (note: string in ASCII format)
        ├── object_ids            # dtype=np.int32, shape=(40775,4)
        └── list_object_ids_per_image   # dtype=np.int32, shape=(40775,1))


Fields
^^^^^^

- ``image_filenames``: image file path+names
    - ``available in``: train, val, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``category``: category names
    - ``available in``: train, val, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``supercategory``: super category names
    - ``available in``: train, val, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``coco_annotations_ids``: reference to coco annotation ids  (useful for evaluating on coco)
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``coco_categories_ids``: reference to coco category ids   (useful for evaluating on coco)
    - ``available in``: train, val, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``coco_images_ids``: reference to coco image filename ids   (useful for evaluating on coco)
    - ``available in``: train, val, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``coco_urls``: coco urls
    - ``available in``: train, val, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``image_id``: image filename ids
    - ``available in``: train, val, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``category_id``: category ids
    - ``available in``: train, val, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``annotation_id``: annotation ids
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``width``: image width
    - ``available in``: train, val, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``height``: image height
    - ``available in``: train, val, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``boxes``: bounding box
    - ``available in``: train, val
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format (x1,y1,x2,y2)
- ``iscrowd``: is crowd (0 - False, 1 - True)
    - ``available in``: train, val
    - ``dtype``: np.uint8
    - ``is padded``: False
    - ``fill value``: -1
- ``segmentation``: segmentation mask
    - ``available in``: train, val
    - ``dtype``: np.float
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: the masks come in 3 different formats, but they are mostly lists of lists. These have been packed (vectorized) into an array with a single dimension in order to be stored in the HDF5 metadata file. To unpack these arrays to their original format, use the ``unsqueeze_list()`` method in ``dbcollection.utils.pad``.
- ``area``: object area
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``object_fields``: list of field names of the object id list
    - ``available in``: train, val, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
    - ``note``: key field (*field name* aggregator)
- ``object_ids``: list of field ids
    - ``available in``: train, val, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: key field (*field id* aggregator)
- ``list_boxes_per_image``: list of bounding boxes per image
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_image_filenames_per_category``: list of image filenames per category
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_image_filenames_per_supercategory``: list of image filenames per supercategory
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_object_ids_per_image``: list of object ids per image
    - ``available in``: train, val, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_objects_ids_per_category``: list of object ids per category
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_objects_ids_per_supercategory``: list of object ids per supercategory
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list


Task: detection_2016
--------------------

::

    /
    ├── train/
    │   ├── image_filenames       # dtype=np.uint8, shape=(82783,74)   (note: string in ASCII format)
    │   ├── category              # dtype=np.uint8, shape=(80,15)      (note: string in ASCII format)
    │   ├── supercategory         # dtype=np.uint8, shape=(12,11)      (note: string in ASCII format)
    │   ├── coco_annotations_ids  # dtype=np.int32, shape=(604907,)
    │   ├── coco_categories_ids   # dtype=np.int32, shape=(80,)
    │   ├── coco_images_ids       # dtype=np.int32, shape=(82783,)
    │   ├── coco_urls             # dtype=np.uint8, shape=(82783,32)   (note: string in ASCII format)
    │   ├── image_id              # dtype=np.int32, shape=(82783,)
    │   ├── category_id           # dtype=np.int32, shape=(80,)
    │   ├── annotation_id         # dtype=np.int32, shape=(604907,)
    │   ├── width                 # dtype=np.int32, shape=(82783,)
    │   ├── height                # dtype=np.int32, shape=(82783,)
    │   ├── boxes                 # dtype=np.float, shape=(604907,4)
    │   ├── iscrowd               # dtype=np.uint8, shape=(2,)
    │   ├── segmentation          # dtype=np.float, shape=(604907,10043)
    │   ├── area                  # dtype=np.int32, shape=(604907,)
    │   ├── object_fields         # dtype=np.uint8, shape=(13,16)      (note: string in ASCII format)
    │   ├── object_ids            # dtype=np.int32, shape=(604907,13)
    │   ├── list_boxes_per_image                    # dtype=np.int32, shape=(82783,93))
    │   ├── list_image_filenames_per_category       # dtype=np.int32, shape=(80,45174))
    │   ├── list_image_filenames_per_supercategory  # dtype=np.int32, shape=(12,45174))
    │   ├── list_object_ids_per_image               # dtype=np.int32, shape=(82783,93))
    │   ├── list_objects_ids_per_category           # dtype=np.int32, shape=(80,185316))
    │   └── list_objects_ids_per_supercategory      # dtype=np.int32, shape=(12,185316))
    │
    ├── val/
    │   ├── image_filenames       # dtype=np.uint8, shape=(40504,74)   (note: string in ASCII format)
    │   ├── category              # dtype=np.uint8, shape=(80,15)      (note: string in ASCII format)
    │   ├── supercategory         # dtype=np.uint8, shape=(12,11)      (note: string in ASCII format)
    │   ├── coco_annotations_ids  # dtype=np.int32, shape=(291875,)
    │   ├── coco_categories_ids   # dtype=np.int32, shape=(80,)
    │   ├── coco_images_ids       # dtype=np.int32, shape=(40504,)
    │   ├── coco_urls             # dtype=np.uint8, shape=(40504,32)   (note: string in ASCII format)
    │   ├── image_id              # dtype=np.int32, shape=(40504,)
    │   ├── category_id           # dtype=np.int32, shape=(80,)
    │   ├── annotation_id         # dtype=np.int32, shape=(291875,)
    │   ├── width                 # dtype=np.int32, shape=(40504,)
    │   ├── height                # dtype=np.int32, shape=(40504,)
    │   ├── boxes                 # dtype=np.float, shape=(291875,4)
    │   ├── iscrowd               # dtype=np.uint8, shape=(2,)
    │   ├── segmentation          # dtype=np.float, shape=(291875,7237)
    │   ├── area                  # dtype=np.int32, shape=(291875,)
    │   ├── object_fields         # dtype=np.uint8, shape=(13,16)      (note: string in ASCII format)
    │   ├── object_ids            # dtype=np.int32, shape=(291875,13)
    │   ├── list_boxes_per_image                    # dtype=np.int32, shape=(40504,93))
    │   ├── list_image_filenames_per_category       # dtype=np.int32, shape=(80,21634))
    │   ├── list_image_filenames_per_supercategory  # dtype=np.int32, shape=(12,21634))
    │   ├── list_object_ids_per_image               # dtype=np.int32, shape=(40504,93))
    │   ├── list_objects_ids_per_category           # dtype=np.int32, shape=(80,88153))
    │   └── list_objects_ids_per_supercategory      # dtype=np.int32, shape=(12,88153))
    │
    ├── test/
    │   ├── image_filenames       # dtype=np.uint8, shape=(81434,72)   (note: string in ASCII format)
    │   ├── category              # dtype=np.uint8, shape=(80,15)      (note: string in ASCII format)
    │   ├── supercategory         # dtype=np.uint8, shape=(12,11)      (note: string in ASCII format)
    │   ├── coco_categories_ids   # dtype=np.int32, shape=(80,)
    │   ├── coco_images_ids       # dtype=np.int32, shape=(81434,)
    │   ├── coco_urls             # dtype=np.uint8, shape=(81434,32)   (note: string in ASCII format)
    │   ├── image_id              # dtype=np.int32, shape=(81434,)
    │   ├── category_id           # dtype=np.int32, shape=(80,)
    │   ├── width                 # dtype=np.int32, shape=(81434,)
    │   ├── height                # dtype=np.int32, shape=(81434,)
    │   ├── object_fields         # dtype=np.uint8, shape=(4,16)      (note: string in ASCII format)
    │   ├── object_ids            # dtype=np.int32, shape=(81434,4)
    │   └── list_object_ids_per_image   # dtype=np.int32, shape=(81434,1))
    │
    └── test_dev/
        ├── image_filenames       # dtype=np.uint8, shape=(20288,72)   (note: string in ASCII format)
        ├── category              # dtype=np.uint8, shape=(80,15)      (note: string in ASCII format)
        ├── supercategory         # dtype=np.uint8, shape=(12,11)      (note: string in ASCII format)
        ├── coco_categories_ids   # dtype=np.int32, shape=(80,)
        ├── coco_images_ids       # dtype=np.int32, shape=(20288,)
        ├── coco_urls             # dtype=np.uint8, shape=(20288,32)   (note: string in ASCII format)
        ├── image_id              # dtype=np.int32, shape=(20288,)
        ├── category_id           # dtype=np.int32, shape=(80,)
        ├── width                 # dtype=np.int32, shape=(20288,)
        ├── height                # dtype=np.int32, shape=(20288,)
        ├── object_fields         # dtype=np.uint8, shape=(4,16)      (note: string in ASCII format)
        ├── object_ids            # dtype=np.int32, shape=(20288,4)
        └── list_object_ids_per_image   # dtype=np.int32, shape=(20288,1))


Fields
^^^^^^

- ``image_filenames``: image file path+names
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``category``: category names
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``supercategory``: super category names
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``coco_annotations_ids``: reference to coco annotation ids  (useful for evaluating on coco)
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``coco_categories_ids``: reference to coco category ids   (useful for evaluating on coco)
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``coco_images_ids``: reference to coco image filename ids   (useful for evaluating on coco)
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``coco_urls``: coco urls
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``image_id``: image filename ids
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``category_id``: category ids
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``annotation_id``: annotation ids
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``width``: image width
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``height``: image height
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``boxes``: bounding box
    - ``available in``: train, val
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format (x1,y1,x2,y2)
- ``iscrowd``: is crowd (0 - False, 1 - True)
    - ``available in``: train, val
    - ``dtype``: np.uint8
    - ``is padded``: False
    - ``fill value``: -1
- ``segmentation``: segmentation mask
    - ``available in``: train, val
    - ``dtype``: np.float
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: the masks come in 3 different formats, but they are mostly lists of lists. These have been packed (vectorized) into an array with a single dimension in order to be stored in the HDF5 metadata file. To unpack these arrays to their original format, use the ``unsqueeze_list()`` method in ``dbcollection.utils.pad``.
- ``area``: object area
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``object_fields``: list of field names of the object id list
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
    - ``note``: key field (*field name* aggregator)
- ``object_ids``: list of field ids
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: key field (*field id* aggregator)
- ``list_boxes_per_image``: list of bounding boxes per image
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_image_filenames_per_category``: list of image filenames per category
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_image_filenames_per_supercategory``: list of image filenames per supercategory
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_object_ids_per_image``: list of object ids per image
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_objects_ids_per_category``: list of object ids per category
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_objects_ids_per_supercategory``: list of object ids per supercategory
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list


Task: caption_2015
------------------

::

    /
    ├── train/
    │   ├── image_filenames       # dtype=np.uint8, shape=(82783,74)   (note: string in ASCII format)
    │   ├── captions              # dtype=np.uint8, shape=(414133,251)   (note: string in ASCII format)
    │   ├── coco_images_ids       # dtype=np.int32, shape=(82783,)
    │   ├── coco_urls             # dtype=np.uint8, shape=(82783,32)   (note: string in ASCII format)
    │   ├── image_id              # dtype=np.int32, shape=(82783,)
    │   ├── width                 # dtype=np.int32, shape=(82783,)
    │   ├── height                # dtype=np.int32, shape=(82783,)
    │   ├── object_fields         # dtype=np.uint8, shape=(5,16)      (note: string in ASCII format)
    │   ├── object_ids            # dtype=np.int32, shape=(414133,5)
    │   ├── list_object_ids_per_image   # dtype=np.int32, shape=(82783,7))
    │   └── list_captions_per_image     # dtype=np.int32, shape=(82783,7))
    │
    ├── val/
    │   ├── image_filenames       # dtype=np.uint8, shape=(40504,70)   (note: string in ASCII format)
    │   ├── captions              # dtype=np.uint8, shape=(202654,74)   (note: string in ASCII format)
    │   ├── coco_images_ids       # dtype=np.int32, shape=(40504,)
    │   ├── coco_urls             # dtype=np.uint8, shape=(40504,32)   (note: string in ASCII format)
    │   ├── image_id              # dtype=np.int32, shape=(40504,)
    │   ├── width                 # dtype=np.int32, shape=(40504,)
    │   ├── height                # dtype=np.int32, shape=(40504,)
    │   ├── object_fields         # dtype=np.uint8, shape=(5,16)      (note: string in ASCII format)
    │   ├── object_ids            # dtype=np.int32, shape=(202654,5)
    │   ├── list_object_ids_per_image   # dtype=np.int32, shape=(40504,7))
    │   └── list_captions_per_image     # dtype=np.int32, shape=(40504,7))
    │
    └── test/
        ├── image_filenames       # dtype=np.uint8, shape=(40775,72)   (note: string in ASCII format)
        ├── category              # dtype=np.uint8, shape=(80,15)      (note: string in ASCII format)
        ├── supercategory         # dtype=np.uint8, shape=(12,11)      (note: string in ASCII format)
        ├── coco_categories_ids   # dtype=np.int32, shape=(80,)
        ├── coco_images_ids       # dtype=np.int32, shape=(40775,)
        ├── coco_urls             # dtype=np.uint8, shape=(40775,32)   (note: string in ASCII format)
        ├── image_id              # dtype=np.int32, shape=(40775,)
        ├── category_id           # dtype=np.int32, shape=(80,)
        ├── width                 # dtype=np.int32, shape=(40775,)
        ├── height                # dtype=np.int32, shape=(40775,)
        ├── object_fields         # dtype=np.uint8, shape=(4,16)      (note: string in ASCII format)
        ├── object_ids            # dtype=np.int32, shape=(40775,4)
        └── list_object_ids_per_image   # dtype=np.int32, shape=(40775,1))


Fields
^^^^^^

- ``image_filenames``: image file path+names
    - ``available in``: train, val, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``captions``: image captions
    - ``available in``: train, val
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``category``: category names
    - ``available in``: test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``supercategory``: super category names
    - ``available in``: test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``coco_categories_ids``: reference to coco category ids   (useful for evaluating on coco)
    - ``available in``: test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``coco_images_ids``: reference to coco image filename ids   (useful for evaluating on coco)
    - ``available in``: train, val, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``coco_urls``: coco urls
    - ``available in``: train, val, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``image_id``: image filename ids
    - ``available in``: train, val, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``category_id``: category ids
    - ``available in``: test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``width``: image width
    - ``available in``: train, val, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``height``: image height
    - ``available in``: train, val, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``object_fields``: list of field names of the object id list
    - ``available in``: train, val, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
    - ``note``: key field (*field name* aggregator)
- ``object_ids``: list of field ids
    - ``available in``: train, val, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: key field (*field id* aggregator)
- ``list_object_ids_per_image``: list of object ids per image
    - ``available in``: train, val, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_captions_per_image``: list of captions per image
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list


Task: caption_2016
------------------

::

    /
    ├── train/
    │   ├── image_filenames       # dtype=np.uint8, shape=(82783,74)   (note: string in ASCII format)
    │   ├── captions              # dtype=np.uint8, shape=(414133,251)   (note: string in ASCII format)
    │   ├── coco_images_ids       # dtype=np.int32, shape=(82783,)
    │   ├── coco_urls             # dtype=np.uint8, shape=(82783,32)   (note: string in ASCII format)
    │   ├── image_id              # dtype=np.int32, shape=(82783,)
    │   ├── width                 # dtype=np.int32, shape=(82783,)
    │   ├── height                # dtype=np.int32, shape=(82783,)
    │   ├── object_fields         # dtype=np.uint8, shape=(5,16)      (note: string in ASCII format)
    │   ├── object_ids            # dtype=np.int32, shape=(414133,5)
    │   ├── list_object_ids_per_image   # dtype=np.int32, shape=(82783,7))
    │   └── list_captions_per_image     # dtype=np.int32, shape=(82783,7))
    │
    ├── val/
    │   ├── image_filenames       # dtype=np.uint8, shape=(40504,70)   (note: string in ASCII format)
    │   ├── captions              # dtype=np.uint8, shape=(202654,74)   (note: string in ASCII format)
    │   ├── coco_images_ids       # dtype=np.int32, shape=(40504,)
    │   ├── coco_urls             # dtype=np.uint8, shape=(40504,32)   (note: string in ASCII format)
    │   ├── image_id              # dtype=np.int32, shape=(40504,)
    │   ├── width                 # dtype=np.int32, shape=(40504,)
    │   ├── height                # dtype=np.int32, shape=(40504,)
    │   ├── object_fields         # dtype=np.uint8, shape=(5,16)      (note: string in ASCII format)
    │   ├── object_ids            # dtype=np.int32, shape=(202654,5)
    │   ├── list_object_ids_per_image   # dtype=np.int32, shape=(40504,7))
    │   └── list_captions_per_image     # dtype=np.int32, shape=(40504,7))
    │
    ├── test/
    │   ├── image_filenames       # dtype=np.uint8, shape=(81434,72)   (note: string in ASCII format)
    │   ├── category              # dtype=np.uint8, shape=(80,15)      (note: string in ASCII format)
    │   ├── supercategory         # dtype=np.uint8, shape=(12,11)      (note: string in ASCII format)
    │   ├── coco_categories_ids   # dtype=np.int32, shape=(80,)
    │   ├── coco_images_ids       # dtype=np.int32, shape=(81434,)
    │   ├── coco_urls             # dtype=np.uint8, shape=(81434,32)   (note: string in ASCII format)
    │   ├── image_id              # dtype=np.int32, shape=(81434,)
    │   ├── category_id           # dtype=np.int32, shape=(80,)
    │   ├── width                 # dtype=np.int32, shape=(81434,)
    │   ├── height                # dtype=np.int32, shape=(81434,)
    │   ├── object_fields         # dtype=np.uint8, shape=(4,16)      (note: string in ASCII format)
    │   ├── object_ids            # dtype=np.int32, shape=(81434,4)
    │   └── list_object_ids_per_image   # dtype=np.int32, shape=(81434,1))
    │
    └── test_dev/
        ├── image_filenames       # dtype=np.uint8, shape=(20288,72)   (note: string in ASCII format)
        ├── category              # dtype=np.uint8, shape=(80,15)      (note: string in ASCII format)
        ├── supercategory         # dtype=np.uint8, shape=(12,11)      (note: string in ASCII format)
        ├── coco_categories_ids   # dtype=np.int32, shape=(80,)
        ├── coco_images_ids       # dtype=np.int32, shape=(20288,)
        ├── coco_urls             # dtype=np.uint8, shape=(20288,32)   (note: string in ASCII format)
        ├── image_id              # dtype=np.int32, shape=(20288,)
        ├── category_id           # dtype=np.int32, shape=(80,)
        ├── width                 # dtype=np.int32, shape=(20288,)
        ├── height                # dtype=np.int32, shape=(20288,)
        ├── object_fields         # dtype=np.uint8, shape=(4,16)      (note: string in ASCII format)
        ├── object_ids            # dtype=np.int32, shape=(20288,4)
        └── list_object_ids_per_image   # dtype=np.int32, shape=(20288,1))


Fields
^^^^^^

- ``image_filenames``: image file path+names
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``captions``: image captions
    - ``available in``: train, val
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``category``: category names
    - ``available in``: test, test_dev
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``supercategory``: super category names
    - ``available in``: test, test_dev
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``coco_categories_ids``: reference to coco category ids   (useful for evaluating on coco)
    - ``available in``: test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``coco_images_ids``: reference to coco image filename ids   (useful for evaluating on coco)
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``coco_urls``: coco urls
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``image_id``: image filename ids
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``category_id``: category ids
    - ``available in``: test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``width``: image width
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``height``: image height
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``object_fields``: list of field names of the object id list
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
    - ``note``: key field (*field name* aggregator)
- ``object_ids``: list of field ids
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: key field (*field id* aggregator)
- ``list_object_ids_per_image``: list of object ids per image
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_captions_per_image``: list of captions per image
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list


Task: keypoints_2016
--------------------

::

    /
    ├── train/
    │   ├── image_filenames       # dtype=np.uint8, shape=(82783,74)   (note: string in ASCII format)
    │   ├── category              # dtype=np.uint8, shape=(80,15)      (note: string in ASCII format)
    │   ├── supercategory         # dtype=np.uint8, shape=(12,11)      (note: string in ASCII format)
    │   ├── coco_annotations_ids  # dtype=np.int32, shape=(185316,)
    │   ├── coco_categories_ids   # dtype=np.int32, shape=(80,)
    │   ├── coco_images_ids       # dtype=np.int32, shape=(82783,)
    │   ├── coco_urls             # dtype=np.uint8, shape=(82783,32)   (note: string in ASCII format)
    │   ├── image_id              # dtype=np.int32, shape=(82783,)
    │   ├── category_id           # dtype=np.int32, shape=(80,)
    │   ├── annotation_id         # dtype=np.int32, shape=(185316,)
    │   ├── width                 # dtype=np.int32, shape=(82783,)
    │   ├── height                # dtype=np.int32, shape=(82783,)
    │   ├── boxes                 # dtype=np.float, shape=(185316,4)
    │   ├── iscrowd               # dtype=np.uint8, shape=(2,)
    │   ├── segmentation          # dtype=np.float, shape=(185316,10043)
    │   ├── area                  # dtype=np.int32, shape=(185316,)
    │   ├── keypoint_names        # dtype=np.uint8, shape=(17,15)      (note: string in ASCII format)
    │   ├── keypoints             # dtype=np.int32, shape=(185316,51)
    │   ├── num_keypoints         # dtype=np.uint8, shape=(18,)
    │   ├── skeleton              # dtype=np.uint8, shape=(19,2)
    │   ├── object_fields         # dtype=np.uint8, shape=(13,16)      (note: string in ASCII format)
    │   ├── object_ids            # dtype=np.int32, shape=(185316,13)
    │   ├── list_boxes_per_image                    # dtype=np.int32, shape=(82783,20))
    │   ├── list_image_filenames_per_num_keypoints  # dtype=np.int32, shape=(17,45174))
    │   ├── list_keypoints_per_image                # dtype=np.int32, shape=(82783,20))
    │   ├── list_object_ids_per_image               # dtype=np.int32, shape=(82783,20))
    │   └── list_object_ids_per_keypoint            # dtype=np.int32, shape=(17,92701))
    │
    ├── val/
    │   ├── image_filenames       # dtype=np.uint8, shape=(40504,70)   (note: string in ASCII format)
    │   ├── category              # dtype=np.uint8, shape=(80,15)      (note: string in ASCII format)
    │   ├── supercategory         # dtype=np.uint8, shape=(12,11)      (note: string in ASCII format)
    │   ├── coco_annotations_ids  # dtype=np.int32, shape=(88153,)
    │   ├── coco_categories_ids   # dtype=np.int32, shape=(80,)
    │   ├── coco_images_ids       # dtype=np.int32, shape=(40504,)
    │   ├── coco_urls             # dtype=np.uint8, shape=(40504,32)   (note: string in ASCII format)
    │   ├── image_id              # dtype=np.int32, shape=(40504,)
    │   ├── category_id           # dtype=np.int32, shape=(80,)
    │   ├── annotation_id         # dtype=np.int32, shape=(88153,)
    │   ├── width                 # dtype=np.int32, shape=(40504,)
    │   ├── height                # dtype=np.int32, shape=(40504,)
    │   ├── boxes                 # dtype=np.float, shape=(88153,4)
    │   ├── iscrowd               # dtype=np.uint8, shape=(2,)
    │   ├── segmentation          # dtype=np.float, shape=(88153,6121)
    │   ├── area                  # dtype=np.int32, shape=(88153,)
    │   ├── keypoint_names        # dtype=np.uint8, shape=(17,15)      (note: string in ASCII format)
    │   ├── keypoints             # dtype=np.int32, shape=(88153,51)
    │   ├── num_keypoints         # dtype=np.uint8, shape=(18,)
    │   ├── skeleton              # dtype=np.uint8, shape=(19,2)
    │   ├── object_fields         # dtype=np.uint8, shape=(13,16)      (note: string in ASCII format)
    │   ├── object_ids            # dtype=np.int32, shape=(88153,13)
    │   ├── list_boxes_per_image                    # dtype=np.int32, shape=(40504,16))
    │   ├── list_image_filenames_per_num_keypoints  # dtype=np.int32, shape=(17,21634))
    │   ├── list_keypoints_per_image                # dtype=np.int32, shape=(40504,16))
    │   ├── list_object_ids_per_image               # dtype=np.int32, shape=(40504,16))
    │   └── list_object_ids_per_keypoint            # dtype=np.int32, shape=(17,43971))
    │
    ├── test/
    │   ├── image_filenames       # dtype=np.uint8, shape=(81434,72)   (note: string in ASCII format)
    │   ├── category              # dtype=np.uint8, shape=(80,15)      (note: string in ASCII format)
    │   ├── supercategory         # dtype=np.uint8, shape=(12,11)      (note: string in ASCII format)
    │   ├── coco_categories_ids   # dtype=np.int32, shape=(80,)
    │   ├── coco_images_ids       # dtype=np.int32, shape=(81434,)
    │   ├── coco_urls             # dtype=np.uint8, shape=(81434,32)   (note: string in ASCII format)
    │   ├── image_id              # dtype=np.int32, shape=(81434,)
    │   ├── category_id           # dtype=np.int32, shape=(80,)
    │   ├── width                 # dtype=np.int32, shape=(81434,)
    │   ├── height                # dtype=np.int32, shape=(81434,)
    │   ├── object_fields         # dtype=np.uint8, shape=(4,16)      (note: string in ASCII format)
    │   ├── object_ids            # dtype=np.int32, shape=(81434,4)
    │   └── list_object_ids_per_image   # dtype=np.int32, shape=(81434,1))
    │
    └── test_dev/
        ├── image_filenames       # dtype=np.uint8, shape=(20288,72)   (note: string in ASCII format)
        ├── category              # dtype=np.uint8, shape=(80,15)      (note: string in ASCII format)
        ├── supercategory         # dtype=np.uint8, shape=(12,11)      (note: string in ASCII format)
        ├── coco_categories_ids   # dtype=np.int32, shape=(80,)
        ├── coco_images_ids       # dtype=np.int32, shape=(20288,)
        ├── coco_urls             # dtype=np.uint8, shape=(20288,32)   (note: string in ASCII format)
        ├── image_id              # dtype=np.int32, shape=(20288,)
        ├── category_id           # dtype=np.int32, shape=(80,)
        ├── width                 # dtype=np.int32, shape=(20288,)
        ├── height                # dtype=np.int32, shape=(20288,)
        ├── object_fields         # dtype=np.uint8, shape=(4,16)      (note: string in ASCII format)
        ├── object_ids            # dtype=np.int32, shape=(20288,4)
        └── list_object_ids_per_image   # dtype=np.int32, shape=(20288,1))


Fields
^^^^^^

- ``image_filenames``: image file path+names
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``category``: category names
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``supercategory``: super category names
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``coco_annotations_ids``: reference to coco annotation ids  (useful for evaluating on coco)
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``coco_categories_ids``: reference to coco category ids   (useful for evaluating on coco)
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``coco_images_ids``: reference to coco image filename ids   (useful for evaluating on coco)
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``coco_urls``: coco urls
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``image_id``: image filename ids
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``category_id``: category ids
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``annotation_id``: annotation ids
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``width``: image width
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``height``: image height
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``boxes``: bounding box
    - ``available in``: train, val
    - ``dtype``: np.float
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: bbox format (x1,y1,x2,y2)
- ``iscrowd``: is crowd (0 - False, 1 - True)
    - ``available in``: train, val
    - ``dtype``: np.uint8
    - ``is padded``: False
    - ``fill value``: -1
- ``segmentation``: segmentation mask
    - ``available in``: train, val
    - ``dtype``: np.float
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: the masks come in 3 different formats, but they are mostly lists of lists. These have been packed (vectorized) into an array with a single dimension in order to be stored in the HDF5 metadata file. To unpack these arrays to their original format, use the ``unsqueeze_list()`` method in ``dbcollection.utils.pad``.
- ``area``: object area
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
- ``keypoint_names``: body joint names
    - ``available in``: train, val
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``keypoints``: body joint coordinates
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: coordinates format [x1,y1,is_visible,x2,y2,is_visible, ...]
- ``num_keypoints``: number of body joints
    - ``available in``: train, val
    - ``dtype``: np.uint8
    - ``is padded``: False
    - ``fill value``: -1
- ``skeleton``: pairwise body joints
    - ``available in``: train, val
    - ``dtype``: np.uint8
    - ``is padded``: False
    - ``fill value``: -1
- ``object_fields``: list of field names of the object id list
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
    - ``note``: key field (*field name* aggregator)
- ``object_ids``: list of field ids
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: key field (*field id* aggregator)
- ``list_boxes_per_image``: list of bounding boxes per image
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_image_filenames_per_category``: list of image filenames per category
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_image_filenames_per_supercategory``: list of image filenames per supercategory
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_object_ids_per_image``: list of object ids per image
    - ``available in``: train, val, test, test_dev
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_objects_ids_per_category``: list of object ids per category
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list
- ``list_objects_ids_per_supercategory``: list of object ids per supercategory
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list


Disclaimer
==========

All rights reserved to the original creators of **MS COCO**.

For information about the dataset and its terms of use, please see this `link <http://mscoco.org/>`_.