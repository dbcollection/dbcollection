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
        filename = URL.get_url_filename(url)
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
        if URL().exists_url_file(url, save_dir):
            if verbose:
                print('File already exists in disk, skip downloading this url.')
            _, _, filename = self.get_url_metadata_and_dir_paths(url, save_dir)
        else:
            filename = URL().download_url(url, save_dir, verbose)
        return filename

    def exists_url_file(self, url, save_dir):
        """Checks if an url file already exists in a directory."""
        _, _, filename = self.get_url_metadata_and_dir_paths(url, save_dir)
        return os.path.exists(filename)

    def get_url_metadata_and_dir_paths(self, url, save_dir):
        url_metadata = self.parse_url_metadata(url)
        download_dir = os.path.join(save_dir, url_metadata["extract_dir"])
        filename = os.path.join(download_dir, url_metadata["filename"])
        return url_metadata, download_dir, filename

    def download_url(self, url, save_dir, verbose):
        """Downloads an url to a file and returns its path in disk."""
        url_metadata, download_dir, filename = self.get_url_metadata_and_dir_paths(url, save_dir)
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        self.download_url_to_file(url_metadata, filename, verbose)
        if url_metadata["md5hash"]:
            self.md5_checksum(filename, url_metadata["md5hash"])
        return filename

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

    def get_value_from_key(self, input, key, default=None):
        """Returns the value of a field in a dictionary if it exists or a predefined value."""
        try:
            return input[key]
        except KeyError:
            return default
        except TypeError:
            return default

    def download_url_to_file(self, url_metadata, filename, verbose=True):
        """Downloads a single url to a file.

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
        method = url_metadata['method']
        url = url_metadata['url']
        if method == 'requests':
            URLDownload().download(url, filename=tmpfile, verbose=verbose)
        elif method == 'googledrive':
            URLDownloadGoogleDrive().download(url, filename=tmpfile)
        else:
            raise InvalidURLDownloadSource('Invalid url source: {}'.format(method))

        # rename temporary file to final output file
        shutil.move(tmpfile, filename)

    def create_temp_file(self, filename):
        """Create a temporary file in the input filename's save directory.

        Parameters
        ----------
        filename : str
            File name + path to save the url's data to disk.

        Returns
        ------
        str
            File name + path of the temporary file.

        """
        filename_dir = os.path.dirname(filename)
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
        file_hash = self.get_file_hash(filename)
        if not file_hash == md5hash:
            raise MD5HashNotEqual("MD5 checksums do not match: {} != {}".format(md5hash, file_hash))

    def get_file_hash(self, filename):
        """Retrieves the checksum of a file.

        Parameters
        ----------
        filename : str
            File name + path on disk.

        Returns
        -------
        str
            Checksum string.

        """
        return hashlib.md5(open(filename, 'rb').read()).hexdigest()

    @classmethod
    def get_url_filename(self, url):
        """Returns the filename for an URL.

        Parameters
        ----------
        url : str/dict
            URL metadata.

        Returns
        -------
        str
            URL file name.

        """
        url_metadata = URL().parse_url_metadata(url)
        return url_metadata['filename']


class URLDownload:
    """Download an URL using the requests module."""

    def download(self, url, filename, verbose=False):
        """Downloads an url data and stores it into a file.

        Parameters
        ----------
        url : str
            URL location.
        filename : str
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
        self.download_url(url, filename, verbose)

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
        request = requests.head(url, allow_redirects=True)
        return request.status_code == 200

    def download_url(self, url, filename, verbose):
        """Download an URL using the 'requests' module."""
        CHUNK_SIZE = 1024
        with requests.get(url, stream=True) as r:
            with open(filename, 'wb') as f:
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


class URLDownloadGoogleDrive:
    """Download an URL from Google Drive."""

    base_url = "https://docs.google.com/uc?export=download"

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

    def get_confirmation_token(self, session, file_id):
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
