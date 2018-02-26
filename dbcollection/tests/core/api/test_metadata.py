"""
Test dbcollection's metadata handling methods/classes.
"""


import pytest

from dbcollection.core.api.metadata import MetadataConstructor


@pytest.fixture()
def metadata_cls(mocker):
    dataset, dummy_metadata = test_metadata()
    mocker.patch.object(MetadataConstructor,
                        'get_metadata_datasets',
                        return_value=dummy_metadata)
    metadata = MetadataConstructor(dataset)
    return metadata


def test_metadata():
    dataset = 'some_db'
    dummy_metadata_dataset = {
        dataset: {
            "default_task": "some_task",
            "tasks": ["taskA", "taskB", "taskC"],
            "constructor": 'dummy_constructor'
        }
    }
    return dataset, dummy_metadata_dataset


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
            MetadataConstructor('too many', 'inputs')

    def test_get_dataset_metadata_from_existing_database(self, mocker, metadata_cls):
        dataset, dummy_metadata_dataset = test_metadata()

        result = metadata_cls.get_dataset_metadata_from_database(dataset)

        assert result == dummy_metadata_dataset[dataset]

    def test_get_dataset_metadata_from_database__raises_error_invalid_dataset(self, mocker, metadata_cls):
        with pytest.raises(KeyError):
            metadata_cls.get_dataset_metadata_from_database('unknown_dataset')

    def test_get_dataset_metadata_from_database__raises_error_missing_input(self, mocker, metadata_cls):
        with pytest.raises(TypeError):
            metadata_cls.get_dataset_metadata_from_database()

    def test_get_dataset_metadata_from_database__raises_error_too_many_input(self, mocker, metadata_cls):
        with pytest.raises(TypeError):
            metadata_cls.get_dataset_metadata_from_database('too many', 'inputs')

    def test_get_default_task(self, mocker, metadata_cls):
        dataset, dummy_metadata_dataset = test_metadata()

        assert metadata_cls.get_default_task() == dummy_metadata_dataset[dataset]['default_task']

    def test_get_default_task__raises_error_has_inputs(self, mocker, metadata_cls):
        with pytest.raises(TypeError):
            metadata_cls.get_default_task('some_input')

    @pytest.mark.parametrize('task', ['', 'default'])
    def test_parse_task_name_return_default_task_name(self, mocker, metadata_cls, task):
        mocker.patch.object(MetadataConstructor, 'get_default_task', return_value='some_default_task_name')

        assert metadata_cls.parse_task_name(task) == 'some_default_task_name'

    def test_parse_task_name_return_input_task_name(self, mocker, metadata_cls):
        assert metadata_cls.parse_task_name('some_task') == 'some_task'

    def test_parse_task_name__raises_error_missing_input(self, mocker, metadata_cls):
        with pytest.raises(TypeError):
            metadata_cls.parse_task_name()

    def test_parse_task_name__raises_error_invalid_input(self, mocker, metadata_cls):
        with pytest.raises(AssertionError):
            metadata_cls.parse_task_name(None)

    def test_parse_task_name__raises_error_too_many_input(self, mocker, metadata_cls):
        with pytest.raises(TypeError):
            metadata_cls.parse_task_name('', '')

    def test_get_tasks(self, mocker, metadata_cls):
        dataset, dummy_metadata_dataset = test_metadata()

        result = metadata_cls.get_tasks()

        assert result == dummy_metadata_dataset[dataset]['tasks']

    def test_get_tasks__raises_error_too_many_input(self, mocker, metadata_cls):
        with pytest.raises(TypeError):
            metadata_cls.get_tasks('input')

    def test_get_constructor(self, mocker, metadata_cls):
        dataset, dummy_metadata_dataset = test_metadata()

        result = metadata_cls.get_constructor()

        assert result == dummy_metadata_dataset[dataset]['constructor']

    def test_get_constructor__raises_error_too_many_input(self, mocker, metadata_cls):
        with pytest.raises(TypeError):
            metadata_cls.get_constructor('input')
