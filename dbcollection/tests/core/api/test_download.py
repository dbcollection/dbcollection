"""
Test dbcollection core API: download.
"""


import pytest

from dbcollection.core.api.download import download, DownloadAPI
from dbcollection.core.cache import CacheManager

from ..dummy_data.example_cache import DataGenerator


def mock_DownloadAPI_init_methods(mocker):
    mocker.patch.object(DownloadAPI, "get_cache_manager", return_value=True)
    mocker.patch.object(DownloadAPI, "get_download_data_dir", return_value='/path/to/cache/downloads/')
    mocker.patch.object(DownloadAPI, "get_download_cache_dir", return_value='/path/to/cache/')


def test_db_data():
    dataset = 'some_dataset'
    data_dir = '/some/dir/path/'
    extract_data = True
    verbose = False
    return dataset, data_dir, extract_data, verbose


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
        _, data_dir, extract_data, verbose = test_db_data()

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
        dataset, data_dir, extract_data, verbose = test_db_data()

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
        dataset, data_dir, extract_data, verbose = test_db_data()

        with pytest.raises(TypeError):
            download_cls = DownloadAPI(dataset, data_dir, extract_data)

    def test_get_download_data_dir_return_data_dir(self, mocker):
        mocker.patch.object(DownloadAPI, "get_cache_manager", return_value=True)
        mocker.patch.object(DownloadAPI, "get_download_cache_dir", return_value='/path/to/cache/')
        dataset, data_dir, extract_data, verbose = test_db_data()

        download_cls = DownloadAPI(dataset, data_dir, extract_data, verbose)
        result = download_cls.get_download_data_dir()

        assert result == data_dir

    @pytest.mark.parametrize("data_dir", ['', None])
    def test_get_download_data_dir_generate_data_dir(self, mocker, data_dir):
        mocker.patch.object(DownloadAPI, "get_cache_manager", return_value=True)
        mocker.patch.object(DownloadAPI, "get_download_cache_dir", return_value='/path/to/cache/')
        mocker.patch.object(DownloadAPI, "get_download_data_dir_from_cache", return_value='/some/path/')
        dataset, _, extract_data, verbose = test_db_data()

        download_cls = DownloadAPI(dataset, data_dir, extract_data, verbose)
        result = download_cls.get_download_data_dir()

        assert result == '/some/path/'

    def test_download_dataset__raise_error_invalid_dataset(self, mocker):
        mock_DownloadAPI_init_methods(mocker)
        dataset, data_dir, extract_data, verbose = test_db_data()

        download_cls = DownloadAPI(dataset, data_dir, extract_data, verbose)
        with pytest.raises(KeyError):
            download_cls.download_dataset()

    def test_download_dataset_run_constructor(self, mocker):
        mock_DownloadAPI_init_methods(mocker)
        mock_constructor = mocker.patch.object(DownloadAPI, "get_dataset_constructor", return_value=mocker.MagicMock())
        dataset, data_dir, extract_data, verbose = test_db_data()

        download_cls = DownloadAPI(dataset, data_dir, extract_data, verbose)
        download_cls.download_dataset()

        assert mock_constructor.called

    def test_update_cache_dataset_exists(self, mocker):
        mock_DownloadAPI_init_methods(mocker)
        mock_exists = mocker.patch.object(DownloadAPI, "exists_dataset_in_cache", return_value=True)
        mock_update = mocker.patch.object(DownloadAPI, "update_dataset_info_in_cache")
        dataset, data_dir, extract_data, verbose = test_db_data()

        download_cls = DownloadAPI(dataset, data_dir, extract_data, verbose)
        download_cls.update_cache()

        assert mock_exists.return_value == True
        assert mock_update.called

    def test_update_cache_dataset_not_exists(self, mocker):
        mock_DownloadAPI_init_methods(mocker)
        mock_exists = mocker.patch.object(DownloadAPI, "exists_dataset_in_cache", return_value=False)
        mock_add = mocker.patch.object(DownloadAPI, "add_dataset_info_to_cache")
        dataset, data_dir, extract_data, verbose = test_db_data()

        download_cls = DownloadAPI(dataset, data_dir, extract_data, verbose)
        download_cls.update_cache()

        assert mock_exists.return_value == False
        assert mock_add.called
