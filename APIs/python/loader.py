#!/usr/bin/env python
# Copyright (C) 2017, Farrajota @ https://github.com/farrajota
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


"""
Dataset loader class.
"""


class Loader:
    """ HDF5 data loading class """

    def __init__(self, name):
        """
        Initialize class.
        """


    def get(self, field_name, id):
        """
        Retrieve the 'i'th' data from the field 'field_name' into a list.

        Parameters:
        -----------
            - field_name: field name identifier [Type=String]
		    - id: index number of the field. If it is a list, returns the data for all the value indexes of that list [Type=long/List]
        Returns:
        --------
            returns a list filled with data.
        """
        pass



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



class DataLoader:
    """ Dataset loader """

    def __init__(self, name):
        """
        Initialize class.
        """
        self.data = Loader(name)
        self.train = self.data['train']
        self.val = self.data['val']
        self.test = self.data['test']

