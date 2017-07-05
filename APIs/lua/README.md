# dbcollection for Torch7

This is a simple Lua wrapper for the Python's dbcollection module. The functionality is almost the same, appart with a few minor differences regarding setting up ranges when fetching data. Internally it uses the Python's dbcollection module for data download/process/management.

# Package installation

## requirements

This package requires:

- Python's dbcollection package installed.
- [Torch7](https://github.com/torch/torch7)
- json
- argcheck

To install Torch7 just follow the steps listed [here](http://torch.ch/docs/getting-started.html#_).

The other packages should come pre-installed along with Torch7, but in case they don't, you can simply install them by doing the following:

```lua
luarocks install json
luarocks install argcheck
```

## installation

To install the Lua/Torch7 dbcollection package, first the Python's version must be installed on your system. If you do not have it installed, then follow the next steps to get it installed on your system:

- step 1: download the git repository to disk.
```
git clone https://github.com/farrajota/dbcollection
```

- step 2: install the Python module.
```
cd dbcollection/ && python setup.py install
```

- step 3: install the Lua package.
```
cd APIs/lua && luarocks make
```

# Usage

This package follows the same API as the Python version. Once installed, to use the package simply require *dbcollection*:
```lua
local dbc = require 'dbcollection.manager'
```

Then, just like with the Python's version, to load a dataset you simply do:
```lua
local mnist = dbc.load{name='mnist'}
```

You can also select a specific task for any dataset by using the `task` option.
```lua
local mnist = dbc.load{name='mnist', task='classification'}
```

This API lets you download+extract most dataset's data directly from its source to the disk. For that, simply use the `download()` method:
```lua
dbc.download{name='cifar10', data_dir='home/some/dir'}
```

## Data fetching

Once a dataset has been loaded, in order to retrieve data you can either use Torch7's `HDF5` API or use the provided methods to retrive data from the .h5 metadata file.

For example, to retrieve an image and its label from the `MNIST` dataset using the Torch7's `HDF5` API you can do the following:
```lua
local images_ptr = mnist.file:read('default/train/images')
local img = images_tr:partial({1,1}, {1,32}, {1,32}, {1,3})

local labels_ptr = mnist.file:read('default/train/labels')
local label = labels_ptr:partial({1,1})
```

or you can use the API provided by this package:
```lua
local img = mnist:get('train', 'images', 1)
local label = mnist:get('train', 'labels', 1)
```


# Documentation

For a more detailed view of the Lua's API documentation see [here](DOCUMENTATION.md#db.documentation).


# License

MIT license (see the LICENSE file in the root dir)