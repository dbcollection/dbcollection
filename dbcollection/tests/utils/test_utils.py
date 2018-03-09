"""
Test dbcollection utils.
"""


import pytest

from dbcollection.utils import nested_lookup


class TestNestedLookup:
    """Unit tests for the nested_lookup method."""

    @pytest.mark.parametrize(
        "key, data, expected",
        [('keyA', {"keyA": 'valA', "keyB": {"keyA": 'valC'}}, ['valA', 'valC']),
         ('keyB', {"keyA": 'valA', "keyB": {"keyA": 'valC'}}, [{"keyA": 'valC'}]),
         ('keyC', {"keyA": 'valA', "keyB": {"keyA": 'valC'}}, [])]
    )
    def test_retrieve_values_from_key(self, key, data, expected):
        result = list(nested_lookup(key, data))

        assert sorted(result) == sorted(expected)

    def test_retrieve_values_from_key_case_insensitive(self):
        data = {'first_name': 'jose', 'second_NAME': 'lopes'}

        result = list(nested_lookup('name', data, True))

        assert sorted(result) == ['jose', 'lopes']

    def test_raises_error_missing_input_args(self):
        with pytest.raises(TypeError):
            nested_lookup()

    def test_raises_error_missing_one_input_args(self):
        with pytest.raises(TypeError):
            nested_lookup('some_key')
