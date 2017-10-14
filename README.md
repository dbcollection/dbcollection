# dbcollection

[![Build Status](https://travis-ci.org/dbcollection/dbcollection.svg?branch=master)](https://travis-ci.org/dbcollection/dbcollection)
[![CircleCI](https://circleci.com/gh/dbcollection/dbcollection/tree/master.svg?style=svg)](https://circleci.com/gh/dbcollection/dbcollection/tree/master)
[![Build status](https://ci.appveyor.com/api/projects/status/85gpibosxhjo8yjl/branch/master?svg=true)](https://ci.appveyor.com/project/farrajota/dbcollection-x3l0d/branch/master)
[![codecov](https://codecov.io/gh/dbcollection/dbcollection/branch/master/graph/badge.svg)](https://codecov.io/gh/dbcollection/dbcollection)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/dbcollection/badge/?version=latest)](http://dbcollection.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/dbcollection.svg)](https://badge.fury.io/py/dbcollection)
[![Anaconda-Server Badge](https://anaconda.org/farrajota/dbcollection/badges/version.svg)](https://anaconda.org/farrajota/dbcollection)


dbcollection is a python module for loading/managing
datasets with a very simple set of commands with
cross-platform and cross-language support in mind and it
is distributed under the MIT license. With this package,
you'll have access (in a quick and simple way) to a
collection of datasets for a variety of tasks such as
object classification, detection, human pose estimation,
captioning or NLP.

This package is available for Windows, Linux and MacOs.

## Supported languages

- Python (>=2.7 or >=3.5)
- Lua/Torch7 ([link](https://github.com/dbcollection/dbcollection-torch7))
- Matlab (>=2014a) ([link](https://github.com/dbcollection/dbcollection-matlab))


## Package installation

### From PyPi

Installing `dbcollection` using pip is simple. For that
purpose, simply do the following command:

```
pip install dbcollection
```

### From Conda

You can also install `dbcollection` via anaconda:

```
conda install -c farrajota dbcollection
```


### From source

To install **dbcollection** from source you need to do
the following setps:

- Clone the repo to your hard drive:

```
git clone --recursive https://github.com/dbcollection/dbcollection
```

- `cd ` to the dbcollection folder and do the command

```
python setup.py install
```

## Getting started

### Basic usage

Using the module is pretty straight-forward. To import it just do:

```python
import dbcollection as dbc
```

To load a dataset, you only need to use a single method that returns a data loader object which can then be used to fetch data from.

```python
>>> mnist = dbc.load('mnist')
```

This data loader object contains information
about the dataset's name, task, data, cache paths, set splits, and some methods for querying and loading data from the `HDF5` metadata file.

For example, if you want to know how the data is structured inside the metadata file, you can simply do the following:

```python
>>> mnist.info()

> Set: test
   - classes,        shape = (10, 2),          dtype = uint8
   - images,         shape = (10000, 28, 28),  dtype = uint8,  (in 'object_ids', position = 0)
   - labels,         shape = (10000,),         dtype = uint8,  (in 'object_ids', position = 1)
   - object_fields,  shape = (2, 7),           dtype = uint8
   - object_ids,     shape = (10000, 2),       dtype = uint8

   (Pre-ordered lists)
   - list_images_per_class,  shape = (10, 1135),  dtype = int32

> Set: train
   - classes,        shape = (10, 2),          dtype = uint8
   - images,         shape = (60000, 28, 28),  dtype = uint8,  (in 'object_ids', position = 0)
   - labels,         shape = (60000,),         dtype = uint8,  (in 'object_ids', position = 1)
   - object_fields,  shape = (2, 7),           dtype = uint8
   - object_ids,     shape = (60000, 2),       dtype = uint8

   (Pre-ordered lists)
   - list_images_per_class,  shape = (10, 6742),  dtype = int32
```

> Note: For a more detailed overview of how to use this
module check the documentation or the available tutorials.


### Notebooks

A more detailed tutorial on using the **dbcollection**
module main APIs for dataset managing and data loading is
provided as a python notebook format [here](todo).


## Documentation

The package documentation is hosted on [Read The Docs](http://dbcollection.readthedocs.io/en/latest/).

The documentation should provide a good starting point for
learning how to use the library.


## Contributing

All contributions, bug reports, bug fixes, documentation
improvements, enhancements and ideas are welcome. If you would like to see additional languages being supported, please consider contributing to the
project.

If you are interested in fixing issues and contributing
directly to the code base, please see the document [How to Contribute](https://github.com/dbcollection/dbcollection/wiki/How-to-Contribute).


## Feedback

For now, use the [Github issues](https://github.com/dbcollection/dbcollection/issues) for requests/bug issues.


## License

Licensed under the [MIT](LICENSE.txt) license.