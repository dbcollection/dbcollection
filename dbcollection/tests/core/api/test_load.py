"""
Test dbcollection core API: load.
"""


import pytest

from dbcollection.core.api.load import load, LoadAPI


class TestCallLoad:
    """Unit tests for the core api load method."""

    def test_call_with_dataset_name(self, mocker):
        pass

    def test_call_with_all_inputs(self, mocker):
        pass

    def test_call__raises_error_no_inputs(self, mocker):
        with pytest.raises(TypeError):
            load()

class TestClassLoadAPI:
    """Unit tests for the LoadAPI class."""
