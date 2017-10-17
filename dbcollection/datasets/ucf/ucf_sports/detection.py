"""
UCF-Sports action detection process functions.
"""


from __future__ import print_function, division
import os
import random
import subprocess
import numpy as np
import progressbar

from dbcollection.datasets import BaseTask

from dbcollection.utils.file_load import load_txt
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list
from dbcollection.utils.hdf5 import hdf5_write_data


class Detection(BaseTask):
    """UCF-Sports action detection preprocessing functions."""

    # metadata filename
    filename_h5 = 'detection'

    classes = ["diving", "golf_swing", "kicking", "lifting", "riding_horse",
               "running", "skateboarding", "swing_bench", "swing_side", "walking"]

    def get_activity_name(self, cname):
        """
        Get the activity by matching a string with a similar name.
        """
        dir_class = {
            "Diving-Side": "diving",
            "Kicking-Front": "kicking",
            "Run-Side": "running",
            "Walk-Front": "walking",
            "Golf-Swing-Back": "golf_swing",
            "Kicking-Side": "kicking",
            "SkateBoarding-Front": "skateboarding",
            "Golf-Swing-Front": "golf_swing",
            "Lifting": "lifting",
            "Swing-Bench": "swing_bench",
            "Golf-Swing-Side": "golf_swing",
            "Riding-Horse": "riding_horse",
            "Swing-SideAngle": "swing_side"
        }

        return dir_class[cname]

    def extract_video_frames(self, video_filename, video_name, save_dir):
        """
        Extract frames from a video.
        """
        assert video_filename
        assert video_name
        assert save_dir

        # setup stdout suppression for subprocess
        try:
            from subprocess import DEVNULL  # py3k
        except ImportError:
            DEVNULL = open(os.devnull, 'wb')

        # extract image frames from the videos
        try:
            img_name = os.path.join(save_dir, video_name)
            cmd = ['ffmpeg', '-i', video_filename, '-f', 'image2',
                   '{}-%04d.jpg'.format(img_name)]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            raise Exception('\n\nError occurred when parsing {}\n'.format(video_filename))

    def load_annotation(self, fname):
        """
        Load the annotations from a file.
        """
        data = load_txt(fname)
        data = data[0].split('\t')[:-1]  # discard the last element
        return [int(s) for s in data]

    def load_files_annotations(self):
        """
        Load activities, videos, filenames paths and annotations from the data directory.
        """
        self.activities_dir = os.path.join('ucf_sports_actions', 'ucf action')
        self.root_dir_imgs = os.path.join(self.data_path, self.activities_dir)

        if self.verbose:
            print(' > Fetch videos, images paths and annotations from dir: {}'
                  .format(self.root_dir_imgs))

        # initialize data dictorionary
        data = {}
        for activity in self.classes:
            data[activity] = {}

        if self.verbose:
            # count the total number of videos
            total_vids = 0
            dirs = os.listdir(self.root_dir_imgs)
            for dname in dirs:
                total_vids += len(os.listdir(os.path.join(self.root_dir_imgs, dname)))

            # setup progressbar
            progbar = progressbar.ProgressBar(maxval=total_vids).start()
            i = 0

        # fetch all activities folders
        activities_dir = os.listdir(self.root_dir_imgs)
        activities_dir.sort()

        # cycle all folders
        for activity in activities_dir:
            activity_ = self.get_activity_name(activity)
            videos = os.listdir(os.path.join(self.root_dir_imgs, activity))
            videos.sort()
            for video in videos:
                dir_path = os.path.join(self.root_dir_imgs, activity, video)
                if os.path.exists(os.path.join(dir_path, 'gt')):
                    all_files = os.listdir(dir_path)
                    all_files.sort()
                    image_filenames = [fname for fname in all_files if fname.endswith('.jpg')]
                    video_filename = [vname for vname in all_files if vname.endswith('.avi')]
                    video_path = os.path.join(self.data_path, self.activities_dir, activity, video)
                    if not any(video_filename):
                        video_filename = 'not_available'
                    else:
                        video_filename = video_filename[0]

                    # check if any image filenames exist
                    if not any(image_filenames):
                        video_filename_path = os.path.join(dir_path, video_filename)
                        video_name = os.path.splitext(os.path.basename(video_filename_path))[0]
                        self.extract_video_frames(video_filename_path, video_name, dir_path)

                        # fetch again the image filenames
                        image_filenames = [fname for fname in all_files if fname.endswith('.jpg')]

                    # add the directory path to the image filenames

                    image_filenames = [os.path.join(video_path, fname) for fname in image_filenames]
                    image_filenames.sort()

                    # load annotations from the .txt files
                    gt_files = os.listdir(os.path.join(self.root_dir_imgs, activity, video, 'gt'))
                    gt_files = [fname for fname in gt_files if fname.endswith('.txt')]
                    gt_files = [os.path.join(self.root_dir_imgs, activity, video, 'gt', fname)
                                for fname in gt_files]
                    gt_files.sort()
                    annotations = [self.load_annotation(f) for _, f in enumerate(gt_files)]

                    # assign data to dict
                    data[activity_][video] = {
                        "video_filename": os.path.join(video_path, video_filename),
                        "image_filenames": image_filenames,
                        "image_annotations": annotations
                    }

                    # update progress bar
                    progbar.update(i)
                    i += 1

        # set progressbar to 100%
        progbar.finish()

        return data

    def split_dataset_generator(self, data, train_percent=2 / 3, num_splits=5):
        """
        Divide dataset into train and test splits
        """
        random.seed(4)

        for i in range(1, num_splits + 1):
            if self.verbose:
                print(' > Generating random dataset splits ({}/{}): '.format(i, num_splits) +
                      'train percentage={}, num splits={}'.format(train_percent, num_splits))

            train_set_name = 'train0' + str(i)
            test_set_name = 'test0' + str(i)

            out_data = {
                train_set_name: {},
                test_set_name: {}
            }

            for activity in data:
                videos = list(data[activity].keys())

                # shuffle videos
                random.shuffle(videos)

                # determine splits
                num_videos = len(videos)
                tr_num_vids = int(num_videos * train_percent)

                # train set
                out_data[train_set_name][activity] = {}
                for video in videos[:tr_num_vids]:
                    out_data[train_set_name][activity][video] = data[activity][video]

                # test set
                out_data[test_set_name][activity] = {}
                for video in videos[tr_num_vids:]:
                    out_data[test_set_name][activity][video] = data[activity][video]

            yield out_data

    def load_data(self):
        """
        Load the data from the files.
        """
        # load video, images filenames and annotations
        data = self.load_files_annotations()

        # divide dataset into train and test splits
        train_percent = 2 / 3
        num_splits = 5
        splits_gen = self.split_dataset_generator(data, train_percent, num_splits)

        return splits_gen

    def convert_data_to_arrays(self, data):
        """
        Convert data to arrays.
        """
        # intialize lists
        object_ids = []
        videos = []
        video_filenames = []
        image_filenames = []
        annotations = []
        total_frames = []
        list_videos_per_class = {}
        list_image_filenames_per_video = []
        list_annotations_per_video = []

        count_video = 0
        for activity_id, activity in enumerate(self.classes):
            videos_ordered = list(data[activity].keys())
            videos_ordered.sort()
            for _, video_name in enumerate(videos_ordered):
                img_fnames = data[activity][video_name]['image_filenames']
                annot = data[activity][video_name]['image_annotations']
                num_imgs = len(img_fnames)
                total_frames.append(num_imgs)

                videos.append(video_name)  # add video name
                video_filenames.append(data[activity][video_name]['video_filename'])

                image_filenames = image_filenames + img_fnames
                annotations = annotations + annot

                # add to list of images per video
                total_imgs = len(image_filenames)
                list_range = list(range(total_imgs - num_imgs, total_imgs))
                list_image_filenames_per_video.append(list_range)
                list_annotations_per_video.append(list_range)

                # add to list of videos per class
                try:
                    list_videos_per_class[activity_id].append(count_video)
                except KeyError:
                    list_videos_per_class[activity_id] = [count_video]

                # add data to 'object_ids'
                # [video, video_filename, list_images_per_video,
                # list_annotations_per_video, activity, total_imgs]
                object_ids.append([count_video, count_video, count_video,
                                   count_video, activity_id, num_imgs])

                # update video counter
                count_video += 1

        return {
            "object_fields": str2ascii(['videos', 'video_filenames',
                                        'list_image_filenames_per_video',
                                        'list_annotations_per_video',
                                        'activities', 'total_frames']),
            "object_ids": np.array(object_ids, dtype=np.int32),
            "videos": str2ascii(videos),
            "video_filenames": str2ascii(video_filenames),
            "activities": str2ascii(self.classes),
            "image_filenames": str2ascii(image_filenames),
            "annotations": np.array(annotations, dtype=np.int32),
            "total_frames": np.array(total_frames, dtype=np.int32),
            "list_videos_per_activity": np.array(pad_list(list(list_videos_per_class.values()), -1),
                                                 dtype=np.int32),
            "list_image_filenames_per_video": np.array(pad_list(list_image_filenames_per_video, -1),
                                                       dtype=np.int32),
            "list_annotations_per_video": np.array(pad_list(list_annotations_per_video, -1),
                                                   dtype=np.int32)
        }

    def add_data_to_source(self, hdf5_handler, data, set_name=None):
        """
        Store data annotations in a nested tree fashion.

        It closely follows the tree structure of the data.
        """
        for activity in data:
            activity_grp = hdf5_handler.create_group(activity)
            for video_name in data[activity]:
                video_grp = activity_grp.create_group(video_name)
                set_data = data[activity][video_name]
                video_grp.create_dataset('image_filenames', data=str2ascii(
                    set_data['image_filenames']), dtype=np.uint8)
                video_grp.create_dataset('video_filename', data=str2ascii(
                    set_data['video_filename']), dtype=np.uint8)
                video_grp.create_dataset('annotations', data=np.array(
                    set_data['image_annotations']), dtype=np.int32)

    def add_data_to_default(self, hdf5_handler, data, set_name=None):
        """
        Add data of a set to the default group.

        For each field, the data is organized into a single big matrix.
        """
        data_array = self.convert_data_to_arrays(data)
        hdf5_write_data(hdf5_handler, 'videos',
                        data_array["videos"],
                        dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'video_filenames',
                        data_array["video_filenames"],
                        dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'activities',
                        data_array["activities"],
                        dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'image_filenames',
                        data_array["image_filenames"],
                        dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'annotations',
                        data_array["annotations"],
                        dtype=np.int32, fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'total_frames',
                        data_array["total_frames"],
                        dtype=np.int32, fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'object_ids',
                        data_array["object_ids"],
                        dtype=np.int32, fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'object_fields',
                        data_array["object_fields"],
                        dtype=np.uint8, fillvalue=0)

        pad_value = -1
        hdf5_write_data(hdf5_handler, 'list_videos_per_activity',
                        data_array["list_videos_per_activity"], dtype=np.int32,
                        fillvalue=pad_value)
        hdf5_write_data(hdf5_handler, 'list_image_filenames_per_video',
                        data_array["list_image_filenames_per_video"], dtype=np.int32,
                        fillvalue=pad_value)
        hdf5_write_data(hdf5_handler, 'list_annotations_per_video',
                        data_array["list_annotations_per_video"], dtype=np.int32,
                        fillvalue=pad_value)
