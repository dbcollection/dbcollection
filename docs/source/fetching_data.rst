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

This Chapter deals with retrieving data from a dataset. In the following sections, we'll address how data is structured and how to fetch (and parse) data samples from a dataset. Also, best practices in retrieving data using this package are detailed at the end of this page. 


Data structure of HDF5 files
============================


How to retrieve data 
====================


object_id 
---------

object_fields
-------------


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



