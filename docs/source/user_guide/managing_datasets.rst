.. _user_managing_datasets:

=================
Managing datasets
=================

In the previous Chapter :ref:`Getting started <getting_started>`, you've seen basic operations
on how to load a dataset, check what available datasets are in **dbcollection** and
to fetch data like image tensors and labels.

In the following sections, we'll explore
in more detail how to use the **dbcollection** dataset management API to deal with loading,
adding or removing datasets with some simple commands.

Furthermore, other functionality like
managing the cache file, finding which datasets are available for download or which tasks does
it have will be covered as well.

.. note::
    This section covers all the necessary steps / ways for you to effectively use this package for dealing with datasets.


Main operations
===============

You have a set of operations at your disposal using the **dbcollection's** API to
manage your datasets. These operations are:

- :ref:`Downloading data files from online resources <user_managing_datasets_download>`
- :ref:`Parsing annotations / metadata of datasets <user_managing_datasets_process>`
- :ref:`Loading a dataset as a data loader object <user_managing_datasets_load>`
- :ref:`Adding a custom dataset <user_managing_datasets_add>`
- :ref:`Removing a dataset or task <user_managing_datasets_remove>`
- :ref:`Modifying the cache <user_managing_datasets_config_cache>`
- :ref:`Querying the cache <user_managing_datasets_query_cache>`
- :ref:`Displaying cache information <user_managing_datasets_print_cache>`
- :ref:`Displaying information about available datasets <user_managing_datasets_list_datasets>`

These operations allows users to do (pretty much) anything needed for managing data files.

A word of warning for **new users**: you must take into consideration the implications of some of these operations like removing datasets data or modyfing the cache may result in permanent data loss.

You should check the section of :ref:`Best practices <user_managing_datasets_best_practices>` if you are unclear on how to proceed in some cases in order to avoid undesired results.


.. _user_managing_datasets_download:

Downloading data files from online resources
============================================

.. warning::
   This section deals with manually downloading source data files of datasets.

   For most users this information may not be necessary or relevant, and you can skip this section altogether and move to the one which deals with :ref:`loading datasets <user_managing_datasets_load>`.

   This is because the ``load()`` method automatically downloads or processes any dataset that has not been previously setup, and it is not required to manually download data files in order to load a dataset.

One use of **dbcollection** is to download data files from online sources. This removes the need
to search where to get the data files from and to locate which specific resources are required.

In some cases, it is not a very challenging thing to do, but in others it can be a daunting task. By
having the necessary resources defined and ready for use, you can save quite some time when dealing
with this process.

To download a dataset you simply need to use the :ref:`download() <core_reference_api_download>` method from the :ref:`core API <core_reference_api>` methods and provide the name of the dataset you want to download. For example, lets download the ``cifar10`` dataset's data files:

.. code-block:: python

   >>> dbc.download('cifar10')

The data files will be stored in a folder named ``cifar10/`` in a pre-defined directory in disk defined by ``dbc.cache.download_dir``. To change this directory you can simpy assign a new path to it: ``dbc.cache.download_dir = 'my/new/path/'``.

If you want to use a different directory to store the data files you can use the ``data_dir`` input argument to specify the path of the data directory you want to store your files:

.. code-block:: python

   >>> dbc.download('cifar10', data_dir='some/other/path/')

This will also create a folder with the same name as the dataset. This is important because
**dbcollection** searches for this dir names when loading the data files. If the names don't
match then it proceeds to download the source files.

After all files have been downloaded, by default, they are extracted into the same folder where they have been stored.

Most source files are compressed for distribution. The ``download()`` method allows to extract these compressed files to disk without you having to manually do it yourself.
If the source data files are all what you want to retrieve, then set the ``extract_data`` input argument to ``False``:

.. code-block:: python

   >>> dbc.download('cifar10', extract_data=False)

.. note::
   This package uses the `patool <https://pypi.python.org/pypi/patool>`_ module for file extraction which supports most data compression formats like TAR, ZIP or RAR.

An important aspect to mention about using this method is that, when using it to download data files of a dataset, it automatically registers in cache where the files are located for that dataset.

So, next time you want to load that dataset, you don't need to explicitly tell where the data is located in disk (if the files still exist of course).


.. _user_managing_datasets_process:

Parsing annotations / metadata of datasets
==========================================

.. warning::
   This section deals with manually parsing annotations of datasets.

   For most users this information is not relevant and you can skip this section altogether and move to the next one which deals with :ref:`loading datasets <user_managing_datasets_load>`.

   This is because the ``load()`` method automatically downloads or processes any dataset that has not been previously setup, and it is not required to manually parse annotations of tasks of datasets in order to load a dataset.

Arguably, one of the most important functionalities of **dbcollection** is automatically processing data annotations.
It is well known that manually parsing data files + annotations of different datasets is no fun.

Moreover, it is time consuming, annoying and repetitive.
Also, it usually results in disks littered with various cache files which are used to store portions of the annotations accross multiple directories for some specific tasks.

**dbcollection** provides a way to deal with these issues. Hand-crafted scripts were developed to parse data annotations of specific tasks of datasets for you.  These annotations are stored in a common format and in a single place on your disk that you can easily track.

.. note::
   Not all annotations are necessary for day to day use, so only the most useful ones are stored.

   If you happen to need an annotation that is not available in our scripts for any particular reason, please feel free to fill an `issue on GitHub <https://github.com/dbcollection/dbcollection/issues>`_ describing what annotation you need, why and for what task + dataset or, better yet, :ref:`contribute with a pull request <pull_request>`.

Processing metadata of dataset's annotations is done by using the :ref:`process() <core_reference_api_process>` method.
Continuing with the previous section example, lets process the metadata files for the ``cifar10`` dataset:

.. code-block:: python

   >>> dbc.process('cifar10')

The method will process the data annotations of this dataset and stores the resulting metadata into an ``HDF5`` file stored in disk. By default, all metadata files are stored in your home directory in ``~/dbcollection/<dataset>/<task>.h5``.

This directory is used to centralize all metadata files in disk and its path can be accessed via ``dbc.cache.cache_dir``. To change the default path, simply assign a new path to it: ``dbc.cache.cache_dir = new/cache/path/``.

Many datasets have many tasks to choose from and these can be listed by the ``info_datasets()`` method described in :ref:`this section <user_managing_datasets_list_datasets>`. To specify which task to process, we must use the ``task`` input argument and assign it a task name:

.. code-block:: python

   >>> dbc.process('cifar10', task='classification')

This processes the annotations of the ``classification`` task and registers them to cache.

We must point out that this example is not the most illustrative of them all because ``cifar10`` only has one task which is ``classification``.

Every dataset has a default task and it is not required to explicitly define one. But, if you want to select a different task, you will need to provide a valid task name for processing.

.. note::
   The ``process()`` method requires that the data files of a dataset have been previously downloaded and registered in the cache.

   If you have not done this, please see the previous section which explains how to download data files of a dataset or see the section further on this page about manually configuring the cache if you happen to have the necessary data files in disk but on a different folder.

The next section covers the ``load()`` method which deals with loading datasets as data loader objects for extracting (meta)data.


.. _user_managing_datasets_load:

Loading a dataset as a data loader object
=========================================

Loading a dataset's metadata is quite simple. For that, we need to use the :ref:`load() <core_reference_api_load>` method
and select a dataset to import. Lets load the ``cifar10`` dataset:

.. code-block:: python

   >>> cifar10 = dbc.load('cifar10')

To load a dataset we just need to specify its name and in return we'll get a ``DataLoader`` object.

.. code-block:: python

   >>> cifar10
   DataLoader: "cifar10" (classification task)

This object contains methods to retrieve data from and attributes with information about the dataset's name, task, metadata file path, sets and other kinds of information.

.. code-block:: python

   >>> cifar10.
   cifar10.data_dir          cifar10.list(             cifar10.size(
   cifar10.db_name           cifar10.object(           cifar10.task
   cifar10.get(              cifar10.object_field_id(  cifar10.test
   cifar10.hdf5_file         cifar10.object_fields     cifar10.train
   cifar10.hdf5_filepath     cifar10.root_path
   cifar10.info(             cifar10.sets

With this ``DataLoader`` object, fetching data like labels, bounding boxes, images filenames, etc., is trivial.

.. note::

   A more detailed look on how (meta)data is stored and retrieved will be described in the Chapter :ref:`Fetching data <user_fetching_data>`.

When loading a dataset for the first time that is not available in disk, the ``load()`` method will download the dataset's data files and parse the annotations into an ``HDF5`` metadata file. The data and metadata files will be stored in the dirs defined in ``dbc.cache.download_dir`` and ``dbc.cache.cache_dir``, respectively. These dirs' paths can me modified by assigning new values to them.

In cases where ou might want to download your data files into a separate directory or you have the dataset's data files available in another directory, you can use the ``data_dir`` input argument to specify which path to use.

Lets load the ``cifar100`` dataset, but this time lets store the data files into a new directory:

.. code-block:: python

   >>> cifar100 = dbc.load('cifar100', data_dir='some/new/path/')

If you haven't downloaded/loaded it yet, it will proceed to download and extract the files to the ``some/new/path/`` path provided in ``data_dir`` and process the default task for this dataset.

When loading/downloading a dataset for the first time, the dataset's information about where the data and the cache files are stored is registered in the ``~/dbcollection.json`` cache file, so that next time you load a specific dataset you'll only need to specify its name without having to provide the path where the data files are stored.

Now, lets talk about tasks of datasets. In the previous examples we've dimissed any references about which task to load in order to keep the examples simple. For some simple datasets, often there's only one task available to use, but for cases like ``coco`` for example, there are many different tasks that have different types of fields. For these cases, it is important to specify which task to use.

To load a specific task, you need to use the ``task`` input argument and assign a name of the task you want to load. If no task is specified, the default task ``task="default"`` is used. For the previous example, we could have done this by specifying the task name as ``classification``:

.. code-block:: python

   >>> cifar100_cls = dbc.load('cifar100', task='classification')

The returned object contains the information of the selected task in its ``__str__()`` method:

.. code-block:: python

   >>> cifar100_cls
   DataLoader: "cifar10" (classification task)

The ``load()`` method is probably the only method you'll ever need to use to load datasets. The Chapter :ref:`Fetching data <user_fetching_data>` continues where this section stopped about dealing with (meta)data. In the following sections deal with adding and removing datasets to / from the cache and what their uses are.

.. note::
   The :ref:`Best practices <user_managing_datasets_best_practices>` section at the end of this page provides some tips about how to setup **dbcollection** in your system in order to never have the need to look at any other method besides ``load()`` for dealing with datasets.


.. _user_managing_datasets_add:

Adding a custom dataset
=======================

The :ref:`add() <core_reference_api_add>` method is used to add custom datasets to the cache.

To add a custom dataset, you need to provide information about the ``name``, ``task``, ``data_dir`` and ``file_path``.
Optionally, you can add a list of ``keywords`` to categorize the dataset.

Lets add a custom dataset to the available datasets list for load in cache:

.. code-block:: python

   >>> dbc.add(name='new_dataset',
               task='new_task',
               data_dir='some/path/data',
               file_path='other/path/metadata/file.h5',
	       keywords=('image_processing', 'classification'))

When loading this dataset, the ``name`` and ``task`` args are required in order to select the dataset. Then, the ``HDF5`` file containing the metadata is loaded as a ``DataLoader`` object and all data files are available in the directory path provided by ``data_dir``.

This method can also be used to add additional tasks to existing datasets. For example, if we wanted to enhance the ``cifar10`` dataset with an extra task which contains custom metadata, you could do something like the following:

.. code-block:: python

   >>> dbc.add(name='cifar10',
               task='custom_classification',
               data_dir='default/path/dir/cifar10',
               file_path='path/to/new/metadata/file.h5')

You can also use the ``add()`` method to assign the path of the data files for a dataset. This would tell the ``load()`` method to search for the data files in a specific path before attempting to execute the code path to download data files.

.. code-block:: python

   >>> dbc.add(name='mnist',
               data_dir='default/path/dir/cifar10',
               task='',  # skips adding the task name
               file_path='')  # skips adding the file path for the task



.. _user_managing_datasets_remove:

Removing a dataset or task
==========================

Removing datasets or tasks is pretty simple. With :ref:`remove() <core_reference_api_remove>`, all you need to do to remove a dataset is to provide the name of the dataset you want to remove from the cache.

.. code-block:: python

   >>> dbc.remove('cifar100')

If you just want to delete a task from a dataset you need to specify both the name of the dataset you want to remove from and the name of the task:

.. code-block:: python

   >>> dbc.remove('cifar100', 'classification')

This removes the ``classification`` task entry from the cache registry and it also deletes the metadata file associated to it.

However, this will not remove the data files from disk. For that, you must use the ``delete_data`` argument and set it to ``True``.

.. code-block:: python

   >>> dbc.remove('cifar100', 'classification', delete_data=True)

.. warning::

   This will permanently remove the data files stored in the ``data_dir`` path associated with the dataset in the cache.


.. _user_managing_datasets_config_cache:

Modifying the cache
===================

There are several ways to manage / modify the cache contents in ``~/dbcollection.json`` or to delete / reset the cache file.

The :ref:`config_cache() <core_reference_api_config_cache>` allows users to do the following operations:

- Change values of fields;
- Delete the cache file / directory;
- Delete the ``~/dbcollection.json`` cache file;
- Reset the cache file.

Lets look at some examples.

First, we can change the default cache directory path and assign it a new path:

.. code-block:: python

   >>> dbc.config_cache('default_cache_dir', 'new/path/cache/')

Or we could change the default directory where data files are downloaded:

.. code-block:: python

   >>> dbc.config_cache('default_download_dir', 'new/path/download/')

Or both at the same time:

.. code-block:: python

   >>> dbc.config_cache(field='info',
                        value={'default_cache_dir', 'new/path/cache/',
                               'default_download_dir': 'new/path/download/'})

Any field can be changed in the cache file just by specifying its name and the new value you want to change it with. The ``field`` arg looks for a string in the cache file and, if it finds a valid match, it replaces the first found match with the value provided with the ``value`` arg.

Other operations this method allows is to delete folders associated with the cache file or even the cache file itself. To remove just the cache folder where all the metadata ``HDF5`` files are stored, you need to do the following:

.. code-block:: python

   >>> dbc.config_cache(delete_cache_dir=True)


If you just want to remove or reset the cache file you can do the following:

.. code-block:: python

   >>> # Remove the cache file
   >>> dbc.config_cache(delete_cache_file=True)

   >>> # Reset the cache file (empty data)
   >>> dbc.config_cache(reset_cache=True)

You can also bundle these arguments together to delete the cache dir and file:

.. code-block:: python

   >>> # Remove the cache file + dir
   >>> dbc.config_cache(delete_cache_file=True, delete_cache_dir=True)

Or do it in one sweep:

.. code-block:: python

   >>> # Remove the cache file + dir
   >>> dbc.config_cache(delete_cache=True)


.. note::

   The ``config_cache()`` method is somewhat limited in its scope compared with other ways to change the cache contents (like directly modifying the cache file manually) but it has the necessary functionality to do the most common operations you might want to do like changing some fields or deleting / reseting the cache.


.. warning::

   The ``config_cache()`` method should be used with extreme caution in order to not permanently delete your configurations. If you are going to use this method, please be aware of dangers of doing so.


.. _user_managing_datasets_query_cache:

Querying the cache
==================

Sometimes you just need to search for some keywords in the cache and you don't want to take the effort to do it with a terminal.

The :ref:`query() <core_reference_api_query>` method allows to search for a pattern in the cache file and returns the contents of that pattern for any match. This means it can return multiple values depending on the the pattern and the configurations registered in your cache file.

For example, you might want to know what are the default paths for the cache and download dirs in your system. To retrieve this information, you can use the ``query()`` method and search for the ``info`` pattern like this:

.. code-block:: python

   >>> dbc.query('info')
   [{'info': {'default_cache_dir': '/home/mf/dbcollection', 'default_download_dir':
   '/home/mf/dbcollection/data/'}}]

We can also list all categories listed in the cache file:

.. code-block:: python

   >>> dbc.query('category')
   [{'category': {'classification': ['mnist', 'cifar10'], 'detection':
   ['leeds_sports_pose'], 'human pose': ['leeds_sports_pose'],
   'image_processing': ['leeds_sports_pose', 'cifar10'], 'keypoints':
   ['leeds_sports_pose']}}]

This can also be useful to locate the contents of a dataset.

.. code-block:: python

   >>> dbc.query('mnist')
   [{'mnist': {'data_dir': '/home/mf/dbcollection/mnist/data', 'keywords':
   ['classification'], 'tasks': {'classification': '/home/mf/dbcollection/mnist/
   classification.h5'}}}]

If the pattern was not found in the cache file, it return an empty dictionary.

.. code-block:: python

   >>> dbc.query('cifar1000')
   []

We can also retrieve information of all datasets that have the same keyword.

.. code-block:: python

   >>> dbc.query('classification')
   [{'dataset': {'cifar10': {'keywords': ['classification']}}}, {'dataset':
   {'mnist': {'keywords': ['classification']}}}]


The ``query()`` method is ment to do simple searches of patterns. It is always much more useful to take a look at the cache file itself, but for its scope it may provide the necessary functionality you might need.


.. _user_managing_datasets_print_cache:

Displaying cache information
============================

You can display the contents of you cache file into the screen by using the :ref:`info_cache() <core_reference_api_info_cache>` method.

It prints the cache file contents in a structured way for easier visualization.

.. code-block:: python

   >>> dbc.info_cache()
   --------------
     Paths info
   --------------
   {
       "default_cache_dir": "/home/mf/dbcollection",
       "default_download_dir": "/home/mf/dbcollection/data/"
   }

   ----------------
     Dataset info
   ----------------
   {
       "cifar10": {
           "data_dir": "/home/mf/dbcollection/data/cifar10/data",
           "keywords": [
               "image_processing",
               "classification"
           ],
           "tasks": {
	       "classification": "/home/mf/dbcollection/cifar10/classification.h5"
           }
       },
       "cifar100": {
           "data_dir": "/home/mf/dbcollection/data/cifar100/data",
           "keywords": [
               "image_processing",
               "classification"
           ],
           "tasks": {
	       "classification": "/home/mf/dbcollection/cifar100/classification.h5"
           }
       },
       "mnist": {
           "data_dir": "/home/mf/dbcollection/mnist/data",
           "keywords": [
               "classification"
           ],
           "tasks": {
               "classification": "/home/mf/dbcollection/mnist/classification.h5"
           }
       }
   }

   ------------------------
     Datasets by category
   ------------------------

      > classification:   ['cifar10', 'cifar100', 'mnist']
      > image_processing: ['cifar10', 'cifar100']

You can select what sections you want to display by using the ``paths_info``, ``datasets_info`` and ``categories_info`` args.

.. code-block:: python

   >>> dbc.info_cache(datasets_info=False, categories_info=False)
   --------------
     Paths info
   --------------
   {
       "default_cache_dir": "/home/mf/dbcollection",
       "default_download_dir": "/home/mf/dbcollection/data/"
   }

   >>> dbc.info_cache(paths_info=False, categories_info=False)
   ----------------
     Dataset info
   ----------------
   {
       "cifar10": {
           "data_dir": "/home/mf/dbcollection/data/cifar10/data",
           "keywords": [
               "image_processing",
               "classification"
           ],
           "tasks": {
	       "classification": "/home/mf/dbcollection/cifar10/classification.h5"
           }
       },
       "cifar100": {
           "data_dir": "/home/mf/dbcollection/data/cifar100/data",
           "keywords": [
               "image_processing",
               "classification"
           ],
           "tasks": {
	       "classification": "/home/mf/dbcollection/cifar100/classification.h5"
           }
       },
       "mnist": {
           "data_dir": "/home/mf/dbcollection/mnist/data",
           "keywords": [
               "classification"
           ],
           "tasks": {
               "classification": "/home/mf/dbcollection/mnist/classification.h5"
           }
       }
   }

   >>> dbc.info_cache(paths_info=False, datasets_info=False)
   ------------------------
     Datasets by category
   ------------------------

      > classification:   ['cifar10', 'cifar100', 'mnist']
      > image_processing: ['cifar10', 'cifar100']

This method also allows you to select information about a single or multiple datasets.

.. code-block:: python

   >>> dbc.info_cache('cifar10')
   --------------
     Paths info
   --------------
   {
       "default_cache_dir": "/home/mf/dbcollection",
       "default_download_dir": "/home/mf/dbcollection/data/"
   }

   ----------------
     Dataset info
   ----------------
   {
       "cifar10": {
           "data_dir": "/home/mf/dbcollection/data/cifar10/data",
           "keywords": [
               "image_processing",
               "classification"
           ],
           "tasks": {
	       "classification": "/home/mf/dbcollection/cifar10/classification.h5"
           }
       }
   }

   ------------------------
     Datasets by category
   ------------------------

      > classification:   ['cifar10']
      > image_processing: ['cifar10']


   >>> dbc.info_cache(['cifar10', 'cifar100'])
   --------------
     Paths info
   --------------
   {
       "default_cache_dir": "/home/mf/dbcollection",
       "default_download_dir": "/home/mf/dbcollection/data/"
   }

   ----------------
     Dataset info
   ----------------
   {
       "cifar10": {
           "data_dir": "/home/mf/dbcollection/data/cifar10/data",
           "keywords": [
               "image_processing",
               "classification"
           ],
           "tasks": {
	       "classification": "/home/mf/dbcollection/cifar10/classification.h5"
           }
       },
       "cifar100": {
           "data_dir": "/home/mf/dbcollection/data/cifar100/data",
           "keywords": [
               "image_processing",
               "classification"
           ],
           "tasks": {
	       "classification": "/home/mf/dbcollection/cifar100/classification.h5"
           }
       }
   }

   ------------------------
     Datasets by category
   ------------------------

      > classification:   ['cifar10', 'cifar100']
      > image_processing: ['cifar10', 'cifar100']


.. _user_managing_datasets_list_datasets:

Displaying information about available datasets
===============================================

Some important information about **dbcollection** is the list of available datasets for load + download. Also, information about what tasks are available per dataset is of great interest.

This is achieved via the :ref:`info_datasets() <core_reference_api_info_datasets>` method that lists what datasets are available for load in your system and what datasets and tasks are available for download.

.. code-block:: python

   >>> dbc.info_datasets()
   ----------------------------------------
     Available datasets in cache for load
   ----------------------------------------
     - cifar10  ['classification']
     - cifar100  ['classification']
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

You can define what information you want to print to the screen via the args ``show_downloaded`` and ``show_available``.

.. code-block:: python

   >>> dbc.info_datasets(show_available=False)
   ----------------------------------------
     Available datasets in cache for load
   ----------------------------------------
     - cifar10  ['classification']
     - cifar100  ['classification']
     - mnist  ['classification']


   >>> dbc.info_datasets(show_downloaded=False)
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

Also, you can list only the datasets that match a certain pattern.

.. code-block:: python

   >>> dbc.info_datasets('pascal', show_downloaded=False)
   -----------------------------------
     Available datasets for download
   -----------------------------------
     - pascal_voc_2007  ['detection']
     - pascal_voc_2012  ['detection']


.. _user_managing_datasets_best_practices:

Best practices
==============

These are some of the recommended practices when dealing with managing datasets using the **dbcollection** package.

There are several ways to achieve the same result and these are some of the most common practices that you might encounter when using this package.


Before downloading / loading a dataset
--------------------------------------

There are some things you should do prior to use the ``download()`` and ``load()`` methods if you don't like the default setup. For example, it is always useful to specify where you want the data files to be stored in your system.

It is best practice to store all your files in the same directory. If you have an SSD drive but you don't want to store eveything there, it is best to use the ``data_dir`` argument tom specify uses cases, while keeping everything else under the same directory.

To do this, set the paths for the ``default_download_dir`` in your cache file. The recommended way to do this is the following:

.. code-block:: python

   >>> dbc.cache.download_dir = 'new/path/to/download/data/'

You can also do this for the cache dir where the metadata files are stored, but it shouldn't be a big deal unless you are really keen for quick data accesses. Likewise, you should use the following way to set the path of the cache dir:

.. code-block:: python

   >>> dbc.cache.cache_dir = 'new/path/to/cache/metadata/'


Removing datasets from cache
----------------------------

The easiest and the less error prone way to remove a dataset from cache is by using the ``remove()`` method. This will parse the cache file and remove any information regarding the specific dataset you are looking to remove.

The same is valid for removing a task of a dataset. Or the data files in your system.

Resetting / deleting the cache file
-----------------------------------

If you must delete or reset the contents of your file, there are two recommended ways for you to do this:

#. Using the ``config_cache()`` method;
#. Manually deleting the file from your filesystem.

Both will accomplish the same goal, so feel free to chose the one that fits you best.


Changing fields / values of the cache
-------------------------------------

Here I strongly recommend you to do this process by hand. This means opening the ``~/dbcollection.json`` file and manually changing the field or value you want. This may be easier to do or to understand what is actually being changed, and it should be less error prone for most users.

Also, this isn't a common operation todo, so take this advice with a grain of salt.


Checking the contents of the cache file
---------------------------------------

The contents of the ``~/dbcollection.json`` cache file may be hard to read when you have many many datasets registered, so it is best to use the ``info_cache()`` because it produces much nicer outputs for the cache, and you always define what data you want to visualize.


Checking what datasets are available for download
-------------------------------------------------

I strongly recommend you to check the documentation in order to see what datasets are available for download / use.

The ``info_datasets()`` does list all available datasets + tasks in the **dbcollection** package and it is fine to see the list of available datasets. However, the documentation has much more information about them.

