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

- Simple API to load/download/setup/manage datasets.
- Simple API to fetch data from a dataset.
- Store and pull data from disk or from memory, you choose!
- Datasets only need to be set/processed once, so next time you use it it will load instantly!
- Cross-platform (**Windows**, **Linux**, **MacOs**).
- Cross-language (**Python**, **Lua/Torch7**, **Matlab**).
- Easily extensible to other languages that support `HDF5` files format.
- Concurrent/parallel data access thanks to `HDF5`.
- Contains a diverse (and growing!) list of popular datasets for machine-, deep-learning tasks (*object detection*, *action recognition*, *human pose estimation*, etc.)


Contents:
=========

.. toctree::
   :maxdepth: 1
   :caption: Introduction

   about

.. toctree::
   :maxdepth: 1
   :caption: User guide

   install
   getting_started
   managing_datasets
   fetching_data
   cache_management

.. toctree::
   :maxdepth: 1
   :caption: Developer guide

   create_new_dataset

.. toctree::
   :maxdepth: 1
   :caption: Reference manual

   reference/core
   reference/datasets
   reference/utils
   available_datasets

.. toctree::
   :maxdepth: 1
   :caption: Contributing

   contributing/how_to_contribute
   contributing/submitting_bugs
   contributing/feedback_channels
   contributing/code_organization
   contributing/coding_guidelines
   contributing/testing_guidelines

.. toctree::
   :maxdepth: 1
   :caption: Other information

   license

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
