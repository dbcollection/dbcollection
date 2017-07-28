"""
Dataset loader class.
"""

import h5py
from dbcollection.utils.string_ascii import convert_ascii_to_str


class DatasetLoader:
    """ Dataset loader (HDF5 data loading) class

    Attributes
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
    file : h5py._hl.files.File
        hdf5 file object handler.
    root_path : str
        Default data group of the hdf5 file.
    sets : list
        List of names of set splits (e.g. train, test, val, etc.)
    object_fields : dict
        Data field names for each set split.
    """


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
		idx : int/list, optional
            Index number of the field. If it is a list, returns the data
            for all the value indexes of that list.

        Returns
        -------
        str/int/list
            Value/list of a field from the metadata cache file.

        """
        assert set_name, 'Must input a valid set name: {}'.format(set_name)
        assert field_name, 'Must input a valid field_name name: {}'.format(field_name)

        field_path = self.root_path + set_name + '/' + field_name
        if idx is None:
            return self.file[field_path].value
        else:
            return self.file[field_path][idx]


    def _convert(self, set_name, idx):
        """Retrieve data from the dataset's hdf5 metadata file in the original format.

        This method fetches all indices of an object(s), and then it looks up for the
        value for each field in 'object_ids' for a certain index(es), and then it
        groups the fetches data into a single list.

        Parameters
        ----------
        set_name : str
            Name of the set.
		idx : int/list
            Index number of the field. If it is a list, returns the data
            for all the indexes of that list as values.

        Returns
        -------
        str/int/list
            Value/list of a field from the metadata cache file.

        """
        assert set_name, 'Must input a valid set name: {}'.format(set_name)
        if isinstance(idx, list):
            assert min(idx) >= 0, 'list must have indexes >= 0: {}'.format(idx)
        else:
            assert idx >= 0, 'idx must be >=0: {}'.format(idx)

        dir_path = self.root_path + set_name + '/'

        # convert idx to a list (in case it is a number)
        if not isinstance(idx, list):
            idx = [idx]

        # fetch the field names composing 'object_ids'
        fields = self.object_fields[set_name]

        # iterate over all ids and build an output list
        output = []
        for idx_ in idx:
            # fetch list of indexes for the current id
            ids = self.file[dir_path + 'object_ids'][idx_]

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


    def object(self, set_name, idx=None, is_value=False):
        """Retrieves a list of all fields' indexes/values of an object composition.

        Retrieves the data's ids or contents of all fields of an object.

        It works as calling :get() for each field individually and grouping
        them into a list.

        Parameters
        ----------
        set_name : str
            Name of the set.
        idx : int/list, optional
            Index number of the field. If it is a list, returns the data
            for all the value indexes of that list. If no index is used,
            it returns the entire data field array.
        is_value : bool, optional
            if False, outputs a list of indexes. If True,
            it outputs the values instead of the indexes.

        Returns:
        --------
        list
            Returns a list of indexes (or values if is_value=True).

        """
        assert set_name, 'Must input a valid set name: {}'.format(set_name)
        if idx is None:
            idx = list(range(0, self.size(set_name)[0]))
        else:
            if isinstance(idx, list):
                if any(idx):
                    assert min(idx) >= 0, 'list must have indexes >= 0: {}'.format(idx)
                else:
                    idx = list(range(0, self.size(set_name)[0]))
            else:
                assert idx >= 0, 'idx must be >=0: {}'.format(idx)

        if is_value:
            return self._convert(set_name, idx)
        else:
            return self.get(set_name, 'object_ids', idx)


    def size(self, set_name, field_name='object_ids'):
        """Size of a field.

        Returns the number of the elements of a field_name.

        Parameters
        ----------
        set_name : str
            Name of the set.
        field_name : str, optional
            Name of the field in the metadata cache file.

        Returns:
        --------
        list
            Returns the size of the object list.

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


    def _print_info(self, set_name):
        """Prints information about the data fields of a set.

        Displays information of all fields available like field name,
        size and shape of all sets. If a 'set_name' is provided, it
        displays only the information for that specific set.

        This method provides the necessary information about a data set
        internals to help determine how to use/handle a specific field.

        Parameters
        ----------
        set_name : str
            Name of the set.

        """
        assert set_name, 'Invalid set name: {}'.format(set_name)

        print('\n> Set: {}'.format(set_name))

        field_path = self.root_path + set_name
        field_names = list(self.file[field_path].keys())

        # prints all fields except list_*
        fields_info = []
        lists_info = []
        for field_name in sorted(field_names):
            f = self.file[self.root_path + set_name + '/' + field_name]

            if field_name.startswith('list_'):
                lists_info.append({
                    "name": str(field_name),
                    "shape": 'shape = {}'.format(str(f.shape)),
                    "type": 'dtype = {}'.format(str(f.dtype))
                })
            else:
                # check if its in 'object_ids'
                s_obj = ''
                if field_name in self.object_fields[set_name]:
                    s_obj = "(in 'object_ids', position = {})".format(self.object_field_id(set_name, field_name))

                fields_info.append({
                    "name": str(field_name),
                    "shape": 'shape = {}'.format(str(f.shape)),
                    "type": 'dtype = {}'.format(str(f.dtype)),
                    "obj": s_obj
                })

        maxsize_name = max([len(d["name"]) for d in fields_info]) + 8
        maxsize_shape = max([len(d["shape"]) for d in fields_info]) + 3
        maxsize_type = max([len(d["type"]) for d in fields_info]) + 3

        for i, info in enumerate(fields_info):
            s_name  = '{:{}}'.format('   - {}, '.format(info["name"]), maxsize_name)
            s_shape = '{:{}}'.format('{}, '.format(info["shape"]), maxsize_shape)
            s_obj   = info["obj"]
            if any(s_obj):
                s_type  = '{:{}}'.format('{},'.format(info["type"]), maxsize_type)
            else:
                s_type  = '{:{}}'.format('{}'.format(info["type"]), maxsize_type)
            print(s_name + s_shape + s_type + s_obj)

        if any(lists_info):
            print('\n   (Pre-ordered lists)')

            maxsize_name = max([len(d["name"]) for d in lists_info]) + 8
            maxsize_shape = max([len(d["shape"]) for d in lists_info]) + 3

            for i, info in enumerate(lists_info):
                s_name  = '{:{}}'.format('   - {}, '.format(info["name"]), maxsize_name)
                s_shape = '{:{}}'.format('{}, '.format(info["shape"]), maxsize_shape)
                s_type  = info["type"]
                print(s_name + s_shape + s_type)


    def info(self, set_name=None):
        """Prints information about the data fields of a set.

        Displays information of all fields available like field name,
        size and shape of all sets. If a 'set_name' is provided, it
        displays only the information for that specific set.

        This method provides the necessary information about a data set
        internals to help determine how to use/handle a specific field.

        Parameters
        ----------
        set_name : str
            Name of the set.

        """
        if set_name:
            self._print_info(set_name)
        else:
            for set_name in sorted(self.sets):
                self._print_info(set_name)
