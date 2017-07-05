<a name="db.documentation"></a>
# Documentation

This section covers the main API methods for dataset managing/data fetching for the Lua/Torch7's dbcollection package.

The dbcollection package is composed by three main groups:

- [dbcollection.manager](#db.manager): dataset manager API module.
    - [load](#db.manager.load): load a dataset.
    - [download](#db.manager.download): download a dataset data to disk.
    - [process](#db.manager.process): process a dataset's metadata and stores it to file.
    - [add](#db.manager.add): add a dataset/task to the list of available datasets for loading.
    - [remove](#db.manager.remove): remove/delete a dataset from the cache.
    - [config_cache](#db.manager.config_cache): configure the cache file.
    - [query](#db.manager.query): do simple queries to the cache.
    - [info](#db.manager.info): prints the cache contents.
- [dbcollection.utils](#db.utils): utility functions.
    - [string_ascii](#db.utils.string_ascii): module containing methods for converting [strings to tensors](#db.utils.string_ascii.convert_string_to_ascii) and [tensors to strings](#db.utils.string_ascii.convert_ascii_to_string).

The [data loading API](#db.loader) contains a few methods for data retrieval/probing:

- [get](#db.loader.get): retrieve data from the dataset's hdf5 metadata file.
- [object](#db.loader.object): retrieves a list of all fields' indexes/values of an object composition.
- [size](#db.loader.size): size of a field.
- [list](#db.loader.list): lists all fields' names.
- [object_fields_id](#db.loader.object_field_id): retrieves the index position of a field in the `object_ids` list.


<a name="db.manager"></a>
## dbcollection.manager

This module is the main modules for easily managing/loading/processing datasets for the `dbcollection` package.
The dataset managing API is composed by the following methods.

<a name="db.manager.load"></a>
### load

```lua
loader = dbcollection.manager.load(name, task, data_dir, verbose, is_test)
```

Returns a loader instant of a `DatasetLoader` class with methods to retrieve/probe data and other informations from the selected dataset.


#### Parameters

- `name`: Name of the dataset. (*type=string*)
- `task`: Name of the task to load. (*type=string, default='default'*)
- `data_dir`: Directory path to store the downloaded data. (*type=string, default=''*)
- `verbose`: Displays text information (if true). (*type=boolean, default=true*)
- `is_test`: Flag used for tests. (*type=boolean, default=false*)


#### Usage examples

You can simply load a dataset by its name like in the following example.

```lua
local dbc = require 'dbcollection.manager'
local mnist = dbc.load('mnist')
```

In cases where you don't have the dataset's data on disk yet (and the selected dataset can be downloaded by the API), you can specify which directory the datset's data files should be stored to and which task should be loaded for this dataset.

```lua
local dbc = require 'dbcollection.manager'
local cifar10 = dbc.load{name='cifar10', task='classification', data_dir='<my_home>/datasets/'}
```

> Note: If you don't specify the directory path where to store the data files, then the files will be stored in the `dbcollection/<dataset>/data` dir where the metadata files are located.


<a name="db.manager.download"></a>
### download

```lua
dbcollection.manager.download(name, data_dir, verbose, is_test)
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

```lua
local dbc = require 'dbcollection.manager'
dbc.download('cifar10')
```

It is good practice to specify where the data will be download to by providing a existing directory path to `data_dir`. (This information is stored in the `dbcollection.json` file stored in your home path.)

```lua
local dbc = require 'dbcollection.manager'
dbc.download({name='cifar10', data_dir='<some_dir>'})
```

In cases where you only want to download the dataset's files without extracting its contents, you can set `extract_data=false` and skip the data extraction/unpacking step.

```lua
local dbc = require 'dbcollection.manager'
dbc.download({name='cifar10', data_dir='<some_dir>', extract_data=false})
```

> Note: this package uses a text progressbar when downloading files from urls for visual purposes (file size, elapsed time, % download, etc.). To disable this feature, set `verbose=false`.


<a name="db.manager.process"></a>
### process

```lua
dbcollection.manager.process(name, task, verbose. is_test)
```

Processes a dataset's metadata and stores it to file. This metadata is stored in a HDF5 file for each task composing the dataset's tasks. For more information about a dataset's metadata format please check the list of available datasets in the [docs](http://dbcollection.readthedocs.io/en/latest/available_datasets.html).

#### Parameters

- `name`: Name of the dataset. (*type=string*)
- `task`: Name of the task to process. (*type=string, default='all'*)
- `verbose`: Displays text information (if true). (*type=boolean, default=true*)
- `is_test`: Flag used for tests. (*type=boolean, default=false*)


#### Usage examples

To process (or reprocess) a dataset's metadata simply do:

```lua
local dbc = require 'dbcollection.manager'
dbc.process('cifar10')
```

> Note: this method allows the user to reset a dataset's metadata format in case of manual or accidental changes to the structure of the data, although most users won't have the need for such functionality on their usage of this package.

```lua
local dbc = require 'dbcollection.manager'
dbc.process('cifar10') -- process all tasks
```

To process only a specific task, you need to specify the task name you want to setup. This is handy when one wants to process only a single task of a bunch of tasks and speed up the processing/loading stage.

```lua
local dbc = require 'dbcollection.manager'
dbc.process({name='cifar10', task='default'}) -- process only the 'default' task
```

> Note: this method allows the user to reset a dataset's metadata format in case of manual or accidental changes to the structure of the data, although most users won't have the need for such functionality on their usage of this package.

<a name="db.manager.add"></a>
### add

```lua
dbcollection.manager.add(name, task, data_dir, verbose)
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

```lua
local dbc = require 'dbcollection.manager'
dbc.add{name='custom1', task='default', data_dir='<data_dir>', file_path='<metadata_file_path>'}
```

> Note: In cases where no external files are required besides the metadata's data, you can set `data_dir`="".


<a name="db.manager.remove"></a>
### remove

```lua
dbcollection.manager.remove(name, task, data_dir, verbose)
```

This method allows for a dataset to be removed from the list of available datasets for load in the cache. It also allows for the user to delete the dataset's files on disk if desired.

#### Parameters

- `name`: Name of the dataset. (*type=string*)
- `delete_data`: Delete all data files from disk for this dataset if True. (*type=boolean, default=false*)
- `is_test`: Flag used for tests. (*type=boolean, default=false*)


#### Usage examples

To remove a dataset simply do:

```lua
local dbc = require 'dbcollection.manager'
dbc.remove('cifar10')
```

If you want to remove the dataset completely from disk, you can set the `delete_data` parameter to `true`.

```lua
local dbc = require 'dbcollection.manager'
dbc.remove('cifar10', true)
```


<a name="db.manager.config_cache"></a>
### config_cache

```lua
dbcollection.manager.config_cache(field, value, delete_cache, delete_cache_dir, delete_cache_file, reset_cache, is_test)
```


Configures the cache file via an API. This method allows to configure the cache file directly by selecting any data field/value. The user can also manually configure the `dbcollection.json` cache file (recommended).

To modify any entry in the cache file, simply input the field name
you want to change along with the new data you want insert. This
applies to any field/data in the file.

Another thing available is to reset/clear the entire cache paths/configs from the file by simply enabling the `reset_cache` flag to `true`.

Also, there is an option to completely remove the cache file+folder
from the disk by enabling `delete_cache` to `true`. This will remove the cache `dbcollection.json` and the `dbcollection/` folder from disk.


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

```lua
local dbc = require 'dbcollection.manager'
dbc.config_cache{field='default_cache_dir', value='<home_dir>/new/path/db/'}
```

If a user wants to remove all files relating to the `dbcollection` package, one can use the `config_cache` to accomplish this in a simple way:

```lua
local dbc = require 'dbcollection.manager'
dbc.config_cache{delete_cache=true}
```

or if the user wants to remove only the cache file:

```lua
local dbc = require 'dbcollection.manager'
dbc.config_cache{delete_cache_file=true}
```

or to remove the cache directory where all the metadata files from all datasets are stored:

```lua
local dbc = require 'dbcollection.manager'
dbc.config_cache{delete_cache_dir=true}
```

or to simply reset the cache file contents:

```lua
local dbc = require 'dbcollection.manager'
dbc.config_cache{reset_cache=true}
```


<a name="db.manager.query"></a>
### query

```lua
dbcollection.manager.query(pattern, is_test)
```

Do simple queries to the cache and displays them to the screen.


#### Parameters

- `pattern`: Field name used to search for a matching pattern in cache data. (*type=string, default='info'*)
- `is_test`: Flag used for tests. (*type=boolean, default=false*)


#### Usage examples

Simple query about the existence of a dataset.

```lua
local dbc = require 'dbcollection.manager'
dbc.query('mnist')
```

It can also retrieve information by category/keyword. For example, this is useful to see which datasets have the same task.

```lua
local dbc = require 'dbcollection.manager'
dbc.query('detection')
```

> Note: this is the same as scanning the `dbcollection.json` cache file yourself, but it has the advantage of grouping information about a certain pattern for you.

<a name="db.manager.info"></a>
### info

```lua
dbcollection.manager.info(list_datasets, is_test)
```

Prints the cache contents to screen. It can also print a list of all available datasets to download/process in the `dbcollection` package.

#### Parameters

- `list_datasets`: Print available datasets in the `dbcollection` package. (*type=boolean, default=false*)
- `is_test`: Flag used for tests. (*type=boolean, default=false*)


#### Usage examples

Print the cache file contents to the screen:

```lua
local dbc = require 'dbcollection.manager'
dbc.info()
```

Display all available datasets to download/process:

```lua
local dbc = require 'dbcollection.manager'
dbc.info(true)
```

<a name="db.loader"></a>
## Data loading API

The data loading API is class composed by some fields containing information about the dataset and some methods to retrieve data.

Loading a dataset using [dbcollection.manager.load()](#db.manager.load) returns an instantiation of the `DatasetLoader` class which contains information about the selected dataset and methods to easily extract data from the metadata file.

The information of the dataset is stored as attributes of the class:

- `name`: Name of the selected dataset. (*type = string*)
- `task`: Name of the selected task. (*type = string*)
- `data_dir`: Directory path where the data files are stored. (*type = string*)
- `cache_path`: Path where the metadata file is located. (*type = string*)
- `file`: The HDF5 file handler of the dataset's metadata. (*type = hdf5.HDF5File*)
- `root_path`: HDF5 root group/path which the methods retrieve data from. (*type = string, default='default/'*)
- `sets`: A list of available sets for the selected dataset (e.g., train/val/test/etc.). (*type = table*)
- `object_fields`: A list of all field names available for each set of the dataset. (*type = table*)

> Note: The list of available `sets` and `object_fields` varies from dataset to dataset.


<a name="db.loader.get"></a>
### get

```lua
data = Loader:get(set_name, field_name, idx)
```

Retrieves data from a dataset's hdf5 metadata file. This method accesses the HDF5 metadata file and searches for a field `field_name` in the selected group `set_name`. If no idx is defined, then it returns a tensor containing the entire data.

#### Parameters

- `set_name`: Name of the set. (*type=string*)
- `field_name`: Name of the data field. (*type=string*)
- `idx`:  Index number of the field. If the input is a table, it uses it as a range of indexes and returns the data for that range. (*type=number or table*)

#### Usage examples

The first, and most common, usage of this method if to retrieve a single piece of data from a data field. Lets retrieve the first image+label from the `MNIST` dataset.

```lua
local dbc = require 'dbcollection.manager'
local mnist = dbc.load('mnist') # returns a DatasetLoader class

local img = mnist:get('train', 'images', 1)
local label = mnist:get('train', 'labels', 1)
```

This method can also be used to retrieve a range of data/values.

```lua
local imgs = mnist:get('train', 'images', {1, 20})
```

Or all values if desired.

```lua
local imgs = mnist:get('train', 'images')
```

<a name="db.loader.object"></a>
### object

```lua
indexes = Loader:object(set_name, idx, is_value)
```

Retrieves a list of all fields' indexes/values of an object composition. If `is_value=true`, instead of returning a tensor containing the object's fields indexes, it returns a table of tensors for each field.

This method is particularly useful when different fields are combined (like in detection tasks) and the required data can be quickly accessed and retrieved in one swoop.

#### Parameters

- `set_name`: Name of the set. (*type=string*)
- `idx`:  Index number of the field. If it is a table, returns the data for all the value indexes of that list. (ty*pe=number or table*)
- `is_value`: Outputs a tensor of indexes (if false) or a table of tensors/values (if true). (*type=boolean, default=false*)


#### Usage examples

Fetch all indexes of an object.

```lua
local dbc = require 'dbcollection.manager'
local mnist = dbc.load('mnist') # returns a DatasetLoader class

local obj_idxs = mnist:object('train', 1)
```

Multiple lists can be retrieved just like with the [get()](#db.loader.get) method.

```lua
local objs_idxs = mnist:object('train', {1, 20})
```

It is also possible to retrieve the values/tensors instead of the indexes.

```lua
local objs_data = mnist:object('train', {1, 20}, true)
```


<a name="db.loader.size"></a>
### size

```lua
size = Loader:size(set_name, field_name)
```

Returns the size of a field.

#### Parameters

- `set_name`: Name of the set. (*type=string*)
- `field_name`: Name of the data field. (*type=string*)

> Note: if `field_name` is not provided, it uses the `object_ids` field instead.

#### Usage examples

Get the size of the images tensor in `MNIST` train set.

```lua
local dbc = require 'dbcollection.manager'
local mnist = dbc.load('mnist') # returns a DatasetLoader class

local images_size = mnist:size('train', 'images')
```

Get the size of the objects in `MNIST` train set.

```lua
local obj_size = mnist:size('train', 'object_ids')
# or
local obj_size = mnist:size('train')
```


<a name="db.loader.list"></a>
### list

```lua
fields = Loader:list(set_name)
```

Lists all field names in a set.

#### Parameters

- `set_name`: Name of the set. (*type=string*)


#### Usage examples

Get all fields available in the `MNIST` test set.

```lua
local dbc = require 'dbcollection.manager'
local mnist = dbc.load('mnist') # returns a DatasetLoader class

local images_size = mnist:list('test')
```


<a name="db.loader.object_field_id"></a>
### object_field_id

```lua
position = Loader:object_field_id(set_name, field_name)
```

Retrieves the index position of a field in the `object_ids` list. This position points to the field name stored in the `object_fields` attribute.

#### Parameters

- `set_name`: Name of the set. (*type=string*)
- `field_name`: Name of the data field. (*type=string*)

#### Usage examples

This example shows how to use this method in order to retrieve the correct fields from an object index list.

```lua
local dbc = require 'dbcollection.manager'
local mnist = dbc.load('mnist') # returns a DatasetLoader class

print('object: images field idx: ', mnist:object_field_id('train', 'images'))
print('object: labels field idx: ', mnist:object_field_id('train', 'labels'))
print('Check if the positions match with the list of fields: ', mnist.object_fields['train'])
```


<a name="db.utils"></a>
## Utils

This module contains some usefull utility functions available to the user.

It is composed by the following modules:

- [dbcollection.utils.string_ascii](#db.utils.string_ascii)

<a name="db.utils.string_ascii"></a>
### dbcollection.utils.string_ascii

This module contains methods to convert strings to ascii and vice-versa. These are usefull when recovering strings from the metadata file that are encoded as `torch.ByteTensors` (this is due to a limitation in the `HDF5` implementation on torch7).

Although one might only need to convert `torch.ByteTensors` to strings, this module contains both methods for ascii-to-string and string-to-ascii.

<a name="db.utils.string_ascii.convert_string_to_ascii"></a>
### convert_string_to_ascii

```lua
tensor = dbcollection.utils.string_ascii.convert_string_to_ascii(input)
```

Convert a string or table of string to a `torch.CharTensor`.

#### Parameters

- `input`: String or a table of strings. (*type=string or table*)

#### Usage examples

Single string.

```lua
local string_ascii = require 'dbcollection.utils.string_ascii'
local toascii_ = string_ascii.convert_str_to_ascii

local str = 'string1'
local ascii_tensor = toascii_(str)

print(ascii_tensor)
 115  116  114  105  110  103   49    0
[torch.CharTensor of size 1x8]

```

Table of strings.

```lua
local string_ascii = require 'dbcollection.utils.string_ascii'
local toascii_ = string_ascii.convert_str_to_ascii

local str = {'string1', 'string2', 'string3'}
local ascii_tensor = toascii_(str)

print(ascii_tensor)
 115  116  114  105  110  103   49    0
 115  116  114  105  110  103   50    0
 115  116  114  105  110  103   51    0
[torch.CharTensor of size 3x8]
```


<a name="db.utils.string_ascii.convert_ascii_to_string"></a>
### convert_ascii_to_string

```lua
str = dbcollection.utils.string_ascii.convert_ascii_to_string(input)
```

Convert a `torch.CharTensor` or `torch.ByteTensor` to a table of strings.

#### Parameters

- `input`: 2D torch tensor. (*type=torch.ByteTensor or torch.CharTensor*)

#### Usage examples

Convert a `torch.CharTensor` to string.

```lua
local string_ascii = require 'dbcollection.utils.string_ascii'
local tostring_ = string_ascii.convert_ascii_to_str

# ascii format of 'string1'
local tensor = torch.CharTensor({{115, 116, 114, 105, 110, 103, 49, 0}})
local str = tostring_(tensor)

print(str)
{
  1 : "string1"
}
```