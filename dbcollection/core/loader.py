"""
Dataset's metadata loader class.
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
        s = hdf5_field.name.split('/')
        self.set = s[1]
        self.name = s[-1]
        self.type = hdf5_field.dtype
        self.shape = hdf5_field.shape
        self.fillvalue = hdf5_field.fillvalue
        if obj_id:
            self.obj_id = obj_id
        else:
            self.obj_id = None

    def get(self, idx=None):
        """Retrieves data of the field from the dataset's hdf5 metadata file.

        This method retrieves the i'th data from the hdf5 file. Also, it is
        possible to retrieve multiple values by inserting a list/tuple of
        number values as indexes.

        Parameters
        ----------
        idx : int/list/tuple, optional
            Index number of he field. If it is a list, returns the data
            for all the value indexes of that list.

        Returns
        -------
        np.ndarray
            Numpy array containing the field's data.
        list
            List of numpy arrays if using a list of indexes.

        """
        if idx is None:
            if self._in_memory:
                data = self.data
            else:
                data = self.data.value
        else:
            data = self.data[idx]
        return data

    def size(self):
        """Size of the field.

        Returns the number of the elements of the field.

        Returns
        -------
        list
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

    def info(self):
        """Prints information about the field.

        Displays information like name, size and shape of the field.

        """
        if hasattr(self, 'obj_id'):
            print('Field: {},  shape = {},  dtype = {},  (in \'object_ids\', position = {})'
                  .format(self.name, str(self.shape), str(self.type), self.obj_id))
        else:
            print('Field: {},  shape = {},  dtype = {}'
                  .format(self.name, str(self.shape), str(self.type)))

    def _set_to_memory(self, is_in_memory):
        """"Stores the contents of the field in a numpy array if True.

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
    data : h5py._hl.group.Group
        hdf5 group object handler.
    set : str
        Name of the set.
    fields : tuple
        List of all field names of the set.
    _object_fields : tuple
        List of all field names of the set contained by the 'object_ids' list.
    nelems : int
        Number of rows in 'object_ids'.

    """

    def __init__(self, hdf5_group):
        """Initialize class."""
        assert hdf5_group, 'Must input a valid hdf5 group'
        self.data = hdf5_group
        self.set = hdf5_group.name.split('/')[-1]
        self.fields = tuple(hdf5_group.keys())
        self._object_fields = tuple(convert_ascii_to_str(hdf5_group['object_fields'].value))
        self.nelems = len(hdf5_group['object_ids'])

        # add fields to the class
        for field in self.fields:
            if field in self._object_fields:
                obj_id = self._object_fields.index(field)
            else:
                obj_id = None
            setattr(self, field, FieldLoader(hdf5_group[field], obj_id))

    def get(self, field, idx=None):
        """Retrieves data from the dataset's hdf5 metadata file.

        This method retrieves the i'th data from the hdf5 file with the
        same 'field' name. Also, it is possible to retrieve multiple values
        by inserting a list/tuple of number values as indexes.

        Parameters
        ----------
        field : str
            Field name.
        idx : int/list/tuple, optional
            Index number of the field. If it is a list, returns the data
            for all the value indexes of that list.

        Returns
        -------
        np.ndarray
            Numpy array containing the field's data.
        list
            List of numpy arrays if using a list of indexes.

        """
        assert field, 'Must input a valid field name: {}'.format(field)
        assert field in self.fields, 'Field \'{}\' does not exist in the \'{}\' set.' \
                                     .format(field, self.set)
        if idx is None:
            return self.data[field].value
        else:
            if isinstance(idx, tuple):
                idx = list(idx)
            return self.data[field][idx]

    def _convert(self, idx):
        """Retrieve data from the dataset's hdf5 metadata file in the original format.

        This method fetches all indices of an object(s), and then it looks up for the
        value for each field in 'object_ids' for a certain index(es), and then it
        groups the fetches data into a single list.

        Parameters
        ----------
        idx : int/list/tuple
            Index number of the field. If it is a list, returns the data
            for all the indexes of that list as values.

        Returns
        -------
        str/int/list
            Value/list of a field from the metadata cache file.

        """
        if isinstance(idx, list) or isinstance(idx, tuple):
            assert min(idx) >= 0, 'list/tuple must have indexes >= 0: {}'.format(idx)
        else:
            assert idx >= 0, 'idx must be >=0: {}'.format(idx)

        # convert idx into a tuple (in case it is a number)
        if not isinstance(idx, tuple):
            idx = (idx,)

        # fetch the field names composing 'object_ids'
        fields = self._object_fields

        # iterate over all ids and build an output list
        output = []
        for idx_ in idx:
            # fetch list of indexes for the current id
            ids = self.data['object_ids'][idx_]

            # fetch data for each element of the list
            data = []
            for i, field_name in enumerate(fields):
                field_id = ids[i]
                if field_id >= 0:
                    data.append(self.data[field_name][field_id])
                else:
                    data.append([])
            output.append(data)

        # output data
        if len(idx) == 1:
            return output[0]
        else:
            return output

    def object(self, idx=None, convert_to_value=False):
        """Retrieves a list of all fields' indexes/values of an object composition.

        Retrieves the data's ids or contents of all fields of an object.

        It basically works as calling the get() method for each individual field
        and then groups all values into a list w.r.t. the corresponding order of
        the fields.

        Parameters
        ----------
        idx : int/list/tuple, optional
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
        if idx is None:
            idx = tuple(range(0, self.nelems))
        else:
            if isinstance(idx, list) or isinstance(idx, tuple):
                if any(idx):
                    assert min(idx) >= 0, 'list/tuple must have indexes >= 0: {}'.format(idx)
                else:
                    raise ValueError('Must input a non-empty list/tuple as index: {}'.format(idx))
            else:
                assert idx >= 0, 'idx must be >=0: {}'.format(idx)

        if convert_to_value:
            return self._convert(idx)
        else:
            return self.get('object_ids', idx)

    def size(self, field='object_ids'):
        """Size of a field.

        Returns the number of the elements of a field.

        Parameters
        ----------
        field : str, optional
            Name of the field in the metadata file.

        Returns
        -------
        list
            Returns the size of a field.

        """
        assert field in self.fields, 'Field \'{}\' does not exist in the \'{}\' set.' \
                                     .format(field, self.set)
        return tuple(self.data[field].shape)

    def list(self):
        """List of all field names.

        Returns
        -------
        list
            List of all data fields of the dataset.

        """
        return self.fields

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

        """
        assert field, 'Must input a valid field: {}'.format(field)
        if field in self._object_fields:
            return self._object_fields.index(field)
        else:
            raise ValueError('Field \'{}\' is not contained in \'object_fields\'.'.format(field))

    def info(self):
        """Prints information about the data fields of a set.

        Displays information of all fields available like field name,
        size and shape of all sets. If a 'set_name' is provided, it
        displays only the information for that specific set.

        This method provides the necessary information about a data set
        internals to help determine how to use/handle a specific field.

        """
        print('\n> Set: {}'.format(self.set))

        # prints all fields except list_*
        fields_info = []
        lists_info = []
        for field in sorted(self.fields):
            f = self.data[field]

            if field.startswith('list_'):
                lists_info.append({
                    "name": str(field),
                    "shape": 'shape = {}'.format(str(f.shape)),
                    "type": 'dtype = {}'.format(str(f.dtype))
                })
            else:
                # check if its in 'object_ids'
                if field in self._object_fields:
                    s_obj = "(in 'object_ids', position = {})" \
                            .format(self.object_field_id(field))
                else:
                    s_obj = ''

                fields_info.append({
                    "name": str(field),
                    "shape": 'shape = {}'.format(str(f.shape)),
                    "type": 'dtype = {}'.format(str(f.dtype)),
                    "obj": s_obj
                })

        maxsize_name = max([len(d["name"]) for d in fields_info]) + 8
        maxsize_shape = max([len(d["shape"]) for d in fields_info]) + 3
        maxsize_type = max([len(d["type"]) for d in fields_info]) + 3

        for i, info in enumerate(fields_info):
            s_name = '{:{}}'.format('   - {}, '.format(info["name"]), maxsize_name)
            s_shape = '{:{}}'.format('{}, '.format(info["shape"]), maxsize_shape)
            s_obj = info["obj"]
            if any(s_obj):
                s_type = '{:{}}'.format('{},'.format(info["type"]), maxsize_type)
            else:
                s_type = '{:{}}'.format('{}'.format(info["type"]), maxsize_type)
            print(s_name + s_shape + s_type + s_obj)

        if any(lists_info):
            print('\n   (Pre-ordered lists)')

            maxsize_name = max([len(d["name"]) for d in lists_info]) + 8
            maxsize_shape = max([len(d["shape"]) for d in lists_info]) + 3

            for i, info in enumerate(lists_info):
                s_name = '{:{}}'.format('   - {}, '.format(info["name"]), maxsize_name)
                s_shape = '{:{}}'.format('{}, '.format(info["shape"]), maxsize_shape)
                s_type = info["type"]
                print(s_name + s_shape + s_type)

    def __len__(self):
        """
        Returns
        -------
        int
            Number of elements

        """
        return self.nelems

    def __str__(self):
        s = 'SetLoader: set<{}>, len<{}>' \
            .format(self.set, self.nelems)
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
        assert name, 'Must input a valid dataset name: {}'.format(name)
        assert task, 'Must input a valid task name: {}'.format(task)
        assert data_dir, 'Must input a valid path for the data directory: {}'.format(data_dir)
        assert hdf5_filepath, 'Must input a valid path for the cache file: {}'.format(hdf5_filepath)

        # store information of the dataset
        self.db_name = name
        self.task = task
        self.data_dir = data_dir
        self.hdf5_filepath = hdf5_filepath

        # create a handler for the cache file
        self.hdf5_file = h5py.File(self.hdf5_filepath, 'r', libver='latest')
        self.root_path = '/'

        # make links for all groups (train/val/test/etc) for easier access
        self.sets = tuple(self.hdf5_file['/'].keys())
        for set_name in self.sets:
            setattr(self, set_name, SetLoader(self.hdf5_file[set_name]))

        # fetch list of field names that compose the object list.
        self.object_fields = {}
        for set_name in self.sets:
            data = self.hdf5_file['/{}/object_fields'.format(set_name)].value
            self.object_fields[set_name] = tuple(convert_ascii_to_str(data))

    def get(self, set_name, field, idx=None):
        """Retrieves data from the dataset's hdf5 metadata file.

        This method retrieves the i'th data from the hdf5 file with the
        same 'field' name. Also, it is possible to retrieve multiple values
        by inserting a list/tuple of number values as indexes.

        Parameters
        ----------
        set_name : str
            Name of the set.
        field : str
            Field name.
        idx : int/list/tuple, optional
            Index number of the field. If it is a list, returns the data
            for all the value indexes of that list.

        Returns
        -------
        np.ndarray
            Numpy array containing the field's data.
        list
            List of numpy arrays if using a list of indexes.

        """
        assert set_name, 'Must input a valid set name: {}'.format(set_name)
        assert set_name in self.sets, 'Set {} does not exist for this dataset.' \
                                      .format(set_name)
        assert field, 'Must input a valid field name: {}'.format(field)
        set_obj = getattr(self, set_name)
        return set_obj.get(field, idx)

    def object(self, set_name, idx=None, convert_to_value=False):
        """Retrieves a list of all fields' indexes/values of an object composition.

        Retrieves the data's ids or contents of all fields of an object.

        It basically works as calling the get() method for each individual field
        and then groups all values into a list w.r.t. the corresponding order of
        the fields.

        Parameters
        ----------
        set_name : str
            Name of the set.
        idx : int/list/tuple, optional
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
        assert set_name, 'Must input a valid set name: {}'.format(set_name)
        assert set_name in self.sets, 'Set {} does not exist for this dataset.' \
                                      .format(set_name)
        set_obj = getattr(self, set_name)
        return set_obj.object(idx, convert_to_value)

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
        list
            Returns the size of a field.

        """
        if set_name is None:
            out = {}
            for set_name_ in self.sets:
                set_obj = getattr(self, set_name_)
                out.update({set_name_: set_obj.size(field)})
            return out
        else:
            assert set_name in self.sets, 'Set {} does not exist for this dataset.' \
                                          .format(set_name)
            set_obj = getattr(self, set_name)
            return set_obj.size(field)

    def list(self, set_name=None):
        """List of all field names of a set.

        Parameters
        ----------
        set_name : str, optional
            Name of the set.

        Returns
        -------
        list
            List of all data fields of the dataset.

        """
        if set_name:
            assert set_name in self.sets, 'Set {} does not exist for this dataset.' \
                                          .format(set_name)
            set_obj = getattr(self, set_name)
            return set_obj.list()
        else:
            out = {}
            for set_name_ in self.sets:
                set_obj = getattr(self, set_name_)
                out.update({set_name_: set_obj.list()})
            return out

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

        """
        assert set_name, 'Must input a valid set name: {}'.format(set_name)
        assert set_name in self.sets, 'Set {} does not exist for this dataset.' \
                                      .format(set_name)
        assert field, 'Must input a valid field name: {}'.format(field)
        set_obj = getattr(self, set_name)
        return set_obj.object_field_id(field)

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

        """
        if set_name:
            assert set_name in self.sets, 'Set {} does not exist for this dataset.' \
                                          .format(set_name)
            set_obj = getattr(self, set_name)
            set_obj.info()
        else:
            for set_name in sorted(self.sets):
                set_obj = getattr(self, set_name)
                set_obj.info()

    def __str__(self):
        s = 'DataLoader: "{}" ({} task)' \
            .format(self.db_name, self.task)
        return s

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.sets)
