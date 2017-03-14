"""
HDF5 storage class.
"""


import os
import h5py


class StorageHDF5:
    """ Manage a HDF5 file """

    def __init__(self, filename, mode):
        """Initialize class.

        Parameters
        ----------
        filename : str
            File name + path for the target metadata file.
        mode : str
            File openining mode: r, r+, w , w+, x, a
        """
        self.fname = filename
        self.mode = mode

        # open a file (read or write mode)
        self.storage = self.open(filename, mode)


    def open(self, name, mode, version='latest'):
        """Open a hdf5 file.

        Parameters
        ----------
        name : str
            File name + path on disk.
        mode : str
            File openining mode: r, r+, w , w+, x, a.
        version : str
            HDF5 file version.

        Returns
        -------
        HDF5 file
            Object handler of the opened file.

        Raises
        ------
            None
        """
        return h5py.File(name, mode, libver=version)


    def close(self):
        """Close the file.

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
        self.storage.close()


    def is_group(self, name):
        """Check if the group name exists.

        Parameters
        ----------
        name : str
            Name of the group

        Returns
        -------
        bool
            If group name exists, then return True. Else return False.

        Raises
        ------
            None
        """
        return name in self.storage.keys()


    def add_group(self, group_name):
        """Create a group in the hdf5 file.

        Parameters
        ----------
        group_name : str
            Name of the group to add.

        Returns
        -------
            None

        Raises
        ------
        ValueError
            If a group already exists.
        """
        try:
            self.storage.create_group(group_name)
        except ValueError: #group already exists
            raise ValueError('Error creating a group.')


    def delete_group(self, name):
        """Delete a group.

        Parameters
        ----------
        name : str
            Name of the group to delete.

        Returns
        -------
            None

        Raises
        ------
            None
        """
        if self.is_group(name):
            del self.storage[name]


    def parse_str(self, group, field_name):
        """Concatenate two strings.

        Parameters
        ----------
        group : str
            Name of a group.
        field_name : str
            Name of a field/sub-group.

        Returns
        -------
        str
            Name of the field/sub-group relative to the root path.

        Raises
        ------
            None
        """
        if group == '/':
            return field_name
        else:
            return group + '/' + field_name


    def is_data(self, group, field_name):
        """Check if the field_name exists.

        Parameters
        ----------
        group : str
            Name of a group.
        field_name : str
            Name of a field/sub-group.

        Returns
        -------
        bool
            If field exists, return True. Else return False.

        Raises
        ------
            None
        """
        # check if the group exists
        if not self.is_group(group):
            #raise Exception('Group name not found: ' + group)
            return False

        return field_name in self.storage[group].keys()


    def add_data(self, group, field_name, data, dtype=None):
        """Add data to a group + field in a hdf5 file.

        Parameters
        ----------
        group : str
            Name of a group.
        field_name : str
            Name of a field/sub-group.
        dtype : numpy.dtype
            Data type of a numpy array.

        Returns
        -------
            None

        Raises
        ------
            None
        """
        if not self.is_group(group):
            self.add_group(group)

        # concatenate string so it is easier to add fields to the h5py file
        field_str = self.parse_str(group, field_name)

        # check if a data convertion is required
        if not dtype is None:
            data = data.astype(dtype)

        # add data to the file
        self.storage.create_dataset(field_str, data=data)


    def delete_data(self, group, field_name):
        """Delete a data field.

        Parameters
        ----------
        group : str
            Name of a group.
        field_name : str
            Name of a field/sub-group.

        Returns
        -------
            None

        Raises
        ------
            None
        """
        if self.is_data(group, field_name):
            # parse string
            field_str = self.parse_str(group, field_name)

            # delete data field
            del self.storage[field_str]
