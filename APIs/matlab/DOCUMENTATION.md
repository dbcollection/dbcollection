<a name="db.documentation"></a>
# Documentation

This section covers the main API methods for dataset managing/data fetching for the Matlab's dbcollection package.

The dbcollection package is composed by three main groups:

- [dbcollection](#db.dbcollection): dataset manager API.
    - [load](#db.dbcollection.load): load a dataset.
    - [download](#db.dbcollection.download): download a dataset data to disk.
    - [process](#db.dbcollection.process): process a dataset's metadata and stores it to file.
    - [add](#db.dbcollection.add): add a dataset/task to the list of available datasets for loading.
    - [remove](#db.dbcollection.remove): remove/delete a dataset from the cache.
    - [config_cache](#db.dbcollection.config_cache): configure the cache file.
    - [query](#db.dbcollection.query): do simple queries to the cache.
    - [info](#db.dbcollection.info): prints the cache contents.
- [dbcollection.utils](#db.utils): utility functions.
    - [string_ascii](#db.utils.string_ascii): module containing methods for converting [strings to arrays](#db.utils.string_ascii.convert_string_to_ascii) and [arrays to strings](#db.utils.string_ascii.convert_ascii_to_string).

The [data loading API](#db.loader) contains a few methods for data retrieval/probing:

- [get](#db.loader.get): retrieve data from the dataset's hdf5 metadata file.
- [object](#db.loader.object): retrieves a list of all fields' indexes/values of an object composition.
- [size](#db.loader.size): size of a field.
- [list](#db.loader.list): lists all fields' names.
- [object_fields_id](#db.loader.object_field_id): retrieves the index position of a field in the `object_ids` list.


<a name="db.dbcollection"></a>
## dbcollection

This class is the main module for easily managing/loading/processing datasets for the `dbcollection` package.
The dataset managing API is composed by the following methods. The (recommended) use of the package is as follows:

```matlab
dbc = dbcollection();
```

The package is structured as a Matlab class. In this documentation we use the above convention to construct the class and to call its methods (similar to the other APIs).

<a name="db.dbcollection.load"></a>
### load

```matlab
loader = dbcollection.load(name, task, data_dir, verbose, is_test)
```

Returns a loader instant of a `dbcollection_DatasetLoader` class with methods to retrieve/probe data and other informations from the selected dataset.

> Note1: It is important to point out that you can pass input arguments in two different ways: (1) by passing values in the correct order or (2) by defining a struct with fields named as the input args. Here it is prefered to pass a struct to the methods because its simpler and its usage is similar to the other APIs where you can specify only the required fields you want to change and let the others use the default values.

> Note2: Another aspect worth mentioning in that optional arguments, i.e., arguments that have a default value, can be skipped by using `[]`. This forces the use of the default value.

#### Parameters

- `name`: Name of the dataset. (*type=string*)
- `task`: Name of the task to load. (*type=string, default='default'*)
- `data_dir`: Directory path to store the downloaded data. (*type=string, default=''*)
- `verbose`: Displays text information (if true). (*type=boolean, default=true*)
- `is_test`: Flag used for tests. (*type=boolean, default=false*)


#### Usage examples

You can simply load a dataset by its name like in the following example.

```matlab
mnist = dbc.load('mnist');
```

In cases where you don't have the dataset's data on disk yet (and the selected dataset can be downloaded by the API), you can specify which directory the dataset's data files should be stored to and which task should be loaded for this dataset.

```matlab
cifar10 = dbc.load(struct('name', 'cifar10', ...
                          'task', 'classification', ...
                          'data_dir', 'path/to/dataset/'));
```

> Note: If you don't specify the directory path where to store the data files, then the files will be stored in the `dbcollection/<dataset>/data` dir where the metadata files are located.


<a name="db.dbcollection.download"></a>
### download

```matlab
dbcollection.download(name, data_dir, extract_data, verbose, is_test);
```

This method will download a dataset's data files to disk. After download, it updates the cache file with the dataset's name and path where the data is stored.


#### Parameters

- `name`: Name of the dataset. (*type=string*)
- `data_dir`: Directory path to store the downloaded data. (*type=string, default='default'*)
- `extract_data`: Extracts/unpacks the data files (if true). (*type=boolean, default=true*)
- `verbose`: Displays text information (if true). (*type=boolean, default=true*)
- `is_test`: Flag used for tests. (*type=boolean, default=false*)



#### Usage examples

A simple usage example for downloading a dataset (without providing a storage path for the data) requires only the name of the target dataset and it will download its data files and then extract them to disk without any supervision required.

```matlab
dbc.download('cifar10');
```

It is good practice to specify where the data will be downloaded to by providing an existing directory path to `data_dir`. (This information is stored in the `dbcollection.json` file stored in your home path.)

```matlab
dbc.download(struct('name', 'cifar10', ...
                    'data_dir', '<some_dir>'));
```

In cases where you only want to download the dataset's data files without extracting its contents, you can set `extract_data` to `false` and skip the data extraction/unpacking step.

```matlab
dbc.download(struct('name', 'cifar10', ...
                    'data_dir', '<some_dir>',
                    'extract_data', false));
```

> Note: this package uses a text progressbar when downloading files from urls for visual purposes (file size, elapsed time, % download, etc.). To disable this feature, set `verbose` to `false`.


<a name="db.dbcollection.process"></a>
### process

```matlab
dbcollection.process(name, task, verbose, is_test)
```

Processes a dataset's metadata and stores it to file. This metadata is stored in a HDF5 file for each task composing the dataset's tasks. For more information about a dataset's metadata format please check the list of available datasets in the [docs](http://dbcollection.readthedocs.io/en/latest/available_datasets.html).

#### Parameters

- `name`: Name of the dataset. (*type=string*)
- `task`: Name of the task to process. (*type=string, default='all'*)
- `verbose`: Displays text information (if true). (*type=boolean, default=true*)
- `is_test`: Flag used for tests. (*type=boolean, default=false*)


#### Usage examples

To process (or reprocess) a dataset's metadata simply do:

```matlab
dbc.process('cifar10');
```

This will process all tasks for a given dataset (default='all'). To process only a specific task, you need to specify the task name you want to setup. This is handy when one wants to process only a single task of a bunch of tasks and speed up the processing/loading stage.

```matlab
dbc.process(struct('name', 'cifar10', ...
                   'task', 'default'));  % process only the 'default' task
```

> Note: this method allows the user to reset a dataset's metadata file content in case of manual or accidental changes to the structure of the data. Most users won't have the need for such functionality on their basic usage of this package.

<a name="db.dbcollection.add"></a>
### add

```matlab
dbcollection.add(name, task, data_dir, verbose)
```

This method provides an easy way to add a custom dataset/task to the `dbcollection.json` cache file without having to manually add them themselves (although it is super easy to do it and recommended!).

#### Parameters

- `name`: Name of the dataset. (*type=string*)
- `task`: Name of the task to load. (*type=string*)
- `data_dir`: Path of the stored data on disk. (*type=string*)
- `file_path`: Path to the metadata HDF5 file. *(type=string*)
- `keywords`: Table of strings of keywords that categorize the dataset. (*type=table, default={}*)
- `is_test`: Flag used for tests. (*type=boolean, default=false*)


#### Usage examples

Adding a custom dataset or a custom task to a dataset requires the user to introduce the dataset's `name`, `task` name, `data_dir` where the data files are stored and the metadata's `file_path` on disk.

```matlab
dbc.add(struct('name', 'custom1', ...
               'task', 'default', ...
               'data_dir', '<data_dir>', ...
               'file_path', '<metadata_file_path>'));
```

> Note: In cases where no external files are required besides the metadata's data, you can set `data_dir` to "".


<a name="db.dbcollection.remove"></a>
### remove

```matlab
dbcollection.remove(name, task, delete_data, verbose)
```

This method allows for a dataset to be removed from the list of available datasets for load in the cache. It also allows for the user to delete the dataset's files on disk if desired.


#### Parameters

- `name`: Name of the dataset to delete. (*type=string*)
- `task`: Name of the task to delete. (*type=string, default='None'*)
- `delete_data`: Delete all data files from disk for this dataset if True. (*type=boolean, default=false*)
- `is_test`: Flag used for tests. (*type=boolean, default=false*)


#### Usage examples

To remove a dataset simply do:

```matlab
dbc.remove('cifar10');
```

If you want to remove the dataset completely from disk, you can set the `delete_data` parameter to `true`.

```matlab
dbc.remove('cifar10', [], true);
```

> Note: To skip an optional value use [].


<a name="db.dbcollection.config_cache"></a>
### config_cache

```matlab
dbcollection.config_cache(field, value, delete_cache, delete_cache_dir, delete_cache_file, reset_cache, is_test)
```

Configures the cache file via API. This method allows to configure the cache file directly by selecting any data field and (re)setting its value. The user can also manually configure the `dbcollection.json` cache file in the filesystem (recommended).

To modify any entry in the cache file, simply input the field name you want to change along with the new data you want to insert. This applies to any existing field.

Another available function is the reset/wipe the entire cache paths/configs from the file. To perform this action set the `reset_cache` input arg to `true`.

Also, there is an option to completely remove the cache file+folder from the disk by enabling `delete_cache` to `true`. This will remove the cache file `dbcollection.json` and the `dbcollection/` folder from disk.

> Warning: Misusing this API method may result in tears. Proceed with caution.

#### Parameters

- `field`: Name of the field to update/modify in the cache file. (*type=string, default='None'*)
- `value`: Value to update the field. (*type=string, default='None'*)
- `delete_cache`: Delete/remove the dbcollection cache file + directory. (*type=boolean, default=false*)
- `delete_cache_dir`: Delete/remove the dbcollection cache directory. (*type=boolean, default=false*)
- `delete_cache_file`: Delete/remove the dbcollection.json cache file. (*type=boolean, default=false*)
- `reset_cache`: Reset the cache file. (*type=boolean, default=false*)
- `is_test`: Flag used for tests. (*type=boolean, default=false*)


#### Usage examples

For example, Lets change the directory where the dbcollection's metadata main folder is stored on disk. This is useful to store/move all the metadata files to another disk.

```matlab
dbc.config_cache(struct('field', 'default_cache_dir', ...
                        'value', '/new/path/to/db/'));
```

If a user wants to remove all files relating to the `dbcollection` package, one can use the `config_cache` to accomplish this in a simple way:

```matlab
dbc.config_cache(struct('delete_cache', 'true'));
```

or if the user wants to remove only the cache file:

```matlab
dbc.config_cache(struct('delete_cache_file', 'true'));
```

or to remove the cache directory where all the metadata files from all datasets are stored (**I hope you are sure about this one...**):

```matlab
dbc.config_cache(struct('delete_cache_dir', 'true'));
```

or to simply reset the cache file contents withouth removing the file:

```matlab
dbc.config_cache(struct('reset_cache', 'true'));
```


<a name="db.dbcollection.query"></a>
### query

```matlab
dbcollection.query(pattern, is_test)
```

Do simple queries to the cache and displays them to the screen.


#### Parameters

- `pattern`: Field name used to search for a matching pattern in cache data. (*type=string, default='info'*)
- `is_test`: Flag used for tests. (*type=boolean, default=false*)


#### Usage examples

Simple query about the existence of a dataset.

```matlab
dbc.query('mnist');
```

It can also retrieve information by category/keyword. For example, this is useful to see which datasets have the same task.

```matlab
dbc.query('detection');
```

> Note: this is the same as scanning the `dbcollection.json` cache file yourself, but it has the advantage of grouping information about a certain pattern for you.

<a name="db.dbcollection.info"></a>
### info

```matlab
dbcollection.info(list_datasets, is_test)
```

Prints the cache contents to screen. It can also prints a list of all available datasets to download/process from the `dbcollection` package.

#### Parameters

- `list_datasets`: Print available datasets in the `dbcollection` package. (*type=boolean, default=false*)
- `is_test`: Flag used for tests. (*type=boolean, default=false*)


#### Usage examples

Print the cache file contents to the screen:

```matlab
dbc.info();
```

Display all available datasets to download/process:

```matlab
dbc.info(true);
```

<a name="db.loader"></a>
## Data loading API

The data loading API is a Matlab class composed by some fields containing information about the dataset and some methods to retrieve data.

Loading a dataset using [dbcollection.load()](#db.dbcollection.load) returns an instantiation of `dbcollection_DatasetLoader` class. It contains information about the selected dataset (name, task, set splits, directory of the data files stored in disk, etc.) and methods to easily extract data from the metadata file.

The information of the dataset is stored as attributes of the class:

- `name`: Name of the selected dataset. (*type = string*)
- `task`: Name of the selected task. (*type = string*)
- `data_dir`: Directory path where the data files are stored. (*type = string*)
- `cache_path`: Path where the metadata file is located. (*type = string*)
- `root_path`: HDF5 root group/path which the methods retrieve data from. (*type = string, default='default/'*)
- `sets`: A list of available sets for the selected dataset (e.g., train/val/test/etc.). (*type = cell*)
- `object_fields`: A list of all field names available for each set of the dataset. (*type = struct*)

> Note: The list of available `sets` (set splits) and `object_fields` (available field names) varies from dataset to dataset.


<a name="db.loader.get"></a>
### get

```matlab
data = loader.get(set_name, field_name, idx);
```

Retrieves data from the dataset's hdf5 metadata file. This method accesses the HDF5 metadata file content and searches for a field `field_name` in the selected group `set_name`. If an index or list of indexes are input, the method returns a slice (rows) of the data's array. If no index is set, it return the entire data array.

#### Parameters

- `set_name`: Name of the set. (*type=string*)
- `field_name`: Name of the data field. (*type=string*)
- `idx`:  Index number of the field. If the input is a table, it uses it as a range of indexes
and returns the data for that range. (*type=number or array of numbers, default=[]*)

#### Usage examples

The first, and most common, usage of this method if to retrieve a single piece of data from a data field. Lets retrieve the first image+label from the `MNIST` dataset.

```matlab
mnist = dbc.load('mnist');
img = mnist.get('train', 'images', 1);
label = mnist.get('train', 'labels', 1);
```

This method can also be used to retrieve a range of data/values.

```matlab
imgs = mnist.get('train', 'images', [1:20]);
```

Or all values if desired.

```matlab
imgs = mnist.get('train', 'images');
```

<a name="db.loader.object"></a>
### object

```matlab
indexes = loader.object(set_name, idx, is_value);
```

Retrieves a list of all fields' indexes/values of an object composition. If `is_value` is `true`, instead of returning an array containing the object's fields indexes, it returns a cell of array containing the extracted data for each field index.

This method is particularly useful when different fields are linked (like in detection tasks with labeled data) and their contents can be quickly accessed and retrieved in one swoop.

#### Parameters

- `set_name`: Name of the set. (*type=string*)
- `idx`:  Index number of the field. If it is a table, returns the data for all the value indexes of that list. (ty*pe=number or array*)
- `is_value`: Outputs an array of indexes (if false) or a cell of arrays/values (if true). (*type=boolean, default=false*)


#### Usage examples

Fetch all indexes of an object. Again, lets use the `MNIST` dataset for this action.

```matlab
mnist = dbc.load('mnist');
obj_idxs = mnist.object('train', 1);
```

Multiple lists can be retrieved just like with the [get()](#db.loader.get) method.

```matlab
objs_idxs = mnist.object('train', [1:10]);
```

It is also possible to retrieve the values/arrays instead of the indexes.

```matlab
objs_data = mnist:object('train', [1:10]], true);
```


<a name="db.loader.size"></a>
### size

```matlab
size = loader.size(set_name, field_name);
```

Returns the size of a field.

#### Parameters

- `set_name`: Name of the set. (*type=string*)
- `field_name`: Name of the data field. (*type=string*)

> Note: if `field_name` is not provided, it uses the `object_ids` field instead.

#### Usage examples

Get the size of the images array from the `MNIST` train set.

```matlab
mnist = dbc.load('mnist');
images_size = mnist.size('train', 'images');
```

Get the size of the objects in `MNIST` train set.

```matlab
obj_size = mnist.size('train', 'object_ids');
% or
obj_size = mnist.size('train');
```


<a name="db.loader.list"></a>
### list

```matlab
fields = loader.list(set_name);
```

Lists all field names in a set.

#### Parameters

- `set_name`: Name of the set. (*type=string*)

#### Usage examples

Get all fields available in the `MNIST` test set.

```matlab
mnist = dbc.load('mnist');
images_size = mnist.list('test');
```


<a name="db.loader.object_field_id"></a>
### object_field_id

```matlab
position = loader.object_field_id(set_name, field_name);
```

Retrieves the index position of a field in the `object_ids` list. This position points to the field name stored in the `object_fields` attribute.

#### Parameters

- `set_name`: Name of the set. (*type=string*)
- `field_name`: Name of the data field. (*type=string*)

#### Usage examples

This example shows how to use this method in order to retrieve the correct fields from an object index list.

```matlab
mnist = dbc.load('mnist');
fprintf('object: images field idx: %d', mnist.object_field_id('train', 'images'))
fprintf('object: labels field idx: %d', mnist:object_field_id('train', 'labels'))
fprintf('Check if the positions match with the list of fields: %s', mnist.object_fields.train)
```


<a name="db.utils"></a>
## Utils

This module contains some useful utility functions available to the user.

It is composed by the following modules:

- [dbcollection.utils.string_ascii](#db.utils.string_ascii): string<->ascii convertion functions.

<a name="db.utils.string_ascii"></a>
### dbcollection.utils.string_ascii

This module contains methods to convert strings to ascii and vice-versa. These are usefull when recovering strings from the metadata file that are encoded as `uint8` arrays.

Although one might only need to convert ascii encoded arrays to strings, this module contains both methods for ascii-to-string and string-to-ascii.

<a name="db.utils.string_ascii.convert_string_to_ascii"></a>
### convert_string_to_ascii

```matlab
ascii_array = dbcollection.utils.string_ascii.convert_string_to_ascii(input);
```

Convert a string or cell of strings to a double array.

#### Parameters

- `input`: String or a cell of strings. (*type=string or cell*)

#### Usage examples

Single string.

```matlab
>> str = 'string1';
>> ascii_array = dbc.utils.string_ascii.convert_str_to_ascii(str);
>> disp(ascii_array)

   115   116   114   105   110   103    49     0
```

Cell of strings.

```matlab
>> str = {'string1', 'string2', 'string3'};
>> ascii_array = dbc.utils.string_ascii.convert_str_to_ascii(str);
>> disp(ascii_tensor)

   115   116   114   105   110   103    49     0
   115   116   114   105   110   103    50     0
   115   116   114   105   110   103    51     0
```


<a name="db.utils.string_ascii.convert_ascii_to_str"></a>
### convert_ascii_to_string

```matlab
str = dbcollection.utils.string_ascii.convert_ascii_to_str(input);
```

Convert a array/matrix to an array of strings.

#### Parameters

- `input`: 2D torch tensor. (*type=array/matrix*)

#### Usage examples

Convert a `torch.CharTensor` to string.

```matlab
% ascii format of 'string1'
>> array = [115, 116, 114, 105, 110, 103, 49, 0];
>> str = dbc.utils.string_ascii.convert_ascii_to_str(array);
>> disp(str)
string1
```