.. _cifar_10_readme:

========
CIFAR-10
========

The **CIFAR-10** dataset consists of 60000 32x32 colour images in 10 classes,
with 6000 images per class. There are 50000 training images and 10000 test images.


Use cases
=========

Image classification.


Properties
==========

- ``name``: cifar10
- ``keywords``: image_processing, classification
- ``dataset size``: 170,5 MB
- ``is downloadable``: **yes**
- ``tasks``: :ref:`classification (default) <cifar10_readme_classification>`


Tasks
=====

.. _cifar10_readme_classification:

classification (default)
------------------------

- :ref:`How to use <classification_how_to_use>`
- :ref:`Properties <classification_properties>`
- :ref:`HDF5 file structure <classification_hdf5_file_structure>`
- :ref:`Fields <classification_fields>`

.. _classification_how_to_use:

How to use
^^^^^^^^^^

.. code-block:: python

    >>> # import the package
    >>> import dbcollection as dbc
    >>>
    >>> # load the dataset
    >>> cifar10 = dbc.load('cifar10')
    >>> cifar10
    DataLoader: "cifar10" (classification task)


.. _classification_properties:

Properties
^^^^^^^^^^

- ``primary use``: image classification
- ``description``: Contains image tensors and label annotations for image classification.
- ``sets``: train, test
- ``metadata file size in disk``: 178,3 MB
- ``has annotations``: **yes**
    - ``which``:
        - labels for each image class/category.
- ``available fields``:
    - :ref:`classes <classification_fields_classes>`
    - :ref:`images <classification_fields_images>`
    - :ref:`labels <classification_fields_labels>`
    - :ref:`object_fields <classification_fields_object_fields>`
    - :ref:`object_ids <classification_fields_object_ids>`
    - :ref:`list_images_per_class <classification_fields_list_images_per_class>`


.. _classification_hdf5_file_structure:

HDF5 file structure
^^^^^^^^^^^^^^^^^^^

::

    /
    ├── train/
    │   ├── classes        # dtype=np.uint8, shape=(10,11)  (note: string in ASCII format)
    │   ├── images         # dtype=np.uint8, shape=(50000,32,32,3)
    │   ├── labels         # dtype=np.uint8, shape=(50000,)
    │   ├── object_fields  # dtype=np.uint8, shape=(2,8)    (note: string in ASCII format)
    │   ├── object_ids     # dtype=np.int32, shape=(50000,2)
    │   └── list_images_per_class   # dtype=np.int32, shape=(10,5000))
    │
    └── test/
        ├── classes        # dtype=np.uint8, shape=(10,11)  (note: string in ASCII format)
        ├── images         # dtype=np.uint8, shape=(10000,32,32,3)
        ├── labels         # dtype=np.uint8, shape=(10000,)
        ├── object_fields  # dtype=np.uint8, shape=(2,8)    (note: string in ASCII format)
        ├── object_ids     # dtype=np.int32, shape=(10000,2)
        └── list_images_per_class   # dtype=np.int32, shape=(10,1000))


.. _classification_fields:

Fields
^^^^^^

.. _classification_fields_classes:

- ``classes``: class names
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format

.. _classification_fields_images:

- ``images``: images tensor
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: False
    - ``fill value``: -1

.. _classification_fields_labels:

- ``labels``: class ids
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: False
    - ``fill value``: -1

.. _classification_fields_object_fields:

- ``object_fields``: list of field names of the object id list
    - ``available in``: train, test
    - ``dtype``: np.uint8
    - ``is padded``: True
    - ``fill value``: 0
    - ``note``: strings stored in ASCII format
    - ``note``: key field (*field name* aggregator)

.. _classification_fields_object_ids:

- ``object_ids``: list of field ids
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: False
    - ``fill value``: -1
    - ``note``: key field (*field id* aggregator)

.. _classification_fields_list_images_per_class:

- ``list_images_per_class``: list of image ids per class
    - ``available in``: train, test
    - ``dtype``: np.int32
    - ``is padded``: True
    - ``fill value``: -1
    - ``note``: pre-ordered list


Disclaimer
==========

All rights reserved to the original creators of **CIFAR-10**.

For information about the dataset and its terms of use, please see this `link <https://www.cs.toronto.edu/~kriz/cifar.html>`_.
