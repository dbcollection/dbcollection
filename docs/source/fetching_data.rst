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

To retrieve data from a dataset, we must first load it. 

In this section we'll continue using the ``mnist`` dataset as our example for explaining how we can retrieve data samples for this dataset.

Loading a dataset
-----------------

This section has been explained in detail in previously Chapters. Therefore, lets load the ``mnist`` dataset in the simplest way possible using the ``load()`` method:

.. code-block:: python

   >>> mnist = dbc.load('mnist')

When selecting a dataset, the ``load()`` method returns a ``Dataloader`` object that contains a series of methods and attributes that will be used to query and store data. 


The DataLoader object
---------------------

Printing this data loader object prints the name of the dataset that is associated with and which task was selected. 

.. code-block:: python

   >>> print(mnist)
   DataLoader: "mnist" (classification task)
   
Now, lets take a better look what attributes and methods this object contains:

.. code-block:: python

   >>> mnist.
   mnist.data_dir          mnist.list(             mnist.size(
   mnist.db_name           mnist.object(           mnist.task
   mnist.get(              mnist.object_field_id(  mnist.test
   mnist.hdf5_file         mnist.object_fields     mnist.train
   mnist.hdf5_filepath     mnist.root_path         
   mnist.info(             mnist.sets 

It contains the following attributes:

- ``data_dir``: Directory path where the source data files are stored in disk;
- ``db_name``: Name of the dataset;
- ``task``: Name of the task;
- ``object_fields``: Data field names for each set;
- ``sets``: List of names of set splits (train, test).

These attributes provide useful information about the loaded dataset. The ``sets`` and ``object_fields`` attributes provide relevant information about the number and name of the set splits and the data fields that each set contains, respectively. 
This is useful information when retrieving data using the ``DataLoader`` API methods.

The API methods for fetching data or information of data for this object are the following:

- ``get()``: Retrieves data from the dataset’s ``HDF5`` metadata file;
- ``object()``: Retrieves a list of all fields’ indexes/values of an object composition;
- ``object_field_id()``: Retrieves the index position of a field in the ``object_ids`` list;
- ``list()``: List of all field names of a set;
- ``size()``: Size of a field;
- ``info()``: Prints information about all data fields of a set.

The first two methods are used to fetch data samples from the ``HDF5`` metadata file.
The other methods provide information about the data fields. 

Regarding fetching data, both ``get()`` and ``object`` methods return data samples, but their purpose differs slightly enough that it justifies having two of such methods. ``get`` is used to fetch data of single fields, while ``object`` is used to collect data from multiple fields that compose an 'object'. 

In the next subsection we'll see more clearly this difference between these two methods.

.. note::

   For more information, see the :ref:`DataLoader <reference_dataloader>` section in the :ref:`Reference manual <reference_manual_index>`.


Fetching data using the get() and object() API methods
------------------------------------------------------

Now, lets proceed to retrieve data using these two API methods. 

Lets sample the first 10 images from the training set. 

.. code-block:: python

   >>> imgs = mnist.get('train', 'images', range(10))
   >>> type(imgs)
   <class 'numpy.ndarray'>
   >>> imgs.shape
   (10, 28, 28)


Retrieving the first 10 images from the ``mnist`` dataset is very simple! You just need to provide the name of the set and the name of the data field you want to retrieve data from and the indices of the samples. 

In turn, this returns a ``numpy.ndarray`` with the images' data. The same procedure is done to retrieve data from the other data fields.

If we wanted to return an image and the label associated with it for a given 'object', we would need to determine the indices of each field so we could fetch the correct samples. This is how you would do this to return the 100th sample object:

.. code-block:: python

   >>> # First, see what fields compose the 'object_ids' field
   >>> mnist.object_fields['train']
   ('images', 'labels')
   >>> # Next, get the indices of the fields for the 100th sample object
   >>> ids = mnist.get('train', 'object_ids', 99)
   >>> ids
   array([99,  1], dtype=int32)
   >>> # Then, fetch the data of the 'images' field
   >>> img = mnist.get('train', 'images', ids[0])
   >>> img.shape
   (28, 28)
   >>> # Finally, fetch the data of the 'labels' field
   >>> lbl = mnist.get('train', 'labels', ids[1])
   >>> lbl
   1

This took quite a few steps to do: first you have to find the name of the fields that compose the 'object', then find the ids for each field and then retrieve the data for each sample.

We can write the same example in fewer lines using the ``object()`` method and obtain the same results.

.. code-block:: python

   >>> # Just to show which fields compose the 'object_ids' field
   >>> mnist.object_fields['train']
   ('images', 'labels')
   >>> # Fetch the data in a single command using 'object()'
   >>> (img, lbl) = mnist.object('train', 99, convert_to_value=True)
   >>> img.shape
   (28, 28)
   >>> lbl
   1

As you can see, it is much simpler to fetch data this way. The ``object()`` method receives the set name and the sample object index we want to fetch. If you don't set ``convert_to_value=True``, the method will only return the indexes of the fields. 

With these methods, you can input an index or a list of indexes and retrieve data for any data field existing in a set.
The values on this lists don't need to be contiguous (thanks to ``h5py``).

For example, fetching the first 5 even images is just a matter of passing the right list:

.. code-block:: python

   >>> imgs = mnist.get('train', 'images', [0, 2, 4, 6, 8])
   >>> imgs.shape
   (5, 28, 28)

Or, if you want to get all images, you don't need to pass any index:

.. code-block:: python

   >>> imgs = mnist.get('train', 'images')
   >>> imgs.shape
   (60000, 28, 28)

These methods are quite flexible about what format of inputs they receive, just as long as the input contains valid value ranges.


Fetching data by accessing data fields directly
-----------------------------------------------

There is another way to fetch data besides using the 


Getting information about sets or data fields
---------------------------------------------

list()
^^^^^^

size()
^^^^^^

info()
^^^^^^


The SetLoader object
--------------------


The FieldLoader object
----------------------






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



