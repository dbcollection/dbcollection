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
    """Check if an url exists."""
    request = requests.head(url, allow_redirects=False)
    if request.status_code == 200:
        return True, ''
    else:
        return False, 'url does not exist: {}'.format(url)


def download_url_requests(url, fname, verbose=False):
    """Download a file (no display text).

    Parameters
    ----------
    url : str
        URL location.
    fname : str
        File name + path to store in disk.
    verbose : bool
        Display progress bar

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
                    progbar = progressbar.ProgressBar(maxval=int(total_length/chunk_size)).start()
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


def download_url_google_drive(file_id, filename, verbose=False):
    """Download a single url from google drive into a file.

    Parameters
    ----------
    file_id : str
        File ID in the google drive.
    filename : str
        File name + path to store in disk.
    verbose : bool
        Display messages + progress bar on screen when downloading the file.

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
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)


    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id' : file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id' : file_id, 'confirm' : token}
        response = session.get(URL, params=params, stream=True)
        status, err = True, ''
    else:
        status, err = False, 'Invalid url: {}. Token does not exist'.format(URL)

    save_response_content(response, filename)

    return status, err


def download_url(url, filename, method, verbose=False):
    """Download a single url data into a file.

    Parameters
    ----------
    url : str
        URL location.
    filename : str
        File name + path to save the url to disk.
    method : str
        Download method (requests or googledrive)
    verbose : bool
        Display messages + progress bar on screen when downloading the file.

    Raises
    ------
    Exception
        If the method does not exit.

    """

    # get filename for temp file in current directory
    (fd, tmpfile) = tempfile.mkstemp(".tmp", prefix=filename, dir=".")
    os.close(fd)
    os.unlink(tmpfile)

    # download the file
    if method == 'requests':
        status, err = download_url_requests(url, tmpfile, verbose)
    elif method == 'googledrive':
        status, err = download_url_google_drive(url, tmpfile, verbose)
    else:
        status, err = False, 'Invalid method: {}'.format(method)

    # rename temporary file to final output file
    if status:
        shutil.move(tmpfile, filename)

    return status, err


def parse_url(url):
    """Returns the url, md5hash and dir strings from a tupple"""

    def get_field_value(d, field):
        """Check if field exists and return its value from a dictionary. Else, return None."""
        if field in d:
            return d[field]
        else:
            return None

    if isinstance(url, str):
        return url, None, os.path.basename(url), '', 'requests'
    elif isinstance(url, dict):
        url_ = get_field_value(url, 'url')
        md5sum = get_field_value(url, 'md5sum')
        save_name = get_field_value(url, 'save_name')
        extract_dir = get_field_value(url, 'extract_dir') or ''
        method = get_field_value(url, 'googledrive') or 'requests'

        if save_name:
            filename = save_name
        else:
            filename = os.path.basename(url_)
        return url_, md5sum, filename, extract_dir, method
    else:
        raise TypeError('Invalid url type: {}'.format(type(url)))


def md5_checksum(filename, md5hash):
    """Check file integrity using a checksum."""
    file_hash = get_hash_value(filename)
    if not file_hash == md5hash:
        print('**WARNING**: md5 checksum does not match for file: {}'.format(filename))
        print('Checksum expected: {}, got: {}'.format(md5hash, file_hash))


def download_extract_all(urls, md5sum, dir_save, extract_data=True, verbose=True):
    """Download urls + extract files to disk.

    Download + extract all url files to disk. If clean_cache is
    True, it removes the download files.

    Parameters
    ----------
    urls : list
        List of URL paths.
    md5sum : list
        List of md5 checksum strings for each url.
    dir_save : str
        Directory path to store the data.
    extract_data : bool
        Extracts/unpacks the data files (if true).
    verbose : bool
        Display messages on screen.

    Raises
    ------
    Exception
        If it is an invalid url type.
    KeyError
        If the download method is invalid.
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
            print('\nDownload url ({}/{}): {}'.format(i+1, len(urls), url))

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
