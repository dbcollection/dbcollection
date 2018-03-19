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


@pytest.fixture()
def mock_get_cache_dir(mocker):
    return mocker.patch.object(CacheAPI, 'get_cache_dir', return_value='/some/dir/cache')


@pytest.fixture()
def mock_get_cache_filename(mocker):
    return mocker.patch.object(CacheAPI, 'get_cache_filename', return_value='/some/dir/dbcollection.json')


class TestClassCacheAPI:
    """Unit tests for the CacheAPI class."""

    def test_init_with_all_input_args(self, mocker, mocks_init_class, test_data):
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

    def test_init__raises_error_no_input_args(self, mocker):
        with pytest.raises(TypeError):
            CacheAPI()

    def test_init__raises_error_too_many_input_args(self, mocker):
        with pytest.raises(TypeError):
            CacheAPI(('some_query',), False, False, False, True, True, True,
                     '/some/dir/cache', '/some/dir/cache/downloads', False,
                     'extra field')

    @pytest.mark.parametrize('call_query, call_rm_cache_dir, call_rm_cache_file, call_reset_cache, call_reset_cache_path, ' +
                             'call_reset_download_path, call_set_cache_path, call_set_download_path', [
                             (True, False, False, False, False, False, False, False),
                             (False, True, False, False, False, False, False, False),
                             (False, False, True, False, False, False, False, False),
                             (False, False, False, True, False, False, False, False),
                             (False, False, False, False, True, False, False, False),
                             (False, False, False, False, False, True, False, False),
                             (False, False, False, False, False, False, True, False),
                             (False, False, False, False, False, False, False, True),
                             (False, True, True, False, False, False, False, False)
                            ])
    def test_run(self, mocker, cache_api_cls, mock_get_cache_dir, mock_get_cache_filename,
                 call_query, call_rm_cache_dir, call_rm_cache_file, call_reset_cache,
                 call_reset_cache_path, call_reset_download_path,
                 call_set_cache_path, call_set_download_path):
        mock_query = mocker.patch.object(CacheAPI, 'get_matching_metadata_from_cache',
                                         return_value=('some', 'vals'))
        mock_remove_cache_dir = mocker.patch.object(CacheAPI, 'remove_cache_dir_from_disk')
        mock_remove_cache_file = mocker.patch.object(CacheAPI, 'remove_cache_file_from_disk')
        mock_reset_cache = mocker.patch.object(CacheAPI, 'reset_cache_file')
        mock_reset_cache_path = mocker.patch.object(CacheAPI, 'reset_cache_dir_path')
        mock_reset_download_path = mocker.patch.object(CacheAPI, 'reset_download_dir_path')
        mock_get_download_dir = mocker.patch.object(CacheAPI, 'get_download_dir', return_value='/some/dir/downloads')
        mock_set_cache_path = mocker.patch.object(CacheAPI, 'set_cache_dir_path')
        mock_set_download_path = mocker.patch.object(CacheAPI, 'set_download_dir_path')

        if not call_query: cache_api_cls.query = ()
        cache_api_cls.delete_cache_dir = call_rm_cache_dir
        cache_api_cls.delete_cache_file = call_rm_cache_file
        cache_api_cls.reset_cache = call_reset_cache
        cache_api_cls.reset_path_cache = call_reset_cache_path
        cache_api_cls.reset_path_downloads = call_reset_download_path
        if not call_set_cache_path: cache_api_cls.set_cache_dir = ''
        if not call_set_download_path: cache_api_cls.set_downloads_dir = ''

        result = cache_api_cls.run()

        if call_query:
            assert result == ('some', 'vals')
        assert mock_query.called == call_query
        assert mock_remove_cache_dir.called == call_rm_cache_dir
        assert mock_get_cache_dir.called == (call_rm_cache_dir or call_reset_cache_path or call_set_cache_path)
        assert mock_remove_cache_file.called == call_rm_cache_file
        assert mock_get_cache_filename.called == call_rm_cache_file
        assert mock_reset_cache.called == call_reset_cache
        assert mock_reset_cache_path.called == call_reset_cache_path
        assert mock_reset_download_path.called == call_reset_download_path
        assert mock_get_download_dir.called == (call_reset_download_path or call_set_download_path)
        assert mock_set_cache_path.called == call_set_cache_path
        assert mock_set_download_path.called == call_set_download_path

    def test_get_matching_metadata_from_cache_and_return_some_patterns(self, mocker, cache_api_cls):
        def side_effect(pattern):
            return [{pattern: 'val'}]
        mock_get_patterns = mocker.patch.object(CacheAPI, 'get_matching_pattern_from_cache', side_effect=side_effect)
        patterns = ('dbA', 'taskB')

        result = cache_api_cls.get_matching_metadata_from_cache(patterns)

        assert mock_get_patterns.called
        assert result == [[{"dbA": 'val'}], [{"taskB": 'val'}]]

    def test_get_matching_metadata_from_cache_and_return_empty_list(self, mocker, cache_api_cls):
        def side_effect(pattern):
            if any(pattern):
                return [{pattern: 'val'}]
            else:
                return []
        mock_get_patterns = mocker.patch.object(CacheAPI, 'get_matching_pattern_from_cache', side_effect=side_effect)
        patterns = ('',)

        result = cache_api_cls.get_matching_metadata_from_cache(patterns)

        assert not mock_get_patterns.called
        assert result == [[]]

    def test_get_matching_metadata_from_cache_and_return_half_empty_list(self, mocker, cache_api_cls):
        def side_effect(pattern):
            if any(pattern):
                return [{pattern: 'val'}]
            else:
                return []
        mock_get_patterns = mocker.patch.object(CacheAPI, 'get_matching_pattern_from_cache', side_effect=side_effect)
        patterns = ('', 'taskB')

        result = cache_api_cls.get_matching_metadata_from_cache(patterns)

        assert mock_get_patterns.called
        assert result == [[], [{"taskB": 'val'}]]

    def test_get_matching_pattern_from_cache(self, mocker, cache_api_cls):
        mock_data = mocker.patch.object(CacheAPI, 'get_cache_data')
        mock_find_pattern = mocker.patch.object(CacheAPI, 'find_pattern_in_dict')
        mock_add_key = mocker.patch.object(CacheAPI, 'add_key_to_results', return_value={})

        result = cache_api_cls.get_matching_pattern_from_cache('some_pattern')

        assert mock_data.called
        assert mock_find_pattern.called
        assert mock_add_key.called
        assert result == {}

    def test_remove_cache_dir_from_disk_and_dir_exists(self, mocker, cache_api_cls, mock_get_cache_dir):
        mock_exists_dir = mocker.patch('os.path.exists', return_value=True)
        mock_rmtree = mocker.patch('shutil.rmtree')

        cache_api_cls.remove_cache_dir_from_disk()

        assert mock_get_cache_dir.called
        assert mock_exists_dir.called
        assert mock_rmtree.called

    def test_remove_cache_dir_from_disk_and_dir_not_exists(self, mocker, cache_api_cls, mock_get_cache_dir):
        mock_exists_dir = mocker.patch('os.path.exists', return_value=False)
        mock_rmtree = mocker.patch('shutil.rmtree')

        cache_api_cls.remove_cache_dir_from_disk()

        assert mock_get_cache_dir.called
        assert mock_exists_dir.called
        assert not mock_rmtree.called

    def test_remove_cache_file_from_disk_and_file_exists(self, mocker, cache_api_cls, mock_get_cache_filename):
        mock_exists_dir = mocker.patch('os.path.exists', return_value=True)
        mock_os_remove = mocker.patch('os.remove')

        cache_api_cls.remove_cache_file_from_disk()

        assert mock_get_cache_filename.called
        assert mock_exists_dir.called
        assert mock_os_remove.called

    def test_remove_cache_file_from_disk_and_file_not_exists(self, mocker, cache_api_cls, mock_get_cache_filename):
        mock_exists_dir = mocker.patch('os.path.exists', return_value=False)
        mock_os_remove = mocker.patch('os.remove')

        cache_api_cls.remove_cache_file_from_disk()

        assert mock_get_cache_filename.called
        assert mock_exists_dir.called
        assert not mock_os_remove.called
