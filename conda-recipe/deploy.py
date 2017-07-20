#!/usr/bin/env python


"""
Deploy dbcollection to pypi and conda.
"""


import os
import shutil
import subprocess


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
    msg = subprocess.run(["conda", 'convert', "-p", "all", artifact_fname, "-o", temp_output_dir], stdout=subprocess.PIPE)

    # upload to anaconda
    print(' > Upload all artifact to all platforms...')
    print('   -- Uploading artifact: {}'.format(artifact_fname))
    msg_upload = subprocess.run(["anaconda", "upload", artifact_fname], stdout=subprocess.PIPE)
    for root, dirs, files in os.walk(temp_output_dir):
        if any(files):
            for fname in files:
                if fname.endswith('.tar.bz2'):
                    print('   -- Uploading artifact: {} '.format(root + '/' + fname))
                    msg = subprocess.run(["anaconda", 'upload', root + '/' + fname], stdout=subprocess.PIPE)


print('\nRemoving temp dir: {}'.format(temp_output_dir))
if os.path.exists(temp_output_dir):
    shutil.rmtree(temp_output_dir, ignore_errors=True)