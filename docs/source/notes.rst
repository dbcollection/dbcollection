.. _my_notes:

Dataset creation
================

- **np.float** is required instead of other smaller types like 
np.float32 or np.float16 because of compatability with torch7
hdf5 package which only accepts DoubleTensors as data.

- **fillvalue** can be a negative number for unsigned data types
because sometimes images can be stored in the hdf5 file (like for 
the case of mnist) and it isn't acceptable to use 0 values as padding
because it can modify the size of the tensors.


intro
-----

- increase code reusage when switching between systems (Windows, Linux)
- easily write scripts to download/process datasets.
- setup the datasets once, avoiding repetitive preprocessing steps when starting my code
- work with multiple languages (Python/Lua/Matlab/etc.).
- have a common framework for building up a list of available datasets for use.


available datasets:
-------------------

Most datasets store the original data in a nested folder format in the ``source`` group in the ``hdf5`` metadata file.
For some APIS, due to the size of the dataset, this nested folder may contain alot of data stored in a nested format,
which causes some APIs to load the nested structured as the file is loaded to memory (``lua/torch7`` API suffers from
this issue). To overcome this problem, all tasks have a version withouth this group in their metadata file.
To load this version, simply append to the end of the task name the suffix ``_d``. Loading times should improve for this
case.
