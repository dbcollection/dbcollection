"""
Test dbcollection utils.
"""


import os
import pytest

from dbcollection.utils.url import (
    check_if_urls_exist,
    download_extract_urls,
    URL
)


def test_download_extract_urls__files_exist(mocker):
    mock_path_exists = mocker.patch("os.path.exists", return_value=True)
    mock_check_urls = mocker.patch("dbcollection.utils.url.check_if_urls_exist", return_value=True)
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
    mock_check_urls = mocker.patch("dbcollection.utils.url.check_if_urls_exist")
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
    mock_check_urls = mocker.patch("dbcollection.utils.url.check_if_urls_exist", return_value=False)
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
    mock_check_urls = mocker.patch("dbcollection.utils.url.check_if_urls_exist")
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
