.. _user_cache_management:

======================
Dealing with the cache
======================

This Chapter addresses managing / configurating the ``~/dbcollection.json`` cache file. 

The ``.json`` file located in your home directory is the central registry of **dbcollection**. Here is stored the information about what datasets have been downloaded / parsed, which tasks are listed for use, where is data stored and what categories exist.

It is important to keep this file in your system's home directory because there is where **dbcollection** tried to locate it. If it is not found, an empty one will be generated. 

A situation that might take you to manually configure this cache file, opposed to letting the package do it for you, is when you have moved data around to other paths in your disk and you need to fix this in the cache file. Here we'll see how to deal with this kind of scenarios.

In this Chapter we'll see the most important operations you may want / need to do to configure the cache file in your system. 


Cache's structure
=================

How the data is structured

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


