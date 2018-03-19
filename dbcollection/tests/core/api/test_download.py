"""
Test dbcollection core API: download.
"""


import os
import pytest

from dbcollection.core.api.download import download, DownloadAPI


@pytest.fixture()
def mocks_init_class(mocker):
    mock_cache = mocker.patch.object(DownloadAPI, "get_cache_manager", return_value=True)
    return [mock_cache]


def assert_mock_init_class(mocks):
    for mock in mocks:
        assert mock.called


@pytest.fixture()
def test_data():
    return {
        "dataset": 'mnist',
        "data_dir": '/some/dir/path/',
        "extract_data": True,
        "verbose": False
    }


class TestCallDownload:
    """Unit tests for the core api download method."""

    def test_call_with_dataset_name(self, mocker, mocks_init_class):
        mock_run = mocker.patch.object(DownloadAPI, "run")

        download("some_dataset")

        assert_mock_init_class(mocks_init_class)
        assert mock_run.called

    def test_call_with_all_input_args(self, mocker, mocks_init_class, test_data):
        mock_run = mocker.patch.object(DownloadAPI, "run")

        download(test_data["dataset"],
                 test_data["data_dir"],
                 test_data["extract_data"],
                 test_data["verbose"])

        assert_mock_init_class(mocks_init_class)
        assert mock_run.called

    def test_call_with_named_input_args(self, mocker, mocks_init_class, test_data):
        mock_run = mocker.patch.object(DownloadAPI, "run")

        download(name=test_data["dataset"],
                 data_dir=test_data["data_dir"],
                 extract_data=test_data["extract_data"],
                 verbose=test_data["verbose"])

        assert_mock_init_class(mocks_init_class)
        assert mock_run.called

    def test_call__raises_error_no_input_args(self, mocker, mocks_init_class):
        mock_run = mocker.patch.object(DownloadAPI, "run")

        with pytest.raises(TypeError):
            download()

    def test_call__raise_error_invalid_dataset_name(self, mocker, mocks_init_class):
        mock_run = mocker.patch.object(DownloadAPI, "run")

        with pytest.raises(AssertionError):
            download(None)

    def test_call__raises_error_too_many_args(self, mocker):
        with pytest.raises(TypeError):
            download('some_dataset', '/some/dir/path', True, True, 'extra_field')


@pytest.fixture()
def download_api_cls(mocker, mocks_init_class, test_data):
    return DownloadAPI(
        name=test_data['dataset'],
        data_dir=test_data['data_dir'],
        extract_data=test_data['extract_data'],
        verbose=test_data['verbose']
    )


class TestClassDownloadAPI:
    """Unit tests for the DownloadAPI class."""

    def test_init_with_all_input_args(self, mocker, mocks_init_class, test_data):
        download_cls = DownloadAPI(name=test_data["dataset"],
                                   data_dir=test_data["data_dir"],
                                   extract_data=test_data["extract_data"],
                                   verbose=test_data["verbose"])

        assert_mock_init_class(mocks_init_class)
        assert download_cls.name == test_data["dataset"]
        assert download_cls.data_dir == test_data["data_dir"]
        assert download_cls.extract_data == test_data["extract_data"]
        assert download_cls.verbose == test_data["verbose"]

    def test_init__raises_error_no_input_args(self, mocker):
        with pytest.raises(TypeError):
            DownloadAPI()

    def test_init__raises_error_too_many_input_args(self, mocker, test_data):
        with pytest.raises(TypeError):
            DownloadAPI(test_data['dataset'], test_data['data_dir'], test_data['extract_data'], test_data['verbose'], 'extra_input')

    def test_init__raises_error_missing_one_input(self, mocker):
        with pytest.raises(TypeError):
            DownloadAPI('some_dataset', '/some/dir/path', False)

    def test_run(self, mocker, download_api_cls):
        mock_exists = mocker.patch.object(DownloadAPI, 'exists_dataset_in_cache', return_value=False)
        mock_download = mocker.patch.object(DownloadAPI, 'download_dataset')
        mock_update = mocker.patch.object(DownloadAPI, 'update_cache')

        download_api_cls.run()

        assert mock_exists.called
        assert mock_download.called
        assert mock_update.called

    def test_run_skip_downloading(self, mocker, download_api_cls):
        mock_exists = mocker.patch.object(DownloadAPI, 'exists_dataset_in_cache', return_value=True)
        mock_download = mocker.patch.object(DownloadAPI, 'download_dataset')
        mock_update = mocker.patch.object(DownloadAPI, 'update_cache')

        download_api_cls.run()

        assert mock_exists.called
        assert not mock_download.called
        assert not mock_update.called

    def test_get_dataset_constructor(self, mocker, download_api_cls):
        mock_metadata_obj = mocker.patch.object(DownloadAPI, "get_dataset_metadata_obj", return_value=mocker.MagicMock())

        download_api_cls.get_dataset_constructor()

        assert mock_metadata_obj.called

    def test_get_download_data_dir__data_dir_valid(self, mocker, download_api_cls):
        mock_get_dir = mocker.patch.object(DownloadAPI, "get_download_data_dir_from_cache", return_value='/some/cache/dir')

        download_api_cls.data_dir = '/valid/dir/path'
        result = download_api_cls.get_download_data_dir()

        assert not mock_get_dir.called
        assert result == '/valid/dir/path'

    def test_get_download_data_dir__data_dir_empty(self, mocker, download_api_cls):
        mock_get_dir = mocker.patch.object(DownloadAPI, "get_download_data_dir_from_cache", return_value='/some/cache/dir')

        download_api_cls.data_dir = ''
        result = download_api_cls.get_download_data_dir()

        assert mock_get_dir.called
        assert result == '/some/cache/dir'

    def get_download_data_dir_from_cache(self, mocker, download_api_cls):
        mock_get_dir = mocker.patch.object(DownloadAPI, "get_cache_download_dir_path", return_value='/download/dir/path')
        mock_create_dir = mocker.patch.object(DownloadAPI, "create_dir")

        result = download_api_cls.get_download_data_dir_from_cache()

        assert mock_get_dir.called
        assert mock_create_dir.called
        assert result == os.path.join('/download/dir/path', download_api_cls.name)

    def test_get_download_cache_dir(self, mocker, download_api_cls):
        mock_get_dir = mocker.patch.object(DownloadAPI, "get_cache_dir", return_value='/cache/dir/path')
        mock_create_dir = mocker.patch.object(DownloadAPI, "create_dir")

        result = download_api_cls.get_download_cache_dir()

        assert mock_get_dir.called
        assert mock_create_dir.called
        assert result == os.path.join('/cache/dir/path', download_api_cls.name)

    def test_download_dataset(self, mocker, download_api_cls):
        mock_data_dir = mocker.patch.object(DownloadAPI, 'get_download_data_dir', return_value='/some/path/data/dir')
        mock_cache_dir = mocker.patch.object(DownloadAPI, 'get_download_cache_dir', return_value='/some/path/cache/dir')
        mock_download = mocker.patch.object(DownloadAPI, "download_dataset_files")

        download_api_cls.download_dataset()

        assert mock_data_dir.called
        assert mock_cache_dir.called
        assert mock_download.called

    def test_download_dataset_files(self, mocker, download_api_cls):
        mock_constructor = mocker.patch.object(DownloadAPI, "get_dataset_constructor", return_value=mocker.MagicMock())

        download_api_cls.download_dataset_files('/some/path/data', '/some/path/cache')

        assert mock_constructor.called

    def test_update_cache__dataset_exists_in_cache(self, mocker, download_api_cls):
        mock_data_dir = mocker.patch.object(DownloadAPI, "get_download_data_dir", return_value='/some/path/data/dir')
        mock_exists = mocker.patch.object(DownloadAPI, "exists_dataset_in_cache", return_value=True)
        mock_update = mocker.patch.object(DownloadAPI, "update_dataset_info_in_cache")
        mock_add = mocker.patch.object(DownloadAPI, "add_dataset_info_to_cache")

        download_api_cls.update_cache()

        assert mock_data_dir.called
        assert mock_exists.called
        assert mock_update.called
        assert not mock_add.called

    def test_update_cache__dataset_does_not_exist_in_cache(self, mocker, download_api_cls):
        mock_data_dir = mocker.patch.object(DownloadAPI, "get_download_data_dir", return_value='/some/path/data/dir')
        mock_exists = mocker.patch.object(DownloadAPI, "exists_dataset_in_cache", return_value=False)
        mock_update = mocker.patch.object(DownloadAPI, "update_dataset_info_in_cache")
        mock_add = mocker.patch.object(DownloadAPI, "add_dataset_info_to_cache")

        download_api_cls.update_cache()

        assert mock_data_dir.called
        assert mock_exists.called
        assert not mock_update.called
        assert mock_add.called

    def test_update_cache_dataset_not_exists(self, mocker, mocks_init_class, download_api_cls):
        mock_exists = mocker.patch.object(DownloadAPI, "exists_dataset_in_cache", return_value=False)
        mock_add = mocker.patch.object(DownloadAPI, "add_dataset_info_to_cache")

        download_api_cls.update_cache()

        assert mock_exists.called
        assert mock_add.called
