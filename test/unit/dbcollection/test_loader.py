"""
dbcollection/loader.py unit testing.
"""


import unittest
from unittest import mock
from unittest.mock import patch, mock_open

dir_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.abspath(os.path.join(dir_path,'..','..','..','dbcollection'))
sys.path.append(lib_path)
import loader


#-----------------------
# Unit Test definitions
#-----------------------

class ManagerHDF5Test(unittest.TestCase):
    """
    Test class.
    """

    def setUp(self):
        """
        Initialize class.
        """
        self.widget = Widget('widget')

    def test_one(self):
        """
        Test one.
        """
        self.assertEqual(self.widget.size(), 1,
             'incorrect default size')

    def test_two(self):
        """
        Test two.
        """
        self.assertEqual(self.widget.size(), 2,
             'incorrect default size')


class LoaderTest(unittest.TestCase):
    """
    Test class.
    """

    def setUp(self):
        """
        Initialize class.
        """
        self.widget = Widget('widget')

    def test_one(self):
        """
        Test one.
        """
        self.assertEqual(self.widget.size(), 1,
             'incorrect default size')

    def test_two(self):
        """
        Test two.
        """
        self.assertEqual(self.widget.size(), 2,
             'incorrect default size')

#----------------
# Run Test Suite
#----------------

def main(level=1):
    unittest.main(verbosity=level)

if __name__ == '__main__':
    main()
