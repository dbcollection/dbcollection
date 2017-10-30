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

There is another way to fetch data besides using ``get()`` and ``object()``. This is done by accessing directly the data fields themselves. To explain this better lets take a look again at the attributes of the ``DataLoader`` object that we've seen before.

.. code-block:: python

   >>> mnist.
   mnist.data_dir          mnist.list(             mnist.size(
   mnist.db_name           mnist.object(           mnist.task
   mnist.get(              mnist.object_field_id(  mnist.test  <---
   mnist.hdf5_file         mnist.object_fields     mnist.train  <---
   mnist.hdf5_filepath     mnist.root_path         
   mnist.info(             mnist.sets 

Note these two attributes highlighted here. These attributes refer to the set splits of the dataset, and are object of type :ref:`SetLoader <core_reference_setloader>`:

.. code-block:: python

   >>> mnist.sets
   ('train', 'test')
   >>> mnist.train
   SetLoader: set<train>, len<60000>
   >>> mnist.test
   SetLoader: set<test>, len<10000>

The set groups in an ``HDF5`` file are converted when loading a ``DataLoader`` object into attributes objects of type ``SetLoader``. These also contain their own set of attributes and methods:

.. code-block:: python

   >>> mnist.train.
   mnist.train.classes                mnist.train.list_images_per_class
   mnist.train.data                   mnist.train.nelems
   mnist.train.fields                 mnist.train.object(
   mnist.train.get(                   mnist.train.object_field_id(
   mnist.train.images                 mnist.train.object_fields
   mnist.train.info(                  mnist.train.object_ids
   mnist.train.labels                 mnist.train.set
   mnist.train.list(                  mnist.train.size(

As you can see, these objects also contain the same methods available in ``DataLoader`` objects and some other attributes that are the data fields of this set.

The only difference between these methods and the ones from ``DataLoader`` is that these do not require you to specify the set name to select data from:

.. code-block:: python

   >>> img = mnist.train.get('images', 0)
   >>> img.shape
   (28, 28)

The attribute fields of ``SetLoader`` objects like, for example, ``mnist.train.classes`` or ``mnist.train.list_images_per_class`` are also special objects of type ``FieldLoader``. 

Lets look at the ``classes`` field:

.. code-block:: python

   >>> train.mnist.classes
   FieldLoader: <HDF5 dataset "classes": shape (10, 11), type "|u1">

   >>> mnist.train.classes.
   mnist.train.classes.data              mnist.train.classes.object_field_id(
   mnist.train.classes.fillvalue         mnist.train.classes.set
   mnist.train.classes.get(              mnist.train.classes.shape
   mnist.train.classes.info(             mnist.train.classes.size(
   mnist.train.classes.name              mnist.train.classes.type
   mnist.train.classes.obj_id

Two important things to mention here. First, when printing the data field, you can see it is of type ``HDF5 dataset``, which means that this field's data is retrieved from disk. Second, some methods available in ``DataLoader`` and ``SetLoader`` are also available here.

.. note:: 

   For more information about how to transfer data to memory see the :ref:`Allocating data to memory <user_fetching_data_to_memory>` section at the end of this page.

The ``FieldLoader`` object contains all necessary information about a data field like ``shape``, ``type``, ``fillvalue`` (used for padding arrays), among others. The ``data`` attribute stores the data buffer that is used to fetch data samples.

To fetch data samples from ``FieldLoader`` objects, you can use common slicing operations like with ``numpy.ndarrays`` or ``HDF5 dataset``:

.. code-block:: python

   >>> mnist.train.classes[0]
   array([ 97, 105, 114, 112, 108,  97, 110, 101,   0,   0,   0], dtype=uint8)

   >>> mnist.train.classes.data[0]
   array([ 97, 105, 114, 112, 108,  97, 110, 101,   0,   0,   0], dtype=uint8)

   >>> mnist.train.classes.get(0)
   array([ 97, 105, 114, 112, 108,  97, 110, 101,   0,   0,   0], dtype=uint8)

All slicing operations used with **numpy** arrays are supported. This is because **h5py** uses **numpy** as the backend. Therefore, you can apply any operations to the output sample that you would do with **numpy** arrays.

.. code-block:: python

   >>> mnist.train.classes[0:5]
   array([[ 97, 105, 114, 112, 108,  97, 110, 101,   0,   0,   0],
       [ 97, 117, 116, 111, 109, 111,  98, 105, 108, 101,   0],
       [ 98, 105, 114, 100,   0,   0,   0,   0,   0,   0,   0],
       [ 99,  97, 116,   0,   0,   0,   0,   0,   0,   0,   0],
       [100, 101, 101, 114,   0,   0,   0,   0,   0,   0,   0]], dtype=uint8)

   >>> mnist.train.classes[0:5][1:3]
   array([[ 97, 117, 116, 111, 109, 111,  98, 105, 108, 101,   0],
          [ 98, 105, 114, 100,   0,   0,   0,   0,   0,   0,   0]], dtype=uint8)

   >>> mnist.train.classes[:, 1:2]
   array([[105],
          [117],
          [105],
          [ 97],
          [101],
          [111],
          [114],
          [111],
          [104],
          [114]], dtype=uint8)

At this point, you should be have mastered everything you may need to know about fetching data using **dbcollection**.

Up until now, we've been focusing on retrieving data samples. However, most of the times you are using this package's API methods is to try to understand / visualize how data is structured and what type is a field composed of.

In the next section, we'll see some handy methods that enables us to visualize how data is structured in a comprehensible format using the REPL.
   

Visualizing information about sets and data fields
==================================================

A good way to see how a dataset is structured is to use the ``info()`` method. 

The ``info()`` method displays information about the sets that compose the dataset and the data fields of each set. It shows the ``shape`` and ``type`` of the fields, and also it the fields are **linked** in ``object_ids`` and in which position.

.. code-block:: python

   >>> mnist.info()

   > Set: test
      - classes,        shape = (10, 2),          dtype = uint8   
      - images,         shape = (10000, 28, 28),  dtype = uint8,  (in 'object_ids', position = 0)
      - labels,         shape = (10000,),         dtype = uint8,  (in 'object_ids', position = 1)
      - object_fields,  shape = (2, 7),           dtype = uint8   
      - object_ids,     shape = (10000, 2),       dtype = uint8   

      (Pre-ordered lists)
      - list_images_per_class,  shape = (10, 1135),  dtype = int32

   > Set: train
      - classes,        shape = (10, 2),          dtype = uint8   
      - images,         shape = (60000, 28, 28),  dtype = uint8,  (in 'object_ids', position = 0)
      - labels,         shape = (60000,),         dtype = uint8,  (in 'object_ids', position = 1)
      - object_fields,  shape = (2, 7),           dtype = uint8   
      - object_ids,     shape = (60000, 2),       dtype = uint8   

      (Pre-ordered lists)
      - list_images_per_class,  shape = (10, 6742),  dtype = int32

With this method, you can display information of a single set if you want. For that, you need to pass the name of the set as input:

.. code-block:: python

   >>> mnist.info('test')

   > Set: test
      - classes,        shape = (10, 2),          dtype = uint8   
      - images,         shape = (10000, 28, 28),  dtype = uint8,  (in 'object_ids', position = 0)
      - labels,         shape = (10000,),         dtype = uint8,  (in 'object_ids', position = 1)
      - object_fields,  shape = (2, 7),           dtype = uint8   
      - object_ids,     shape = (10000, 2),       dtype = uint8   

      (Pre-ordered lists)
      - list_images_per_class,  shape = (10, 1135),  dtype = int32

If you are calling this method from an attribute field that is a ``SetLoader`` object, you don't need to specify the name of the set.

.. code-block:: python

   >>> mnist.test.info()

   > Set: test
      - classes,        shape = (10, 2),          dtype = uint8   
      - images,         shape = (10000, 28, 28),  dtype = uint8,  (in 'object_ids', position = 0)
      - labels,         shape = (10000,),         dtype = uint8,  (in 'object_ids', position = 1)
      - object_fields,  shape = (2, 7),           dtype = uint8   
      - object_ids,     shape = (10000, 2),       dtype = uint8   

      (Pre-ordered lists)
      - list_images_per_class,  shape = (10, 1135),  dtype = int32

You can even use this method on data fields!

.. code-block:: python

   >>> mnist.test.images.info()
   Field: images,  shape = (10000, 28, 28),  dtype = uint8,  (in 'object_ids', position = None)

   >>> mnist.test.labels.info()
   Field: labels,  shape = (10000,),  dtype = uint8,  (in 'object_ids', position = 1)


Along with the ``info()`` method, you have access to two additional methods: ``size()`` and ``list()``. 

``size()`` returns a dictionary or a tuple of the ``shape`` of a data field. As with the ``info()`` method, you can use it in several ways:

.. code-block:: python

   >>> mnist.size()
   {'train': (60000, 2), 'test': (10000, 2)}

   >>> mnist.size('train')
   (60000, 2)

   >>> mnist.size('train', 'images')
   (60000, 28, 28)

   >>> mnist.test.size()
   (10000, 2)

   >>> mnist.test.images.size()
   (10000, 28, 28)


The ``list()`` method also returns a dictionary or a tuple, but it contains the names of all data fields of a set or sets.

.. code-block:: python

   >>> mnist.list()
   {'train': ('classes', 'labels', 'object_fields', 'object_ids', 'images', 
   'list_images_per_class'), 'test': ('classes', 'labels', 'object_fields', 
   'object_ids', 'images', 'list_images_per_class')}

   >>> mnist.list('train')
   ('classes', 'labels', 'object_fields', 'object_ids', 'images', 
   'list_images_per_class')

These three methods enables you to quickly visualize the structure of a dataset and its data, and also to get the shape or names of some data fields with these simple commands.

Next comes the :ref:`Parsing data <user_fetching_data_parsing_data>` section. This section shows how to deal with some quirks of the way data is stored in ``HDF5`` files. This is very important w.r.t. **dbcollection** because some trade-offs had to be made regarding data allocation into arrays.


.. _user_fetching_data_parsing_data:

Parsing data
============

Unpadding lists
---------------

String<->ASCII convertion
-------------------------


.. _user_fetching_data_to_memory:

Allocating data to memory
=========================

Best practices
==============



