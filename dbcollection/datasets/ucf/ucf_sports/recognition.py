"""
UCF-Sports action recognition process functions.
"""


from __future__ import print_function, division
import os
import random
import subprocess
import math
import numpy as np
import progressbar
from PIL import Image

from dbcollection.datasets import BaseTask

from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list
from dbcollection.utils.hdf5 import hdf5_write_data


class Recognition(BaseTask):
    """UCF-Sports action recognition preprocessing functions """

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

    def get_video_filename(self, all_files):
        """Returns the video filename."""
        assert all_files

        video_filename = [vname for vname in all_files if vname.endswith('.avi')]

        if not any(video_filename):
            video_filename = 'not_available'
        else:
            video_filename = video_filename[0]
        return video_filename

    def get_image_filenames(self, dir_path, video_filename, activity, video, all_files):
        """Return a list of all image filenames sorted."""
        assert dir_path
        assert video_filename
        assert activity
        assert video
        assert all_files

        image_filenames = [fname for fname in all_files if fname.endswith('.jpg')]

        # check if any image filenames exist
        if not any(image_filenames):
            video_filename_path = os.path.join(dir_path, video_filename)
            video_name = os.path.splitext(os.path.basename(video_filename_path))[0]
            self.extract_video_frames(video_filename_path, video_name, dir_path)

            # fetch again the image filenames
            image_filenames = [fname for fname in all_files if fname.endswith('.jpg')]

        # add the directory path to the image filenames
        image_filenames = [os.path.join(self.activities_dir, activity, video, fname)
                           for fname in image_filenames]
        image_filenames.sort()

        return image_filenames

    def get_image_bndboxes(self, dir_path, all_files):
        """Returns a list of bounding boxes for each image."""
        assert dir_path
        assert all_files

        # check if exists ground-truth bounding boxes
        image_bboxes = []
        if os.path.exists(os.path.join(dir_path, 'gt')):
            all_files = os.listdir(os.path.join(dir_path, 'gt'))
            bbox_filenames = [fname for fname in all_files if fname.endswith('.txt')]
            bbox_filenames.sort()

            for i, fname in enumerate(bbox_filenames):
                boxes = open(os.path.join(dir_path, 'gt', fname), 'r').read().split('\t')
                image_bboxes.append([int(boxes[0]),
                                     int(boxes[1]),
                                     int(boxes[0]) + int(boxes[2]) - 1,
                                     int(boxes[1]) + int(boxes[3]) - 1])  # [x1,y1,x2,y2]
        else:
            # center crop the image
            all_files = os.listdir(dir_path)
            all_files = [fname for fname in all_files if fname.endswith('.jpg')]
            all_files.sort()
            for i, fname in enumerate(all_files):
                # image_bboxes.append([0, 0, 0, 0])
                im = Image.open(os.path.join(dir_path, fname))
                width, height = im.size  # (width,height) tuple
                pad_x = int((width - height) / 2)
                image_bboxes.append([pad_x, 1, pad_x + height, height])  # [x1,y1,x2,y2]

        return image_bboxes

    def get_files_paths(self):
        """
        Load activities, videos and filenames paths from the data directory.
        """
        self.activities_dir = os.path.join('ucf_sports_actions', 'ucf action')
        self.root_dir_imgs = os.path.join(self.data_path, self.activities_dir)

        if self.verbose:
            print(' > Fetch videos and images paths from dir: {}'
                  .format(self.root_dir_imgs))

        # initialize data dictorionary
        data = {}
        for activity in self.classes:
            data[activity] = []

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
        for folder in activities_dir:
            activity = self.get_activity_name(folder)
            videos = os.listdir(os.path.join(self.root_dir_imgs, folder))
            videos.sort()
            for video in videos:
                dir_path = os.path.join(self.root_dir_imgs, folder, video)
                all_files = os.listdir(dir_path)
                all_files.sort()

                video_filename = self.get_video_filename(all_files)
                image_filenames = self.get_image_filenames(dir_path, video_filename, folder,
                                                           video, all_files)
                image_bboxes = self.get_image_bndboxes(dir_path, all_files)

                # assign data to dict
                data[activity].append({
                    "video_folder_name": os.path.join(folder, video),
                    "video_filename": os.path.join(self.activities_dir, folder,
                                                   video, video_filename),
                    "image_filenames": image_filenames,
                    "image_bboxes": image_bboxes
                })

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
                num_videos = len(data[activity])
                tr_num_vids = math.ceil(num_videos * train_percent)
                random_video_ids = np.random.permutation(range(num_videos)).tolist()
                train_ids = random_video_ids[:tr_num_vids]
                test_ids = random_video_ids[tr_num_vids:]

                # train set
                out_data[train_set_name][activity] = []
                for video_id in sorted(train_ids):
                    out_data[train_set_name][activity].append(data[activity][video_id])

                # test set
                out_data[test_set_name][activity] = []
                for video_id in sorted(test_ids):
                    out_data[test_set_name][activity].append(data[activity][video_id])

            yield out_data

    def load_data(self):
        """
        Load the data from the files.
        """
        # load video and images filenames
        data = self.get_files_paths()

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
        activities = self.classes
        object_fields = ['image_filenames', 'boxes', 'videos', "activities"]
        object_ids = []
        videos = []
        video_filenames_ids = []
        video_boxes_ids = []
        image_filenames = []
        bboxes = []
        activity_video_ids = []

        counter_files_id = 0
        counter_video_id = 0
        for activity_id, activity in enumerate(activities):

            video_ids = []
            for _, video_data in enumerate(data[activity]):
                videos.append(video_data['video_folder_name'])
                video_ids.append(counter_video_id)
                img_fnames = video_data['image_filenames']
                boxes = video_data['image_bboxes']

                fname_ids = []
                bboxes_ids = []
                for i, fname in enumerate(img_fnames):
                    image_filenames.append(fname)
                    bboxes.append(boxes[i])
                    fname_ids.append(counter_files_id)
                    bboxes_ids.append(counter_files_id)

                    object_ids.append([counter_files_id, counter_files_id,
                                       counter_video_id, activity_id])

                    # increment file counter
                    counter_files_id += 1

                num_imgs = len(img_fnames)

                video_filenames_ids.append(fname_ids)
                video_boxes_ids.append(bboxes_ids)

                # increment video counter
                counter_video_id += 1

            activity_video_ids.append(video_ids)

        return {
            "activities": str2ascii(activities),
            "videos": str2ascii(videos),
            "image_filenames": str2ascii(image_filenames),
            "boxes": np.array(bboxes, dtype=np.int32),
            "object_ids": np.array(object_ids, dtype=np.int32),
            "object_fields": str2ascii(object_fields),

            "list_object_ids_per_video": np.array(pad_list(video_filenames_ids, -1),
                                                  dtype=np.int32),
            "list_filenames_per_video": np.array(pad_list(video_filenames_ids, -1),
                                                 dtype=np.int32),
            "list_boxes_per_video": np.array(pad_list(video_boxes_ids, -1),
                                             dtype=np.int32),
            "list_videos_per_activity": np.array(pad_list(activity_video_ids, -1),
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

    def add_data_to_default(self, hdf5_handler, data, set_name=None):
        """
        Add data of a set to the default group.

        For each field, the data is organized into a single big matrix.
        """
        data_array = self.convert_data_to_arrays(data)
        hdf5_write_data(hdf5_handler, 'activities',
                        data_array["activities"],
                        dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'videos',
                        data_array["videos"],
                        dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'image_filenames',
                        data_array["image_filenames"],
                        dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'boxes',
                        data_array["boxes"],
                        dtype=np.int32, fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'object_ids',
                        data_array["object_ids"],
                        dtype=np.int32, fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'object_fields',
                        data_array["object_fields"],
                        dtype=np.uint8, fillvalue=0)

        pad_value = -1
        hdf5_write_data(hdf5_handler, 'list_object_ids_per_video',
                        data_array["list_object_ids_per_video"],
                        dtype=np.int32, fillvalue=pad_value)
        hdf5_write_data(hdf5_handler, 'list_filenames_per_video',
                        data_array["list_filenames_per_video"],
                        dtype=np.int32, fillvalue=pad_value)
        hdf5_write_data(hdf5_handler, 'list_boxes_per_video',
                        data_array["list_boxes_per_video"],
                        dtype=np.int32, fillvalue=pad_value)
        hdf5_write_data(hdf5_handler, 'list_videos_per_activity',
                        data_array["list_videos_per_activity"],
                        dtype=np.int32, fillvalue=pad_value)
