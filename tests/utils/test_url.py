"""
Test dbcollection utils.
"""


import os
import pytest

from dbcollection.core.exceptions import (
    InvalidURLDownloadSource,
    MD5HashNotEqual,
    URLDoesNotExist
)
from dbcollection.utils.url import (
    check_if_url_files_exist,
    download_extract_urls,
    extract_archive_file,
    URL,
    URLDownload,
    URLDownloadGoogleDrive
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

    def test_parse_url_metadata__string(self, mocker):
        dummy_value = 'dummy_val'
        mock_get_value = mocker.patch.object(URL, "get_value_from_key", return_value=dummy_value)

        url = 'http://url1.zip'
        url_metadata = URL().parse_url_metadata(url)

        assert mock_get_value.call_count == 4
        assert url_metadata == {
            "url": url,
            "md5hash": dummy_value,
            "filename": dummy_value,
            "extract_dir": dummy_value,
            "method": dummy_value
        }

    def test_parse_url_metadata__dict(self, mocker):
        dummy_value = 'dummy_val'
        mock_get_value = mocker.patch.object(URL, "get_value_from_key", return_value=dummy_value)

        url = {'url': 'http://url1.zip'}
        url_metadata = URL().parse_url_metadata(url)

        assert mock_get_value.call_count == 4
        assert url_metadata == {
            "url": url['url'],
            "md5hash": dummy_value,
            "filename": dummy_value,
            "extract_dir": dummy_value,
            "method": dummy_value
        }

    def test_parse_url_metadata__invalid_url_type(self, mocker):
        with pytest.raises(AssertionError):
            url = ['http://url1.zip']
            url_metadata = URL().parse_url_metadata(url)

    def test_get_value_from_key__key_exists(self, mocker):
        dictionary = {"url": 'http://dummy_url.html', "md5hash": 'dummy_hash'}
        key = 'url'
        value = URL().get_value_from_key(dictionary, key)

        assert value == dictionary[key]

    def test_get_value_from_key__key_doesnt_exist(self, mocker):
        value = URL().get_value_from_key(
            dictionary={"url": 'http://dummy_url.html', "md5hash": 'dummy_hash'},
            key='filename',
            default='default'
        )

        assert value == 'default'

    def test_download_url_to_file(self, mocker):
        dummy_temp_file = 'dummy_file'
        mock_temp_file = mocker.patch.object(URL, "create_temp_file", return_value=dummy_temp_file)
        mock_download_url = mocker.patch.object(URLDownload, "download")
        mock_download_googledrive = mocker.patch.object(URLDownloadGoogleDrive, "download")
        mock_move = mocker.patch("shutil.move")

        url_metadata = {"dummy": 'data', "method": 'requests'}
        filename = 'dummy_filename.zip'
        verbose = True
        URL().download_url_to_file(
            url_metadata=url_metadata,
            filename=filename,
            verbose=verbose
        )

        mock_temp_file.assert_called_once_with(filename)
        mock_download_url.assert_called_once_with(url_metadata, filename=dummy_temp_file, verbose=verbose)
        assert not mock_download_googledrive.called
        mock_move.assert_called_once_with(dummy_temp_file, filename)

    def test_download_url_to_file__via_googledrive(self, mocker):
        dummy_temp_file = 'dummy_file'
        mock_temp_file = mocker.patch.object(URL, "create_temp_file", return_value=dummy_temp_file)
        mock_download_url = mocker.patch.object(URLDownload, "download")
        mock_download_googledrive = mocker.patch.object(URLDownloadGoogleDrive, "download")
        mock_move = mocker.patch("shutil.move")

        url_metadata = {"dummy": 'data', "method": 'googledrive'}
        filename = 'dummy_filename.zip'
        verbose = True
        URL().download_url_to_file(
            url_metadata=url_metadata,
            filename=filename,
            verbose=verbose
        )

        mock_temp_file.assert_called_once_with(filename)
        assert not mock_download_url.called
        mock_download_googledrive.assert_called_once_with(url_metadata, filename=dummy_temp_file)
        mock_move.assert_called_once_with(dummy_temp_file, filename)

    def test_download_url_to_file__raises_exception(self, mocker):
        dummy_temp_file = 'dummy_file'
        mock_temp_file = mocker.patch.object(URL, "create_temp_file", return_value=dummy_temp_file)
        with pytest.raises(InvalidURLDownloadSource):
            URL().download_url_to_file(
                url_metadata={"dummy": 'data', "method": 'invalid_method'},
                filename='dummy_filename.zip',
                verbose=True
            )

    def test_create_temp_file(self, mocker):
        dummy_file = mocker.MagicMock()
        dummy_filename = "filename.tmp"
        mock_create_file = mocker.patch("tempfile.mkstemp", return_value=(dummy_file, dummy_filename))
        mock_close = mocker.patch("os.close")
        mock_unlink = mocker.patch("os.unlink")

        filename_dir = os.path.join('some', 'path', 'to', 'data')
        filename = os.path.join(filename_dir, 'filename1.zip')
        tmpfile = URL().create_temp_file(filename)

        assert tmpfile == dummy_filename
        mock_create_file.assert_called_once_with(".tmp", prefix=filename, dir=filename_dir)
        mock_close.assert_called_once_with(dummy_file)
        mock_unlink.assert_called_once_with(dummy_filename)

    def test_md5_checksum(self, mocker):
        dummy_hash = 'a5s6dea9s8rtqw1s1g45jk4s4dfg49'
        mock_get_hash = mocker.patch.object(URL, "get_file_hash", return_value=dummy_hash)

        filename = os.path.join('some', 'path', 'to', 'filename1.zip')
        md5hash = 'a5s6dea9s8rtqw1s1g45jk4s4dfg49'
        URL().md5_checksum(filename=filename, md5hash=md5hash)

        mock_get_hash.assert_called_once_with(filename)

    def test_md5_checksum__raises_error(self, mocker):
        dummy_hash = 'a5s6dea9s8rtqw1s1g45jk4s4dfg49'
        mock_get_hash = mocker.patch.object(URL, "get_file_hash", return_value=dummy_hash)

        with pytest.raises(MD5HashNotEqual):
            filename = os.path.join('some', 'path', 'to', 'filename1.zip')
            md5hash = '87897asd98f74asd4fas6d4as8v46t'
            URL().md5_checksum(filename=filename, md5hash=md5hash)

    def test_get_url_filename(self, mocker):
        mock_exists = mocker.patch.object(URL, "exists_url_file", return_value=True)

        url = 'http://dummy_url.html'
        save_dir = os.path.join('some', 'dir')
        response = URL.get_url_filename(url=url, save_dir=save_dir)

        mock_exists.assert_called_once_with(url, save_dir)
        assert response == True


class TestURLDownload:
    """Unit tests for the URLDownload class."""

    def test_download(self, mocker):
        mock_exists_url = mocker.patch.object(URLDownload, "check_exists_url", return_value=True)
        mock_download_url = mocker.patch.object(URLDownload, "download_url")

        url='http://dummy_url.html',
        filename=os.path.join('path', 'to', 'filename1.zip'),
        verbose=False
        URLDownload.download(url=url, filename=filename, verbose=verbose)

        mock_exists_url.assert_called_once_with(url)
        mock_download_url.assert_called_once_with(url, filename, verbose)

    def test_download__raises_error(self, mocker):
        mock_exists_url = mocker.patch.object(URLDownload, "check_exists_url", return_value=False)

        with pytest.raises(URLDoesNotExist):
            URLDownload.download(
                url='http://dummy_url.html',
                filename=os.path.join('path', 'to', 'filename1.zip'),
                verbose=False
            )

    def test_check_exists_url__success_200(self, mocker):
        dummy_request = mocker.MagicMock()
        dummy_request.status_code = 200
        mock_requests = mocker.patch("requests.head", return_value=dummy_request)

        url = 'http://dummy_url.html'
        response = URLDownload().check_exists_url(url)

        mock_requests.assert_called_once_with(url, allow_redirects=False)
        assert response == True

    def test_check_exists_url__failure(self, mocker):
        dummy_request = mocker.MagicMock()
        dummy_request.status_code = 300
        mock_requests = mocker.patch("requests.head", return_value=dummy_request)

        url = 'http://dummy_url.html'
        response = URLDownload().check_exists_url(url)

        mock_requests.assert_called_once_with(url, allow_redirects=False)
        assert response == False
