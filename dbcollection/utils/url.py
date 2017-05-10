"""
Download functions.
"""


from __future__ import print_function, division
import os
import urllib
import hashlib
import patoolib
import requests
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


def download_url_progressbar(url, file_save_name):
    """Download a file (displays a progress bar).

    Parameters
    ----------
    url : str
        URL location.
    file_save_name : str
        File name + path to store on disk.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    chunk_size = 4096*2
    max_size = 1024*1024
    with open(file_save_name, 'wb') as f:
        response = requests.get(url, stream=True)
        file_size = response.headers.get('content-length')

        if file_size is None:
            f.write(response.content)
        else:
            file_size = int(file_size)
            if file_size >= max_size*10:
                chunk_size = max_size
            num_bars = file_size / chunk_size
            progbar = progressbar.ProgressBar(maxval=num_bars).start()
            i = 0
            for data in response.iter_content(chunk_size=chunk_size):
                f.write(data)
                progbar.update(i)
                i += 1


def download_url_nodisplay(url, file_save_name):
    """Download a file (no display text).

    Parameters
    ----------
    url : str
        URL location.
    file_save_name : str
        File name + path to store on disk.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    with urllib.request.urlopen(url) as response, open(file_save_name, 'wb') as out_file:
        data = response.read() # a `bytes` object
        out_file.write(data)


def download_url(url, dir_path, fname_save, verbose=False):
    """Download a single url data into a file.

    Parameters
    ----------
    url : str
        URL location.
    dir_path : str
        Directory path to store the file.
    fname_save : str
        File name + path.
    verbose : bool
        Display messages + progress bar on screen when downloading the file.

    Returns
    -------
        None

    Raises
    ------
        None
    """
    # save file
    file_save_name = fname_save

    # check if the filename already exists
    if os.path.exists(file_save_name):
        return True

    # check if the path exists
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # download the file
    if verbose:
        download_url_progressbar(url, file_save_name)
    else:
        download_url_nodisplay(url, file_save_name)


def download_url_google_drive(file_id, dir_path, fname_save, verbose=False):
    """Download a single url from google drive into a file.

    Parameters
    ----------
    file_id : str
        File ID.
    dir_path : str
        Directory path to store the file.
    fname_save : str
        File name + path.
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

    # save file
    file_save_name = fname_save

    # check if the filename already exists
    if os.path.exists(file_save_name):
        return True

    # check if the path exists
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id' : file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id' : file_id, 'confirm' : token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, file_save_name)


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

        # download file
        if isinstance(url, str):
            # get download save filename
            filename = os.path.join(dir_save, os.path.basename(url))

            if download_url(url, dir_save, filename, verbose) and verbose:
                print('File already exists, skip downloading this url.')
                continue
        elif isinstance(url, list):
            # get download save filename
            filename = os.path.join(dir_save, url[-1])

            if url[0] is 'googledrive':
                if download_url_google_drive(url[1], dir_save, filename, verbose) and verbose:
                    print('File already exists, skip downloading this url.')
                    continue
            else:
                raise KeyError('Undefined key: {}. Valid keys: googledrive.'.format(url[0]))

        # check md5 sum (if available)
        if any(md5sum):
            file_hash = get_hash_value(filename)
            if not file_hash == md5sum:
                print('**WARNING**: md5 checksum does not match for file: {}'.format(filename))
                print('Checksum expected: {}, got: {}'.format(md5sum, file_hash))

        # extract file
        if extract_data:
            patoolib.extract_archive(filename, outdir=dir_save, verbosity=verbose)

