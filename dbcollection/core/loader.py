"""
Dataset's metadata loader classes.
"""


import h5py
from dbcollection.utils.string_ascii import convert_ascii_to_str


class FieldLoader(object):
    """Field metadata loader class.

    This class contains several methods to fetch data from a specific
    field of a set (group) in a hdf5 file. It contains useful information
    about the field and also several methods to fetch data.

    Parameters
    ----------
    hdf5_field : h5py._hl.dataset.Dataset
        hdf5 field object handler.
    obj_id : int, optional
        Position of the field in 'object_fields'.

    Attributes
    ----------
    data : h5py._hl.dataset.Dataset
        hdf5 group object handler.
    set : str
        Name of the set.
    name : str
        Name of the field.
    type : type
        Type of the field's data.
    shape : tuple
        Shape of the field's data.
    fillvalue : int
        Value used to pad arrays when storing the data in the hdf5 file.
    obj_id : int
        Identifier of the field if contained in the 'object_ids' list.

    """

    def __init__(self, hdf5_field, obj_id=None):
        """Initialize class."""
        assert hdf5_field, 'Must input a valid hdf5 dataset.'

        self.data = hdf5_field
        self.hdf5_handler = hdf5_field
        self._in_memory = False
        self.set = self._get_set_name()
        self.name = self._get_field_name()
        self.shape = hdf5_field.shape
        self.type = hdf5_field.dtype
        self.fillvalue = hdf5_field.fillvalue
        self.obj_id = obj_id

    def _get_set_name(self):
        hdf5_object_str = self._get_hdf5_object_str()
        return hdf5_object_str[1]

    def _get_field_name(self):
        hdf5_object_str = self._get_hdf5_object_str()
        return hdf5_object_str[-1]

    def _get_hdf5_object_str(self):
        return self.hdf5_handler.name.split('/')

    def get(self, index=None, convert_to_str=False):
        """Retrieves data of the field from the dataset's hdf5 metadata file.

        This method retrieves the i'th data from the hdf5 file. Also, it is
        possible to retrieve multiple values by inserting a list/tuple of
        number values as indexes.

        Parameters
        ----------
        index : int/list/tuple, optional
            Index number of he field. If it is a list, returns the data
            for all the value indexes of that list.
        convert_to_str : bool, optional
            Convert the output data into a string.
            Warning: output must be of type np.uint8

        Returns
        -------
        np.ndarray/list/str
            Numpy array containing the field's data.
            If convert_to_str is set to True, it returns a string
            or list of strings.

        Note
        ----
        When using lists/tuples of indexes, this method sorts the list
        and removes duplicate values. This is because the h5py
        api requires the indexing elements to be in increasing order when
        retrieving data.

        """
        if index is None:
            data = self._get_all_idx()
        else:
            data = self._get_range_idx(index)
        if convert_to_str:
            data = convert_ascii_to_str(data)
        return data

    def _get_all_idx(self):
        """Return the full data array."""
        if self._in_memory:
            return self.data
        else:
            return self.data.value

    def _get_range_idx(self, idx):
        """Return a slice of the data array."""
        assert idx is not None
        if isinstance(idx, int):
            return self.data[idx]
        else:
            size = len(idx)
            if size > 1:
                return self.data[sorted(set(idx))]
            elif size == 1:
                return self.data[idx[0]]
            else:
                return self._get_all_idx()

    def size(self):
        """Size of the field.

        Returns the number of the elements of the field.

        Returns
        -------
        tuple
            Returns the size of the field.

        """
        return self.shape

    def object_field_id(self):
        """Retrieves the index position of the field in the 'object_ids' list.

        This method returns the position of the field in the 'object_ids' object.
        If the field is not contained in this object, it returns a null value.

        Returns
        -------
        int
            Index of the field in the 'object_ids' list.

        """
        return self.obj_id

    def info(self, verbose=True):
        """Prints information about the field.

        Displays information like name, size and shape of the field.

        Parameters
        ----------
        verbose : bool, optional
            If true, display extra information about the field.

        """
        if verbose:
            if hasattr(self, 'obj_id'):
                print('Field: {},  shape = {},  dtype = {},  (in \'object_ids\', position = {})'
                      .format(self.name, str(self.shape), str(self.type), self.obj_id))
            else:
                print('Field: {},  shape = {},  dtype = {}'
                      .format(self.name, str(self.shape), str(self.type)))

    def _set_to_memory(self, is_in_memory):
        """Stores the contents of the field in a numpy array if True.

        Parameters
        ----------
        is_in_memory : bool
            Move the data to memory (if True).

        """
        assert isinstance(is_in_memory, bool), 'Invalid input. Must insert a boolean type.'
        if is_in_memory:
            self.data = self.hdf5_handler.value
        else:
            self.data = self.hdf5_handler
        self._in_memory = is_in_memory

    def _get_to_memory(self):
        """Modifies how data is accessed and stored.

        Accessing data from a field can be done in two ways: memory or disk.
        To enable data allocation and access from memory requires the user to
        specify a boolean. If set to True, data is allocated to a numpy ndarray
        and all accesses are done in memory. Otherwise, data is kept in disk and
        accesses are done using the HDF5 object handler.

        """
        return self._in_memory

    to_memory = property(_get_to_memory, _set_to_memory)

    def __getitem__(self, index):
        """
        Parameters
        ----------
        index : int
            Index

        Returns
        -------
        np.ndarray
            Numpy data array.

        """
        return self.data[index]

    def __len__(self):
        """
        Returns
        -------
        int
            Number of samples

        """
        return self.shape[0]

    def __str__(self):
        if self._in_memory:
            s = 'FieldLoader: <numpy.ndarray "{}": shape {}, type "{}">' \
                .format(self.name, self.data.shape, self.data.dtype)
        else:
            s = 'FieldLoader: ' + self.data.__str__()
        return s

    def __repr__(self):
        return str(self)


class SetLoader(object):
    """Set metadata loader class.

    This class contains several methods to fetch data from a specific
    set (group) in a hdf5 file. It contains useful information about a
    specific group and also several methods to fetch data.

    Parameters
    ----------
    hdf5_group : h5py._hl.group.Group
        hdf5 group object handler.

    Attributes
    ----------
    hdf5_group : h5py._hl.group.Group
        hdf5 group object handler.
    set : str
        Name of the set.
    fields : tuple
        List of all field names of the set.
    object_fields : tuple
        List of all field names of the set contained by the 'object_ids' list.
    nelems : int
        Number of rows in 'object_ids'.

    """

    def __init__(self, hdf5_group):
        """Initialize class."""
        assert hdf5_group, 'Must input a valid hdf5 group'

        self.hdf5_group = hdf5_group
        self.set = self._get_set_name()
        self.object_fields = self._get_object_fields()
        self.nelems = self._get_num_elements()
        self._fields = self._get_field_names()
        self.fields = self._load_hdf5_fields()  # add all hdf5 datasets as data fields

        self._fields_info = []
        self._lists_info = []

    def _get_set_name(self):
        hdf5_object_str = self.hdf5_group.name
        str_split = hdf5_object_str.split('/')
        return str_split[-1]

    def _get_object_fields(self):
        object_fields_data = self.hdf5_group['object_fields'].value
        output = convert_ascii_to_str(object_fields_data)
        if type(output) == 'string':
            output = (output,)
        return output

    def _get_field_names(self):
        return tuple(self.hdf5_group.keys())

    def _get_num_elements(self):
        return len(self.hdf5_group['object_ids'])

    def _load_hdf5_fields(self):
        fields = {}
        for field in self._fields:
            obj_id = self._get_obj_id_field(field)
            fields[field] = FieldLoader(self.hdf5_group[field], obj_id)
        return fields

    def _get_obj_id_field(self, field):
        if field in self.object_fields:
            return self.object_fields.index(field)
        else:
            return None

    def get(self, field, index=None, convert_to_str=False):
        """Retrieves data from the dataset's hdf5 metadata file.

        This method retrieves the i'th data from the hdf5 file with the
        same 'field' name. Also, it is possible to retrieve multiple values
        by inserting a list/tuple of number values as indexes.

        Parameters
        ----------
        field : str
            Field name.
        index : int/list/tuple, optional
            Index number of the field. If it is a list, returns the data
            for all the value indexes of that list.
        convert_to_str : bool, optional
            Convert the output data into a string.
            Warning: output must be of type np.uint8

        Returns
        -------
        np.ndarray/list/str
            Numpy array containing the field's data.
            If convert_to_str is set to True, it returns a string
            or list of strings.

        Raises
        ------
        KeyError
            If the field does not exist in the list.

        """
        assert field, 'Must input a valid field name.'
        try:
            return self.fields[field].get(index=index, convert_to_str=convert_to_str)
        except KeyError:
            raise KeyError('\'{}\' does not exist in the \'{}\' set.'.format(field, self.set))

    def object(self, index=None, convert_to_value=False):
        """Retrieves a list of all fields' indexes/values of an object composition.

        Retrieves the data's ids or contents of all fields of an object.

        It basically works as calling the get() method for each individual field
        and then groups all values into a list w.r.t. the corresponding order of
        the fields.

        Parameters
        ----------
        index : int/list/tuple, optional
            Index number of the field. If it is a list, returns the data
            for all the value indexes of that list. If no index is used,
            it returns the entire data field array.
        convert_to_value : bool, optional
            If False, outputs a list of indexes. If True,
            it outputs a list of arrays/values instead of indexes.

        Returns
        -------
        list
            Returns a list of indexes or, if convert_to_value is True,
            a list of data arrays/values.

        """
        indexes = self._get_object_indexes(index)
        if convert_to_value:
            indexes = self._convert(indexes.tolist())
        return indexes

    def _get_object_indexes(self, index):
        return self.get('object_ids', index)

    def _convert(self, index):
        """Retrieve data from the dataset's hdf5 metadata file in the original format.

        This method fetches all indices of an object(s), and then it looks up for the
        value for each field in 'object_ids' for a certain index(es), and then it
        groups the fetches data into a single list.

        Parameters
        ----------
        index : list
            List of indexes of data fields.

        Returns
        -------
        List
            Value/list of a field from the metadata cache file.

        Raises
        ------
        TypeError
            If index is not a list of ints or a list of lists.

        """
        assert index, 'Must input a valid index.'
        if isinstance(index[0], int):
            output = self._convert_to_value_single_object(index)
        elif isinstance(index[0], list):
            output = []
            for idx in index:
                output.append(self._convert_to_value_single_object(idx))
        else:
            raise TypeError("Invalid input index format.")
        return output

    def _convert_to_value_single_object(self, idx):
        data = []
        for i, field in enumerate(self.object_fields):
            if idx[i] >= 0:
                data.append(self.get(field, idx[i]))
            else:
                data.append([])  # undefined index retrieves an empty list
        return data

    def size(self, field='object_ids'):
        """Size of a field.

        Returns the number of the elements of a field.

        Parameters
        ----------
        field : str, optional
            Name of the field in the metadata file.

        Returns
        -------
        tuple
            Returns the size of the field.

        Raises
        ------
        KeyError
            If field is invalid or does not exist in the fields dict.

        """
        try:
            return self.fields[field].shape
        except KeyError:
            raise KeyError('\'{}\' does not exist in the \'{}\' set.'.format(field, self.set))

    def list(self):
        """List of all field names.

        Returns
        -------
        list
            List of all data fields of the dataset.

        """
        return self._fields

    def object_field_id(self, field):
        """Retrieves the index position of a field in the 'object_ids' list.

        This method returns the position of a field in the 'object_ids' object.
        If the field is not contained in this object, it returns a null value.

        Parameters
        ----------
        field : str
            Name of the field in the metadata file.

        Returns
        -------
        int
            Index of the field in the 'object_ids' list.

        Raises
        ------
        KeyError
            If field does not exists in the list of object fields.

        """
        assert field, 'Must input a valid field.'
        try:
            return self.fields[field].object_field_id()
        except KeyError:
            raise KeyError('\'{}\' is not contained in \'object_fields\'.'.format(field))

    def info(self):
        """Prints information about the data fields of a set.

        Displays information of all fields available like field name,
        size and shape of all sets. If a 'set_name' is provided, it
        displays only the information for that specific set.

        This method provides the necessary information about a data set
        internals to help determine how to use/handle a specific field.

        """
        print('\n> Set: {}'.format(self.set))
        self._set_fields_lists_info()
        self._print_info_fields()
        self._print_info_lists()

    def _set_fields_lists_info(self):
        if any(self._fields_info):
            return
        for field in sorted(self.fields):
            if self._is_field_a_list(field):
                self._lists_info.append(self._get_list_info(field))
            else:
                self._fields_info.append(self._get_field_info(field))

    def _is_field_a_list(self, field):
        assert field
        return field.startswith('list_')

    def _get_list_info(self, field):
        assert field
        return {
            "name": str(field),
            "shape": 'shape = {}'.format(str(self.fields[field].shape)),
            "type": 'dtype = {}'.format(str(self.fields[field].type))
        }

    def _get_field_info(self, field):
        assert field
        s_obj = ''
        if field in self.object_fields:
            obj_id = self.object_field_id(field)
            s_obj = "(in 'object_ids', position = {})".format(obj_id)

        return {
            "name": str(field),
            "shape": 'shape = {}'.format(str(self.fields[field].shape)),
            "type": 'dtype = {}'.format(str(self.fields[field].type)),
            "obj": s_obj
        }

    def _print_info_fields(self):
        maxsize_name, maxsize_shape, maxsize_type = self._get_max_sizes_fields()
        for i, info in enumerate(self._fields_info):
            s_name = '{:{}}'.format('   - {}, '.format(info["name"]), maxsize_name)
            s_shape = '{:{}}'.format('{}, '.format(info["shape"]), maxsize_shape)
            s_obj = info["obj"]
            if any(s_obj):
                s_type = '{:{}}'.format('{},'.format(info["type"]), maxsize_type)
            else:
                s_type = '{:{}}'.format('{}'.format(info["type"]), maxsize_type)
            print(s_name + s_shape + s_type + s_obj)

    def _get_max_sizes_fields(self):
        maxsize_name = max([len(d["name"]) for d in self._fields_info]) + 8
        maxsize_shape = max([len(d["shape"]) for d in self._fields_info]) + 3
        maxsize_type = max([len(d["type"]) for d in self._fields_info]) + 3
        return maxsize_name, maxsize_shape, maxsize_type

    def _print_info_lists(self):
        if any(self._lists_info):
            print('\n   (Pre-ordered lists)')
            maxsize_name, maxsize_shape = self._get_max_sizes_lists()
            for i, info in enumerate(self._lists_info):
                s_name = '{:{}}'.format('   - {}, '.format(info["name"]), maxsize_name)
                s_shape = '{:{}}'.format('{}, '.format(info["shape"]), maxsize_shape)
                s_type = info["type"]
                print(s_name + s_shape + s_type)

    def _get_max_sizes_lists(self):
        maxsize_name = max([len(d["name"]) for d in self._lists_info]) + 8
        maxsize_shape = max([len(d["shape"]) for d in self._lists_info]) + 3
        return maxsize_name, maxsize_shape

    def __len__(self):
        """
        Returns
        -------
        int
            Number of elements

        """
        return self.nelems

    def __str__(self):
        s = 'SetLoader: set<{}>, len<{}>'.format(self.set, self.nelems)
        return s

    def __repr__(self):
        return str(self)


class DataLoader(object):
    """Dataset metadata loader class.

    This class contains several methods to fetch data from a hdf5 file
    by using simple, easy to use functions for (meta)data handling.

    Parameters
    ----------
    name : str
        Name of the dataset.
    task : str
        Name of the task.
    data_dir : str
        Path of the dataset's data directory on disk.
    hdf5_filepath : str
        Path of the metadata cache file stored on disk.

    Attributes
    ----------
    db_name : str
        Name of the dataset.
    task : str
        Name of the task.
    data_dir : str
        Path of the dataset's data directory on disk.
    hdf5_filepath : str
        Path of the hdf5 metadata file stored on disk.
    hdf5_file : h5py._hl.files.File
        hdf5 file object handler.
    root_path : str
        Default data group of the hdf5 file.
    sets : tuple
        List of names of set splits (e.g. train, test, val, etc.)
    object_fields : dict
        Data field names for each set split.

    """

    def __init__(self, name, task, data_dir, hdf5_filepath):
        """Initialize class."""
        assert name, 'Must input a valid dataset name.'
        assert task, 'Must input a valid task name.'
        assert data_dir, 'Must input a valid path for the data directory.'
        assert hdf5_filepath, 'Must input a valid path for the cache file.'

        self.db_name = name
        self.task = task
        self.data_dir = data_dir
        self.hdf5_filepath = hdf5_filepath
        self.hdf5_file = self._load_hdf5_file()
        self.root_path = '/'
        self._sets = self._get_sets()
        self.object_fields = self._get_object_fields()

        self.sets = self._get_set_loaders()

    def _load_hdf5_file(self):
        return h5py.File(self.hdf5_filepath, 'r', libver='latest')

    def _get_sets(self):
        return tuple(sorted(self.hdf5_file['/'].keys()))

    def _get_object_fields(self):
        """# fetch list of field names that compose the object list."""
        object_fields = {}
        for set_name in self._sets:
            data = self.hdf5_file['/{}/object_fields'.format(set_name)].value
            object_fields[set_name] = tuple(convert_ascii_to_str(data))
        return object_fields

    def _get_set_loaders(self):
        """Return a dictionary with list of set loaders."""
        sets = {}
        for set_name in self._sets:
            sets[set_name] = SetLoader(self.hdf5_file[set_name])
        return sets

    def get(self, set_name, field, index=None, convert_to_str=False):
        """Retrieves data from the dataset's hdf5 metadata file.

        This method retrieves the i'th data from the hdf5 file with the
        same 'field' name. Also, it is possible to retrieve multiple values
        by inserting a list/tuple of number values as indexes.

        Parameters
        ----------
        set_name : str
            Name of the set.
        field : str
            Name of the data field.
        idx : int/list/tuple, optional
            Index number of the field. If it is a list, returns the data
            for all the value indexes of that list.
        convert_to_str : bool, optional
            Convert the output data into a string.
            Warning: output must be of type np.uint8

        Returns
        -------
        np.ndarray/list/str
            Numpy array containing the field's data.
            If convert_to_str is set to True, it returns a string
            or list of strings.

        Raises
        ------
        KeyError
            If set name is not valid or does not exist.

        """
        assert set_name, 'Must input a set name.'
        assert field, 'Must input a field name.'
        try:
            return self.sets[set_name].get(field, index, convert_to_str=convert_to_str)
        except KeyError:
            self._raise_error_invalid_set_name(set_name)

    def _raise_error_invalid_set_name(self, set_name):
        raise KeyError("'{}' does not exist in the sets list: {}".format(set_name, self._sets))

    def object(self, set_name, index=None, convert_to_value=False):
        """Retrieves a list of all fields' indexes/values of an object composition.

        Retrieves the data's ids or contents of all fields of an object.

        It basically works as calling the get() method for each individual field
        and then groups all values into a list w.r.t. the corresponding order of
        the fields.

        Parameters
        ----------
        set_name : str
            Name of the set.
        index : int/list/tuple, optional
            Index number of the field. If it is a list, returns the data
            for all the value indexes of that list. If no index is used,
            it returns the entire data field array.
        convert_to_value : bool, optional
            If False, outputs a list of indexes. If True,
            it outputs a list of arrays/values instead of indexes.

        Returns
        -------
        list
            List of indexes of the data fields available in 'object_fields'.
            If convert_to_value is set to True, it returns a list of data
            instead of indexes.

        Raises
        ------
        KeyError
            If set name is not valid or does not exist.

        """
        assert set_name, 'Must input a valid set name.'
        try:
            return self.sets[set_name].object(index, convert_to_value)
        except KeyError:
            self._raise_error_invalid_set_name(set_name)

    def size(self, set_name=None, field='object_ids'):
        """Size of a field.

        Returns the number of the elements of a field.

        Parameters
        ----------
        set_name : str, optional
            Name of the set.
        field : str, optional
            Name of the field in the metadata file.

        Returns
        -------
        list/dict
            Returns the size of a field.

        Raises
        ------
        KeyError
            If set name is not valid or does not exist.

        """
        if set_name is None:
            return self._get_size_all_sets(field)
        else:
            return self._get_size_single_set(set_name, field)

    def _get_size_all_sets(self, field):
        assert field
        out = {}
        for set_name in self.sets:
            out[set_name] = self.sets[set_name].size(field)
        return out

    def _get_size_single_set(self, set_name, field):
        assert set_name
        assert field
        try:
            return self.sets[set_name].size(field)
        except KeyError:
            self._raise_error_invalid_set_name(set_name)

    def list(self, set_name=None):
        """List of all field names of a set.

        Parameters
        ----------
        set_name : str, optional
            Name of the set.

        Returns
        -------
        list/dict
            List of all data fields of the dataset.

        Raises
        ------
        KeyError
            If set name is not valid or does not exist.

        """
        if set_name is None:
            return self._get_list_all_sets()
        else:
            return self._get_list_single_set(set_name)

    def _get_list_all_sets(self):
        out = {}
        for set_name in self.sets:
            out.update({set_name: self.sets[set_name].list()})
        return out

    def _get_list_single_set(self, set_name):
        assert set_name
        try:
            return self.sets[set_name].list()
        except KeyError:
            self._raise_error_invalid_set_name(set_name)

    def object_field_id(self, set_name, field):
        """Retrieves the index position of a field in the 'object_ids' list.

        This method returns the position of a field in the 'object_ids' object.
        If the field is not contained in this object, it returns a null value.

        Parameters
        ----------
        set_name : str
            Name of the set.
        field : str
            Name of the field in the metadata file.

        Returns
        -------
        int
            Index of the field in the 'object_ids' list.

        Raises
        ------
        KeyError
            If set name is not valid or does not exist.

        """
        assert set_name, 'Must input a valid set name.'
        assert field, 'Must input a valid field name.'
        try:
            return self.sets[set_name].object_field_id(field)
        except KeyError:
            self._raise_error_invalid_set_name(set_name)

    def info(self, set_name=None):
        """Prints information about all data fields of a set.

        Displays information of all fields of a set group inside the hdf5
        metadata file. This information contains the name of the field, as well
        as the size/shape of the data, the data type and if the field is
        contained in the 'object_ids' list.

        If no 'set_name' is provided, it displays information for all available
        sets.

        This method only shows the most useful information about a set/fields
        internals, which should be enough for most users in helping to
        determine how to use/handle a specific dataset with little effort.

        Parameters
        ----------
        set_name : str, optional
            Name of the set.

        Raises
        ------
        KeyError
            If set name is not valid or does not exist.

        """
        if set_name is None:
            self._print_info_all_sets()
        else:
            self._print_info_single_set(set_name)

    def _print_info_all_sets(self):
        for set_name in sorted(self.sets):
            self.sets[set_name].info()

    def _print_info_single_set(self, set_name):
        assert set_name
        try:
            self.sets[set_name].info()
        except KeyError:
            self._raise_error_invalid_set_name(set_name)

    def __len__(self):
        return len(self.sets)

    def __str__(self):
        s = "DataLoader: {} ('{}' task)".format(self.db_name, self.task)
        return s

    def __repr__(self):
        return str(self)
