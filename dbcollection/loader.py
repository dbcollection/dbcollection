"""
Dataset loader class.
"""


import storage


class ManagerHDF5:
    """ HDF5 data loading class """


    def __init__(self, handler_file, group_name):
        """Initialize class.

        Parameters
        ----------
        cache_path : str
            Path to the metadata cache file on disk.

        Returns
        -------
            None
        """
        self.data = handler_file.storage[group_name]


    def get(self, field_name, id):
        """
        Retrieve the 'i'th' data from the field 'field_name' into a list.

        Parameters
        ----------
            - field_name: field name identifier [Type=String]
		    - id: index number of the field. If it is a list, returns the data for all the value indexes of that list [Type=long/List]
        Returns:
        --------
            returns a list filled with data.
        """
        pass
        # >>> fiquei aqui <<<<



    def object_id(self, id, is_value=False):
        """
        Retrieve the data of all fields of an object: It works as calling :get() for each field individually and grouping them into a list.

        Parameters:
        -----------
            - id: index number of the object list. If it is a list, returns the data for all the value indexes of that list [Type=long/List]
            - is_value: if False, outputs a list of indexes. If True, it outputs the values instead of the indexes. [Type=Boolean, default=False]

        Returns:
        --------
            Returns a list of indexes (or values if is_value=True)
        """
        pass



    def size(self, field_name=None):
        """
        Returns the size of the elements of a field_name.

        Parameters:
        -----------
            - field_name: field name identifier [Type=String]

        Returns:
        --------
            returns the number of elements of a field
            (if empty it returns the size of the object list).
        """
        pass


    def list(self):
        """
        Lists all field names (order w.r.t. the object list position).
        """
        pass



class Loader:
    """ Dataset loader """

    
    def __init__(self, name, category, task, data_path, cache_path):
        """Initialize class.

        Parameters
        ----------
        name : str
            Name of the dataset.
        category : str
            Category of the dataset (e.g. image processing, natural language processing)
        task : str
            Name of the task.
        data_path : str
            Path to the dataset's data on disk.
        cache_path : str
            Path to the metadata cache file on disk.

        Returns
        -------
            None
        """
        # store info
        self.name = name
        self.category = category
        self.task = task
        self.data_path = data_path
        self.cache_path = cache_path

        # load the cache file 
        self.file = storage.StorageHDF5()

        # make links for all groups (train/val/test) for easier access
        self.add_group_links()


    def add_group_links(self):
        """
        Adds links for the groups for easier access to data.
        """
        for name in self.file.storage.keys():
            setattr(self, name, ManagerHDF5(self.file, name))
