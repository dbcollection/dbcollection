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
        None
    """
    try:
        return hashlib.md5(open(fname, 'rb').read()).hexdigest()
    except (IOError, OSError):
        raise IOError('Error opening file: {}'.format(fname))


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

    Returns
    -------
        None

    Raises
    ------
        None
    """
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

    Returns
    -------
        None

    Raises
    ------
        None
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

    save_response_content(response, filename)


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

    Returns
    -------
        None

    Raises
    ------
        None
    """

    # get filename for temp file in current directory
    (fd, tmpfile) = tempfile.mkstemp(".tmp", prefix=filename, dir=".")
    os.close(fd)
    os.unlink(tmpfile)

    # download the file
    if method == 'requests':
        download_url_requests(url, tmpfile, verbose)
    elif method == 'googledrive':
        download_url_google_drive(url, tmpfile, verbose)
    else:
        raise Exception('Invalid method: {}'.format(method))

    # rename temporary file to final output file
    shutil.move(tmpfile, filename)


def check_if_file_exists(filename, dir_save, verbose=True):
    """Check if the file exists in a directory.

    Parameters
    ----------
    filename : str
        Name of the file.
    dir_save : str
        Path of the directory to store the file.
    verbose : bool
        Display messages on screen.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # check if the path exists
    if not os.path.exists(dir_save):
        os.makedirs(dir_save)

    # check if the filename already exists
    return os.path.exists(filename)


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

    Returns
    -------
        None

    Raises
    ------
        None
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

        # parse filename
        if isinstance(url, str):
            filename = os.path.join(dir_save, os.path.basename(url))
        elif isinstance(url, list):
            filename = os.path.join(dir_save, url[-1])
        else:
            raise Exception('Invalid url type: {}'.format(type(url)))

        # check if file exists in disk
        if check_if_file_exists(filename, dir_save, verbose):
            print('File already exists, skip downloading this url.')
        else:
            if isinstance(url, str):
                method = 'requests'
            elif isinstance(url, list):
                if url[0] is 'googledrive':
                    method = 'googledrive'
                    url = url[1]
                else:
                    raise KeyError('Invalid key: {}. Valid keys: googledrive.'.format(url[0]))

            # download file
            download_url(url, filename, method, verbose)

            # check md5 sum (if available)
            if any(md5sum):
                file_hash = get_hash_value(filename)
                if not file_hash == md5sum:
                    print('**WARNING**: md5 checksum does not match for file: {}'.format(filename))
                    print('Checksum expected: {}, got: {}'.format(md5sum, file_hash))

        # extract file
        if extract_data:
            patoolib.extract_archive(filename, outdir=dir_save, verbosity=verbose)
