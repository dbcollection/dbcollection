"""
Test dbcollection utils.
"""


import os
import pytest

from dbcollection.utils.url import (
    check_if_url_files_exist,
    download_extract_urls,
    extract_archive_file,
    URL
)


def test_download_extract_urls__files_exist(mocker):
    mock_path_exists = mocker.patch("os.path.exists", return_value=True)
    mock_check_urls = mocker.patch("dbcollection.utils.url.check_if_url_files_exist", return_value=True)
    mock_makedirs = mocker.patch("os.makedirs")
    mock_download = mocker.patch.object(URL, "download")
    mock_extract_files = mocker.patch("dbcollection.utils.url.extract_archive_file")

    urls = ['http://url1.zip', 'http://url2.zip']
    save_dir = os.path.join('path', 'to', 'save', 'dir')
    download_extract_urls(urls, save_dir, True, True)

    mock_path_exists.assert_called_once_with(save_dir)
    mock_check_urls.assert_called_once_with(urls, save_dir)
    assert not mock_makedirs.called


def test_download_extract_urls__download_files_and_savedir_does_not_exist(mocker):
    mock_path_exists = mocker.patch("os.path.exists", return_value=False)
    mock_check_urls = mocker.patch("dbcollection.utils.url.check_if_url_files_exist")
    mock_makedirs = mocker.patch("os.makedirs")
    mock_download = mocker.patch.object(URL, "download", return_value='filename.zip')
    mock_extract_files = mocker.patch("dbcollection.utils.url.extract_archive_file")

    urls = ['http://url1.zip']
    save_dir = os.path.join('path', 'to', 'save', 'dir')
    download_extract_urls(urls, save_dir, True, True)

    mock_path_exists.assert_called_once_with(save_dir)
    assert not mock_check_urls.called
    mock_makedirs.assert_called_once_with(save_dir)
    mock_download.assert_called_once_with(urls[0], save_dir, True)
    mock_extract_files.assert_called_once_with('filename.zip', save_dir)


def test_download_extract_urls__download_files_and_savedir_exists(mocker):
    mock_path_exists = mocker.patch("os.path.exists", return_value=True)
    mock_check_urls = mocker.patch("dbcollection.utils.url.check_if_url_files_exist", return_value=False)
    mock_makedirs = mocker.patch("os.makedirs")
    mock_download = mocker.patch.object(URL, "download", return_value='filename.zip')
    mock_extract_files = mocker.patch("dbcollection.utils.url.extract_archive_file")

    urls = ['http://url1.zip']
    save_dir = os.path.join('path', 'to', 'save', 'dir')
    download_extract_urls(urls, save_dir, True, True)

    mock_path_exists.assert_called_once_with(save_dir)
    mock_check_urls.assert_called_once_with(urls, save_dir)
    assert not mock_makedirs.called
    mock_download.assert_called_once_with(urls[0], save_dir, True)
    mock_extract_files.assert_called_once_with('filename.zip', save_dir)


def test_download_extract_urls__download_files_and_savedir_does_not_exist_and_skip_extract_data(mocker):
    mock_path_exists = mocker.patch("os.path.exists", return_value=False)
    mock_check_urls = mocker.patch("dbcollection.utils.url.check_if_url_files_exist")
    mock_makedirs = mocker.patch("os.makedirs")
    mock_download = mocker.patch.object(URL, "download", return_value='filename.zip')
    mock_extract_files = mocker.patch("dbcollection.utils.url.extract_archive_file")

    urls = ['http://url1.zip']
    save_dir = os.path.join('path', 'to', 'save', 'dir')
    download_extract_urls(urls, save_dir, False, True)

    mock_path_exists.assert_called_once_with(save_dir)
    assert not mock_check_urls.called
    mock_makedirs.assert_called_once_with(save_dir)
    mock_download.assert_called_once_with(urls[0], save_dir, True)
    assert not mock_extract_files.called

def test_check_if_url_files_exist__files_exist(mocker):
    dummy_filename = 'some_filename.zip'
    mock_get_filename = mocker.patch.object(URL, "get_url_filename", return_value=dummy_filename)
    mock_exists = mocker.patch('os.path.exists', return_value=True)

    urls = ['http://url1.zip', 'http://url.2zip']
    save_dir = os.path.join('path', 'to', 'save', 'dir')
    result = check_if_url_files_exist(urls, save_dir)

    mock_get_filename.assert_called_once_with(urls[0], save_dir)
    mock_exists.assert_called_once_with(os.path.join(save_dir, dummy_filename))
    assert result == True

def test_check_if_url_files_exist__files_dont_exist(mocker):
    dummy_filename = 'some_filename.zip'
    mock_get_filename = mocker.patch.object(URL, "get_url_filename", return_value=dummy_filename)
    mock_exists = mocker.patch('os.path.exists', return_value=False)

    urls = ['http://url1.zip', 'http://url.2zip']
    save_dir = os.path.join('path', 'to', 'save', 'dir')
    result = check_if_url_files_exist(
        urls=urls,
        save_dir=save_dir
    )

    assert mock_get_filename.call_count == 2
    assert mock_exists.call_count == 2
    assert result == False

def test_extract_archive_file(mocker):
    mock_patoolib = mocker.patch('patoolib.extract_archive')

    filename = 'some_filename.zip',
    save_dir = os.path.join('path', 'to', 'data', 'dir')
    extract_archive_file(filename, save_dir)

    mock_patoolib.assert_called_once_with(filename, outdir=save_dir)


class TestURL:
    """Unit tests for the URL class."""

    def test_download__url_exists(self, mocker):
        mock_exists_file = mocker.patch.object(URL, "exists_url_file", return_value=True)
        mock_download_url = mocker.patch.object(URL, "download_url")

        url = 'http://url1.zip'
        save_dir = os.path.join('path', 'to', 'data', 'dir')
        URL.download(
            url=url,
            save_dir=save_dir,
            verbose=True
        )

        mock_exists_file.assert_called_once_with(url, save_dir)
        assert not mock_download_url.called

    def test_download__url_not_exists(self, mocker):
        mock_exists_file = mocker.patch.object(URL, "exists_url_file", return_value=False)
        mock_download_url = mocker.patch.object(URL, "download_url")

        url = 'http://url1.zip'
        save_dir = os.path.join('path', 'to', 'data', 'dir')
        URL.download(
            url=url,
            save_dir=save_dir,
            verbose=True
        )

        mock_exists_file.assert_called_once_with(url, save_dir)
        mock_download_url.assert_called_once_with(url, save_dir, True)

    @pytest.mark.parametrize("file_exists", [True, False])
    def test_exists_url_file(self, mocker, file_exists):
        dummy_metadata = {'dummy': 'data'}
        dummy_dir = os.path.join('some', 'path', 'to', 'data')
        dummy_filename = os.path.join('some', 'path', 'to', 'data', 'file1.zip')
        mock_get_metadata = mocker.patch.object(URL, "get_url_metadata_and_dir_paths", return_value=(dummy_metadata, dummy_dir, dummy_filename))
        mock_exists = mocker.patch("os.path.exists", return_value=file_exists)

        url = 'http://url1.zip'
        save_dir = os.path.join('path', 'to', 'data', 'dir')
        result = URL().exists_url_file(url, save_dir)

        mock_get_metadata.assert_called_once_with(url, save_dir)
        mock_exists.assert_called_once_with(dummy_filename)
        assert result == file_exists

    def test_get_url_metadata_and_dir_paths(self, mocker):
        dummy_extract_dir = os.path.join('some', 'dir', 'to', 'extract')
        dummy_filename = 'filename1.zip'
        dummy_metadata = {"extract_dir": dummy_extract_dir, "filename": dummy_filename}
        mock_parse_url = mocker.patch.object(URL, "parse_url_metadata", return_value=dummy_metadata)

        url = 'http://url1.zip'
        save_dir = os.path.join('path', 'to', 'data', 'dir')
        url_metadata, download_dir, filename = URL().get_url_metadata_and_dir_paths(url, save_dir)

        mock_parse_url.assert_called_once_with(url)
        assert url_metadata == dummy_metadata
        assert download_dir == os.path.join(save_dir, dummy_extract_dir)
        assert filename == os.path.join(save_dir, dummy_metadata["extract_dir"], dummy_metadata["filename"])

    def test_download_url(self, mocker):
        dummy_metadata = {'md5hash': 'dummy_hash'}
        dummy_download_dir = os.path.join('some', 'path', 'to', 'data')
        dummy_filename = os.path.join('some', 'path', 'to', 'data', 'file1.zip')
        mock_get_metadata = mocker.patch.object(URL, "get_url_metadata_and_dir_paths", return_value=(dummy_metadata, dummy_download_dir, dummy_filename))
        mock_exists = mocker.patch("os.path.exists", return_value=False)
        mock_create_dir = mocker.patch("os.makedirs")
        mock_download = mocker.patch.object(URL, "download_url_to_file")
        mock_md5_checksum = mocker.patch.object(URL, "md5_checksum")

        url = 'http://url1.zip'
        save_dir = os.path.join('path', 'to', 'data', 'dir')
        verbose=True
        URL().download_url(
            url=url,
            save_dir=save_dir,
            verbose=verbose
        )

        mock_get_metadata.assert_called_once_with(url, save_dir)
        mock_exists.assert_called_once_with(dummy_download_dir)
        mock_create_dir.assert_called_once_with(dummy_download_dir)
        mock_download.assert_called_once_with(dummy_metadata, dummy_filename, verbose)
        mock_md5_checksum.assert_called_once_with(dummy_filename, dummy_metadata['md5hash'])
