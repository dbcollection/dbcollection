.. _imagenet_ilsvrc2012_readme:

===================
ImageNet ILSVRC2012
===================

**ImageNet** is an image database organized according to the **WordNet** hierarchy
(currently only the nouns), in which each node of the hierarchy is depicted by 
hundreds and thousands of images.

The **Large Scale Visual Recognition Challenge 2012 (ILSVRC2012)** is a subset of
the large hand-labeled ImageNet dataset (10,000,000 labeled images depicting 10,000+ object categories). 
The training data is a subset of **ImageNet** containing the 1000 categories and 1.2 million images


Use cases
=========

Image classification.


Properties
==========

- ``name``: ilsvrc2012
- ``keywords``: image_processing, classification
- ``dataset size``: 154,6 GB
- ``is downloadable``: **no**
    - ``data setup``: create a folder or symlink with the name ``ilsvrc2012/`` where you have stored and unpacked the data files and, when loading the dataset, use the ``data_dir`` input argument to specify the data's folder path.
- ``tasks``:
    - classification: **(default)**
        - ``primary use``: image classification
        - ``description``: Contains image filenames and label annotations for image classification.
        - ``sets``: train, val
        - ``metadata file size in disk``: 6,8 MB
        - ``has annotations``: **yes**
            - ``which``:
                - labels for each image class/category.
                - descriptions for each class/category.
    - raw256:
        - ``primary use``: image classification
        - ``description``: Contains image filenames and label annotations for image classification.
        - ``sets``: train, val
        - ``metadata file size in disk``: 6,8 MB
        - ``has annotations``: **yes**
            - ``which``:
                - labels for each image class/category.
                - descriptions for each class/category.


Metadata structure (HDF5)
=========================

Task: classification
--------------------

::

    /
    ├── train/
    │   ├── image_filenames   # dtype=np.uint8, shape=(1281166,76)  (note: string in ASCII format)
    │   ├── classes           # dtype=np.uint8, shape=(1000,10)       (note: string in ASCII format)
    │   ├── labels            # dtype=np.uint8, shape=(1000,122)
    │   ├── descriptions      # dtype=np.uint8, shape=(1000,256)       (note: string in ASCII format)
    │   ├── object_fields     # dtype=np.uint8, shape=(2,16)         (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(1281166,2)
    │   └── list_image_filenames_per_class   # dtype=np.int32, shape=(1000,1300))
    │
    └── val/
        ├── image_filenames   # dtype=np.uint8, shape=(50000,67)  (note: string in ASCII format)
        ├── classes           # dtype=np.uint8, shape=(1000,10)       (note: string in ASCII format)
        ├── labels            # dtype=np.uint8, shape=(1000,122)
        ├── descriptions      # dtype=np.uint8, shape=(1000,256)       (note: string in ASCII format)
        ├── object_fields     # dtype=np.uint8, shape=(2,16)         (note: string in ASCII format)
        ├── object_ids        # dtype=np.int32, shape=(50000,2)
        └── list_image_filenames_per_class   # dtype=np.int32, shape=(1000,50))


Fields
^^^^^^

- ``images``: image file path + name
    - ``available in``: train, val
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``classes``: class names
    - ``available in``: train, val
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``labels``: label names
    - ``available in``: train, val
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``descriptions``: class descriptions
    - ``available in``: train, val
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``object_fields``: list of field names of the object id list
    - ``available in``: train, val
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
    - ``note``: key field (*field name* aggregator)
- ``object_ids``: list of field ids
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: key field (*field id* aggregator)
- ``list_image_filenames_per_class``: list of image filenames per class
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list


Task: raw256
------------

::

    /
    ├── train/
    │   ├── image_filenames   # dtype=np.uint8, shape=(1281166,76)  (note: string in ASCII format)
    │   ├── classes           # dtype=np.uint8, shape=(1000,10)       (note: string in ASCII format)
    │   ├── labels            # dtype=np.uint8, shape=(1000,122)
    │   ├── descriptions      # dtype=np.uint8, shape=(1000,256)       (note: string in ASCII format)
    │   ├── object_fields     # dtype=np.uint8, shape=(2,16)         (note: string in ASCII format)
    │   ├── object_ids        # dtype=np.int32, shape=(1281166,2)
    │   └── list_image_filenames_per_class   # dtype=np.int32, shape=(1000,1300))
    │
    └── val/
        ├── image_filenames   # dtype=np.uint8, shape=(50000,67)  (note: string in ASCII format)
        ├── classes           # dtype=np.uint8, shape=(1000,10)       (note: string in ASCII format)
        ├── labels            # dtype=np.uint8, shape=(1000,122)
        ├── descriptions      # dtype=np.uint8, shape=(1000,256)       (note: string in ASCII format)
        ├── object_fields     # dtype=np.uint8, shape=(2,16)         (note: string in ASCII format)
        ├── object_ids        # dtype=np.int32, shape=(50000,2)
        └── list_image_filenames_per_class   # dtype=np.int32, shape=(1000,50))


Fields
^^^^^^

- ``images``: image file path + name
    - ``available in``: train, val
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``classes``: class names
    - ``available in``: train, val
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``labels``: label names
    - ``available in``: train, val
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``descriptions``: class descriptions
    - ``available in``: train, val
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``object_fields``: list of field names of the object id list
    - ``available in``: train, val
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
    - ``note``: key field (*field name* aggregator)
- ``object_ids``: list of field ids
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: key field (*field id* aggregator)
- ``list_image_filenames_per_class``: list of image filenames per class
    - ``available in``: train, val
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list


Disclaimer
==========

All rights reserved to the original creators of **ILSVRC2012**.

For information about the dataset and its terms of use, please see this `link <http://www.image-net.org>`_.