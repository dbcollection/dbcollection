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





Basic operations
================

Getting information about a dataset 
-----------------------------------

Adding datasets
---------------

Adding tasks
------------

Removing datasets
-----------------

Adding tasks
------------

Modifying data
--------------

Reset the cache
---------------

Check if a dataset exists
-------------------------

Check if a task exists
----------------------



Other useful operations
=======================

Change the default metadata cache directory
-------------------------------------------

reset to the default value

Change the default download directory path
------------------------------------------

reset to the default value

Reloading the cache
-------------------

Reload the cache


