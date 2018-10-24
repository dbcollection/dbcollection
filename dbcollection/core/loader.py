"""
Dataset's metadata loader classes.
"""


import math
import numpy as np
import pandas as pd
import h5py
from dbcollection.utils.string_ascii import convert_ascii_to_str


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
    hdf5_filename : str
        Path of the metadata cache file stored on disk.

    Attributes
    ----------
    dataset : str
        Name of the dataset.
    task : str
        Name of the task.
    data_dir : str
        Path of the dataset's data directory on disk.
    hdf5_filename : str
        Path of the hdf5 metadata file stored on disk.
    hdf5_file : h5py._hl.files.File
        hdf5 file object handler.
    sets : tuple
        List of names of set splits (e.g. train, test, val, etc.)
    columns : dict
        Data field names for each set split.

    """

    def __init__(self, name, task, data_dir, hdf5_filename):
        """Initialize class."""
        assert name, 'Must input a valid dataset name.'
        assert task, 'Must input a valid task name.'
        assert data_dir, 'Must input a valid path for the data directory.'
        assert hdf5_filename, 'Must input a valid path for the cache file.'

        self.dataset = name
        self.task = task
        self.data_dir = data_dir
        self.hdf5_filename = hdf5_filename
        self.hdf5_file = self._load_hdf5_file()
        self.sets = self._get_set_names()
        self._sets_loader = self._get_set_loaders()
        self.columns = self._get_column_names()
        self.types = self._get_types()

    def _load_hdf5_file(self):
        return h5py.File(self.hdf5_filename, 'r', libver='latest')

    def _get_set_names(self):
        return tuple(sorted(self.hdf5_file['/'].keys()))

    def _get_column_names(self):
        """Return a list of the column names that compose the set."""
        columns = {}
        for set_name in self.sets:
            data = self.hdf5_file['/{}/__COLUMNS__'.format(set_name)].value
            columns[set_name] = tuple(convert_ascii_to_str(data))
        return columns

    def _get_types(self):
        """Return a list of the types for each column."""
        pass

    def _get_set_loaders(self):
        """Return a dictionary with list of set loaders."""
        return {set_name: SetLoader(self.hdf5_file[set_name], self.data_dir) for set_name in self.sets}

    def get(self, set_name, index=None, field=None, parse=False):
        """Retrieves data from the dataset's hdf5 metadata file.

        This method retrieves the i'th data from the hdf5 file with the
        same 'field' name. Also, it is possible to retrieve multiple values
        by inserting a list/tuple of number values as indexes.

        Parameters
        ----------
        set_name : str
            Name of the set.
        idx : int/list/tuple, optional
            Index number of the field. If it is a list, returns the data
            for all the value indexes of that list. Default: None.
        field : str, optional
            Name of the data field. Defaul: None.
        parse : bool, optional
            Convert the output data into a string. Default: False.
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
        try:
            return self._sets_loader[set_name].get(index=index, field=field, parse=parse)
        except KeyError:
            self._raise_error_invalid_set_name(set_name)

    def _raise_error_invalid_set_name(self, set_name):
        raise KeyError("'{}' does not exist in the sets list: {}".format(set_name, self.sets))

    def size(self, set_name=None):
        """Size of each setof the dataset .

        Returns the number of the elements of a field.

        Parameters
        ----------
        set_name : str, optional
            Name of the set. Default: None.

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
            return {set_name: self._sets_loader[set_name].size() for set_name in self._sets_loader}
        else:
            try:
                return self._sets_loader[set_name].size()
            except KeyError:
                self._raise_error_invalid_set_name(set_name)

    def list(self, set_name=None):
        """Returns all column names of a set.

        Parameters
        ----------
        set_name : str, optional
            Name of the set. Default: None.

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
            return {set_name: self._sets_loader[set_name].list() for set_name in self._sets_loader}
        else:
            try:
                return self._sets_loader[set_name].list()
            except KeyError:
                self._raise_error_invalid_set_name(set_name)

    def get_column_id(self, set_name, field):
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
            return self._sets_loader[set_name].get_column_id(field)
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
        for set_name in sorted(self._sets_loader):
            self._sets_loader[set_name].info()

    def _print_info_single_set(self, set_name):
        assert set_name
        try:
            self._sets_loader[set_name].info()
        except KeyError:
            self._raise_error_invalid_set_name(set_name)

    def sample(self, set_name, n=1, frac=None, replace=False, random_state=None):
        """Return a random sample of items.

        You can use `random_state` for reproducibility.

        Parameters
        ----------
        set_name : str
            Name of the set.
        n : int, optional
            Number of items from axis to return. Cannot be used with `frac`.
            Default = 1 if `frac` = None.
        frac : float, optional
            Fraction of axis items to return. Cannot be used with `n`.
        replace : boolean, optional
            Sample with or without replacement. Default = False.
        random_state : int or numpy.random.RandomState, optional
            Seed for the random number generator (if int), or numpy RandomState
            object.

        Returns
        -------
        List of values.
        """
        assert set_name
        assert n >= 1
        return self._sets_loader[set_name].sample(n=n, frac=frac, replace=replace, random_state=random_state)

    def __len__(self):
        return len(self._sets_loader)

    def __str__(self):
        s = "DataLoader: {} ('{}' task)".format(self.dataset, self.task)
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
    columns : tuple
        List of all field names of the set contained by the 'object_ids' list.
    nelems : int
        Number of rows in 'object_ids'.

    """

    def __init__(self, hdf5_group, data_dir):
        """Initialize class."""
        assert hdf5_group, 'Must input a valid hdf5 group'
        assert data_dir, 'Must input a valid directory'

        self.hdf5_group = hdf5_group
        self.data_dir = data_dir
        self.set = self._get_set_name()
        self.columns = self._get_column_names()
        self.dtypes = self._get_column_data_types()
        self.lists = self._get_preordered_lists()
        self.num_elements = self._get_num_elements()
        self.shape = np.array([self.num_elements, len(self.columns)])
        self._fields = self._get_field_names()
        self.fields = self._load_hdf5_fields()  # add all hdf5 datasets as data fields
        self._fields_info = []
        self._lists_info = []

    def _get_set_name(self):
        hdf5_object_str = self.hdf5_group.name
        str_split = hdf5_object_str.split('/')
        return str_split[-1]

    def _get_column_names(self):
        columns_data = self.hdf5_group['__COLUMNS__'].value
        output = convert_ascii_to_str(columns_data)
        if type(output) == 'string':
            output = (output,)
        return output

    def _get_column_data_types(self):
        types_data = self.hdf5_group['__TYPES__'].value
        types = convert_ascii_to_str(types_data)
        if type(types) == 'string':
            types = (types,)
        return types

    def _get_preordered_lists(self):
        fields = []
        for field in self.hdf5_group.keys():
            if field.startswith("list_"):
                fields.append(field)
        return fields

    def _get_field_names(self):
        return tuple(self.hdf5_group.keys())

    def _get_num_elements(self):
        return len(self.hdf5_group[self.columns[0]])

    def _load_hdf5_fields(self):
        fields = {}
        for field in self._fields:
            obj_id = self._get_obj_id_field(field)
            fields[field] = FieldLoader(self.hdf5_group[field], obj_id, self.data_dir)
        return fields

    def _get_obj_id_field(self, field):
        if field in self.columns:
            return self.columns.index(field)
        else:
            return None

    def get(self, index=None, field=None, parse=False):
        """Retrieves data from the dataset's hdf5 metadata file.

        This method retrieves the i'th data from the hdf5 file with the
        same 'field' name. Also, it is possible to retrieve multiple values
        by inserting a list/tuple of number values as indexes.

        Parameters
        ----------
        index : int | list | tuple, optional
            Index number of the field. If it is a list, returns the data
            for all the value indexes of that list. Default: None.
        field : str
            Field name.
        parse : bool, optional
            Convert the output data into its original format.
            Default: False.

        Returns
        -------
        np.ndarray | list | str
            Numpy array containing the field's data.
            If convert_to_str is set to True, it returns a string
            or list of strings.
        """
        if field:
            assert field in self.columns + self.lists, "'{}' does not exist in the '{}' set.".format(field, self.set)
            data = self._get_field_data(field, index, parse)
        else:
            if index is None:
                index = list(range(len(self)))
            else:
                if isinstance(index, int):
                    index = [index]
            data = []
            for idx in index:
                data.append([self._get_field_data(field, idx, parse) for field in self.columns])
        if len(data) == 1:
            return data[0]
        else:
            return data

    def _get_field_data(self, field, index, parse):
        return self.fields[field].get(index=index, parse=parse)

    def size(self):
        """Size of the set.

        Returns the number of the elements of the set.

        Returns
        -------
        int
            Number of elements in the set.
        """
        return self.num_elements

    def list(self):
        """List of all column names.

        Returns
        -------
        list
            List of all data fields of the dataset.

        """
        return self.columns + self.lists

    def get_column_id(self, field):
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
            return self.fields[field].column_id
        except KeyError:
            raise KeyError('\'{}\' is not contained in \'__COLUMNS__\'.'.format(field))

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
            "type": 'dtype = {}'.format(str(self.fields[field].dtype))
        }

    def _get_field_info(self, field):
        assert field
        s_obj = ''
        if field in self.columns:
            obj_id = self.get_column_id(field)
            s_obj = "(in 'object_ids', position = {})".format(obj_id)

        return {
            "name": str(field),
            "shape": 'shape = {}'.format(str(self.fields[field].shape)),
            "type": 'dtype = {}'.format(str(self.fields[field].dtype)),
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

    def sample(self, n=1, frac=None, replace=False, random_state=None):
        """Return a random sample of items.

        You can use `random_state` for reproducibility.

        Parameters
        ----------
        n : int, optional
            Number of items from axis to return. Cannot be used with `frac`.
            Default = 1 if `frac` = None.
        frac : float, optional
            Fraction of axis items to return. Cannot be used with `n`.
        replace : boolean, optional
            Sample with or without replacement. Default = False.
        random_state : int or numpy.random.RandomState, optional
            Seed for the random number generator (if int), or numpy RandomState
            object.

        Returns
        -------
        List of values.
        """
        assert n >= 1
        idx = generate_random_indices(len(self), n, frac=frac, replace=replace,
                                      random_state=random_state)
        if len(idx) == 1:
            samples = self.get(int(idx))
        else:
            samples = [self.get(int(i)) for i in idx]
        return samples

    def head(self, n=5):
        """
        Return the first elements of a field.

        This function is mainly useful to preview the values of the
        field without displaying all of the data data.

        Parameters
        ----------
        n : int, optional
            Number of values to return. Default: 5.
            It must be greater than 0.

        Returns
        -------
        np.ndarray
            Subset of the original field with the first ``n`` values.
        """
        assert n > 0, "Sample size must be greater than 0: {}.".format(n)
        if n == 1:
            return self.get(0)
        else:
            return self.get(list(range(n)))

    def tail(self, n=5):
        """Returns last n rows of each group.

        Parameters
        ----------
        n : int, optional
            Number of values to return. Default: 5.
            It must be greater than 0.

        Returns
        -------
        np.ndarray
            Subset of the original field with the last ``n`` values.
        """
        assert n > 0, "Sample size must be greater than 0: {}.".format(n)
        size = len(self)
        return self.get(list(range(size - n, size)))

    def to_pandas(self, columns=None):
        """Converts the field into a Pandas Series.

        Parameters
        ----------
        columns : str, optional
            Name to give to the Pandas DataFrame's columns.
            Default: None.

        Returns
        -------
        pandas.DataFrame
        """
        if columns is None:
            columns = self.columns
        df = pd.DataFrame(data=self.get(), columns=columns)
        return df

    def __len__(self):
        """
        Returns
        -------
        int
            Number of elements

        """
        return self.num_elements

    def __str__(self):
        return 'SetLoader: set<{}>, len<{}>'.format(self.set, self.num_elements)

    def __repr__(self):
        return str(self)


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
        Position of the field in '__COLUMNS__'.

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

    def __init__(self, hdf5_field, column_id=None, data_dir=None):
        """Initialize class."""
        assert hdf5_field, 'Must input a valid hdf5 dataset.'
        self.data = hdf5_field
        self.data_dir = data_dir
        self.hdf5_handler = hdf5_field
        self.set = self._get_set_name()
        self.name = self._get_field_name()
        self.shape = hdf5_field.shape
        self.dtype = hdf5_field.dtype
        self.fillvalue = hdf5_field.fillvalue
        self.column_id = column_id

    def _get_set_name(self):
        hdf5_object_str = self._get_hdf5_object_str()
        return hdf5_object_str[1]

    def _get_field_name(self):
        hdf5_object_str = self._get_hdf5_object_str()
        return hdf5_object_str[-1]

    def _get_hdf5_object_str(self):
        return self.hdf5_handler.name.split('/')

    def get(self, index=None, parse=False):
        """Retrieves data of the field from the dataset's hdf5 metadata file.

        This method retrieves the i'th data from the hdf5 file. Also, it is
        possible to retrieve multiple values by inserting a list/tuple of
        number values as indexes.

        Parameters
        ----------
        index : int | list | tuple, optional
            Index number of the field. If it is a list, returns the data
            for all the value indexes of that list.
            Default: None.
        parse : bool, optional
            Convert the output data into its original format.
            Default: False.

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
            data = self.data.value
        else:
            data = self._get_range_idx(index)
        if parse:
            data = convert_ascii_to_str(data)
        return data

    def _get_range_idx(self, idx):
        """Return a slice of the data array.

        Parameters
        ----------
        index : int | list | tuple
            Index number of the field. If it is a list, returns the
            data for all the value indexes of that list.

        Returns
        -------
        h5py.Dataset
            Returns the data for a single or set of indexes.
        """
        assert idx is not None
        if isinstance(idx, int):
            return self.data[idx]
        else:
            size = len(idx)
            assert len(idx) > 0
            if size > 1:
                return self.data[sorted(set(idx))]
            elif size == 1:
                return self.data[idx[0]]
            else:
                raise Exception("Invalid index range: {idx}".format(idx=idx))

    def size(self):
        """Size of the field.

        Returns the number of the elements of the field.

        Returns
        -------
        tuple
            Returns the size of the field.

        """
        return self.shape

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
                      .format(self.name, str(self.shape), str(self.dtype), self.obj_id))
            else:
                print('Field: {},  shape = {},  dtype = {}'
                      .format(self.name, str(self.shape), str(self.dtype)))
        else:
            return {
                "name": self.name,
                "shape": self.shape,
                "dtype": self.dtype
            }

    def sample(self, n=1, frac=None, replace=False, random_state=None):
        """Return a random sample of items.

        You can use `random_state` for reproducibility.

        Parameters
        ----------
        n : int, optional
            Number of items from axis to return. Cannot be used with `frac`.
            Default = 1 if `frac` = None.
        frac : float, optional
            Fraction of axis items to return. Cannot be used with `n`.
        replace : boolean, optional
            Sample with or without replacement. Default = False.
        random_state : int or numpy.random.RandomState, optional
            Seed for the random number generator (if int), or numpy RandomState
            object.

        Returns
        -------
        List of values.
        """
        assert n >= 1
        idx = generate_random_indices(len(self), n, frac=frac, replace=replace,
                                      random_state=random_state)
        return np.array([self.get(int(i)) for i in idx])

    def head(self, n=5):
        """
        Return the first elements of a field.

        This function is mainly useful to preview the values of the
        field without displaying all of the data data.

        Parameters
        ----------
        n : int, optional
            Number of values to return. Default: 5.
            It must be greater than 0.

        Returns
        -------
        np.ndarray
            Subset of the original field with the first ``n`` values.
        """
        assert n > 0, "Sample size must be greater than 0: {}.".format(n)
        return self.get(list(range(0, n)))

    def tail(self, n=5):
        """Returns last n rows of each group.

        Parameters
        ----------
        n : int, optional
            Number of values to return. Default: 5.
            It must be greater than 0.

        Returns
        -------
        np.ndarray
            Subset of the original field with the last ``n`` values.
        """
        assert n > 0, "Sample size must be greater than 0: {}.".format(n)
        size = len(self)
        return self.get(list(range(size - n, size)))

    def to_pandas(self, name=None):
        """Converts the field into a Pandas Series.

        Parameters
        ----------
        name : str, optional
            Name to give to the Pandas Series. Default: None.

        Returns
        -------
        pandas.Series
        """
        if name is None:
            name = self.name
        return pd.Series(self.data, name=name)

    @property
    def values(self):
        return self.hdf5_handler.value

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
        return 'FieldLoader: ' + self.data.__str__()

    def __repr__(self):
        return str(self)


def generate_random_indices(length, n, frac=None, replace=None, random_state=None):
    """Generates random indices."""
    if random_state:
        np.random.seed(random_state)
    if frac:
        num_samples = math.floor(frac * length)
    else:
        num_samples = n
    if replace:
        idx = np.random.choice(length, num_samples)
    else:
        idx = np.random.permutation(length)[:num_samples]
    return idx
