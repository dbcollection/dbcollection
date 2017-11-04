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


Accessing the cache
===================

ways of accessing the contents of the cache file

Displaying information about its contents
=========================================

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


