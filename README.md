# Easily manage your dataset's data

[![Build Status](https://travis-ci.org/farrajota/dbcollection.svg?branch=add_appveyor_support)](https://travis-ci.org/farrajota/dbcollection)
[![CircleCI](https://circleci.com/gh/farrajota/dbcollection/tree/master.svg?style=svg)](https://circleci.com/gh/farrajota/dbcollection/tree/master)
[![Build status](https://ci.appveyor.com/api/projects/status/rwrp7q1j9ytebkps?svg=true)](https://ci.appveyor.com/project/farrajota/dbcollection)
[![codecov](https://codecov.io/gh/farrajota/dbcollection/branch/master/graph/badge.svg)](https://codecov.io/gh/farrajota/dbcollection)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/dbcollection/badge/?version=latest)](http://dbcollection.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/dbcollection.svg)](https://badge.fury.io/py/dbcollection)


dbcollection is a python module for loading/managing datasets with a very simple set of commands with cross-platform and cross-language support in mind and it is distributed under a MIT license.


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
import dbcollection.manager as dbc
```

To load a dataset, you need to use `dbc` API `load()` method.

> Note: by default, the `MNIST` dataset is already included in the package, so loading it does not need to download/setup any data. However, this may not be valid for most datasets.

```python
mnist = dbc.load('mnist')
```

This returns a loader API class which contains information about the dataset's name, task, data and cache paths, sets, the HDF5 file handler and four methods to retrieve data from the file: `get()`, `size()`, `object()` and `list()`.

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


- Python (>=2.7 or >=3.4)
- Lua/[Torch7](https://github.com/torch/torch7)
- Matlab (comming soon)

> Note: If you would like to see additional languages being supported, please consider contributing to the project.


# Documentation

The package documentation is hosted on [Read The Docs](http://dbcollection.readthedocs.io/en/latest/).

The documentation should provide a good starting point for learning how to use the library.


# Contributing

All contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are welcome.

If you are interested in fixing issues and contributing directly to the code base, please see the document [How to Contribute](https://github.com/farrajota/dbcollection/wiki/How-to-Contribute).

# Feedback

For now, use the [Github issues](https://github.com/farrajota/dbcollection/issues) for requests/bug issues.

# License

MIT license (see the `LICENSE` file)