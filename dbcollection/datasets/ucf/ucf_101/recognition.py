"""
UCF101 action recognition process functions.
"""


from __future__ import print_function, division
import os
import numpy as np
import progressbar

from dbcollection.datasets import BaseTask

from dbcollection.utils.file_load import load_txt
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list
from dbcollection.utils.hdf5 import hdf5_write_data

from .extract_frames import extract_video_frames


class Recognition(BaseTask):
    """UCF101 action recognition preprocessing functions."""

    # metadata filename
    filename_h5 = 'recognition'

    def load_classes(self):
        """
        Load action classes from the annotation files.
        """
        filename = os.path.join(self.data_path, 'ucfTrainTestlist', 'classInd.txt')
        data = load_txt(filename)
        return [row_str.split(' ')[1] for row_str in data if any(row_str)]

    def load_file(self, fname):
        """
        Load data from a .txt file.
        """
        filename = os.path.join(self.data_path, 'ucfTrainTestlist', fname)
        data = load_txt(filename)
        return [row_str.split(' ')[0] for row_str in data if any(row_str)]

    def convert_to_dict(self, data):
        """
        Parse the data list into a table. (keys=classes, values=videos)
        """
        out_dict = {}
        for content in data:
            str_split = content.split('/')
            class_name = str_split[0]
            video_name = os.path.splitext(str_split[1])[0]

            try:
                out_dict[class_name].append(video_name)
            except KeyError:
                out_dict[class_name] = [video_name]

        # order video names per class
        for class_name in out_dict:
            out_dict[class_name].sort()

        return out_dict

    def load_train_test_splits(self):
        """
        Load train+test index lists from the annotation files.
        """
        splits = [
            ['trainlist01.txt', 'train01'],
            ['trainlist02.txt', 'train02'],
            ['trainlist03.txt', 'train03'],
            ['testlist01.txt', 'test01'],
            ['testlist02.txt', 'test02'],
            ['testlist03.txt', 'test03']
        ]
        splits_idx = {}
        for names in splits:
            data = self.load_file(names[0])
            splits_idx[names[1]] = self.convert_to_dict(data)

        return splits_idx

    def get_set_data(self, set_split, class_list):
        """
        Retrieve the specific data for the set
        """
        # cycle all sets
        out = {}
        iset = 0
        for set_name in set_split:

            if self.verbose:
                iset += 1
                print('\n > Split ({}/{}): {}'.format(iset, len(set_split.keys()), set_name))

            # initialize lists
            object_ids = []
            videos = []
            video_filenames = []
            image_filenames = []
            total_frames = []
            list_videos_per_class = {}
            list_image_filenames_per_video = []
            source_data = {}  # stores the folder tree of the classes + videos + image files

            if self.verbose:
                total_vids = sum([len(set_split[set_name][category])
                                  for category in set_split[set_name]])
                progbar = progressbar.ProgressBar(maxval=total_vids).start()
                i = 0

            # fill the lists
            count_video, count_imgs = 0, 0
            for class_id, category in enumerate(class_list):
                source_data[category] = {}
                # class_id = class_list.index(category)
                for _, video_name in enumerate(set_split[set_name][category]):
                    videos.append(video_name)  # add video name
                    video_dir = os.path.join(self.root_dir_imgs, category, video_name)
                    video_filenames.append(os.path.join('UCF-101', category, video_name + '.avi'))

                    # fetch all files in the dir
                    images_fnames = os.listdir(video_dir)

                    # remove any file that does not have .jpg ext
                    images_fnames = [fname for fname in images_fnames if fname.endswith('.jpg')]

                    # add category + video_name to the file paths
                    images_fnames = [os.path.join(self.data_path, self.images_dir,
                                                  category, video_name, fname)
                                     for fname in images_fnames]
                    images_fnames.sort()  # sort images
                    image_filenames = image_filenames + images_fnames  # add images filenames
                    count_imgs += len(images_fnames)
                    total_frames.append(count_imgs)

                    # add image filenames to source
                    source_data[category][video_name] = {
                        "images": str2ascii(images_fnames),
                        "video": str2ascii(video_filenames[-1])
                    }

                    # add to list of images per video
                    list_range = list(range(count_imgs - len(images_fnames), count_imgs))
                    list_image_filenames_per_video.append(list_range)

                    # add to list of videos per class
                    try:
                        list_videos_per_class[class_id].append(count_video)
                    except KeyError:
                        list_videos_per_class[class_id] = [count_video]

                    # add data to 'object_ids'
                    # [video, video_filename, list_images_per_video,
                    # class (activity), total_imgs]
                    object_ids.append(
                        [count_video, count_video, count_video, class_id, count_video])

                    # update video counter
                    count_video += 1

                    # update progress bar
                    if self.verbose:
                        i += 1
                        progbar.update(i)

            # set progressbar to 100%
            progbar.finish()

            out[set_name] = {
                "object_fields": str2ascii(['videos', 'video_filenames',
                                            'list_image_filenames_per_video',
                                            'activities', 'total_frames']),
                "object_ids": np.array(object_ids, dtype=np.int32),
                "videos": str2ascii(videos),
                "video_filenames": str2ascii(video_filenames),
                "activities": str2ascii(class_list),
                "image_filenames": str2ascii(image_filenames),
                "total_frames": np.array(total_frames, dtype=np.int32),
                "list_videos_per_activity": np.array(pad_list(list(list_videos_per_class.values()),
                                                              -1), dtype=np.int32),
                "list_image_filenames_per_video": np.array(pad_list(list_image_filenames_per_video,
                                                                    -1), dtype=np.int32),
                "source_data": source_data
            }

        return out

    def load_data(self):
        """
        Load the data from the files.
        """
        self.images_dir = 'UCF-101-images'
        self.root_dir_imgs = os.path.join(self.data_path, self.images_dir)

        # extract images from videos into a new folder
        if not os.path.exists(self.root_dir_imgs):
            extract_video_frames(self.data_path, self.verbose)

        # load classes
        class_list = self.load_classes()

        # load train+test set splits
        set_splits_vids = self.load_train_test_splits()

        # fetch folder struct
        if self.verbose:
            print('==> Processing train/set data splits:')
        set_splits_data = self.get_set_data(set_splits_vids, class_list)

        yield set_splits_data

    def add_data_to_source(self, hdf5_handler, data, set_name=None):
        """
        Store data annotations in a nested tree fashion.

        It closely follows the tree structure of the data.
        """
        for category in data['source_data']:
            category_grp = hdf5_handler.create_group(category)
            for video_name in data[set_name]['source_data'][category]:
                video_grp = category_grp.create_group(video_name)
                video_grp.create_dataset(
                    'images_path', data=data['source_data'][category][video_name]['images'])
                video_grp.create_dataset(
                    'video_path', data=data['source_data'][category][video_name]['video'])

    def add_data_to_default(self, hdf5_handler, data, set_name=None):
        """
        Add data of a set to the default group.

        For each field, the data is organized into a single big matrix.
        """
        hdf5_write_data(hdf5_handler, 'activities',
                        data["activities"],
                        dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'videos',
                        data["videos"],
                        dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'video_filenames',
                        data["video_filenames"],
                        dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'image_filenames',
                        data["image_filenames"],
                        dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'total_frames',
                        data["total_frames"],
                        dtype=np.int32, fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'object_ids',
                        data["object_ids"],
                        dtype=np.int32, fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'object_fields',
                        data["object_fields"],
                        dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'list_videos_per_activity',
                        data["list_videos_per_activity"],
                        dtype=np.int32, fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'list_image_filenames_per_video',
                        data["list_image_filenames_per_video"],
                        dtype=np.int32, fillvalue=-1)
