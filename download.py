from clint.textui import progress
import urllib
import requests
import tarfile
import zipfile
import os

# create directory if not existing
def create_dir(dirName, verbose):
    if verbose:
        print('Creating directory: {}'.format(dirName))
    os.makedirs(dirName)


# download files to disk
def download_file(url, dirName, fnameSave, verbose):
    # save file 
    file_save_name = dirName+fnameSave

    # check if the path exists
    if not os.path.exists(dirName):
        create_dir(dirName, verbose)

    # download the file
    if verbose:
        print('Downloading {} to: {}'.format(url, file_save_name))
        r = requests.get(url, stream=True)
        with open(file_save_name, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                if chunk:
                    f.write(chunk)
                    f.flush()
    else:
        with urllib.request.urlopen(url) as response, open(file_save_name, 'wb') as out_file:
          data = response.read() # a `bytes` object
          out_file.write(data)


# retrieve filename extension
def get_file_extension(fname):
    str_split = fname.split('.')
    return str_split[-1]

# extract zip file
def extract_file_zip(fname, path):
    zip_ref = zipfile.ZipFile(fname, 'r')
    zip_ref.extractall(path)
    zip_ref.close()

# extract .tar file
def extract_file_tar(fname, path):
    tar = tarfile.open(fname)
    tar.extractall(path)
    tar.close()

# extract files to disk
def extract_file(path, fname, verbose):
    file_name = path + fname

    if verbose:
        print('Extracting file to disk: {}'.format(file_name))

    # check filename extension
    extension = get_file_extension(fname)

    if extension == 'zip':
        extract_file_zip(file_name, path)
    elif extension == 'tar' or extension == 'gz':
        extract_file_tar(file_name, path)
    else:
        raise Exception('Undefined extension: {}'.format(extension))

def remove_file(fname):
    # check if the path exists
    if os.path.exists(fname):
        os.remove(fname)