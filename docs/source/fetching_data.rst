.. _user_fetching_data:

=============
Fetching data
=============

Apart from managing datasets, another goal of **dbcollection** is to provide a way to easily pull data samples of a dataset in a straight-forward manner. Just like managing datasets, fetching data is also very easy!

To accomplish this feat, we make use of the ``HDF5`` file format. This enables us to overcome some issues related with other commonly used data formats like ``.json``, ``.csv`` or plain ``.txt`` for storing data:

- The ``HDF5`` file structure is easy to understand;
- Easy to use API;
- Data accesses from disk are fast;
- It uses a file handler so it does not need to load the entire file to memory;
- Efficient in fetching chunks of data;
- It offers lots of useful features like data compression.

Another useful feature of this file format is how the data is structured. Internally, it acts like a file system in the sense that data is stored hierarchically, so you'll have your data structure well defined.

Also, since you don't need to load the entire file into memory, you save:

- **Resources**: big datasets will have the same impact on the system's memory as small datasets;
- **Time**: because only a file handler is required to access data, loading a dataset is a quick process.

This Chapter deals with retrieving data from a dataset. In the following sections, we'll address how data is structured and how to fetch (and parse) data samples from a dataset. Also, best practices about retrieving data using this package are detailed at the end of this page. 


Data structure of a dataset in an HDF5 file
===========================================

Before proceeding on explaining how to retrieve data from a dataset, it is important to explain how data is stored inside an ``HDF5`` file.


The data file resembles a file system, so lets assume that the root of this file system is defined by the ``/`` symbol.

::

   /
   ...

Datasets are usually split into several sets of data which are normally used for training, validation and testing. Some might have more splits, other fewer, but generally this is how they are setup. 

To better explain this, we'll use the :ref:`MNIST <mnist_readme>` dataset as an example to describe how datasets are structured inside an ``HDF5`` file.

The ``mnist`` dataset contains two set splits: **train** and **test**. In an ``HDF5`` file these are called ``Groups`` and they are basically folders inside the file.

::

    /
    ├── train/
    │   ...
    │
    └── test/
        ...

Now, for each split, several data fields compose the metadata / annotations of the dataset. These can be images, labels, filenames, bounding boxes, ordered lists, etc., and they convey the available information to be retrieved by the user. In an ``HDF5`` file these are called ``Datasets`` and they store arrays of data as fields.

The ``mnist`` dataset contains the following fields for each set:

::

    /
    ├── train/
    │   ├── classes        
    │   ├── images         
    │   ├── labels        
    │   ├── object_fields  
    │   ├── object_ids     
    │   └── list_images_per_class  
    │
    └── test/
        ├── classes        
        ├── images         
        ├── labels       
        ├── object_fields  
        ├── object_ids 
        └── list_images_per_class 


As you can see, data is stored in a hierarchical way inside a metadata file. 

.. note::

   Notice that both sets have the same fields. This is not the case for other datasets. For more information about how a certain dataset is structured see the :ref:`Available datasets <available_datasets>` Chapter.

Now, there are some aspects that need to be addressed about some of fields of these sets. 

For clarity sake, lets only consider the ``train`` set of this example. We could split these fields into three categories: 

#. **data fields**, 
#. **object fields** 
#. **organized list(s)**. 

The **data fields** category represents the actual data contents of the dataset. For the ``mnist`` example, there only exists information about the ``labels``, ``classes`` and ``images`` tensors. Each is a N-dimensional array of data where each row corresponds to a sample of data, and the dimensionality of these arrays varies between types of fields.

The **object fields** category is made of special crafted fields that exist in all datasets in this package. They are basically aggregators of data fields, for example tables of databases that aggregate foreign keys of other tables.

Here, we have two fields that do this job for us: ``object_fields`` and ``object_ids``. ``object_fields`` is an 2D array that contains an ordered list of the set's field names. These names are used for fetching data of these data fields by some API methods, but, more importantly, it shows how data is structured in the ``object_ids`` field. 
This last field is also an 2D array but it contains indexes of data fields instead. It is this field that correlates different labels / classes for different images for this example. For other datasets, for example, it is this field that links image files with labels with bounding boxes, etc. In the following sections we'll see more clearly the role of these two fields in fetching data.

Lastly, the **organized list(s)** category corresponds to pre-ordered, pre-computed lists that may be helpful for some use cases. For example, for object detection scenarios, having a list of order bounding boxes per image may be useful for selecting only one box per image when creating batches of data. The number of these list fields varies from dataset to dataset, but their use case should be easy to understand just by looking at its name.

In summary, it is important to understand how datasets are structure before proceeding to retrieve data from them. Also, every dataset has its data structured in its own way, but the relationship between them is known via two special fields (``object_fields`` and ``object_ids``). With this knowledge, you should now be ready to tackle how to fetch data from the metadata files associated to a given task of a dataset.

.. note::

   If you want to know more about how the available datasets in this package are structured, please see the :ref:`Available datasets <available_datasets>` Chapter for more information about them.


Retrieving data from a dataset
==============================



Loading a dataset
=================

The DataLoader object
=====================

Attributes
----------

The SetLoader object
====================

Attributes
----------

The FieldLoader object
======================

Attributes
----------





Retrieving data from a dataset
==============================

There are two ways to fetch data samples from a daatset:

- Via API method calls;
- By accessing the data fields directly.

API methods
-----------

get()
^^^^^

object()
^^^^^^^^

object_field_id()
^^^^^^^^^^^^^^^^^

Accessing data fields contents
------------------------------


Parsing data
============

Unpadding lists
---------------

String<->ASCII convertion
-------------------------



Information about a specific set or data field
==============================================

list()
------

size()
------

info()
------


Best practices
==============



