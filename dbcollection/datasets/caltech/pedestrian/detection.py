"""
Caltech Pedestrian detection process functions.
"""


from __future__ import print_function, division
import os
import numpy as np
import h5py
import progressbar

from dbcollection.utils.file_load import load_json
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list
from dbcollection.utils.caltech_pedestrian_extractor.converter import extract_data


class Detection:
    """ Caltech Pedestrian detection preprocessing functions """

    classes = ['person', 'people', 'person-fa', 'person?', 'empty']


    def __init__(self, data_path, cache_path, verbose=True):
        """
        Initialize class.
        """
        self.cache_path = cache_path
        self.data_path = data_path
        self.verbose = verbose
        self.extracted_data_path = os.path.join(data_path, 'extracted_data')


    def convert_extract_data(self):
        """
        Extract + convert .jpg + .json files from the .seq and .vbb files.
        """
        if not os.path.exists(self.extracted_data_path):
            extract_data(self.data_path, self.extracted_data_path)


    def load_data(self):
        """
        Load the data from the dataset's files.
        """
        # extract data
        self.convert_extract_data()

        sets = {
            "train" : ['set00', 'set01', 'set02', 'set03', 'set04', 'set05'],
            "test" : ['set06', 'set07', 'set08', 'set09', 'set10']
        }

        for set_name in sets:
            data = {set_name : {}}

            if self.verbose:
                print('> Loading data files for the set: {}'.format(set_name))

            # progressbar
            if self.verbose:
                prgbar = progressbar.ProgressBar(max_value=len(sets[set_name]))


            for i, set_data in enumerate(sets[set_name]):
                data[set_name][set_data] = {}

                extracted_data_dir = os.path.join(self.extracted_data_path, set_data)

                # list all folders
                folders = os.listdir(extracted_data_dir)
                folders.sort()

                for video in folders:
                    # fetch all images filenames
                    img_fnames = os.listdir(os.path.join(extracted_data_dir, video, 'images'))
                    img_fnames = [os.path.join('extracted_data', set_data, video, 'images', fname) for fname in img_fnames]
                    img_fnames.sort()

                    # fetch all annotations filenames
                    annotation_fnames = os.listdir(os.path.join(extracted_data_dir, video, 'annotations'))
                    annotation_fnames = [os.path.join('extracted_data', set_data, video, 'annotations', fname) for fname in annotation_fnames]
                    annotation_fnames.sort()

                    data[set_name][set_data][video] = {
                        "images" : img_fnames,
                        "annotations" : annotation_fnames
                    }

                # update progressbar
                if self.verbose:
                    prgbar.update(i)

            # reset progressbar
            if self.verbose:
                prgbar.finish()

            yield data


    def store_data_raw(self, handler, data, set_name):
        """
        Add data of a set to the raw file.
        """
        if self.verbose:
            print('> Adding data to the raw file:')
            prgbar = progressbar.ProgressBar(max_value=len(data))

        # create set group
        set_name_grp = handler.create_group(set_name)

        for i, set_data in enumerate(data):
            set_grp = set_name_grp.create_group(set_data)
            for video in data[set_data]:
                video_grp = set_grp.create_group(video)
                video_grp['image_filenames'] = str2ascii(data[set_data][video]['images'])
                video_grp['annotation_filenames'] = str2ascii(data[set_data][video]['annotations'])
                #img_fnames = data[set_data][video]['images']
                #annot_fnames = data[set_data][video]['annotations']
                #for j in range(0, len(img_fnames)):
                #    img_annot_grp = video_grp.create_group(str(j))
                #    img_annot_grp['image_filename'] = img_fnames[j]
                #    img_annot_grp['annotation_filenames'] = annot_fnames[j]

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # update progressbar
        if self.verbose:
            prgbar.finish()


    def store_data_default(self, handler, data, set_name):
        """
        Add data of a set to the default file.
        """
        object_fields = ['image_filenames', 'classes', 'boxes', 'boxesv', 'id', 'occlusion']
        image_filenames = []
        bbox = [[0, 0, 0, 0]]
        bboxv = [[0, 0, 0, 0]]
        lbl_id = [[-1]]
        occlusion = [[-1]]
        object_id = []

        list_image_filenames_per_class = []
        list_boxes_per_image = []
        list_boxesv_per_image = []
        list_object_ids_per_image = []
        list_objects_ids_per_class = []
        #list_objects_ids_per_id = []
        #list_objects_ids_per_occlusion= []

        if self.verbose:
            print('> Adding data to default file...')
            prgbar = progressbar.ProgressBar(max_value=len(data))

        img_counter = 0
        obj_counter = 0
        for i, set_data in enumerate(data):
            for video in data[set_data]:
                img_fnames = data[set_data][video]["images"]
                annot_fnames = data[set_data][video]["annotations"]

                # cycle all images + annotations
                for j in range(0, len(img_fnames)):
                    # add image filename
                    image_filenames.append(img_fnames[j])

                    # load annotation file
                    annotation = load_json(os.path.join(self.data_path, annot_fnames[j]))

                    if any(annotation):
                        for obj in annotation:
                            bbox.append(obj['pos'])
                            if isinstance(obj['posv'], list):
                                bboxv.append(obj['posv'])
                            else:
                                bboxv.append([0, 0, 0, 0])
                            lbl_id.append(obj['id'])
                            occlusion.append(obj['occl'])
                            class_lbl = self.classes.index(obj['lbl'])

                            # img, class, bbox, bboxv, id, occlusion
                            object_id.append([img_counter, class_lbl, obj_counter,
                                            obj_counter, obj_counter, obj_counter])

                            # increment counter
                            obj_counter += 1
                    else:
                        # img, class, bbox, bboxv, id, occlusion
                        object_id.append([img_counter, len(self.classes), 0, 0, 0, 0])

                    # increment counter
                    img_counter += 1

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # update progressbar
        if self.verbose:
            prgbar.finish()

        if self.verbose:
            print('> Processing lists...')

        # Process lists
        for i in range(len(self.classes)):
            imgs_per_class = [val[0] for j, val in enumerate(object_id) if val[1] == i]
            imgs_per_class = list(set(imgs_per_class)) # get unique values
            imgs_per_class.sort()
            list_image_filenames_per_class.append(imgs_per_class)

        for i in range(len(image_filenames)):
            boxes_per_img = [val[2] for j, val in enumerate(object_id) if val[0] == i]
            boxes_per_img = list(set(boxes_per_img)) # get unique values
            boxes_per_img.sort()
            list_boxes_per_image.append(boxes_per_img)

        for i in range(len(image_filenames)):
            boxesv_per_img = [val[3] for j, val in enumerate(object_id) if val[0] == i]
            boxesv_per_img = list(set(boxesv_per_img)) # get unique values
            boxesv_per_img.sort()
            list_boxesv_per_image.append(boxesv_per_img)

        for i in range(len(image_filenames)):
            objs_per_img = [j for j, val in enumerate(object_id) if val[0] == i and val[2] != 0]
            objs_per_img = list(set(objs_per_img)) # get unique values
            objs_per_img.sort()
            list_object_ids_per_image.append(objs_per_img)

        for i in range(len(self.classes)):
            objs_per_class = [j for j, val in enumerate(object_id) if val[1] == i]
            objs_per_class = list(set(objs_per_class)) # get unique values
            objs_per_class.sort()
            list_objects_ids_per_class.append(objs_per_class)


        handler['image_filenames'] = str2ascii(image_filenames)
        handler['classes'] = str2ascii(self.classes)
        handler['boxes'] = np.array(bbox, dtype=np.float)
        handler['boxesv'] = np.array(bboxv, dtype=np.float)
        handler['id'] = np.array(lbl_id, dtype=np.int32)
        handler['occlusion'] = np.array(occlusion, dtype=np.float)
        handler['object_ids'] = np.array(object_id, dtype=np.int32)
        handler['object_fields'] = str2ascii(object_fields)

        handler['list_image_filenames_per_class'] = np.array(pad_list(list_image_filenames_per_class, -1), dtype=np.int32)
        handler['list_boxes_per_image'] = np.array(pad_list(list_boxes_per_image, -1), dtype=np.int32)
        handler['list_boxesv_per_image'] = np.array(pad_list(list_boxesv_per_image, -1), dtype=np.int32)
        handler['list_object_ids_per_image'] = np.array(pad_list(list_object_ids_per_image, -1), dtype=np.int32)
        handler['list_objects_ids_per_class'] = np.array(pad_list(list_objects_ids_per_class, -1), dtype=np.int32)

        if self.verbose:
            print('> Done.')


    def process_metadata(self):
        """
        Process metadata and store it in a hdf5 file.
        """
        # create/open hdf5 files with subgroups for train/val/test/etc
        file_name = os.path.join(self.cache_path, 'detection.h5')
        file_name_raw = os.path.join(self.cache_path, 'detection_raw.h5')
        fileh5 = h5py.File(file_name, 'w', version='latest')
        fileh5_raw = h5py.File(file_name_raw, 'w', version='latest')

        if self.verbose:
            print('\n==> Storing metadata to file: {}'.format(file_name))

        # setup data generator
        data_gen = self.load_data()

        for data in data_gen:
            for set_name in data:

                if self.verbose:
                    print('\nSaving set metadata: {}'.format(set_name))

                # add data to the **raw** file
                self.store_data_raw(fileh5_raw, data[set_name], set_name)

                 # add data to the **default** file
                self.store_data_default(fileh5, data[set_name], set_name)

        # close file
        fileh5.close()
        fileh5_raw.close()

        # return information of the task + cache file
        return file_name, file_name_raw


    def run(self):
        """
        Run task processing.
        """
        return self.process_metadata()