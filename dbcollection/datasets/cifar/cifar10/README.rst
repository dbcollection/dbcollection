.. _cifar_10_readme:

CIFAR-10
========

The **CIFAR-10** dataset consists of 60000 32x32 colour images in 10 classes,
with 6000 images per class. There are 50000 training images and 10000 test images.


Use cases
---------

Image classification.


Properties
----------

- ``name``: cifar10
- ``tasks``: classification
- ``keywords``: image_processing, classification
- ``sets``: train, test
- ``description``: Contains image tensors and label annotations for image classification.
- ``is downloadable``: **yes**
- ``dataset size``: 170,5 MB
- ``metadata file size``:
    - **classification**: 178,3 MB
- ``has annotations``: **yes**
    - ``which``:
        - labels for each image class/category.


Metadata structure (HDF5)
-------------------------

::

    /
    ├── train/
    │   ├── classes        # dtype=numpy.uint8, shape=(10,11)  (note: string in ASCII format)
    │   ├── images         # dtype=numpy.uint8, shape=(50000,32,32,3)
    │   ├── labels         # dtype=numpy.uint8, shape=(50000,)
    │   ├── object_fields  # dtype=numpy.uint8, shape=(2,8)    (note: string in ASCII format)
    │   ├── object_ids     # dtype=numpy.int32, shape=(50000,2)
    │   └── list_images_per_class    # dtype=numpy.int32, shape=(10,5000))
    │
    └── test/
        ├── classes        # dtype=numpy.uint8, shape=(10,11)  (note: string in ASCII format)
        ├── images         # dtype=numpy.uint8, shape=(10000,32,32,3)
        ├── labels         # dtype=numpy.uint8, shape=(10000,)
        ├── object_fields  # dtype=numpy.uint8, shape=(2,8)    (note: string in ASCII format)
        ├── object_ids     # dtype=numpy.int32, shape=(10000,2)
        └── list_images_per_class    # dtype=numpy.int32, shape=(10,1000))


Fields
^^^^^^

- ``classes``: class descriptions.
- ``images``: images array.
- ``labels``: class ids.
- ``object_fields``: list of fields composing the object id list.
- ``object_ids``: list of field ids.
- ``list_images_per_class``: list of image ids per class.


Disclaimer
----------

All rights reserved to the original creators of **CIFAR-10**.

For information about the dataset and its terms of use, please see this `link <https://www.cs.toronto.edu/~kriz/cifar.html>`_.