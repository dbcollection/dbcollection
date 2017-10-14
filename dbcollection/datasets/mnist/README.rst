.. _mnist_readme:

================================
MNIST Handwritten Digit Database
================================

The **MNIST** database of handwritten digits has a
training set of 60,000 examples, and a test set of 10,000 examples. It is a
subset of a larger set available from **NIST**.
The digits have been size-normalized and centered in a fixed-size image.


Use cases
=========

Image classification.


Properties
==========

- ``name``: mnist
- ``keywords``: image_processing, classification
- ``dataset size``: 11,6 MB
- ``is downloadable``: **yes**
- ``tasks``:
    - classification: **(default)**
        - ``primary use``: image classification
        - ``description``: Contains image tensors and label annotations for image classification.
        - ``sets``: train, test
        - ``metadata file size in disk``: 6,8 MB
        - ``has annotations``: **yes**
            - ``which``:
                - labels for each image class/category.


Metadata structure (HDF5)
=========================

Task: classification
--------------------

::

    /
    ├── train/
    │   ├── classes        # dtype=np.uint8, shape=(10,2)   (note: string in ASCII format)
    │   ├── images         # dtype=np.uint8, shape=(60000,28,28)
    │   ├── labels         # dtype=np.uint8, shape=(60000,)
    │   ├── object_fields  # dtype=np.uint8, shape=(2,7)    (note: string in ASCII format)
    │   ├── object_ids     # dtype=np.int32, shape=(60000,2)
    │   └── list_images_per_class   # dtype=np.int32, shape=(10,6742))
    │
    └── test/
        ├── classes        # dtype=np.uint8, shape=(10,2)  (note: string in ASCII format)
        ├── images         # dtype=np.uint8, shape=(10000,28,28)
        ├── labels         # dtype=np.uint8, shape=(10000,)
        ├── object_fields  # dtype=np.uint8, shape=(2,7)    (note: string in ASCII format)
        ├── object_ids     # dtype=np.int32, shape=(10000,2)
        └── list_images_per_class   # dtype=np.int32, shape=(10,1135))


Fields
^^^^^^

- ``classes``: class names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
- ``images``: images tensor
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: False
    - ``fill value``: -1
- ``labels``: class ids
    - ``available in``: train, test
    - ``dtype``: np.uint8
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
- ``list_images_per_class``: list of image ids per class
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list


Disclaimer
==========

All rights reserved to the original creators of **MNIST**.

For information about the dataset and its terms of use, please see this `link <http://yann.lecun.com/exdb/mnist/>`_.