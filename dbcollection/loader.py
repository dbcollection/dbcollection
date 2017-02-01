"""
Dataset loader class.
"""


from .storage import StorageHDF5
from .utils import convert_ascii_str


class ManagerHDF5:
    """ HDF5 data loading class """


    def __init__(self, data_handler):
        """
        Initialize class.

        Parameters
        ----------
        data_handler : dict (hdf5)
            A handler for a hdf5 dictionary.
        """
        self.data = data_handler

        # fetch list of field names that compose the object list.
        self.object_fields = convert_ascii_str(self.data['object_fields'])


    def get(self, field_name, idx):
        """Get data from file.

        Retrieve the i'th data from the field 'field_name' into a list.

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
        return self.data[field_name][idx]


    def object(self, idx, is_value=False):
        """Get list of ids/values of an object.

        Retrieve the data of all fields of an object: It works as calling :get() for
        each field individually and grouping them into a list.

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
            return self.data['object_id'][idx]
        else:
            # convert idx to a list (in case it is a number)
            if not isinstance(idx, list):
                idx = [idx]

            # fetch the field names composing 'object_id'
            fields = self.object_fields

            # iterate over all ids and build an output list
            output = []
            for idx_ in idx:
                # fetch list od indexes for the current id
                ids = self.data['object_id'][idx_]

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


    def size(self, field_name=None):
        """Size of a field.

        Returns the size of the elements of a field_name.

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
        return self.data[field_name or 'object_id'].shape[0]


    def list(self):
        """
        Lists all field names.

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
        return self.data.keys()


class DatasetLoader:
    """ Dataset loader """


    def __init__(self, name, category, task, data_dir, cache_path):
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
        # store info
        self.name = name
        self.category = category
        self.task = task
        self.data_dir = data_dir
        self.cache_path = cache_path

        # load the cache file
        self.file = StorageHDF5(self.cache_path, 'r')

        # make links for all groups (train/val/test) for easier access
        self.add_group_links()


    def add_group_links(self):
        """
        Adds links for the groups for easier access to data.

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
        for name in self.file.storage.keys():
            setattr(self, name, ManagerHDF5(self.file.storage[name]))
