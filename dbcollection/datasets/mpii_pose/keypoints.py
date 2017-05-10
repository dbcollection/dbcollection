"""
MPII Keypoints process functions.
"""


from __future__ import print_function, division
import os
import numpy as np
import h5py
import progressbar

from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list
from dbcollection.utils.file_load import load_matlab


class Keypoints:
    """ MPII Keypoints preprocessing functions """

    # metadata filename
    filename_h5 = 'keypoint'

    keypoints_labels = [
        'right ankle',      #-- 1
        'right knee',       #-- 2
        'right hip',        #-- 3
        'left hip',         #-- 4
        'left knee',        #-- 5
        'left ankle',       #-- 6
        'pelvis',           #-- 7
        'thorax',           #-- 8
        'upper neck',       #-- 9
        'head top',         #-- 10
        'right wrist',      #-- 11
        'right elbow',      #-- 12
        'right shoulder',   #-- 13
        'left shoulder',    #-- 14
        'left elbow',       #-- 15
        'left wrist'        #-- 16
    ]


    def __init__(self, data_path, cache_path, verbose=True):
        """
        Initialize class.
        """
        self.cache_path = cache_path
        self.data_path = data_path
        self.verbose = verbose


    def load_annotations(self):
        """
        Load annotations from file and split them to train and test sets.
        """
        annot_filepath = os.path.join(self.data_path, 'mpii_human_pose_v1_u12_2', 'mpii_human_pose_v1_u12_1.mat')

        if self.verbose:
            print('\n> Loading annotations file: {}'.format(annot_filepath))

        # load annotations file
        annotations = load_matlab(annot_filepath)

        # total number of files
        nfiles = len(annotations["RELEASE"][0][0][3])

        # progressbar
        if self.verbose:
            print('\n> Parsing data from the annotations...')
            prgbar = progressbar.ProgressBar(max_value=nfiles)

        data = {
            "train" : {},
            "test" : {}
        }


        for ifile in range(nfiles):
            if annotations['RELEASE'][0][0][1][0][ifile] == 0:
                set_name = 'test'
            else:
                set_name = 'train'

            # image annots
            image_filename = os.path.join('images', str(annotations['RELEASE'][0][0][0][0][ifile][0][0][0][0][0]))

            # parse keypoints
            if any(annotations['RELEASE'][0][0][0][0][ifile][3][0]):
                frame_sec = int(annotations['RELEASE'][0][0][0][0][ifile][2][0][0])
                video_idx = int(annotations['RELEASE'][0][0][0][0][ifile][3][0][0])

                poses_annots = []
                for i in range(annotations['RELEASE'][0][0][0][0][ifile][1][0]):
                    keypoints = [[0, 0, 0]] * 16  # [x, y, is_visible]
                    for j in range(len(annotations['RELEASE'][0][0][0][0][ifile][1][0][i][4][0][0][0][0])):
                        idx = annotations['RELEASE'][0][0][0][0][ifile][1][0][i][4][0][0][0][0][j][0][0][0]
                        x = annotations['RELEASE'][0][0][0][0][ifile][1][0][i][4][0][0][0][0][j][1][0][0]
                        y = annotations['RELEASE'][0][0][0][0][ifile][1][0][i][4][0][0][0][0][j][2][0][0]

                        if any(annotations['RELEASE'][0][0][0][0][ifile][1][0][i][4][0][0][0][0][j][3]):
                            is_visible = int(annotations['RELEASE'][0][0][0][0][ifile][1][0][i][4][0][0][0][0][j][3][0])
                        else:
                            is_visible = -1
                        keypoints[idx] = [x, y, is_visible]

                    poses_annots.append({
                        "x1" : annotations['RELEASE'][0][0][0][0][ifile][1][0][i][0][0][0],
                        "y1" : annotations['RELEASE'][0][0][0][0][ifile][1][0][i][1][0][0],
                        "x2" : annotations['RELEASE'][0][0][0][0][ifile][1][0][i][2][0][0],
                        "y2" : annotations['RELEASE'][0][0][0][0][ifile][1][0][i][3][0][0],
                        "keypoints" : keypoints,
                        "scale" : annotations['RELEASE'][0][0][0][0][ifile][1][0][i][5][0][0],
                        "objpos" : {
                            "x" : annotations['RELEASE'][0][0][0][0][ifile][1][0][i][6][0][0][0][0][0],
                            "y" : annotations['RELEASE'][0][0][0][0][ifile][1][0][i][6][0][0][1][0][0],
                        }
                    })
            else:
                frame_sec, video_idx = -1, -1

                poses_annots = []
                for i in range(annotations['RELEASE'][0][0][0][0][ifile][1][0]):
                    poses_annots.append({
                        "scale" : annotations['RELEASE'][0][0][0][0][ifile][1][0][i][0][0][0],
                        "objpos" : {
                            "x" : annotations['RELEASE'][0][0][0][0][ifile][1][0][i][1][0][0][0][0][0],
                            "y" : annotations['RELEASE'][0][0][0][0][ifile][1][0][i][1][0][0][1][0][0],
                        }
                    })

            # single person
            single_person = [0]
            if any(annotations['RELEASE'][0][0][3][ifile][0]):
                for i in range(len(annotations['RELEASE'][0][0][3][ifile][0])):
                    single_person.append(int(annotations['RELEASE'][0][0][3][ifile][0][i][0]))

            # activity/action id
            act = {"cat_name" : '', "act_name" : '', "act_id" : -1}
            if any(annotations['RELEASE'][0][0][4][ifile][0]):
                act = {
                    "cat_name" : str(annotations['RELEASE'][0][0][4][ifile][0][0][0]),
                    "act_name" : str(annotations['RELEASE'][0][0][4][ifile][0][1][0]),
                    "act_id" : int(annotations['RELEASE'][0][0][4][ifile][0][2][0][0])
                }

            # add fields to data
            data[set_name] = {
                "image_filename" : image_filename,
                "frame_sec" : frame_sec,
                "video_idx" : video_idx,
                "poses_annotations" : poses_annots,
                "activity" : act,
                "single_person" : single_person
            }

        # fetch video ids
        videonames = []
        for ivideo in range(len(annotations['RELEASE'][0][0][5][0])):
            videonames.append(annotations['RELEASE'][0][0][5][0][ivideo][0])

        return data, videonames


    def load_data(self):
        """
        Load data of the dataset (create a generator).
        """
        # load annotations
        annotations, videonames = self.load_annotations()

        for set_name in annotations:
            if self.verbose:
                print('\n> Loading data files for the set: ' + set_name)

            yield {set_name : [annotations[set_name], videonames]}


    def add_data_to_source(self, handler, data):
        """
        Store classes + filenames as a nested tree.
        """
        # split list
        data_, videonames = data

        if self.verbose:
            print('> Adding data to source group:')
            prgbar = progressbar.ProgressBar(max_value=len(data_))

        handler["videonames"] = str2ascii(videonames)
        handler["keypoint_names"] = str2ascii(self.keypoints_labels)

        for i, annot in enumerate(data_):
            file_grp = handler.create_group(str(i))
            file_grp['image_filename'] = str2ascii(annot["image_filename"])
            file_grp['frame_sec'] = np.array(annot["frame_sec"], dtype=np.int32)
            file_grp['video_idx'] = np.array(annot["video_idx"], dtype=np.int32)
            file_grp['single_person_id'] = np.array(annot["single_person"], dtype=np.uint8)

            activity_grp = file_grp.create_group("activity")
            activity_grp['category_name'] = str2ascii(annot["activity"]["cat_name"])
            activity_grp['activity_name'] = str2ascii(annot["activity"]["act_name"])
            activity_grp['activity_id'] = np.array(annot["activity"]["act_id"], dtype=np.int32)

            pose_annot_grp = file_grp.create_group("pose_annotations")
            for j in range(len(annot["poses_annotations"])):
                pose_grp = pose_annot_grp.create_group(str(j))
                pose_grp["scale"] = np.array(annot["poses_annotations"][j]["scale"], dtype=np.float)
                pose_grp["objpos/x"] = np.array(annot["poses_annotations"][j]["objpos"]["x"], dtype=np.float)
                pose_grp["objpos/y"] = np.array(annot["poses_annotations"][j]["objpos"]["y"], dtype=np.float)

                if "x1" in annot["poses_annotations"][j]:
                    pose_grp["x1"] = np.array(annot["poses_annotations"][j]["x1"], dtype=np.float)
                    pose_grp["y1"] = np.array(annot["poses_annotations"][j]["y1"], dtype=np.float)
                    pose_grp["x2"] = np.array(annot["poses_annotations"][j]["x2"], dtype=np.float)
                    pose_grp["y2"] = np.array(annot["poses_annotations"][j]["y2"], dtype=np.float)
                    pose_grp["keypoints"] = np.array(annot["poses_annotations"][j]["keypoints"], dtype=np.float)


            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # update progressbar
        if self.verbose:
            prgbar.finish()


    def add_data_to_default(self, handler, data, set_name):
        """
        Add data of a set to the default group.
        """
        # split list
        data_, videonames = data

        if set_name == 'test':
            is_train = False
        else:
            is_train = True

        image_filenames = []
        frame_sec = []
        video_idx = []
        single_person_id_list = []
        category_name, activity_name, activity_id = [], [], []
        scale = []
        objpos = [] # [x, y]
        head_bbox = []
        keypoints = []

        object_id = []

        if is_train:
            object_fields = ["image_filenames", "head_bbox",
                             "keypoints", "scale", "objpos",
                             "frame_sec", "video_idx"]
        else:
            object_fields = ["image_filenames", "scale", "objpos"]

        # adicionar listas
        list_object_ids_per_image = []
        list_single_person_per_image = []
        list_keypoints_per_image = []

        if self.verbose:
            print('> Adding data to default group:')
            prgbar = progressbar.ProgressBar(max_value=len(data_))


        obj_per_img_counter = 0
        for i, annot in enumerate(data_):
            image_filenames.append(annot["image_filename"])

            if is_train:
                frame_sec.append(annot["frame_sec"])
                video_idx.append(annot["video_idx"])
                category_name.append(annot["activity"]["cat_name"])
                activity_name.append(annot["activity"]["act_name"])
                activity_id.append(annot["activity"]["act_id"])

            objs_per_image = []
            keypoints_per_image = []
            single_person_per_image = []
            for j, pose_annot in enumerate(annot["poses_annotations"]):
                scale.append(pose_annot["scale"])
                objpos.append([pose_annot["objpos"]["x"],
                               pose_annot["objpos"]["y"]])

                if j+1 in annot["single_person"]:
                    single_person_per_image.append(obj_per_img_counter)

                if is_train:
                    head_bbox.append([pose_annot["x1"],
                                      pose_annot["y1"],
                                      pose_annot["x2"],
                                      pose_annot["y2"]])
                    keypoints.append(pose_annot["keypoints"])

                    object_id.append([i, j, j, j, j, i, i])

                    # add object_id to the keypoint list
                    keypoints_per_image.append(obj_per_img_counter)
                else:
                    object_id.append([i, j, j])

                # add object_id to the list
                objs_per_image.append(obj_per_img_counter)

                # update counter
                obj_per_img_counter += 1

            list_object_ids_per_image.append(objs_per_image)
            list_single_person_per_image.append(single_person_per_image)
            list_keypoints_per_image.append(keypoints_per_image)

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # update progressbar
        if self.verbose:
            prgbar.finish()


        handler['image_filenames'] = str2ascii(image_filenames)
        handler['scale'] = np.array(scale, dtype=np.float)
        handler['objpos'] = np.array(objpos, dtype=np.float)
        handler['object_ids'] = np.array(object_id, dtype=np.int32)
        handler['object_fields'] = str2ascii(object_fields)
        handler['videonames'] = str2ascii(videonames)
        handler['keypoint_names'] = str2ascii(self.keypoints_labels)

        handler['list_object_ids_per_image'] = np.array(pad_list(list_object_ids_per_image, -1), dtype=np.int32)
        handler['list_single_person_per_image'] = np.array(pad_list(list_single_person_per_image, -1), dtype=np.int32)

        if is_train:
            handler['frame_sec'] = np.array(frame_sec, dtype=np.int32)
            handler['video_idx'] = np.array(video_idx, dtype=np.int32)
            handler['category_name'] = str2ascii(category_name)
            handler['activity_name'] = str2ascii(activity_name)
            handler['activity_id'] = np.array(activity_id, dtype=np.int32)
            handler['head_bbox'] = np.array(head_bbox, dtype=np.float)
            handler['keypoints'] = np.array(keypoints, dtype=np.float)

            handler['list_keypoints_per_image'] = np.array(pad_list(list_keypoints_per_image, -1), dtype=np.int32)


    def process_metadata(self):
        """
        Process metadata and store it in a hdf5 file.
        """

        # create/open hdf5 file with subgroups for train/val/test
        file_name = os.path.join(self.cache_path, self.filename_h5 + '.h5')
        fileh5 = h5py.File(file_name, 'w', version='latest')

        if self.verbose:
            print('\n==> Storing metadata to file: {}'.format(file_name))

        # setup data generator
        data_gen = self.load_data()

        for data in data_gen:
            for set_name in data:

                if self.verbose:
                    print('\nSaving set metadata: {}'.format(set_name))

                # add data to the **source** group
                sourceg = fileh5.create_group('source/' + set_name)
                self.add_data_to_source(sourceg, data[set_name])

                # add data to the **default** group
                defaultg = fileh5.create_group('default/' + set_name)
                self.add_data_to_default(defaultg, data[set_name], set_name)

        # close file
        fileh5.close()

        # return information of the task + cache file
        return file_name


    def run(self):
        """
        Run task processing.
        """
        return self.process_metadata()


class KeypointsNoSourceGrp(Keypoints):
    """ FLIC Keypoints (default grp only - no source group) task class """

    # metadata filename
    filename_h5 = 'keypoint_d'

    def add_data_to_source(self, handler, data, set_name):
        """
        Dummy method
        """
        # do nothing