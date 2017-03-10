"""
Dataset loader class.
"""


from .storage import StorageHDF5
from .utils import convert_ascii_to_str


#---------------------------------------------------------
# Data fetching API from the hdf5 metadata file
#---------------------------------------------------------

class ManagerHDF5:
    """ HDF5 data loading class """

    def __init__(self, data_handler):
        """Initialize class.

        Parameters
        ----------
        data_handler : hdf5
            A handler for a hdf5 file.
        """
        self.data = data_handler

        # fetch list of field names that compose the object list.
        self.object_fields = convert_ascii_to_str(self.data['object_fields'].value)


    def get(self, field_name, idx=None):
        """Get data from file.

        Retrieve the i'th data from the field 'field_name'.

        Parameters
        ----------
        field_name : str
            Field name identifier.
		idx : int/list
            Index number of the field. If it is a list, returns the data
            for all the value indexes of that list

        Returns
        -------
        str, int, list
            Value/list of a field from the metadata cache file.

        Raises
        ------
            None
        """
        if idx is None:
            return self.data[field_name].value
        else:
            return self.data[field_name][idx]


    def object(self, idx, is_value=False):
        """Get list of ids/values of an object.

        Retrieves the data's ids or contents of all fields of an object. 

        It works as calling :get() for each field individually and grouping 
        them into a list.

        Parameters
        ----------
        idx : int, long or list
            Index number of the field. If it is a list, returns the data
            for all the value indexes of that list
        is_value : bool
            if False, outputs a list of indexes. If True,
            it outputs the values instead of the indexes.

        Returns:
        --------
        list
            Returns a list of indexes (or values if is_value=True).

        Raises
        ------
            None
        """
        if not is_value:
            return self.data['object_ids'][idx]
        else:
            # convert idx to a list (in case it is a number)
            if not isinstance(idx, list):
                idx = [idx]

            # fetch the field names composing 'object_ids'
            fields = self.object_fields

            # iterate over all ids and build an output list
            output = []
            for idx_ in idx:
                # fetch list od indexes for the current id
                ids = self.data['object_ids'][idx_]

                # fetch data for each element of the list
                data = []
                for i, field_name in enumerate(fields):
                    data.append(self.data[field_name][ids[i]])
                output.append(data)

            # output data
            if len(idx) == 1:
                return output[0]
            else:
                return output


    def size(self, field_name=None, full=False):
        """Size of a field.

        Returns the number of the elements of a field_name.

        Parameters
        ----------
        field_name : str
            Name of the field in the metadata cache file.

        Returns:
        --------
        int, long
            Returns the number of elements of a field
            (if empty it returns the size of the object list).

        Raises
        ------
            None
        """
        if full:
            return list(self.data[field_name or 'object_ids'].shape)
        else:
            return self.data[field_name or 'object_ids'].shape[0]


    def list(self):
        """Lists all field names.

        Parameters
        ----------
            None

        Returns
        -------
            None

        Raises
        ------
            None
        """
        return list(self.data.keys())


    def object_field_id(self, field_name):
        """Retrieves the index position of a field in the object id list.

        Parameters
        ----------
        field_name : str
            Name of the data field.

        Returns
        -------
        int
            Index of the field_name on the list.

        Raises
        ------
        ValueError
            If field_name does not exist on the 'object_fields' list.
        """
        try:
            return self.object_fields.index(field_name)
        except ValueError:
            raise ValueError('Field name \'{}\' does not exist.'.format(field_name))


#---------------------------------------------------------
# Dataset loader functions + dataset info
#---------------------------------------------------------

class DatasetLoader:
    """ Dataset loader """


    def __init__(self, name, task, data_dir, cache_path):
        """Initialize class.

        Parameters
        ----------
        name : str
            Name of the dataset.
        category : str
            Category of the dataset (e.g. image processing, natural language processing)
        task : str
            Name of the task.
        data_dir : str
            Path of the dataset's data directory on disk.
        cache_path : str
            Path of the metadata cache file stored on disk.
        """
        # store information of the dataset
        self.name = name
        self.task = task
        self.data_dir = data_dir
        self.cache_path = cache_path

        # create a handler for the cache file
        self.file = StorageHDF5(self.cache_path, 'r')

        # make links for all groups (train/val/test/etc) for easier access
        self.sets = []
        for name in self.file.storage.keys():
            self.sets.append(name)
            setattr(self, name, ManagerHDF5(self.file.storage[name+'/default']))
