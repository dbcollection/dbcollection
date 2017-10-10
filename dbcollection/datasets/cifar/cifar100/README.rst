.. _cifar_100_readme:

CIFAR-100
=========

This dataset is just like the **CIFAR-10**, except it has 100 classes containing 600
images each. There are 500 training images and 100 testing images per class.
The 100 classes in the **CIFAR-100** are grouped into 20 superclasses.
Each image comes with a "fine" label (the class to which it belongs) and a "coarse"
label (the superclass to which it belongs).


Use cases
---------

Image classification.


Properties
----------

- ``name``: cifar100
- ``tasks``: classification
- ``keywords``: image_processing, classification
- ``sets``: train, test
- ``description``: Contains image tensors and label annotations for image classification.
- ``is downloadable``: **yes**
- ``dataset size``: 355,3 MB
- ``metadata file size``:
    - **classification**: 177,8 MB
- ``has annotations``: **yes**
    - ``which``:
        - labels for each image class/category.


Metadata structure (HDF5)
-------------------------

::

    /
    ├── train/
    │   ├── classes        # dtype=numpy.uint8, shape=(100,18)  (note: string in ASCII format)
    │   ├── superclasses   # dtype=numpy.uint8, shape=(20,31)   (note: string in ASCII format)
    │   ├── images         # dtype=numpy.uint8, shape=(50000,32,32,3)
    │   ├── labels         # dtype=numpy.uint8, shape=(50000,)
    │   ├── coarse_labels  # dtype=numpy.uint8, shape=(50000,)
    │   ├── object_fields  # dtype=numpy.uint8, shape=(3,13)    (note: string in ASCII format)
    │   ├── object_ids     # dtype=numpy.int32, shape=(50000,3)
    │   ├── list_images_per_class    # dtype=numpy.int32, shape=(100,500))
    │   └── list_images_per_superclass    # dtype=numpy.int32, shape=(20,2500))
    │
    └── test/
        ├── classes        # dtype=numpy.uint8, shape=(100,18)  (note: string in ASCII format)
        ├── superclasses   # dtype=numpy.uint8, shape=(20,31)   (note: string in ASCII format)
        ├── images         # dtype=numpy.uint8, shape=(10000,32,32,3)
        ├── labels         # dtype=numpy.uint8, shape=(10000,)
        ├── coarse_labels  # dtype=numpy.uint8, shape=(10000,)
        ├── object_fields  # dtype=numpy.uint8, shape=(3,13)    (note: string in ASCII format)
        ├── object_ids     # dtype=numpy.int32, shape=(10000,3)
        ├── list_images_per_class         # dtype=numpy.int32, shape=(100,100))
        └── list_images_per_superclass    # dtype=numpy.int32, shape=(20,500))


Fields
^^^^^^

- ``classes``: class descriptions.
- ``superclasses``: super class descriptions. It is composed of groups of classes per super class.
- ``images``: images array.
- ``labels``: class ids.
- ``coarse_labels``: superclass ids.
- ``object_fields``: list of fields composing the object id list.
- ``object_ids``: list of field ids.
- ``list_images_per_class``: list of image ids per class.
- ``list_images_per_superclass``: list of image ids per superclass.


Disclaimer
----------

All rights reserved to the original creators of **CIFAR-100**.

For information about the dataset and its terms of use, please see this `link <https://www.cs.toronto.edu/~kriz/cifar.html>`_.