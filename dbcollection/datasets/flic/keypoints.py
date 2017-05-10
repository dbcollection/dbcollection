"""
FLIC Keypoints process functions.
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
    """ FLIC Keypoints preprocessing functions """

    # metadata filename
    filename_h5 = 'keypoint'

    keypoints_labels = [
        'Left_Shoulder',  #-- 1
        'Left_Elbow',     #-- 2
        'Left_Wrist',     #-- 3
        'Right_Shoulder', #-- 4
        'Right_Elbow',    #-- 5
        'Right_Wrist',    #-- 6
        'Left_Hip',       #-- 7
        'Right_Hip',      #-- 8
        'Left_Eye',       #-- 9
        'Right_Eye',      #-- 10
        'Nose'            #-- 11
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
        annot_filepath = os.path.join(self.data_path, 'FLIC', 'examples.mat')

        # load annotations file
        annotations = load_matlab(annot_filepath)

        data = {
            "train" : {},
            "test" : {}
        }


        for annot in annotations['examples'][0]:
            if annot[-1][0][0] == 0:
                set_name = 'train'
            else:
                set_name = 'test'

            width, height, _ = annot[4][0].tolist()
            moviename = annot[1][0]
            filename = os.path.join('FLIC', 'images', annot[3][0])
            torso_box = annot[6][0].tolist(),  # [x1,y1,x2,y2]
            parts = [
                [annot[2][0][0], annot[2][1][0]],    #-- 1, Left_Shoulder
                [annot[2][0][1], annot[2][1][1]],    #-- 2, Left_Elbow
                [annot[2][0][2], annot[2][1][2]],    #-- 3, Left_Wrist
                [annot[2][0][3], annot[2][1][3]],    #-- 4, Right_Shoulder
                [annot[2][0][4], annot[2][1][4]],    #-- 5, Right_Elbow
                [annot[2][0][5], annot[2][1][5]],    #-- 6, Right_Wrist
                [annot[2][0][6], annot[2][1][6]],    #-- 7, Left_Hip
                [annot[2][0][9], annot[2][1][9]],    #-- 8, Right_Hip
                [annot[2][0][12], annot[2][1][12]],  #-- 9, Left_Eye
                [annot[2][0][13], annot[2][1][13]],  #-- 10, Right_Eye
                [annot[2][0][16], annot[2][1][16]]   #-- 11, Nose
            ]

            if filename in data[set_name]:
                data[set_name][filename]["object"].append({
                    "torso_box" : torso_box,
                    "parts" : parts
                })
            else:
                d = {
                    "width" : width,
                    "height" : height,
                    "moviename" : moviename,
                    "object" : [{
                        "torso_box" : torso_box,
                        "parts" : parts
                    }]
                }
                data[set_name].update({filename : d})

        return data


    def load_data(self):
        """
        Load data of the dataset (create a generator).
        """
        # load annotations
        annotations = self.load_annotations()

        for set_name in annotations:
            if self.verbose:
                print('\n> Loading data files for the set: ' + set_name)

            yield {set_name : annotations[set_name]}


    def add_data_to_source(self, handler, data):
        """
        Store classes + filenames as a nested tree.
        """

        if self.verbose:
            print('> Adding data to source group:')
            prgbar = progressbar.ProgressBar(max_value=len(data))

        keypoint_names = str2ascii(self.keypoints_labels)

        for i, fname in enumerate(data):
            file_grp = handler.create_group(str(i))
            annot = data[fname]
            file_grp['image_filename'] = str2ascii(fname)
            file_grp['moviename'] = str2ascii(annot["moviename"])
            file_grp['width'] = np.array(annot["width"], dtype=np.int32)
            file_grp['height'] = np.array(annot["height"], dtype=np.int32)
            file_grp['keypoint_names'] = keypoint_names

            for j, obj in enumerate(annot["object"]):
                obj_grp = file_grp.create_group(str(j))
                obj_grp['torso_box'] = np.array(obj["torso_box"], dtype=np.float)
                obj_grp['keypoints'] = np.array(obj["parts"], dtype=np.float)

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # update progressbar
        if self.verbose:
            prgbar.finish()


    def add_data_to_default(self, handler, data):
        """
        Add data of a set to the default group.
        """
        image_filenames = []
        width = []
        height = []
        movienames = []
        torso_boxes = []
        keypoints = []
        object_id = []

        object_fields = ["image_filenames", "movienames", "torso_boxes",
                         "keypoints", "width", "height"]

        list_object_ids_per_image = []

        if self.verbose:
            print('> Adding data to default group:')
            prgbar = progressbar.ProgressBar(max_value=len(data))


        for i, fname in enumerate(data):
            annotation = data[fname]
            movienames.append(annotation["moviename"])

        # remove duplicated entries
        movienames = list(set(movienames))

        obj_per_img_counter = 0
        for i, fname in enumerate(data):
            annotation = data[fname]
            image_filenames.append(fname)
            width.append(annotation["width"])
            height.append(annotation["height"])

            objs_per_image = []
            for obj in annotation["object"]:
                torso_boxes.append(obj["torso_box"])
                keypoints.append(obj["parts"])

                object_id.append([i, movienames.index(annotation["moviename"]),
                                  obj_per_img_counter, obj_per_img_counter, i, i])

                # add object_id to the list
                objs_per_image.append(obj_per_img_counter)

                # update counter
                obj_per_img_counter += 1

            list_object_ids_per_image.append(objs_per_image)

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # update progressbar
        if self.verbose:
            prgbar.finish()


        handler['image_filenames'] = str2ascii(image_filenames)
        handler['movienames'] = str2ascii(movienames)
        handler['width'] = np.array(width, dtype=np.int32)
        handler['height'] = np.array(height, dtype=np.int32)
        handler['object_ids'] = np.array(object_id, dtype=np.int32)
        handler['object_fields'] = str2ascii(object_fields)
        handler['torso_boxes'] = np.array(torso_boxes, dtype=np.float)
        handler['keypoints'] = np.array(keypoints, dtype=np.float)
        handler['keypoint_names'] = str2ascii(self.keypoints_labels)

        handler['list_object_ids_per_image'] = np.array(pad_list(list_object_ids_per_image, -1), dtype=np.int32)


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
                self.add_data_to_default(defaultg, data[set_name])

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

    def add_data_to_source(self, handler, data):
        """
        Dummy method
        """
        # do nothing