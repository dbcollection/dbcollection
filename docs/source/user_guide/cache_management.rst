.. _user_cache_management:

==================
Managing the cache
==================

This Chapter addresses managing / configurating the cache registry of used datasets.

The ``~/dbcollection.json`` cache file located in your home directory is the central registry of **dbcollection**. Here is stored the information about what datasets have been downloaded / parsed, which tasks are listed for use, where is data stored and what categories exist.

It is important to keep this file in your system's home directory because there is where **dbcollection** tried to locate it. If it is not found, an empty one will be generated.

A situation that might take you to manually configure this cache file, opposed to letting the package do it for you, is when you have moved data around to other paths in your disk and you need to fix this in the cache file. Here we'll see how to deal with this kind of scenarios.

In this Chapter we'll see the most important operations you may want / need to do to configure the cache file in your system.


Cache's structure
=================

The ``~/dbcollection.json`` cache file is composed of three main sections:

- ``info``: holds default paths configurations;
- ``datasets``: list of datasets information like data path, tasks and keywords;
- ``category``: list of datasets grouped by categories (e.g., classification, keypoints, object_detection, etc.).

For example, this is how a cache file is generally formatted:

.. code-block:: json

   {
       "info": {
            "default_cache_dir": "/home/mf/dbcollection",
            "default_download_dir": "/home/mf/dbcollection/downloaded_data"
       },
       "datasets": {
           "mnist": {
                "data_dir": "/home/mf/dbcollection/downloaded_data/mnist/data",
                "keywords": [
                    "image_processing",
                    "classification",
                ],
                "tasks": {
                    "classification": "/home/mf/dbcollection/mnist/classification.h5"
                }
           }
       },
       "category": {
            "classification": [
                "mnist"
            ],
            "image_processing": [
                "mnist"
            ],
       }
    }

The ``info`` section contains default paths of where the ``HDF5`` metadata files and source data files are stored.

The ``datasets`` section stores the metadata information for each dataset loaded in the system. Here you'll find what tasks have been processed, where the source data files are stored and what keywords define them.

The ``category`` section contains all categories defined in the ``keywords`` field of each dataset and groups them by name. The main purpose for this section is to help find similar datasets for a certain category.


Accessing the cache's contents
==============================

To access the cache's contents you can:

- Open the ``~/dbcollection.json`` cache file in the filesystem;
- Use the ``config_cache()``, ``query()`` and ``info_cache()`` methods;
- Use the ``.cache`` attribute which is loaded when importing the package.

Opening the cache file is the easiest way to visualize and modify the contents of the cache.

The ``config_cache()``, ``query()`` and ``info_cache()`` methods are useful when simple operations like displaying the cache contents or modifying a field is required.

The last way to access the cache is by accessing the ``.cache`` attribute of the package. When importing **dbcollection**, the cache file is automatically loaded into memory as a :ref:`CacheManager <core_reference_cache_management>` object.

.. code-block:: python

   >>> import dbcollection as dbc
   >>> dbc.cache
   <dbcollection.core.cache.CacheManager object at 0x7f2875878550>

This object contains methods attributes and methods for managing the cache in a deeper level compared to the previous ways to deal with the cache registry.

Here is the list of attributes and methods that compose the ``CacheManager`` object:

.. code-block:: python

   >>> dbc.cache.
   dbc.cache.__class__(                  dbc.cache._set_download_dir(
   dbc.cache.__delattr__(                dbc.cache.add_data(
   dbc.cache.__dict__                    dbc.cache.add_keywords(
   dbc.cache.__dir__(                    dbc.cache.cache_dir
   dbc.cache.__doc__                     dbc.cache.cache_filename
   dbc.cache.__eq__(                     dbc.cache.check_dataset_name(
   dbc.cache.__format__(                 dbc.cache.clear(
   dbc.cache.__ge__(                     dbc.cache.create_os_home_dir(
   dbc.cache.__getattribute__(           dbc.cache.data
   dbc.cache.__gt__(                     dbc.cache.delete_category_entry(
   dbc.cache.__hash__(                   dbc.cache.delete_dataset(
   dbc.cache.__init__(                   dbc.cache.delete_dataset_cache(
   dbc.cache.__le__(                     dbc.cache.delete_entry(
   dbc.cache.__lt__(                     dbc.cache.delete_task(
   dbc.cache.__module__                  dbc.cache.download_dir
   dbc.cache.__ne__(                     dbc.cache.exists_dataset(
   dbc.cache.__new__(                    dbc.cache.exists_task(
   dbc.cache.__reduce__(                 dbc.cache.get_dataset_storage_paths(
   dbc.cache.__reduce_ex__(              dbc.cache.get_task_cache_path(
   dbc.cache.__repr__(                   dbc.cache.info(
   dbc.cache.__setattr__(                dbc.cache.is_empty(
   dbc.cache.__sizeof__(                 dbc.cache.is_test
   dbc.cache.__str__(                    dbc.cache.modify_field(
   dbc.cache.__subclasshook__(           dbc.cache.read_data_cache(
   dbc.cache.__weakref__                 dbc.cache.read_data_cache_file(
   dbc.cache._cache_dir                  dbc.cache.reload_cache(
   dbc.cache._default_cache_dir_path(    dbc.cache.reset_cache(
   dbc.cache._empty_data(                dbc.cache.reset_cache_dir(
   dbc.cache._get_cache_dir(             dbc.cache.reset_download_dir(
   dbc.cache._get_download_dir(          dbc.cache.update(
   dbc.cache._os_remove(                 dbc.cache.write_data_cache(
   dbc.cache._set_cache_dir(

The cache's contents are stored in a dictionary under the ``.data`` attribute. Although this way of accessing the contents of the cache is a bit more complex than the other two, it does provide some functionality that is very useful for certain cases.

In the following sections we'll take a look at the most common operations that you might need to know to manage **dbcollection**'s cache like adding, modifying or deleting a dataset or task or reseting path defaults.

.. note::

   The ``CacheManager`` object contains many methods for specific actions, and, to learn more about them, it is encouraged to take a look at the **reference manual** for more details about them. Only the most important ones will be covered in this Chapter.


Displaying the cache's contents
===============================

To visualize the cache's contents you can:

- Open the cache file in your filesystem;
- Use ``dbc.info_cache()`` or ``dbc.cache.info()`` methods to display the contents to the screen;

These two methods display the same information about the cache, so use whichever method you prefer.


Basic operations
================

The most common operations you may need are *adding*, *modifying*, *deleting* and *querying* the cache.

There are other available operations you can do, but on this section we'll focus on these four basic operations which should cover most use cases when dealing with the cache registry.

.. note::

   All following operations can be done by manually  opening the file modyfing its contents. Here, we'll only focus on doing these operations using the available attributes / methods in **dbcollection**.


Getting information about a dataset
-----------------------------------

To fetch the cache's contents about a dataset, you can access the ``.data`` attribute. For example, to fetch the data about the ``mnist`` dataset, you can do the following:

.. code-block:: python

   >>> dbc.cache.data['dataset']['mnist']
   {'data_dir': '/home/mf/dbcollection/downloaded_data/mnist/data', 'tasks':
   {'classification': '/home/mf/dbcollection/mnist/classification.h5'}, 'keywords':
   'classification'}


Adding a dataset
----------------

Inserting a data into the cache is done by using the ``add_data()`` method. It requires the name and the data in order to insert it into the registry. This will create an entry under the ``datasets`` and ``category`` sections.

.. code-block:: python

   >>> # add a custom dataset
   >>> dbc.cache.add_data('new_dataset',
                          {'data_dir': '/some/new/dir',
                           'tasks': {'some_task': '/path/to/task/some_task.h5'},
                           'keywords': ['list', 'of', 'keywords']})


Adding a task
-------------

To add a task to an existing dataset, you can proceed in two ways.

#. The first way is to use the ``.data`` attribute field and insert a new task into the dictionary:

   .. code-block:: python

      >>> # add a new task to mnist
      >>> dbc.cache.data['dataset']['mnist']['tasks'].update({'new_task': 'path/to/new/task.h5'})
      >>> dbc.cache.write_data_cache(dbc.cache.data)  # write the changes to disk

#. The second way is by using the ``.add_data()`` method:

   .. code-block:: python

      >>> # get mnist data
      >>> mnist_metadata = dbc.cache.data['dataset']['mnist']
      >>> # add a new task
      >>> mnist_metadata['tasks'].update({'new_task': 'path/to/new/task.h5'})
      >>> dbc.cache.add_data('mnist', mnist_metadata, is_append=True)


Removing a dataset
------------------

Removing dataset entrys is pretty simple. To do this use the ``delete_dataset()`` method to remove the dataset from the cache:

.. code-block:: python

   >>> dbc.cache.delete_dataset('mnist')

Please note that this will also remove the dataset's directory in disk.

.. warning::

   You cannot remove a dataset simply by removing the entry from ``.data``'s dictionary. This would require you to write the changes to disk and you would also need to remove all the registries of the dataset from ``category``.


Removing a task
---------------

Just like removing datasets, to remove a task you simply need to call the ``delete_task()`` method. This method requires you to specify the dataset's name and the task you want to remove. This will remove the task entry from the cache and its file from disk.

.. code-block:: python

   >>> dbc.cache.delete_dataset('mnist', 'classification')


Modifying data
--------------

The process of modifying data is simillar to assigning new information to the cache.

The easiest way to do this is by changing the contents of ``.data`` and writting the changes back to disk:

.. code-block:: python

   >>> # do stuff to data
   >>> dbc.cache.data['info']['default_download_dir'] = 'new/save/dir'
   >>> # write changes to disk
   >>> dbc.cache.write_data_cache(dbc.cache.data)


Reset the cache
---------------

There might come a time where you need to reset the configurations of your cache.

For whatever reason you may need to do this, you just need to use the ``reset_cache()`` method and it will reset the contents of your cache file, leaving it empty of information about datasets and restoring the default paths for the cache downloaded files diretories.

.. code-block:: python

   >>> dbc.cache.reset_cache(force_reset=True)

.. note::

   You have to explicitly set ``force_reset`` to ``True``. This is a failsafe mechanism to avoid unintended resets of the cache.


Check if a dataset exists
-------------------------

To see if a dataset exists you can:

#. Check if the name exists in ``.data``.

   .. code-block:: python

      >>> 'mnist' in dbc.cache.data['datasets']
      True

#. Use the ``exists_dataset()`` method.

   .. code-block:: python

      >>> dbc.cache.exists_dataset('mnist')
      True


Check if a task exists
----------------------

To check if a task exists for a dataset you can:

#. Transverse the dataset's metadata in ``.data`` and look for a particular task name.

   .. code-block:: python

      >>> 'classification' in dbc.cache.data['datasets']['mnist']['tasks']
      True

#. Use the ``exists_task()`` method.

   .. code-block:: python

      >>> dbc.cache.exists_task('mnist', 'classification')
      True


Other useful operations
=======================

Here are a few other operations that will be very useful for you to use.

Change the default metadata cache directory
-------------------------------------------

Changing the directory where the ``HDF5`` metadata files are stored may be usefull if you want to store these files in another disk like an SSD.

To do this, you simply need to assign a new path to the ``.cache_dir`` attribute field and it will automatically register it both in memory and in disk.

.. code-block:: python

   >>> dbc.cache.cache_dir = 'new/path/cache/'

Also, you can check what the current path where the cache data is stored by printing this field:

.. code-block:: python

   >>> dbc.cache.cache_dir
   'new/path/cache/'


Change the default download directory path
------------------------------------------

Like with the cache directory, you can also change the default path where source data files of datasets are stored via the ``.download_dir`` attribute field.

Just assign a new path to it to change where the source files are stored in disk:

.. code-block:: python

   >>> dbc.cache.download_dir = 'new/save/path/download/data/'

Likewise, to see check what is the default path where downloaded data files are stored just print this field:

.. code-block:: python

   >>> dbc.cache.download_dir
   'new/save/path/download/data/'


Reloading the cache
-------------------

Consider the following: you've changed something in the cache file (manually or by some other way) but you want to discard them and get back the previous cache state.

This is achieved by useing the ``reload_cache()`` method which loads the cache's contents in disk back to memory, regenerating the previous information.

.. code-block:: python

   >>> dbc.cache.reload_cache()


