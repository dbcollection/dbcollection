"""
Test dbcollection utils.
"""


import pytest

from dbcollection.utils import (
    nested_lookup,
    merge_dicts
)


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


class TestMergeDicts:
    """Unit tests for the merge_dicts method."""

    def test_merge_two_dicts(self):
        dict1 = {4: ['some', 'data', 'here'], 1:{"a":"A"},2:{"b":"B"},3:{'d': {'Y':2, 'U':(3,2,1), 4: ('stuff')}}}
        dict2 = {2:{"c":"C"},3:{"d":"D"}}

        result = merge_dicts(dict1, dict2)

        assert sorted(dict(result)) == sorted({1: {'a': 'A'}, 2: {'b': 'B', 'c': 'C'}, 3: {'d': {'Y': 2, 4: 'stuff', 'X': 1, 'U': (3, 2, 1)}}, 4: ['some', 'data', 'here']})

    def test_raises_error_missing_input_args(self):
        with pytest.raises(TypeError):
            merge_dicts()

    def test_raises_error_missing_one_input_args(self):
        with pytest.raises(TypeError):
            merge_dicts({1:1})

    def test_raises_error_missing_too_many_input_args(self):
        with pytest.raises(TypeError):
            merge_dicts({1:1}, {2:2}, {3:3})

