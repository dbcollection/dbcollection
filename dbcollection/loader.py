"""
Dataset loader class.
"""

import h5py
from dbcollection.utils.string_ascii import convert_ascii_to_str


class DatasetLoader:
    """ Dataset loader (HDF5 data loading) class """


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
        assert name, 'Must input a valid dataset name: {}'.format(name)
        assert task, 'Must input a valid task name: {}'.format(task)
        assert data_dir, 'Must input a valid path for the data directory: {}'.format(data_dir)
        assert cache_path, 'Must input a valid path for the cache file: {}'.format(cache_path)

        # store information of the dataset
        self.name = name
        self.task = task
        self.data_dir = data_dir
        self.cache_path = cache_path

        # create a handler for the cache file
        self.file = h5py.File(self.cache_path, 'r', libver='latest')
        self.root_path = 'default/'

        # make links for all groups (train/val/test/etc) for easier access
        self.sets = [name for name in self.file['default/'].keys()]

        # fetch list of field names that compose the object list.
        self.object_fields = {}
        for set_name in self.sets:
            data = self.file['default/{}/object_fields'.format(set_name)].value
            self.object_fields[set_name] = convert_ascii_to_str(data)


    def get(self, set_name, field_name, idx=None):
        """Retrieve data from the dataset's hdf5 metadata file.

        Retrieve the i'th data from the field 'field_name'.

        Parameters
        ----------
        set_name : str
            Name of the set.
        field_name : str
            Field name identifier.
		idx : int/list
            Index number of the field. If it is a list, returns the data
            for all the value indexes of that list
            (optional, default=None)

        Returns
        -------
        str, int, list
            Value/list of a field from the metadata cache file.

        Raises
        ------
            None
        """
        assert set_name, 'Must input a valid set name: {}'.format(set_name)
        assert field_name, 'Must input a valid field_name name: {}'.format(field_name)

        field_path = self.root_path + set_name + '/' + field_name
        if idx is None:
            return self.file[field_path].value
        else:
            return self.file[field_path][idx]


    def object(self, set_name, idx, is_value=False):
        """Retrieves a list of all fields' indexes/values of an object composition.

        Retrieves the data's ids or contents of all fields of an object.

        It works as calling :get() for each field individually and grouping
        them into a list.

        Parameters
        ----------
        set_name : str
            Name of the set.
        idx : int, long, list
            Index number of the field. If it is a list, returns the data
            for all the value indexes of that list
        is_value : bool
            if False, outputs a list of indexes. If True,
            it outputs the values instead of the indexes.
            (optional, default=False)

        Returns:
        --------
        list
            Returns a list of indexes (or values if is_value=True).

        Raises
        ------
            None
        """
        assert set_name, 'Must input a valid set name: {}'.format(set_name)
        if isinstance(idx, list):
            assert min(idx) >= 0, 'list must have indexes >= 0: {}'.format(idx)
        else:
            assert idx >= 0, 'idx must be >=0: {}'.format(idx)

        dir_path = self.root_path + set_name + '/'
        field_path = dir_path + 'object_ids'
        if not is_value:
            return self.file[field_path][idx]
        else:
            # convert idx to a list (in case it is a number)
            if not isinstance(idx, list):
                idx = [idx]

            # fetch the field names composing 'object_ids'
            fields = self.object_fields[set_name]

            # iterate over all ids and build an output list
            output = []
            for idx_ in idx:
                # fetch list of indexes for the current id
                ids = self.file[field_path][idx_]

                # fetch data for each element of the list
                data = []
                for i, field_name in enumerate(fields):
                    field_id = ids[i]
                    if field_id >= 0:
                        data.append(self.file[dir_path + field_name][field_id])
                    else:
                        data.append([])
                output.append(data)

            # output data
            if len(idx) == 1:
                return output[0]
            else:
                return output


    def size(self, set_name, field_name='object_ids'):
        """Size of a field.

        Returns the number of the elements of a field_name.

        Parameters
        ----------
        set_name : str
            Name of the set.
        field_name : str
            Name of the field in the metadata cache file.
            (optional, default='object_ids')

        Returns:
        --------
        list
            Returns the size of the object list.

        Raises
        ------
            None
        """
        assert set_name, 'Must input a valid set name: {}'.format(set_name)

        field_path = self.root_path + set_name + '/' + field_name
        return list(self.file[field_path].shape)


    def list(self, set_name):
        """Lists all fields' names.

        Parameters
        ----------
        set_name : str
            Name of the set.

        Returns
        -------
        list
            List of all data fields of the dataset.

        Raises
        ------
            None
        """
        assert set_name, 'Must input a valid set name: {}'.format(set_name)

        field_path = self.root_path + set_name
        return list(self.file[field_path].keys())


    def object_field_id(self, set_name, field_name):
        """Retrieves the index position of a field in the 'object_ids' list.

        Parameters
        ----------
        set_name : str
            Name of the set.
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
        assert set_name, 'Must input a valid set name: {}'.format(set_name)
        assert field_name, 'Must input a valid field_name name: {}'.format(field_name)

        try:
            return self.object_fields[set_name].index(field_name)
        except ValueError:
            raise ValueError('Field name \'{}\' does not exist.'.format(field_name))
