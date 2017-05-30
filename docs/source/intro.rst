.. _introduction:

Introduction
=============

What it is
----------

TODO


Why does this project exist
---------------------------

From personal experience, working with different datasets under different systems/languages ultimately results in boilerplate code, long preprocessing/initialization times and its often leads to non-reusable code.


What problems does it solve
---------------------------

This project tries to tackle some of the problems that I have been facing:

- increase code reusage when switching between systems (Windows, Linux)
- easily write scripts to download/process datasets.
- setup the datasets once, avoiding repetitive preprocessing steps when starting my code
- work with multiple languages (Python/Lua/Matlab/etc.).
- have a common framework for building up a list of available datasets for use.


How does it work
----------------

This module uses python for writting scripts for data download and metadata processing. The reason for using python was simple: it provides a simple, easy, fast and portable format to write code and it is considered the "lingua franca" in computer science.

The processed metadata is stored to disk by using the HDF5 file format. This format provides some key features:

- portable across languages and operating systems;
- fast access to data;
- easy to use;
- allows concurrent reads of the same file;
- data can be stored in a nested way (like a folder tree)

Also, by using the HDF5 format, it is simple to deploy a common API to interface with the stored metadata and other languages that have HDF5 support. For more information about the HDF5 file format see [here](https://support.hdfgroup.org/HDF5/).

The **dbcollection** manager API creates a folder in your home dir named `~/dbcollection` where all the metadata files and grouped. The contents of this folder is tracked by a .json cache file which is stored in your home dir named `~/dbcollection.json` which contains information/configurations of the stored datasets.


Main features
-------------

- cross-platform (Windows, Linux, MacOs).
- cross-language (python, lua/torch7, matlab).
- simple API to load/download/setup/manage datasets
- simple API to fetch (meta)data of a dataset
- datasets only need to be set once
- all data is stored on disk, therefore the impact on RAM is reduced (handy for large datasets)
- desined with concurrent/parallel data access in mind
- a diverse (and growing) list of popular datasets are available to the end user
- allows the user to focus on more important tasks on their research instead of managing datasets (it always takes alot more time than expected, trust me!)


Roadmap
-------

TODO
