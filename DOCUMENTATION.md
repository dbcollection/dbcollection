<a name="db.documentation"></a>
# Python API documentation

This section covers the main API methods for dataset managing/data fetching for the Python's dbcollection package.

The dbcollection package is composed by three main groups:

- [dbcollection](#db): dataset manager API.
    - [load](#db.load): load a dataset.
    - [download](#db.download): download a dataset data to disk.
    - [process](#db.process): process a dataset's metadata and stores it to file.
    - [add](#db.add): add a dataset/task to the list of available datasets for loading.
    - [remove](#db.remove): remove/delete a dataset from the cache.
    - [config_cache](#db.config_cache): configure the cache file.
    - [query](#db.query): do simple queries to the cache.
    - [info](#db.info): prints the cache contents.
- [dbcollection.utils](#db.utils): utility functions.
    - [string_ascii](#db.utils.string_ascii): module containing methods for converting [strings to tensors](#db.utils.string_ascii.convert_string_to_ascii) and [tensors to strings](#db.utils.string_ascii.convert_ascii_to_string).
    - [pad](#db.utils.pad): methods for [padding](#db.utils.pad.pad_list) and/or [unpadding](#db.utils.pad.unpad_list) lists.

The [data loading API](#db.loader) contains a few methods for data retrieval/probing:

- [get](#db.loader.get): retrieve data from the dataset's hdf5 metadata file.
- [object](#db.loader.object): retrieves a list of all fields' indexes/values of an object composition.
- [size](#db.loader.size): size of a field.
- [list](#db.loader.list): lists all fields' names.
- [object_fields_id](#db.loader.object_field_id): retrieves the index position of a field in the `object_ids` list.


<a name="db"></a>
## dbcollection

This module is the main module for easily managing/loading/processing datasets for the `dbcollection` package.
The dataset managing API is composed by the following methods. The (recommended) use of the package is as follows:

```python
import dbcollection as dbc
```

The library is structured as a table. In this documentation we use the above convention to import the module and to call its methods (similar to the other APIs).


<a name="db.load"></a>
### load

```python
loader = dbc.load(name, task, data_dir, verbose, is_test)
```

Returns a loader instant of a `DatasetLoader` class with methods to retrieve/probe data and other informations from the selected dataset.

#### Parameters

- `name`: Name of the dataset. (*type=string*)
- `task`: Name of the task to load. (*type=string, default='default'*)
- `data_dir`: Directory path to store the downloaded data. (*type=string, default=''*)
- `verbose`: Displays text information (if True). (*type=boolean, default=True*)
- `is_test`: Flag used for tests. (*type=boolean, default=False*)


#### Usage examples

You can simply load a dataset by its name like in the following example.

```python
mnist = dbc.load('mnist')
```

In cases where you don't have the dataset's data on disk yet (and the selected dataset can be downloaded by the API), you can specify which directory the dataset's data files should be stored to and which task should be loaded for this dataset.

```python
cifar10 = dbc.load(name='cifar10',
                   task='classification',
                   data_dir='<my_home>/datasets/')
```

> Note: If you don't specify the directory path where to store the data files, then the files will be stored in the `dbcollection/<dataset>/data` dir where the metadata files are located.


<a name="db.download"></a>
### download

```python
dbc.download(name, data_dir, extract_data, verbose, is_test)
```

This method will download a dataset's data files to disk. After download, it updates the cache file with the dataset's name and path where the data is stored.

#### Parameters

- `name`: Name of the dataset. (*type=string*)
- `data_dir`: Directory path to store the downloaded data. (*type=string, default='default'*)
- `extract_data`: Extracts/unpacks the data files (if True). (*type=boolean, default=True*)
- `verbose`: Displays text information (if True). (*type=boolean, default=True*)
- `is_test`: Flag used for tests. (*type=boolean, default=False*)

#### Usage examples

A simple usage example for downloading a dataset (without providing a storage path for the data) requires only the name of the target dataset and it will download its data files and then extract them to disk without any supervision required.

```python
dbc.download('cifar10')
```

It is good practice to specify where the data will be download to by providing a existing directory path to `data_dir`. (This information is stored in the `dbcollection.json` file stored in your home path.)

```python
dbc.download(name='cifar10', data_dir='<some_dir>')
```

In cases where you only want to download the dataset's files without extracting its contents, you can set `extract_data=False` and skip the data extraction/unpacking step.

```python
dbc.download(name='cifar10',
             data_dir='<some_dir>',
             extract_data=False)
```

> Note: this package uses a text progressbar when downloading files from urls for visual purposes (file size, elapsed time, % download, etc.). To disable this feature, set `verbose=False`.


<a name="db.process"></a>
### process

```python
dbc.process(name, task, verbose, is_test)
```

Processes a dataset's metadata and stores it to file. This metadata is stored in a HDF5 file for each task composing the dataset's tasks. For more information about a dataset's metadata format please check the list of available datasets in the [docs](http://dbcollection.readthedocs.io/en/latest/available_datasets.html).

#### Parameters

- `name`: Name of the dataset. (*type=string*)
- `task`: Name of the task to process. (*type=string, default='all'*)
- `verbose`: Displays text information (if True). (*type=boolean, default=True*)
- `is_test`: Flag used for tests. (*type=boolean, default=False*)

#### Usage examples

To process (or reprocess) a dataset's metadata simply do:

```python
dbc.process('cifar10')
```

This will process all tasks for a given dataset (default='all'). To process only a specific task, you need to specify the task name you want to setup. This is handy when one wants to process only a single task of a bunch of tasks and speed up the processing/loading stage.

```python
dbc.process(name='cifar10', task='default')  # process only the 'default' task
```

> Note: this method allows the user to reset a dataset's metadata file content in case of manual or accidental changes to the structure of the data. Most users won't have the need for such functionality on their basic usage of this package.

<a name="db.add"></a>
### add

```python
dbc.add(name, task, data_dir, file_path, keywords, verbose, is_test)
```

This method provides an easy way to add a custom dataset/task to the `dbcollection.json` cache file without having to manually add them themselves (although it is super easy to do it and recommended!).

#### Parameters

- `name`: Name of the dataset. (*type=string*)
- `task`: Name of the task to load. (*type=string*)
- `data_dir`: Path of the stored data on disk. (*type=string*)
- `file_path`: Path to the metadata HDF5 file. *(type=string*)
- `keywords`: List of strings of keywords that categorize the dataset. (*type=list, default=[]*)
- `is_test`: Flag used for tests. (*type=boolean, default=False*)

#### Usage examples

Adding a custom dataset or a custom task to a dataset requires the user to introduce the dataset's `name`, `task` name, `data_dir` where the data files are stored and the metadata's `file_path` on disk.

```python
dbc.add(name='custom1',
        task='default',
        data_dir='<data_dir>',
        file_path='<metadata_file_path>')
```

> Note: In cases where no external files are required besides the metadata's data, you can set `data_dir`="".


<a name="db.remove"></a>
### remove

```python
dbc.remove(name, task, data_dir, verbose, is_test)
```

This method allows for a dataset to be removed from the list of available datasets for load in the cache. It also allows for the user to delete the dataset's files on disk if desired.

#### Parameters

- `name`: Name of the dataset. (*type=string*)
- `task`: Name of the task to delete. (*type=string, default='None'*)
- `delete_data`: Delete all data files from disk for this dataset if True. (*type=boolean, default=False*)
- `is_test`: Flag used for tests. (*type=boolean, default=False*)

#### Usage examples

To remove a dataset simply do:

```python
dbc.remove('cifar10')
```

If you want to remove the dataset completely from disk, you can set the `delete_data` parameter to `True`.

```python
dbc.remove(name='cifar10', delete_data=True)
```


<a name="db.config_cache"></a>
### config_cache

```python
dbc.config_cache(field, value, delete_cache, delete_cache_dir, delete_cache_file, reset_cache, is_test)
```

Configures the cache file via API. This method allows to configure the cache file directly by selecting any data field and (re)setting its value. The user can also manually configure the `dbcollection.json` cache file in the filesystem (recommended).

To modify any entry in the cache file, simply input the field name you want to change along with the new data you want to insert. This applies to any existing field.

Another available function is the reset/wipe the entire cache paths/configs from the file. To perform this action set the `reset_cache` input arg to `True`.

Also, there is an option to completely remove the cache file+folder from the disk by enabling `delete_cache` to `True`. This will remove the cache file `dbcollection.json` and the `dbcollection/` folder from disk.

> Warning: Misusing this API method may result in tears. Proceed with caution.

#### Parameters

- `field`: Name of the field to update/modify in the cache file. (*type=string, default=None*)
- `value`: Value to update the field. (*type=string, default=None*)
- `delete_cache`: Delete/remove the dbcollection cache file + directory. (*type=boolean, default=False*)
- `delete_cache_dir`: Delete/remove the dbcollection cache directory. (*type=boolean, default=False*)
- `delete_cache_file`: Delete/remove the dbcollection.json cache file. (*type=boolean, default=False*)
- `reset_cache`: Reset the cache file. (*type=boolean, default=False*)
- `is_test`: Flag used for tests. (*type=boolean, default=False*)

#### Usage examples

For example, Lets change the directory where the dbcollection's metadata main folder is stored on disk. This is useful to store/move all the metadata files to another disk.

```python
dbc.config_cache(field='default_cache_dir',
                 value='<home_dir>/new/path/db/')
```

If a user wants to remove all files relating to the `dbcollection` package, one can use the `config_cache` to accomplish this in a simple way:

```python
dbc.config_cache(delete_cache=True)
```

or if the user wants to remove only the cache file:

```python
dbc.config_cache(delete_cache_file=True)
```

or to remove the cache directory where all the metadata files from all datasets are stored (**I hope you are sure about this one...**):

```python
dbc.config_cache(delete_cache_dir=True)
```

or to simply reset the cache file contents withouth removing the file:

```python
dbc.config_cache(reset_cache=True)
```

<a name="db.query"></a>
### query

```python
dbc.query(pattern, is_test)
```

Do simple queries to the cache and displays them to the screen.

#### Parameters

- `pattern`: Field name used to search for a matching pattern in cache data. (*type=string, default='info'*)
- `is_test`: Flag used for tests. (*type=boolean, default=False*)

#### Usage examples

Simple query about the existence of a dataset.

```python
dbc.query('mnist')
```

It can also retrieve information by category/keyword. For example, this is useful to see which datasets have the same task.

```python
dbc.query('detection')
```

> Note: this is the same as scanning the `dbcollection.json` cache file yourself, but it has the advantage of grouping information about a certain pattern for you.


<a name="db.info"></a>
### info

```python
dbc.info(name, paths_info, datasets_info, categories_info, is_test)
```

Prints the cache contents to screen. It can also print a list of all available datasets to download/process in the `dbcollection` package.

#### Parameters

- `name`: Name of the dataset to display information. (*type=string, default=None*)
- `paths_info`: Print the paths info to screen. (*type=boolean, default=True*)
- `datasets_info`: Print the datasets info to screen. If a string is provided, it selects only the information of that string (dataset name). (*type=boolean/string, default=True*)
- `categories_info`: Print the paths info to screen. If a string is provided, it selects only the information of that string (dataset name). (*type=boolean/string, default=True*)
- `is_test`: Flag used for tests. (*type=boolean, default=False*)


#### Usage examples

Print the cache file contents to the screen:

```python
dbc.info()
```

Display all available datasets to download/process:

```python
dbc.info('all')
```

> TODO: Add more examples for the other options

<a name="db.loader"></a>
## Data loading API

The data loading API is class composed by some fields containing information about the dataset and some methods to retrieve data.

Loading a dataset using [dbcollection.load()](#db.load) returns an instantiation of the `DatasetLoader` class. It contains information about the selected dataset (name, task, set splits, directory of the data files stored in disk, etc.) and methods to easily extract data from the metadata file.

The information of the dataset is stored as attributes of the class:

- `name`: Name of the selected dataset. (*type=string*)
- `task`: Name of the selected task. (*type=string*)
- `data_dir`: Directory path where the data files are stored. (*type=string*)
- `cache_path`: Path where the metadata file is located. (*type=string*)
- `file`: The HDF5 file handler of the dataset's metadata. (*type=hdf5.HDF5File*)
- `root_path`: HDF5 root group/path which the methods retrieve data from. (*type = string, default='default/'*)
- `sets`: A list of available sets for the selected dataset (e.g., train/val/test/etc.). (*type=list*)
- `object_fields`: A list of all field names available for each set of the dataset. (*type=list*)

> Note: The list of available `sets` (set splits) and `object_fields` (available field names) varies from dataset to dataset.


<a name="db.loader.get"></a>
### get

```python
data = loader.get(set_name, field_name, idx)
```

Retrieves data from a dataset's HDF5 metadata file. This method accesses the HDF5 metadata file and searches for a field `field_name` in the selected group `set_name`. If an index or list of indexes are input, the method returns a slice (rows) of the data's tensor. If no index is set, it return the entire data tensor.

#### Parameters

- `set_name`: Name of the set. (*type=string*)
- `field_name`: Name of the data field. (*type=string*)
- `idx`:  Index number of the field. If the input is a list, it uses it as a range of indexes and returns the data for that range. (*type=number or list*)

#### Usage examples

The first, and most common, usage of this method if to retrieve a single piece of data from a data field. Lets retrieve the first image+label from the `MNIST` dataset.

```python
>>> mnist = dbc.load('mnist')  # returns a DatasetLoader class
>>> img = mnist.get('train', 'images', 0)
>>> label = mnist.get('train', 'labels', 0)
>>> print(img.shape)
(28, 28)
>>> print(label)
5
```

This method can also be used to retrieve a range of data/values.

```python
>>> imgs = mnist.get('train', 'images', list(range(20)))
>>> print(imgs.shape)
(20, 28, 28)
```

Or all values if desired.

```python
>>> imgs = mnist.get('train', 'images')
>>> print(imgs.shape)
(60000, 28, 28)
```


<a name="db.loader.object"></a>
### object

```python
indexes = loader.object(set_name, idx, is_value)
```

Retrieves a list of all fields' indexes/values of an object composition. If `is_value=True`, instead of returning a tensor containing the object's fields indexes, it returns a list of tensors for each field.

This method is particularly useful when different fields are linked (like in detection tasks with labeled data) and their contents can be quickly accessed and retrieved in one swoop.

#### Parameters

- `set_name`: Name of the set. (*type=string*)
- `idx`:  Index number of the field. If it is a list, returns the data for all the value indexes of that list. If the list is empty, it returns all the values of the field.  (ty*pe=number or list*)
- `is_value`: Outputs a tensor of indexes (if false) or a list of tensors/values (if True). (*type=boolean, default=false*)

#### Usage examples

Fetch all indexes of an object.

```python
>>> mnist = dbc.load('mnist')
>>> obj_idx = mnist.object('train', 0)
>>> obj_idx
array([0, 5], dtype=int32)
```

Multiple lists can be retrieved just like with the [get()](#db.loader.get) method.

```python
>>> obj_idx = mnist.object('train', list(range(10)))
>>> obj_idx
array([[0, 5],
       [1, 0],
       [2, 4],
       [3, 1],
       [4, 9],
       [5, 2],
       [6, 1],
       [7, 3],
       [8, 1],
       [9, 4]], dtype=int32)
```

It is also possible to retrieve the values/tensors instead of the indexes.

```python
>>> obj_data = mnist.object('train', 0, True)
>>> obj_data[0].shape  # image data
(28, 28)
>>> obj_data[1]  # label
1
```


<a name="db.loader.size"></a>
### size

```python
size = loader.size(set_name, field_name)
```

Returns the size of a field.

#### Parameters

- `set_name`: Name of the set. (*type=string*)
- `field_name`: Name of the data field. (*type=string*)

> Note: if `field_name` is not provided, it uses the `object_ids` field instead.

#### Usage examples

Get the size of the images tensor in `MNIST` train set.

```python
>>> mnist = dbc.load('mnist')
>>> mnist.size('train', 'images')
[60000, 28, 28]
```

Get the size of the objects in `MNIST` train set.

```python
>>> mnist.size('train', 'object_ids')
[60000, 2]
# or
>>> mnist.size('train')  # defaults to 'object_ids'
[60000, 2]
```


<a name="db.loader.list"></a>
### list

```python
fields = loader.list(set_name)
```

Lists all field names in a set.

#### Parameters

- `set_name`: Name of the set. (*type=string*)

#### Usage examples

Get all fields available in the `MNIST` test set.

```python
>>> mnist = dbc.load('mnist')
>>> mnist.list('test')
['classes', 'labels', 'object_fields', 'images', 'object_ids', 'list_images_per_class']
```


<a name="db.loader.info"></a>
### info

```python
loader.info(set_name)
```

Prints information about the data fields of a set.

Displays information of all fields available like field name, size and shape of all sets. If a `set_name` is provided, it displays only the information for that specific set.

#### Parameters

- `set_name`: Name of the set. (*type=string*)


#### Usage examples

Display all field information for the `MNIST` dataset.

```python
>>> mnist = dbc.load('mnist')
>>> mnist.info()

> Set: test
   - classes,        shape = (10, 2),          dtype = uint8
   - images,         shape = (10000, 28, 28),  dtype = uint8,  (in 'object_ids', position = 0)
   - labels,         shape = (10000,),         dtype = uint8,  (in 'object_ids', position = 1)
   - object_fields,  shape = (2, 7),           dtype = uint8
   - object_ids,     shape = (10000, 2),       dtype = int32

   (Pre-ordered lists)
   - list_images_per_class,  shape = (10, 1135),  dtype = int32

> Set: train
   - classes,        shape = (10, 2),          dtype = uint8
   - images,         shape = (60000, 28, 28),  dtype = uint8,  (in 'object_ids', position = 0)
   - labels,         shape = (60000,),         dtype = uint8,  (in 'object_ids', position = 1)
   - object_fields,  shape = (2, 7),           dtype = uint8
   - object_ids,     shape = (60000, 2),       dtype = int32

   (Pre-ordered lists)
   - list_images_per_class,  shape = (10, 6742),  dtype = int32
```

List only the information of the `MNIST` train set.

```python
>>> mnist.info('train')

> Set: train
   - classes,        shape = (10, 2),          dtype = uint8
   - images,         shape = (60000, 28, 28),  dtype = uint8,  (in 'object_ids', position = 0)
   - labels,         shape = (60000,),         dtype = uint8,  (in 'object_ids', position = 1)
   - object_fields,  shape = (2, 7),           dtype = uint8
   - object_ids,     shape = (60000, 2),       dtype = int32

   (Pre-ordered lists)
   - list_images_per_class,  shape = (10, 6742),  dtype = int32

```


<a name="db.loader.object_field_id"></a>
### object_field_id

```python
position = loader.object_field_id(set_name, field_name)
```

Retrieves the index position of a field in the `object_ids` list. This position points to the field name stored in the `object_fields` attribute.

#### Parameters

- `set_name`: Name of the set. (*type=string*)
- `field_name`: Name of the data field. (*type=string*)

#### Usage examples

This example shows how to use this method in order to retrieve the correct fields from an object index list.

```python
>>> mnist = dbc.load('mnist')
>>> print('object field idx (image): ', mnist.object_field_id('train', 'images'))
object field idx (image):  0
>>> print('object field idx (label): ', mnist.object_field_id('train', 'labels'))
object field idx (label):  1
>>> mnist.object_fields['train']  # fields list (should match the position)
['images', 'labels']
```


<a name="db.utils"></a>
## Utils

This module contains some useful utility functions available to the user.

It is composed by the following modules:

- [dbcollection.utils.string_ascii](#db.utils.string_ascii)


<a name="db.utils.string_ascii"></a>
### dbcollection.utils.string_ascii

This module contains methods to convert strings to ascii and vice-versa. These are useful when recovering strings from the metadata file that are encoded as `numpy.uint8`  (this is due to a limitation in the `HDF5` implementation on torch7 which only supports tensors).

Although one might only need to convert `numpy.uint8` to strings, this module contains both methods for ascii-to-string and string-to-ascii convertion.


<a name="db.utils.string_ascii.convert_string_to_ascii"></a>
### convert_string_to_ascii

```python
tensor = dbc.utils.string_ascii.convert_string_to_ascii(input)
```

Convert a string or list of string to a `numpy.uint8`.

#### Parameters

- `input`: String or a list of strings. (*type=string or list*)

#### Usage examples

Convert a string to ASCII as a `numpy` array.

```python
>>> from dbcollection.utils.string_ascii import convert_str_to_ascii
>>> convert_str_to_ascii('string1')
array([115, 116, 114, 105, 110, 103,  49,   0], dtype=uint8)
```

Convert a list of strings to ASCII as a `numpy` array.

```python
>>> from dbcollection.utils.string_ascii import convert_str_to_ascii
>>> convert_str_to_ascii(['string1', 'string2', 'string3'])
array([[115, 116, 114, 105, 110, 103,  49,   0],
       [115, 116, 114, 105, 110, 103,  50,   0],
       [115, 116, 114, 105, 110, 103,  51,   0]], dtype=uint8)
```


<a name="db.utils.string_ascii.convert_ascii_to_string"></a>
### convert_ascii_to_string

```python
string = dbc.utils.string_ascii.convert_ascii_to_string(input)
```

Convert a `numpy.uint8` to a list of strings.

#### Parameters

- `input`: 2D torch tensor. (*type=numpy.uint8*)

#### Usage examples

Convert a `numpy` array to string.

```python
>>> from dbcollection.utils.string_ascii import convert_ascii_to_str
>>> import numpy as np
>>> tensor = np.array([[115, 116, 114, 105, 110, 103, 49, 0]], dtype=np.uint8)  # ascii format of 'string1'
>>> convert_ascii_to_str(tensor)
['string1']
```


<a name="db.utils.pad"></a>
### dbcollection.utils.pad

This module contains methods for padding and/or unpadding python lists.

The padding methods pad uneven lists of lists with an input value in order to have all lists with the same length. This methods are used mainly when storing data to the HDF5 files.

The unpadding method removes a (padding) value from a list of lists, keeping the remaining data. It is useful when retrieving data from the HDF5 file that has been previously padded.

<a name="db.utils.pad.pad_list"></a>
### pad_list

```python
tensor = dbc.utils.pad.pad_list(listA, val)
```

Pad list of lists with 'val' such that all lists have the same length.

#### Parameters

- `listA`: List of lists of different sizes. (*type=list*)
- `val`: Value to pad the lists. (*type=number, default=-1*)

#### Usage examples

Pad an uneven list of lists with a value.

```python
>>> from dbcollection.utils.pad import pad_list
>>> pad_list([[0, 1, 2, 3], [45, 6], [7, 8], [9]])  # pad with -1 (default)
[[0, 1, 2, 3], [4, 5, 6, -1], [7, 8, -1, -1], [9-1, -1 -1]]
>>> pad_list([[1,2], [3, 4]])  # does nothing
[[1, 2], [3, 4]]
>>> pad_list([[], [1], [3, 4, 5]], 0)  # pad lists with 0
[[0, 0, 0], [1, 0, 0], [3, 4, 5]]
```


<a name="db.utils.pad.pad_list2"></a>
### pad_list2

```python
tensor = dbc.utils.pad.pad_list2(listA, val)
```

Pad list of lists of lists with 'val' such that all lists have the same length.

#### Parameters

- `listA`: List of lists of of lists different sizes. (*type=list*)
- `val`: Value to pad the lists. (*type=number, default=-1*)

#### Usage examples

Pad an uneven list of lists of lists with a value.

```python
>>> from dbcollection.utils.pad import pad_list2
>>> pad_list2([[[], [1]], [[5, 6]]])
[None, None, None]  **TODO: fix this**
```


<a name="db.utils.pad.unpad_list"></a>
### unpad_list

```python
string = dbc.utils.pad.unpad_list(listA, val)
```

Unpad list of lists with which has values equal to 'val'.

#### Parameters

- `listA`: List of lists of different sizes. (*type=list*)
- `val`: Value to unpad the lists. (*type=number, default=-1*)

#### Usage examples

Remove the padding values of a list of lists.

```python
>>> from dbcollection.utils.pad import unpad_list
>>> unpad_list([[1,2,3,-1,-1],[5,6,-1,-1,-1]])
[[1, 2, 3], [5, 6]]
>>> unpad_list([[5,0,-1],[1,2,3,4,5]], 5)
[[0, -1], [1, 2, 3, 4]]
```