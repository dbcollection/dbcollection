"""
Download functions.
"""


from __future__ import print_function, division
import os
import hashlib
import shutil
import tempfile
import requests
import patoolib
import progressbar

from dbcollection.core.exceptions import (
    GoogleDriveFileIdDoesNotExist,
    InvalidURLDownloadSource,
    MD5HashNotEqual,
    URLDoesNotExist,
)


def get_hash_value(fname):
    """Retrieve the checksum of a file.

    Parameters
    ----------
    fname : str
        File name + path on disk.

    Returns
    -------
    str
        Checksum string.

    Raises
    ------
    IOError
        If the file cannot be opened
    """
    try:
        return hashlib.md5(open(fname, 'rb').read()).hexdigest()
    except (IOError, OSError):
        raise IOError('Error opening file: {}'.format(fname))


def check_url_exists(url):
    """Check if an url exists.

    Parameters
    ----------
    url : str
        Url path.

    Returns
    -------
    bool
        True if url exists, False otherwise
    str
        A message if a url request succeeded or failed.
    """
    request = requests.head(url, allow_redirects=False)
    if request.status_code == 200:
        return True, ''
    else:
        return False, 'url does not exist: {}'.format(url)


def download_url_requests(url, fname, verbose=False):
    """Downloads a file from an url.

    Parameters
    ----------
    url : str
        URL location.
    fname : str
        File name + path to store in disk.
    verbose : bool, optional
        Display progress bar

    Returns
    -------
    bool
        True if the url is valid, False otherwise.
    str
        A message if a url request succeeded or failed.
    """

    status, err = check_url_exists(url)

    if status:
        r = requests.get(url, stream=True)
        with open(fname, 'wb') as f:
            if verbose:
                total_length = int(r.headers.get('content-length'))
                if total_length is None:
                    f.write(r.content)
                else:
                    chunk_size = 1024
                    progbar_length = int(total_length / chunk_size)
                    progbar = progressbar.ProgressBar(maxval=progbar_length).start()
                    i = 0
                    for data in r.iter_content(chunk_size=chunk_size):
                        if data:
                            f.write(data)
                            f.flush()
                            progbar.update(i)
                            i += 1
                    progbar.finish()
            else:
                f.write(r.content)

        r.close()
    return status, err


def download_url_google_drive(file_id, filename):
    """Download a single url from google drive into a file.

    Parameters
    ----------
    file_id : str
        File ID in the google drive.
    filename : str
        File name + path to store in disk.

    Returns
    -------
    bool
        True if the url is valid, False otherwise.
    str
        A message if a url request succeeded or failed.
    """

    def get_confirm_token(response):
        """Get confirmation token."""
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    def save_response_content(response, destination):
        """Save to file."""
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
        status, err = True, ''
    else:
        status, err = False, 'Invalid url: {}. Token does not exist'.format(URL)

    save_response_content(response, filename)

    return status, err


def download_url(url, filename, method, verbose=False):
    """Downloads a single url into a file.

    Parameters
    ----------
    url : str
        URL location.
    filename : str
        File name + path to save the url to disk.
    method : str
        Download method (requests or googledrive)
    verbose : bool, optional
        Display messages + progress bar on screen when downloading the file.

    Returns
    -------
    bool
        True if the url is valid, False otherwise.
    str
        A message if a url request succeeded or failed.

    Raises
    ------
    Exception
        If the input download method is invalid.

    """

    # get filename for temp file in current directory
    (fd, tmpfile) = tempfile.mkstemp(".tmp", prefix=filename, dir=".")
    os.close(fd)
    os.unlink(tmpfile)

    # download the file
    if method == 'requests':
        status, err = download_url_requests(url, tmpfile, verbose)
    elif method == 'googledrive':
        status, err = download_url_google_drive(url, tmpfile)
    else:
        status, err = False, 'Invalid method: {}'.format(method)

    # rename temporary file to final output file
    if status:
        shutil.move(tmpfile, filename)

    return status, err


def parse_url(url):
    """Returns the url, md5hash and dir strings from a tupple.

    Parameters
    ----------
    url : str
        Url path.

    Returns
    -------
    str
        Url path.
    str
        Md5 Hash string.
    str
        Url's file name.
    str
        Dir to store/extract the file
    str
        Download method (googledrive, requests, etc.).

    Raises
    ------
    TypeError
        If an url is invalid.

    """

    def get_field_value(dict_url, field):
        """Check if field exists and return its value from a dictionary. Else, return None."""
        if field in dict_url:
            return dict_url[field]
        else:
            return None

    if isinstance(url, str):
        return url, None, os.path.basename(url), '', 'requests'
    elif isinstance(url, dict):
        if 'googledrive' in url:
            url_ = get_field_value(url, 'googledrive')
            md5hash = get_field_value(url, 'md5hash')
            save_name = get_field_value(url, 'save_name')
            extract_dir = get_field_value(url, 'extract_dir') or ''
            method = 'googledrive'
        else:
            url_ = get_field_value(url, 'url')
            md5hash = get_field_value(url, 'md5hash')
            save_name = get_field_value(url, 'save_name')
            extract_dir = get_field_value(url, 'extract_dir') or ''
            method = 'requests'

        if save_name:
            filename = save_name
        else:
            filename = os.path.basename(url_)
        return url_, md5hash, filename, extract_dir, method
    else:
        raise TypeError('Invalid url type: {}'.format(type(url)))


def md5_checksum(filename, md5hash):
    """Check file integrity using a checksum.

    Parameters
    ----------
    filename : str
        File path + name.
    md5hash : str
        Md5 hash string.
    """
    file_hash = get_hash_value(filename)
    if not file_hash == md5hash:
        msg = '**WARNING**: md5 checksum does not match for file: {}'.format(filename) \
              + '\nChecksum expected: {}, got: {}'.format(md5hash, file_hash)
        print(msg)


def download_extract_all(urls, dir_save, extract_data=True, verbose=True):
    """Download urls + extract files to disk.

    Download + extract all url files to disk. If clean_cache is
    True, it removes the download files.

    Parameters
    ----------
    urls : list/tuple
        List/tuple of URL paths.
    dir_save : str
        Directory to store the downloaded data.
    extract_data : bool, optional
        Extracts/unpacks the data files (if true).
    verbose : bool, optional
        Display messages on screen if set to True.

    Raises
    ------
    Exception
        If it is an invalid url type.

    """
    # Check if urls is a str
    if isinstance(urls, str):
        urls = [urls]

    # check if the save directory exists
    if not os.path.exists(dir_save):
        os.makedirs(dir_save)

    # download + extract data and remove temporary files
    for i, url in enumerate(urls):
        if verbose:
            print('\nDownload url ({}/{}): {}'.format(i + 1, len(urls), url))

        url, md5hash, filename, extract_dir, method = parse_url(url)

        save_dir = os.path.join(dir_save, extract_dir)
        filename = os.path.join(save_dir, filename)

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        if os.path.exists(filename):
            print('File already exists, skip downloading this url.')
        else:
            status, err = download_url(url, filename, method, verbose)
            if not status:
                raise Exception(err)

            if md5hash:
                md5_checksum(filename, md5hash)
            if extract_data:
                patoolib.extract_archive(filename, outdir=save_dir, verbosity=verbose)


def download_extract_urls(urls, save_dir, extract_data=True, verbose=True):
    """Download urls + extract files to disk.

    Parameters
    ----------
    urls : list/tuple/dict
        URL paths.
    dir_save : str
        Directory to store the downloaded data.
    extract_data : bool, optional
        Extracts/unpacks the data files (if true).
    verbose : bool, optional
        Display messages on screen if set to True.

    """
    if os.path.exists(save_dir):
        if check_if_url_files_exist(urls, save_dir):
            return True
    else:
        os.makedirs(save_dir)

    for url in urls:
        filename = URL.download(url, save_dir, verbose)
        if extract_data:
            extract_archive_file(filename, save_dir)


def check_if_url_files_exist(urls, save_dir):
    """Evaluates if all url filenames exist on disk.

    Parameters
    ----------
    urls : list/tuple/dict
        URL paths.
    dir_save : str
        Directory to store the downloaded data.

    """
    for url in urls:
        filename = URL.get_url_filename(url, save_dir)
        filepath = os.path.join(save_dir, filename)
        if os.path.exists(filepath):
            return True
    return False


def extract_archive_file(filename, save_dir):
    """Extracts a file archive's data to a directory.

    Parameters
    ----------
    filename : str
        File name + path of the archive file.
    dir_save : str
        Directory to extract the file archive.

    """
    patoolib.extract_archive(filename, outdir=save_dir)


class URL:
    """URL manager class."""

    @classmethod
    def download(self, url, save_dir, verbose=True):
        """Downloads a single url into a file.

        Parameters
        ----------
        url : str/dict
            URL path and/or metadata (if dict).
        save_dir : str
            Directory path to save the downloaded file.
        verbose : bool, optional
            Display messages + progress bar on screen when downloading the file.

        """
        if self.exists_url_file(url, save_dir):
            if verbose:
                print('File already exists, skip downloading this url.')
        else:
            self.download_url(url, save_dir, verbose)

    def exists_url_file(self, url, save_dir):
        _, _, filename = self.get_url_metadata_and_dir_paths(url, save_dir)
        return os.path.exists(filename)

    def get_url_metadata_and_dir_paths(self, url, save_dir):
        url_metadata = self.parse_url_metadata(url)
        download_dir = os.path.join(save_dir, url_metadata["extract_dir"])
        filename = os.path.join(download_dir, url_metadata["filename"])
        return url_metadata, download_dir, filename

    def download_url(self, url, save_dir, verbose):
        """Downloads an url to a file."""
        url_metadata, download_dir, filename = self.get_url_metadata_and_dir_paths(url, save_dir)
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        self.download_url_to_file(url_metadata, filename, verbose)
        if url_metadata["md5hash"]:
            self.md5_checksum(filename, url_metadata["md5hash"])

    def parse_url_metadata(self, url):
        """Returns the url, md5hash and dir strings from a tupple.

        Parameters
        ----------
        url : str/dict
            URL path and/or metadata (if dict).

        Returns
        -------
        dict
            Metadata with URL's path, md5hash, filename, extract dir and method type.

        """
        assert isinstance(url, (str, dict)), 'Invalid url type: {}. Valid types: str, dict.'.format(type(url))

        if isinstance(url, str):
            url_ = url
        else:
            url_ = url['url']

        return {
            "url": url_,
            "md5hash": self.get_value_from_key(url, key='md5hash', default=None),
            "filename": self.get_value_from_key(url, key='save_name', default=os.path.basename(url_)),
            "extract_dir": self.get_value_from_key(url, key='extract_dir', default=''),
            "method": self.get_value_from_key(url, key='source', default='requests'),
        }

    def get_value_from_key(self, dictionary, key, default=None):
        """Returns the value of a field in a dictionary if it exists or a predefined value."""
        try:
            return dictionary[field]
        except KeyError:
            return default

    def download_url_to_file(self, url_metadata, filename, verbose=True):
        """Downloads a single url into a file.

        Parameters
        ----------
        url_metadata : dict
            URL metadata.
        filename : str
            File name + path to save the url's data to disk.
        verbose : bool, optional
            Display messages + progress bar on screen when downloading the file.

        Raises
        ------
        InvalidURLDownloadSource
            If the input download method is invalid.

        """
        # Create temporary file to store the downloaded data
        tmpfile = self.create_temp_file(filename)

        # download the file
        if method == 'requests':
            URLDownload.download(url, filename=tmpfile, verbose=verbose)
        elif method == 'googledrive':
            URLDownloadGoogleDrive.download(url, filename=tmpfile)
        else:
            raise InvalidURLDownloadSource('Invalid url source: {}'.format(method))

        # rename temporary file to final output file
        shutil.move(tmpfile, filename)

    def create_temp_file(self, filename):
        """Create a temporary file in filename's save directory.

        Parameters
        ----------
        filename : str
            File name + path to save the url's data to disk.

        Returns
        ------
        str
            File name + path of the temporary file.

        """
        filename_dir = os.path.commonpath(filename)
        (fd, tmpfile) = tempfile.mkstemp(".tmp", prefix=filename, dir=filename_dir)
        os.close(fd)
        os.unlink(tmpfile)
        return tmpfile

    def md5_checksum(self, filename, md5hash):
        """Check file integrity using a checksum.

        Parameters
        ----------
        filename : str
            File path + name of the downloaded url.
        md5hash : str
            Md5 hash string.

        Raises
        ------
        MD5HashNotEqual
            MD5 hash checksum do not match.

        """
        file_hash = self.get_hash_value(filename)
        if not file_hash == md5hash:
            raise MD5HashNotEqual("MD5 checksums do not match: {} != {}".format(md5hash, file_hash))

    def get_hash_value(self, fname):
        """Retrieve the checksum of a file.

        Parameters
        ----------
        fname : str
            File name + path on disk.

        Returns
        -------
        str
            Checksum string.

        """
        return hashlib.md5(open(fname, 'rb').read()).hexdigest()

    @classmethod
    def get_url_filename(self, url, save_dir):
        """Checks if an url file already exists in a directory.

        Parameters
        ----------
        url : str/dict
            URL metadata.
        save_dir : str
            Directory path where the file is supposed to be.

        Returns
        -------
        bool
            True if a file exists for the input url.
            Otherwise, returns False.

        """
        return self.exists_url_file(url, save_dir)


class URLDownload:
    """Download an URL using the requests module."""

    @classmethod
    def download(self, url, fname, verbose=False):
        """Downloads a file from an url.

        Parameters
        ----------
        url : str
            URL location.
        fname : str
            File name + path to store the downloaded data to disk.
        verbose : bool, optional
            Display progress bar

        Raises
        ------
        URLDoesNotExist
            If an URL is invalid/does not exist.

        """
        if not self.check_exists_url(url):
            raise URLDoesNotExist("Invalid url or does not exist: {}".format(url))

        CHUNK_SIZE = 1024
        with requests.get(url, stream=True) as r:
            with open(fname, 'wb') as f:
                if verbose:
                    total_length = int(r.headers.get('content-length'))
                    if total_length is None:
                        f.write(r.content)
                    else:
                        progbar_length = int(total_length / CHUNK_SIZE)
                        progbar = progressbar.ProgressBar(maxval=progbar_length).start()
                        i = 0
                        for data in r.iter_content(chunk_size=CHUNK_SIZE):
                            if data:
                                f.write(data)
                                f.flush()
                                progbar.update(i)
                                i += 1
                        progbar.finish()
                else:
                    f.write(r.content)

    def check_exists_url(self, url):
        """Check if an url exists.

        Parameters
        ----------
        url : str
            Url path.

        Returns
        ------
        bool
            Returns True if the url request returns a 200 status code.

        """
        request = requests.head(url, allow_redirects=False)
        return request.status_code == 200


class URLDownloadGoogleDrive:
    """Download an URL from Google Drive."""

    base_url = "https://docs.google.com/uc?export=download"

    @classmethod
    def download(self, file_id, filename):
        """Download a single url from google drive into a file.

        Parameters
        ----------
        file_id : str
            File ID in the google drive.
        filename : str
            File name + path to store the downloaded data to disk.

        """
        session = requests.Session()
        token = self.get_confirmation_token(session, file_id)
        response = session.get(self.base_url, params={'id': file_id, 'confirm': token}, stream=True)
        self.save_response_content(response, filename)

    def get_confirmation_token(self, session, params):
        """Returns a confirmation token.

        Parameters
        ----------
        session : requests.sessions.Session
            Request session.
        file_id : str
            File ID in the google drive.

        Returns
        ------
        str
            Token string.

        Raises
        ------
        GoogleDriveFileIdDoesNotExist
            If the google drive's file id is invalid.

        """
        response = session.get(self.base_url, params={'id': file_id}, stream=True)
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        raise GoogleDriveFileIdDoesNotExist('Invalid google drive file id: {}.'.format(file_id))

    def save_response_content(self, response, filename):
        """Saves a session data to file.

        Parameters
        ----------
        response : requests.models.Response
            Session response.
        filename : str
            File name + path to store the downloaded data to disk.

        """
        CHUNK_SIZE = 32768
        with open(filename, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
