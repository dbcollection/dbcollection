.. dbcollection documentation master file, created by
   sphinx-quickstart on Mon Mar 13 17:41:01 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to dbcollection's documentation!
========================================

``dbcollection`` is a library for downloading/parsing/managing datasets via very simple commands.
It was built from the ground up to be cross-platform (Windows, Linux, MacOS) and
cross-language (Python, Lua, Matlab, etc.) This is achieved by using the popular ``HDF5`` file format
to store (meta)data of the parsed datasets and Python for scripting. By doing so, this library can target
any platform that supports Python and any language that has biddings for HDF5.


This library contains a (growing) list of popular datasets in computer science for many fields like object detection,
classification, human body joint detection, captioning, etc. This provides a great way to quickly start hacking on
a number of different tasks by skipping the boring task of learning and setting/parsing datasets (and pray for the data
provided by the original creators to be clean!).

Also, since it has been developed with community in mind,
this encourages the users to write and share their scripts for downloading/parsing other datasets with the community.


The code is open source (MIT license) and is available on `Github <https://github.com/farrajota/dbcollection/>`_.


Contents:
---------

.. toctree::
   :maxdepth: 1

   intro
   install
   tutorial/index
   reference/index
   datasets/index
   contributing
   license

