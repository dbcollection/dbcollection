#!/usr/bin/env python


"""
Deploy dbcollection to pypi and conda.

Warning: run this script from the root dir of the project.
"""


from __future__ import print_function
import os
import shutil
import subprocess


cwd = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(cwd, 'build')
if os.path.exists(build_dir):
    print('Removing dir: {}'.format(build_dir))
    shutil.rmtree(build_dir, ignore_errors=True)

dist_dir = os.path.join(cwd, 'dist')
if os.path.exists(dist_dir):
    print('Removing dir: {}'.format(dist_dir))
    shutil.rmtree(dist_dir, ignore_errors=True)


# PyPi
print('PyPi: Upload sdist...')
msg1 = subprocess.run(["python", 'setup.py', 'sdist', 'upload'], stdout=subprocess.PIPE)
print('PyPi: Upload bdist_wheel...')
msg2 = subprocess.run(["python", 'setup.py', 'bdist_wheel', 'upload'], stdout=subprocess.PIPE)


# Conda
python_versions = ["2.7", "3.5", "3.6"]
for i, pyver in enumerate(python_versions):
    print('\nAnaconda: Start build {}/{}'.format(i+1, len(python_versions)))
    print(' > Python version: {}'.format(pyver))

    temp_output_dir = 'output_build'
    print(' > Saving artifacts to dir: {}'.format(temp_output_dir))
    if os.path.exists(temp_output_dir):
        shutil.rmtree(temp_output_dir, ignore_errors=True)

    # build conda
    print(' > Build conda recipe...')
    cmd = ["conda", 'build', '--python={}'.format(pyver), '--no-anaconda-upload', 'conda-recipe']
    msg = subprocess.run(cmd, stdout=subprocess.PIPE)

    # parse string message
    print(' > Parse conda artifact file name + path...')
    msg_s = str(msg)
    str_ini = "If you want to upload package(s) to anaconda.org later, type:\\n\\nanaconda upload "
    str_end = "\\n\\n# To have conda build upload to anaconda.org automatically"
    ini_id = msg_s.find(str_ini) + len(str_ini)
    end_id = msg_s.find(str_end)
    artifact_fname = msg_s[ini_id:end_id]
    print(' > Artifact name: {}'.format(artifact_fname))


    # convert to all platforms
    print(' > Convert artifact to all platforms...')
    msg = subprocess.run(["conda", 'convert', "-p", "all", artifact_fname, "-o", temp_output_dir],
                         stdout=subprocess.PIPE)

    # upload to anaconda
    print(' > Upload all artifact to all platforms...')
    print('   -- Uploading artifact: {}'.format(artifact_fname))
    msg_upload = subprocess.run(["anaconda", "upload", artifact_fname], stdout=subprocess.PIPE)
    for root, dirs, files in os.walk(temp_output_dir):
        if any(files):
            for fname in files:
                if fname.endswith('.tar.bz2'):
                    print('   -- Uploading artifact: {} '.format(root + '/' + fname))
                    msg = subprocess.run(["anaconda", 'upload', root + '/' + fname],
                                         stdout=subprocess.PIPE)


if os.path.exists(temp_output_dir):
    print('\nRemoving temp dir: {}'.format(temp_output_dir))
    shutil.rmtree(temp_output_dir, ignore_errors=True)

if os.path.exists(build_dir):
    print('\nRemoving temp dir: {}'.format(build_dir))
    shutil.rmtree(build_dir, ignore_errors=True)

if os.path.exists(dist_dir):
    print('\nRemoving temp dir: {}'.format(dist_dir))
    shutil.rmtree(dist_dir, ignore_errors=True)
