"""
Test dbcollection core API: info.
"""


import pytest

from dbcollection.core.api.info import info, InfoAPI


@pytest.fixture()
def mocks_init_class(mocker):
    mock_cache = mocker.patch.object(InfoAPI, "get_cache_manager", return_value=True)
    return [mock_cache]


def assert_mock_call(mocks):
    for mock in mocks:
        assert mock.called


@pytest.fixture()
def test_data():
    return {
        "by_dataset": ('datasetA', 'datasetB'),
        "by_task": ('taskA', 'taskB'),
        "by_category": ('categoryA', 'categoryB'),
        "show_info": True,
        "show_datasets": True,
        "show_categories": True,
        "show_system": True,
        "show_available": True
    }


class TestCallInfo:
    """Unit tests for the core api info method."""

    def test_call_with_all_input_args(self, mocker, mocks_init_class, test_data):
        mock_run = mocker.patch.object(InfoAPI, "run")

        info(test_data['by_dataset'],
             test_data['by_task'],
             test_data['by_category'],
             test_data['show_info'],
             test_data['show_datasets'],
             test_data['show_categories'],
             test_data['show_system'],
             test_data['show_available'])

        assert mock_run.called

    def test_call_with_named_input_args(self, mocker, mocks_init_class, test_data):
        mock_run = mocker.patch.object(InfoAPI, "run")

        info(by_dataset=test_data['by_dataset'],
             by_task=test_data['by_task'],
             by_category=test_data['by_category'],
             show_info=test_data['show_info'],
             show_datasets=test_data['show_datasets'],
             show_categories=test_data['show_categories'],
             show_system=test_data['show_system'],
             show_available=test_data['show_available'])

        assert mock_run.called

    def test_call_without_optional_input_args(self, mocker):
        mock_run = mocker.patch.object(InfoAPI, "run")

        info()

        assert mock_run.called

    def test_call__raises_error_too_many_args(self, mocker, test_data):
        with pytest.raises(TypeError):
            info(test_data['by_dataset'],
                 test_data['by_task'],
                 test_data['by_category'],
                 test_data['show_info'],
                 test_data['show_datasets'],
                 test_data['show_categories'],
                 test_data['show_system'],
                 test_data['show_available'],
                 'extra_input')


class TestClassInfoAPI:
    """Unit tests for the InfoAPI class."""

    def test_init_with_all_input_args(self, mocker, mocks_init_class, test_data):
        info_api = InfoAPI(by_dataset=test_data['by_dataset'],
                           by_task=test_data['by_task'],
                           by_category=test_data['by_category'],
                           show_info=test_data['show_info'],
                           show_datasets=test_data['show_datasets'],
                           show_categories=test_data['show_categories'],
                           show_system=test_data['show_system'],
                           show_available=test_data['show_available'])

        assert_mock_call(mocks_init_class)
        assert info_api.by_dataset == test_data['by_dataset']
        assert info_api.by_task == test_data['by_task']
        assert info_api.by_category == test_data['by_category']
        assert info_api.show_info == test_data['show_info']
        assert info_api.show_datasets == test_data['show_datasets']
        assert info_api.show_categories == test_data['show_categories']
        assert info_api.show_system == test_data['show_system']
        assert info_api.show_available == test_data['show_available']

    def test_init__raises_error_no_input_args(self, mocker):
        with pytest.raises(TypeError):
            InfoAPI()

    def test_init__raises_error_too_many_input_args(self, mocker):
        with pytest.raises(TypeError):
            InfoAPI(('some_db',), ('some_task',), ('some_category',),
                    False, True, False, True, False, 'extra_input')

    def test_init__raises_error_missing_one_input_arg(self, mocker):
        with pytest.raises(TypeError):
            InfoAPI(('some_db',), ('some_task',), ('some_category',),
                    False, True, False, True)

    @pytest.mark.parametrize('call_show_info, call_show_dataset, call_show_category, ' +
                             'call_show_system_dbs, call_show_available_dbs', [
        (True, False, False, False, False),
        (False, True, False, False, False),
        (False, False, True, False, False),
        (False, False, False, True, False),
        (False, False, False, False, True),
        (True, True, True, False, False),  # all cache active
        (False, False, False, True, True)
    ])
    def test_run(self, mocker, mocks_init_class, test_data, call_show_info, call_show_dataset,
                 call_show_category, call_show_system_dbs, call_show_available_dbs):
        mock_show_info = mocker.patch.object(InfoAPI, 'display_info_section_from_cache')
        mock_show_dataset = mocker.patch.object(InfoAPI, 'display_dataset_section_from_cache')
        mock_show_category = mocker.patch.object(InfoAPI, 'display_category_section_from_cache')
        mock_show_system = mocker.patch.object(InfoAPI, 'display_registered_datasets_in_cache')
        mock_show_available = mocker.patch.object(InfoAPI, 'display_available_datasets_supported_by_dbcollection')

        info_api = InfoAPI(by_dataset=test_data['by_dataset'],
                           by_task=test_data['by_task'],
                           by_category=test_data['by_category'],
                           show_info=call_show_info,
                           show_datasets=call_show_dataset,
                           show_categories=call_show_category,
                           show_system=call_show_system_dbs,
                           show_available=call_show_available_dbs)

        info_api.run()

        assert mock_show_info.called == call_show_info
        assert mock_show_dataset.called == call_show_dataset
        assert mock_show_category.called == call_show_category
        assert mock_show_system.called == call_show_system_dbs
        assert mock_show_available.called == call_show_available_dbs

    @pytest.mark.parametrize('call_show_info, call_show_dataset, call_show_category, ' +
                             'call_show_system_dbs, call_show_available_dbs', [
        (True, True, True, True, False),
        (True, True, True, False, True),
        (True, True, True, True, True)
    ])
    def test_run_cache_prints_disabled_when_using_show_systemor_show_available(self, mocker, mocks_init_class,
            call_show_info, call_show_dataset, call_show_category, call_show_system_dbs, call_show_available_dbs):
        mock_show_info = mocker.patch.object(InfoAPI, 'display_info_section_from_cache')
        mock_show_dataset = mocker.patch.object(InfoAPI, 'display_dataset_section_from_cache')
        mock_show_category = mocker.patch.object(InfoAPI, 'display_category_section_from_cache')
        mock_show_system = mocker.patch.object(InfoAPI, 'display_registered_datasets_in_cache')
        mock_show_available = mocker.patch.object(InfoAPI, 'display_available_datasets_supported_by_dbcollection')

        info_api = InfoAPI(by_dataset=('', ),
                           by_task=('', ),
                           by_category=('', ),
                           show_info=call_show_info,
                           show_datasets=call_show_dataset,
                           show_categories=call_show_category,
                           show_system=call_show_system_dbs,
                           show_available=call_show_available_dbs)

        info_api.run()

        assert not mock_show_info.called
        assert not mock_show_dataset.called
        assert not mock_show_category.called
        assert mock_show_system.called == call_show_system_dbs
        assert mock_show_available.called == call_show_available_dbs
