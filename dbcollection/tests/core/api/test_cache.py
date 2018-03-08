"""
Test dbcollection core API: cacbe.
"""


import pytest

from dbcollection.core.api.cache import cache, CacheAPI


@pytest.fixture()
def mocks_init_class(mocker):
    mock_cache = mocker.patch.object(CacheAPI, "get_cache_manager", return_value=True)
    return [mock_cache]


def assert_mock_call(mocks):
    for mock in mocks:
        assert mock.called


@pytest.fixture()
def test_data():
    return {
        "query": ('some_task', 'some_dataset'),
        "delete_cache": False,
        "delete_cache_dir": True,
        "delete_cache_file": True,
        "reset_cache": False,
        "reset_path_cache": True,
        "reset_path_downloads": True,
        "set_cache_dir": '/some/dir/cache',
        "set_downloads_dir": '/some/dir/cache/downloads',
        "verbose": True
    }


class TestCallCache:
    """Unit tests for the core api cache method."""

    def test_call_with_all_input_args(self, mocker, mocks_init_class, test_data):
        mock_run = mocker.patch.object(CacheAPI, "run")

        cache(test_data["query"],
              test_data["delete_cache"],
              test_data["delete_cache_dir"],
              test_data["delete_cache_file"],
              test_data["reset_cache"],
              test_data["reset_path_cache"],
              test_data["reset_path_downloads"],
              test_data["set_cache_dir"],
              test_data["set_downloads_dir"],
              test_data["verbose"])

        assert_mock_call(mocks_init_class)
        assert mock_run.called

    def test_call_with_named_input_args(self, mocker, mocks_init_class, test_data):
        mock_run = mocker.patch.object(CacheAPI, "run")

        cache(query=test_data["query"],
              delete_cache=test_data["delete_cache"],
              delete_cache_dir=test_data["delete_cache_dir"],
              delete_cache_file=test_data["delete_cache_file"],
              reset_cache=test_data["reset_cache"],
              reset_path_cache=test_data["reset_path_cache"],
              reset_path_downloads=test_data["reset_path_downloads"],
              set_cache_dir=test_data["set_cache_dir"],
              set_downloads_dir=test_data["set_downloads_dir"],
              verbose=test_data["verbose"])

        assert_mock_call(mocks_init_class)
        assert mock_run.called

    def test_call_without_optional_input_args(self, mocker, mocks_init_class):
        mock_run = mocker.patch.object(CacheAPI, "run")

        cache()

        assert_mock_call(mocks_init_class)
        assert mock_run.called

    def test_call__raises_error_too_many_args(self, mocker, test_data):
        with pytest.raises(TypeError):
            cache(test_data["query"],
                  test_data["delete_cache"],
                  test_data["delete_cache_dir"],
                  test_data["delete_cache_file"],
                  test_data["reset_cache"],
                  test_data["reset_path_cache"],
                  test_data["reset_path_downloads"],
                  test_data["set_cache_dir"],
                  test_data["set_downloads_dir"],
                  test_data["verbose"],
                  'extra_input')


class TestClassCacheAPI:
    """Unit tests for the CacheAPI class."""

    def test_init_with_all_input_agrstest_init_with_all_input_agrs(self, mocker):
        pass

    def test_init__raises_error_no_input_args(self, mocker):
        pass

    def test_init__raises_error_too_many_input_args(self, mocker):
        pass

    def test_init__raises_error_missing_one_input_arg(self, mocker):
        pass

    def test_run(self, mocker):
        pass
