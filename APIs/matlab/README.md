# dbcollection for Matlab

This is a simple wrapper for the Python's dbcollection module for Matlab. The functionality is almost the same, appart with a few minor differences regarding setting up ranges when fetching data. Internally it uses the Python's dbcollection module for data download/process/management.


## Package installation

## requirements

This package requires:

- dbcollection (Python).
- Matlab >= 2014a
- [JSONlab](https://github.com/fangq/jsonlab)

> Note: The code my work on previous versions of Matlab,
but since it was developed and tested only on Matlab 2014a
I cannot provide any garantees concerning older version.


### Installation

To install the dbcollection's Matlab API, first the Python's version must be installed on your system. If you do not have it installed, then follow the next steps to get it installed on your system:

- step 1: install the package via pip

```
pip install dbcollection
```

- step 2: download the git repository to disk.

```
git clone https://github.com/farrajota/dbcollection
```

- step 3: add the `dbcollection/APIs/matlab/` to your Matlab path.

```
addpath('<path>/dbcollection/APIs/matlab/');
```


Also, this package requires the [JSONlab](https://github.com/fangq/jsonlab) json encoder/decoder to work. To install this package just download the repo to disk

```
git clone https://github.com/fangq/jsonlab
```

and add it to Matlab path:

```
addpath('/path/to/jsonlab');
```


## Getting started

### Usage

This package follows the same API as the Python version. Once installed, to use the package simply call the class *dbcollection*:

```matlab
dbc = dbcollection();
```

Then, just like in Python, to load a dataset you simply do:

```matlab
mnist = dbc.load('mnist');
```

You can also select a specific task for any dataset by using the `task` option.

```matlab
mnist = dbc.load(struct('name', 'mnist', 'task', 'classification'));
```

This API lets you download+extract most dataset's data directly from its source to the disk. For that, you can use the `download()` method to fetch data online from the dataset's source repository:

```matlab
dbc.download(struct('name', 'cifar10', 'data_dir', 'some/dir/path'));
```

### Data fetching

Once a dataset has been loaded, in order to retrieve data
you can either use Matlab's `HDF5` API or use the provided
methods to retrive data from the .h5 metadata file.

For example, to retrieve an image and its label from the `MNIST` dataset using the Matlab's `HDF5` API you can do the following:

```matlab
imgs = h5read(mnist.cache_path, 'default/train/images');  % fetch data
imgs = permute(imgs, ndims(imgs):-1:1);  % permute dimensions to the original format
img = imgs(1,:,:,:);  % slice array

labels = h5read(mnist.cache_path, 'default/train/labels');  % fetch data
labels = permute(labels, ndims(labels):-1:1);  % permute dimensions to the original format
label = labels(1,:);  % slice array
```

or you can use the API provided by this package:

```matlab
img = mnist.get('train', 'images', 1)
label = mnist.get('train', 'labels', 1)
```


## Documentation

For a more detailed view of the Matlab's API documentation see [here](DOCUMENTATION.md#db.documentation).


## License

MIT license (see the LICENSE file in the root dir)