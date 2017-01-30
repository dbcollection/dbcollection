"""
Dataset loader class.
"""


from .storage import StorageHDF5
from .utils import convert_ascii_str


class ManagerHDF5:
    """ HDF5 data loading class """


    def __init__(self, data_handler):
        """Initialize class.

        Parameters
        ----------
        data_handler : dict (hdf5)
            A handler for hdf5 'dictionary'.

        Returns
        -------
            None
        """
        self.data = data_handler

        # fetch list of field names that compose the object list.
        try:
            self.object_fields = convert_ascii_str(self.data['object_fields'])
        except KeyError:
            raise


    def get(self, field_name, id):
        """Get data from file.

        Retrieve the i'th data from the field 'field_name' into a list.

        Parameters
        ----------
        field_name : str
            Field name identifier.
		id : int, long or list
            Index number of the field. If it is a list, returns the data
            for all the value indexes of that list

        Returns
        -------
        str, int, long, float, list
            Returns a value/list of a field from the metadata cache file.
        """
        try:
            return self.data[field_name][id]
        except KeyError:
            raise


    def object(self, id, is_value=False):
        """Get list of ids/values of an object.

        Retrieve the data of all fields of an object: It works as calling :get() for
        each field individually and grouping them into a list.

        Parameters
        ----------
        id : int, long or list
            Index number of the field. If it is a list, returns the data
            for all the value indexes of that list
        is_value : bool
            if False, outputs a list of indexes. If True,
            it outputs the values instead of the indexes.

        Returns:
        --------
        list
            Returns a list of indexes (or values if is_value=True).
        """
        if not is_value:
            return self.data['object_id'][id]
        else:
            # convert id to a list (in case it is a number)
            if not isinstance(id, list):
                id_ = [id]
            else:
                id_ = id

            # fetch the field names composing 'object_id'
            fields = self.object_fields

            # iterate over all ids and build an output list
            output = []
            for idx in id_:
                # fetch list od indexes for the current id
                ids = self.data['object_id'][idx]

                # fetch data for each element of the list
                #output.append = [self.data[field_name][ids[i]] for i, field_name in enumerate(fields)]
                data = []
                for i, field_name in enumerate(fields):
                    data.append(self.data[field_name][ids[i]])
                output.append(data)

            # output data
            if len(id_) == 1:
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
        """
        try:
            return self.data[field_name].shape[0]
        except KeyError:
            return self.data['object_id'].shape[0]


    def list(self):
        """
        Lists all field names.
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

        Returns
        -------
            None
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
        """
        for name in self.file.storage.keys():
            setattr(self, name, ManagerHDF5(self.file.storage[name]))
