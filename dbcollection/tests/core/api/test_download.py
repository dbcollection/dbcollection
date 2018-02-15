"""
Test dbcollection core API: download.
"""


import pytest

from dbcollection.core.api.download import download, DownloadAPI
from dbcollection.core.cache import CacheManager, CacheDataManager

from ..dummy_data.example_cache import DataGenerator


def mock_DownloadAPI_init_methods(mocker):
    mocker.patch.object(DownloadAPI, "get_cache_manager", return_value=True)
    mocker.patch.object(DownloadAPI, "get_download_data_dir", return_value='/path/to/cache/downloads/')
    mocker.patch.object(DownloadAPI, "get_download_cache_dir", return_value='/path/to/cache/')


class TestCallDownload:
    """Unit tests for the core api download method."""

    def test_call_with_dataset_name(self, mocker):
        mock_DownloadAPI_init_methods(mocker)
        mock_run = mocker.patch.object(DownloadAPI, "run")
        dataset = 'mnist'

        download(dataset)

        assert mock_run.called

    def test_call_all_parameters(self, mocker):
        mock_DownloadAPI_init_methods(mocker)
        mock_run = mocker.patch.object(DownloadAPI, "run")
        dataset = 'mnist'
        data_dir = '/some/dir/path'
        extract_data = True
        verbose = True

        download(dataset, data_dir, extract_data, verbose)

        assert mock_run.called

    def test_call__raise_error_missing_inputs(self, mocker):
        mock_DownloadAPI_init_methods(mocker)
        mock_run = mocker.patch.object(DownloadAPI, "run")

        with pytest.raises(TypeError):
            download()

    def test_call__raise_error_invalid_dataset_name(self, mocker):
        mock_DownloadAPI_init_methods(mocker)
        mock_run = mocker.patch.object(DownloadAPI, "run")
        dataset = None

        with pytest.raises(AssertionError):
            download(dataset)


class TestClassDownloadAPI:
    """Unit tests for the DownloadAPI class."""

    def test_init_with_all_inputs(self, mocker):
        mock_DownloadAPI_init_methods(mocker)
        dataset = 'some_dataset'
        data_dir = '/some/dir/path'
        extract_data = True
        verbose = False

        download_cls = DownloadAPI(dataset, data_dir, extract_data, verbose)

        assert download_cls.name == dataset
        assert download_cls.data_dir == data_dir
        assert download_cls.extract_data == extract_data
        assert download_cls.verbose == verbose
        assert download_cls.cache_manager == True  # mocked value
        assert download_cls.save_data_dir == '/path/to/cache/downloads/'
        assert download_cls.save_cache_dir == '/path/to/cache/'

    def test_init__raises_error_missing_inputs(self, mocker):
        with pytest.raises(TypeError):
            download_cls = DownloadAPI()

    def test_init__raises_error_missing_one_input(self, mocker):
        dataset = 'some_dataset'
        data_dir = '/some/dir/path'
        extract_data = True

        with pytest.raises(TypeError):
            download_cls = DownloadAPI(dataset, data_dir, extract_data)

    def test_get_download_data_dir_return_data_dir(self, mocker):
        mocker.patch.object(DownloadAPI, "get_cache_manager", return_value=True)
        mocker.patch.object(DownloadAPI, "get_download_cache_dir", return_value='/path/to/cache/')
        dataset = 'some_dataset'
        data_dir = '/some/dir/path'
        extract_data = True
        verbose = False

        download_cls = DownloadAPI(dataset, data_dir, extract_data, verbose)
        result = download_cls.get_download_data_dir()

        assert result == data_dir

    @pytest.mark.parametrize("data_dir", ['', None])
    def test_get_download_data_dir_generate_data_dir(self, mocker, data_dir):
        mocker.patch.object(DownloadAPI, "get_cache_manager", return_value=True)
        mocker.patch.object(DownloadAPI, "get_download_cache_dir", return_value='/path/to/cache/')
        mocker.patch.object(DownloadAPI, "get_download_data_dir_from_cache", return_value='/some/path/')
        dataset = 'some_dataset'
        extract_data = True
        verbose = False

        download_cls = DownloadAPI(dataset, data_dir, extract_data, verbose)
        result = download_cls.get_download_data_dir()

        assert result == '/some/path/'

    def test_download_dataset__raise_error_invalid_dataset(self, mocker):
        mock_DownloadAPI_init_methods(mocker)
        dataset = 'some_dataset'
        data_dir = '/some/dir/path'
        extract_data = True
        verbose = False

        download_cls = DownloadAPI(dataset, data_dir, extract_data, verbose)
        with pytest.raises(KeyError):
            download_cls.download_dataset()

    def test_download_dataset_run_constructor(self, mocker):
        mock_DownloadAPI_init_methods(mocker)
        mock_constructor = mocker.patch.object(DownloadAPI, "get_dataset_constructor", return_value=mocker.MagicMock())
        dataset = 'mnist'
        data_dir = '/some/dir/path'
        extract_data = True
        verbose = False

        download_cls = DownloadAPI(dataset, data_dir, extract_data, verbose)
        download_cls.download_dataset()

        assert mock_constructor.called
