"""
Extract image frames from videos.
"""

from __future__ import print_function, division
import os
import subprocess
import progressbar


def get_filepaths_names(root_path):
    filenames, video_names, categories = [], [], []
    for root, _, files in os.walk(root_path, topdown=True):
        if any(files):
            filenames = filenames + [os.path.join(root, fname) for fname in files]
            vid_names = [os.path.splitext(fname)[0] for fname in files if fname.endswith('.avi')]
            video_names = video_names + vid_names
            categories = categories + [os.path.basename(root)] * len(files)
    return filenames, categories, video_names


def extract_video_frames(root_path, verbose=True):
    """
    Extract frames from all videos of the UCF-101 dataset.
    """
    assert os.path.isdir(root_path)

    # setup paths
    data_dir = os.path.join(root_path, 'UCF-101')
    save_dir = os.path.join(root_path, 'UCF-101-images')

    if verbose:
        print('==> (UCF-101) Extracting image frames from videos to disk: {}'.format(save_dir))
        print('Warning: This will take a few minutes.')

    # get videos file name+path, categories + video names
    filenames, categories, videos = get_filepaths_names(data_dir)
    num_vids = len(filenames)

    # setup stdout suppression for subprocess
    try:
        from subprocess import DEVNULL  # py3k
    except ImportError:
        DEVNULL = open(os.devnull, 'wb')

    # cycle all files and extract frames from them
    progbar = progressbar.ProgressBar(maxval=num_vids).start()
    for i in range(0, num_vids):
        # setup save dir
        save_path = os.path.join(save_dir, categories[i], videos[i])

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # extract image frames from the videos
        try:
            subprocess.Popen('ffmpeg -i {} -f image2 {}-%04d.jpg'
                             .format(filenames[i], os.path.join(save_path, 'image')),
                             shell=True, stdout=DEVNULL, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            raise Exception('\n\nError occurred when parsing {}\n'.format(filenames[i]))

        # update progress bar
        progbar.update(i)

    if verbose:
        progbar.update(num_vids)
        print('Extraction complete.')
