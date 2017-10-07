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
