# dbcollection: Easily manage your datasets

dbcollection is a python module for loading/managing datasets with a very simple set of commands with cross-platform and cross-language support in mind and it is distributed under a MIT license.

# ***WARNING***

This code is under refactoring, so some links/features may not be working properly. This should be cleared soon.


## Why does this project exist

From personal experience, working with different datasets under different systems/languages ultimately results in boilerplate code, long preprocessing/initialization times and its often leads to non-reusable code.

## What problems does it solve

This project tries to tackle some of the problems that I have been facing:

- increase code reusage when switching between systems (Windows, Linux)
- easily write scripts to download/process datasets.
- setup the datasets once, avoiding repetitive preprocessing steps when starting my code
- work with multiple languages (Python/Lua/Matlab/etc.).
- have a common framework for building up a list of available datasets for use.

## How does it work

This module uses python for writting scripts for data download and metadata processing. The reason for using python was simple: it provides a simple, easy, fast and portable format to write code and it is considered the "lingua franca" in computer science.

The processed metadata is stored to disk by using the HDF5 file format. This format provides some key features:

- portable across languages and operating systems;
- fast access to data;
- easy to use;
- allows concurrent reads of the same file;
- data can be stored in a nested way (like a folder tree)

Also, by using the HDF5 format, it is simple to deploy a common API to interface with the stored metadata and other languages that have HDF5 support. For more information about the HDF5 file format see [here](https://support.hdfgroup.org/HDF5/).

The **dbcollection** manager API creates a folder in your home dir named `~/dbcollection` where all the metadata files and grouped. The contents of this folder is tracked by a .json cache file which is stored in your home dir named `~/dbcollection.json` which contains information/configurations of the stored datasets.

## Main features

- cross-platform (Windows, Linux, MacOs).
- cross-language (python, lua/torch7, matlab).
- simple API for dataset load/setup/management.
- setup the data only once.
- avoids RAM memory usage by storing/loading all metadata on/from disk.
- concurrent/parallel data access.
- increasing list of available datasets.
- simplified user experience by providing data management (download + processing) for many popular datasets in computer vision.

# Package installation

## From PyPi

Simple do the following command to install this package:
```
pip install dbcollection
```

## From source

To install **dbcollection** from source you need to do the following setps:

- Clone the repo to your hard drive:
```
git clone https://github.com/farrajota/dbcollection
```
- `cd ` to the dbcollection folder and do the command
```
python setup.py install
```

# Usage

Using the module is pretty straight-forward. To import it just do:

```python
import dbcollection as dbc
```

To load a dataset, you need to use `dbc.manager` API `load()` method. 

> Note: by default, the `MNIST` dataset is already included in the package, so loading it does not need to download/setup any data. However, this may not be valid for most datasets.

```python
mnist = dbc.manager.load('mnist')
```

This returns a loader API class which contains information about the dataset's name, task, data and cache paths, sets, the HDF5 file handler and four methods to retrieve data from the HDF5 file: `get()`, `size()`, `object()` and `list()`.

Finally, to retrieve data from the `MNIST` data loader and display it you can do the following:

```python
# display mnist's data info
print('######### info #########\n')
print('Dataset: ' + mnist.name)
print('Task: ' + mnist.task)
print('Data path: ' + mnist.data_dir)
print('Metadata cache path: ' + mnist.cache_path)
print('Sets: ', mnist.sets)

# plot the first data sample from the train set
import matplotlib.pyplot as plt
plt.imshow(mnist.get("train", "data", 0))
plt.show()
```

> Note: For a more detailed overview of how to use this module check the next section.

## Tutorial

A more detailed tutorial on using the **dbcollection** module main APIs for dataset managing and data loading is provided as a python notebook format [here](todo).


# Supported languages

For now, these are currently the supported languages by this package:
- Python (>=2.7 or >=3.4)
- Lua/[Torch7](https://github.com/torch/torch7)
- Matlab (comming soon)

If you would like to see some language being supported, please consider contributing to this project.

# Contributing

To contribute to dbcollection, please check the contibution page. .... TODO link

# Available datasets

For a detailed list of all available datasets please check [this link](). .... TODO link

# Documentation

See the [docs](todo) for more information. .... TODO link


# License

MIT license (see the LICENSE file)