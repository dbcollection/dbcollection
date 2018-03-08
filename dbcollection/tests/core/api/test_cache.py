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
        "query": 'some_task',
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


@pytest.fixture()
def cache_api_cls(mocker, mocks_init_class, test_data):
    return CacheAPI(
        query=(test_data["query"],),
        delete_cache=test_data["delete_cache"],
        delete_cache_dir=test_data["delete_cache_dir"],
        delete_cache_file=test_data["delete_cache_file"],
        reset_cache=test_data["reset_cache"],
        reset_path_cache=test_data["reset_path_cache"],
        reset_path_downloads=test_data["reset_path_downloads"],
        set_cache_dir=test_data["set_cache_dir"],
        set_downloads_dir=test_data["set_downloads_dir"],
        verbose=test_data["verbose"]
    )


class TestClassCacheAPI:
    """Unit tests for the CacheAPI class."""

    def test_init_with_all_input_agrs(self, mocker, mocks_init_class, test_data):
        cache_api = CacheAPI(query=(test_data["query"],),
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
        assert cache_api.query == (test_data["query"],)
        assert cache_api.delete_cache == test_data["delete_cache"]
        assert cache_api.delete_cache_dir == test_data["delete_cache_dir"]
        assert cache_api.delete_cache_file == test_data["delete_cache_file"]
        assert cache_api.reset_cache == test_data["reset_cache"]
        assert cache_api.reset_path_cache == test_data["reset_path_cache"]
        assert cache_api.reset_path_downloads == test_data["reset_path_downloads"]
        assert cache_api.set_cache_dir == test_data["set_cache_dir"]
        assert cache_api.set_downloads_dir == test_data["set_downloads_dir"]
        assert cache_api.verbose == test_data["verbose"]

    def test_init__raises_error_too_many_input_args(self, mocker):
        with pytest.raises(TypeError):
            CacheAPI(('some_query',), False, False, False, True, True, True,
                     '/some/dir/cache', '/some/dir/cache/downloads', False,
                     'extra field')

    def test_run_query_only(self, mocker, cache_api_cls):
        mock_query = mocker.patch.object(CacheAPI, 'get_matching_metadata_from_cache',
                                         return_value=('some', 'vals'))

        result = cache_api_cls.run()

        assert mock_query.called
        assert result == ('some', 'vals')
