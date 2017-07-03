# dbcollection for Matlab

This is a simple wrapper for the Python's dbcollection module for Matlab. The functionality is almost the same, appart with a few minor differences regarding setting up ranges when fetching data. Internally it uses the Python's dbcollection module for data download/process/management.


## Package installation

## requirements

This package requires:

- dbcollection package installed in Python.
- Matlab >= 2014a
- [JSONlab](https://github.com/fangq/jsonlab)

> Note: The code my work on previous versions of Matlab,
but since it was developed and tested only on Matlab 2014a
I cannot provide any garantees concerning older version.


### Installation

To install this package, add APIS/matlab/ to the Matlab path.

Also, this package requires the [JSONlab](https://github.com/fangq/jsonlab) json encoder/decoder to work. To install this package just download the repo to disk

```
git clone https://github.com/fangq/jsonlab
```

and add it to Matlab's path:

```
addpath('/path/to/jsonlab');
```


## Usage

**TODO**


## Documentation

**TODO**


## License

MIT license (see the LICENSE file in the root dir)