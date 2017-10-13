.. _user_getting_started:

===============
Getting started
===============

Before you start using this package, there are a few things you should be aware
in order to improve your experience when managing datasets. First, :ref:`setting up
the paths <user_setup_paths>` to store data/metada files is important in order to keep things
organized and in the same place. Next, you should also take a look at
the :ref:`available datasets <available_datasets>` data file's size in disk in order to check if you have enough
disk space to store them.

After this is done, take a look at the :ref:`contents of the package <user_contents_package>` before
proceeding to learning how to use the API of this module in the :ref:`basic usage <user_basic_usage>` section.


.. _user_setup_paths:

Setting up paths
==============================

**dbcollection** uses a json cache file stored in your home directory (``~/dbcollection.json``) to log what datasets have been loaded, what tasks have been used
and where data is stored. When first installing this package, the default paths where downloaded data files and .h5 metadata files are stored are defined
in the cache file to store data in ``~\dbcollection\``.

You can chose to store your data files or metadata files into separate dirs on a disk or on separate disks
by modifying the paths of these two fields: ``default_cache_dir`` and ``default_download_dir``. You can either manually change the paths in the ``~\dbcollection.json``
file under the ``info`` key or you can do it by using **dbcollection**. To use the latter, you can do the following::

    # import the package
    import dbcollection as dbc

    # directly access the fields and assign new paths
    dbc.cache.cache_dir = 'new/cache/path'
    dbc.cache.download_dir = 'new/download_data/path'

This will change the paths where the metadata files (``cache_dir``) and the downloaded files (``download_dir``) are stored in disk.
In case you want to reset the paths to the original defaults you can simply do::

    # reset the metadata cache dir to the default path
    dbc.cache.reset_cache_dir()

    # reset the data download dir to the default path
    dbc.cache.reset_download_dir()

With this you should be able to easily locate where data/metadata files are being stored in disk
without having to manually specify a path everytime you setup a new dataset.


.. _user_contents_package:

Contents of the package
==============================

The **dbcollection** package comes with several API methods and other features to help managing datasets
with very little overhead. These include:

- API methods for managing datasets and fetching data;
- API for managing/querying the cache file;
- A list of available datasets;
- utility methods for parsing loaded data, load different types of data files,
  downloading urls, string convertions, or constructing a tree of files in a dir.

The following sections will describe in more detail these features one by one and how to use them.
Next, comes a brief tutorial on how to use this package to quickly start hacking
new stuff with it.

.. _user_basic_usage:

Basic usage
==============================

To use this package you first need to import it.

.. code-block:: python

    import dbcollection as dbc

Then, to load a dataset, all you need to do is call the ``load()`` method with
the name of the dataset you want to load. For example, lets load the ``mnist``
dataset.

.. code-block:: python

    >>> mnist = dbc.load('mnist')

This returns a :ref:`DataLoader <reference_dataloader>` object which contains all necessary methods to fetch data
for this dataset.

Notice the name of the dataset is all lower case. The name of a dataset must be the exact one, and to have the right one
you should check the list of available datasets to see the correct name.
To do this you can use the ``info_datasets()`` method to list all available datasets names and tasks.

.. code-block:: python

    >>> dbc.info_datasets()
    ----------------------------------------
    Available datasets in cache for load
    ----------------------------------------
    - mnist  ['classification']

    -----------------------------------
    Available datasets for download
    -----------------------------------
    - caltech_pedestrian  ['detection', 'detection_10x', 'detection_30x']
    - cifar10  ['classification']
    - cifar100  ['classification']
    - coco  ['caption_2015', 'caption_2016', 'detection_2015', 'detection_2016', 'keypoints_2016']
    - flic  ['keypoints']
    - ilsvrc2012  ['classification', 'raw256']
    - inria_pedestrian  ['detection']
    - leeds_sports_pose  ['keypoints', 'keypoints_original']
    - leeds_sports_pose_extended  ['keypoints']
    - mnist  ['classification']
    - mpii_pose  ['keypoints', 'keypoints_full']
    - pascal_voc_2007  ['detection']
    - pascal_voc_2012  ['detection']
    - ucf_101  ['recognition']
    - ucf_sports  ['recognition']

This returns two lists, one for used datasets on your system, and the other is a list
of all available datasets to download and their respective tasks for processing. Please
notice that the ``mnist`` dataset we've just loaded has the ``classification`` task setup.
This is due to this task being the default task that is selected if no task is specified
at loading time. Also, a list of all available tasks is displayed in the **Available datasets for download**
list.

.. note::
    For more information about the available datasets and tasks see :ref:`here <available_datasets>`.

Returning to the previous example about loading the ``mnist`` dataset, the resulting data loading object
contains several methods to fetch data from the metadata file, as well as other information like the task name,
the set splits, where the data files are located, etc.

.. code-block:: python

    >>> mnist.
    mnist.data_dir          mnist.hdf5_filepath     mnist.object_field_id(  mnist.size(
    mnist.db_name           mnist.info(             mnist.object_fields     mnist.task
    mnist.get(              mnist.list(             mnist.root_path         mnist.test
    mnist.hdf5_file         mnist.object(           mnist.sets              mnist.train

The API methods for fetching and querying the metadata file are quite handy.
For example, to see how the metadata file is structured and what data fields it contains,
you simply have to use the ``info()`` method in order to have an idea of how data is organized.

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

This way, you get a general idea of how the dataset's data is split and what fields
compose each set, and also their type or shape. This method and its output are described in more detail in
the :ref:`fetching data <user_fetching_data>` section.

To fetch data, you can use two methods to retrieve a chunk of data by using the
:ref:`get() <>` and :ref:`object() <>` methods. These two are complementary to one another,
but when you need to fetch data from a single field you use the ``get()`` method, and when
you need to retrieve data from a set of fields you'll use the ``object()`` method.
For example, lets retrieve the first 10 images from the training set of ``mnist``:

.. code-block:: python

   >>> imgs = mnist.get('train', 'images', range(10))
   >>> imgs.shape
   (10, 28, 28)

Fetching data is simple! If can retrieve this same data in two other ways.
The first way is to grab the train set data altogether and then using the
same method:

.. code-block:: python

   >>> train = mnist.train  # get a data loader object of the train set
   >>> train
   SetLoader: set<train>, len<60000>
   >>> imgs = train.get('images', range(10))
   >>> imgs.shape
   (10, 28, 28)

The difference here is that you can grab the train set as a separate object
and do all your operations with it. Also, here you don't have to explicitly
define the set to fetch data from, but you still have to define the field name.

The second way you can fetch data is by targeting the actual field you want to retrieve
data from. Just like the previous examples, we can grab the first 10 images from
the ``mnist`` train set in the following ways:

.. code-block:: python

   >>> # First way
   >>> images = mnist.train.images  # get a data loader object of the images field
   >>> images
   FieldLoader: <HDF5 dataset "images": shape (60000, 28, 28), type "|u1">
   >>> images.get(range(10))
   >>> imgs.shape
   (10, 28, 28)

   >>> # Second way
   >>> imgs = images[0:10]
   >>> imgs.shape
   (10, 28, 28)

For single fields you can do array slicing operations likewith numpy arrays.
All of these operations convey the same results, and it is up to the user to
decide which one fits his/hers needs best.

We've see so far how fetching data from single fields is done, but most cases you
want to grab sets of related data fields like, for example, the image and label.
This information is conveyd by two key fields in the metadata files that relate different
fields ids with each other: the ``object_fields`` and ``object_ids`` fields.
The ``object_ids`` field is a list of indexes of fields defined in the ``object_fields`` field.
So, to get the right label for a given image you just need to collect the ids of each field
and then fetch their data. To do this, we'll use the ``object()`` method to grab the ids of the
fields for the *100th* item:

.. code-block:: python

   >>> # Grab the ids of the image and label fields of the 100th element
   >>> ids = mnist.object('train', 99)
   >>> ids
   array([99,  1], dtype=uint8)
   >>> # Fetch the image data
   >>> img = mnist.get('train', 'images', ids[0])
   >>> img.shape
   (28, 28)
   >>> # Fetch the label data
   >>> label = mnist.get('train', 'labels', ids[1])
   >>> label
   0

Another way you can do this to get the same data, without having to manually
fetch data from every field, is to use the ``convert_to_value`` argument in ``object()``
and set it to ``True``. This will automatically fetch the data of all fields and return them
in a list.

.. code-block:: python

   >>> # Grab the ids of the image and label fields of the 100th element
   >>> (img, label) = mnist.object('train', 99, convert_to_value=True)
   >>> img.shape
   (28, 28)
   >>> label
   0

As you can see, this can be quite handy when multiple fields compose an object element.
You'll mostly use a combination of ``get()`` and ``object()`` to fetch data from a dataset
in your code, and this is all you'll probably need.

The two last methods I would like to point to are :ref:`list() <>` and :ref:`size() <>`. The
``list()`` method lists all data fields available for each set and the ``size()`` method returns
the size of a field. The purpose of these methods is to mearly serve as information source for
the user.

With this information, you should be able to have a sufficient understanding of how ``dbcollection`` works
and how to take advantage of its features. In the following sections we'll dive deeper on more
advanced features and use cases that can help you get more from this module.
