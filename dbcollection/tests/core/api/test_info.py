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

    def test_call(self, mocker, mocks_init_class, test_data):
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

    def test_call_with_named_args(self, mocker, mocks_init_class, test_data):
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

    def test_call_without_optional_args(self, mocker):
        mock_run = mocker.patch.object(InfoAPI, "run")

        info()

        assert mock_run.called

    def test_call__raises_error_too_many_input_args(self, mocker, test_data):
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

    def test_init_with_all_input_args(self, mocker):
        pass

    def test_init__raises_error_no_input_args(self, mocker):
        pass

    def test_init__raises_error_too_many_input_args(self, mocker):
        pass

    def test_init__raises_error_missing_one_input_arg(self, mocker):
        pass

    def test_run(self, mocker):
        pass
