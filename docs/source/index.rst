.. dbcollection documentation master file, created by
   sphinx-quickstart on Mon Mar 13 17:41:01 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

========================================
Welcome to dbcollection's documentation!
========================================

``dbcollection`` is a library for downloading/parsing/managing datasets via simple methods.
It was built from the ground up to be *cross-platform* (**Windows**, **Linux**, **MacOS**) and
*cross-language* (**Python**, **Lua**, **Matlab**, **etc.**). This is achieved by using the popular ``HDF5`` file format
to store (meta)data of manually parsed datasets and **Python** for scripting. By doing so, this library can target
any platform that supports **Python** and any language that has bindings for ``HDF5``.


This library contains a (growing) list of popular datasets in computer science for many fields like **object detection**,
**classification**, **human body joint detection**, **captioning**, etc. This provides a great way to quickly start hacking on
a number of different tasks by skipping the boring task of learning how to set/parse datasets (and sometimes dealing with wrongly annotated data).


Also, since it has been developed with community in mind,
this should encourage users to write and share their scripts for downloading/parsing other datasets with the community.

The project's code is publicly available on `GitHub <https://github.com/dbcollection/dbcollection>`_
and it is licensed under the :ref:`MIT license <license>`.


Main features
=============

- Simple API to load/download/setup/manage datasets
- Simple API to fetch data of a dataset
- All data is stored in disk, resulting in reduced RAM usage (useful for large datasets)
- Datasets only need to be setup once
- Cross-platform (**Windows**, **Linux**, **MacOs**).
- Cross-language (**Python**, **Lua/Torch7**, **Matlab**).
- Easily extensible to other languages that have support for ``HDF5`` files
- Concurrent/parallel data access is possible thanks to the ``HDF5`` file format
- Diverse list of popular datasets are available for use
- All datasets were manually parsed by someone, meaning that some of the quirks were already solved for you


Contents:
=========

.. toctree::
   :maxdepth: 1

   introduction
   install
   tutorial/index
   reference/index
   available_datasets
   contributing/index
   license

