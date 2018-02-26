"""
Test dbcollection's metadata handling methods/classes.
"""


import pytest

from dbcollection.core.api.metadata import MetadataConstructor


class TestMetadataConstructor:
    """Unit tests for the MetadataConstructor class."""

    def test_init_class(self, mocker):
        mock_get_dataset = mocker.patch.object(MetadataConstructor, 'get_dataset_metadata_from_database', return_value=True)
        mock_get_metadata = mocker.patch.object(MetadataConstructor, 'get_metadata_datasets', return_value=True)

        metadata = MetadataConstructor('some_db')

        assert mock_get_dataset.called
        assert mock_get_metadata.called
        assert metadata.name == 'some_db'

    def test_init_class__raise_error_missing_inputs(self, mocker):
        with pytest.raises(TypeError):
            MetadataConstructor()

    def test_init_class__raise_error_too_many_inputs(self, mocker):
        with pytest.raises(TypeError):
            MetadataConstructor('too', 'many', 'inputs')

    #def test_get_dataset_metadata_from_database(self, mocker):
    #    name =
