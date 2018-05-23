"""
Caltech Pedestrian detection process functions.
"""


from __future__ import print_function, division
import os
import numpy as np
import progressbar

from dbcollection.datasets import BaseTaskNew

from dbcollection.utils.file_load import load_json
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list
from dbcollection.utils.hdf5 import hdf5_write_data
from dbcollection.utils.db.caltech_pedestrian_extractor.converter import extract_data


class Detection(BaseTaskNew):
    """Caltech Pedestrian detection preprocessing functions."""

    filename_h5 = 'detection'
    skip_step = 30
    classes = ('person', 'person-fa', 'people', 'person?')
    sets = {
        "train": ('set00', 'set01', 'set02', 'set03', 'set04', 'set05'),
        "test": ('set06', 'set07', 'set08', 'set09', 'set10')
    }

    def load_data(self):
        """
        Fetches the train/test data.
        """
        yield {"train": self.load_data_set(is_test=False)}
        yield {"test": self.load_data_set(is_test=True)}

    def load_data_set(self, is_test):
        """Fetches the train/test data."""
        assert isinstance(is_test, bool), "Must input a valid boolean input."
        unpack_dir = self.unpack_raw_data_files()
        set_name, partitions = self.get_set_partitions(is_test=is_test)
        image_filenames, annotation_filenames = self.get_annotations_data(set_name, partitions, unpack_dir)
        return {
            "image_filenames": image_filenames,
            "annotation_filenames": annotation_filenames
        }

    def unpack_raw_data_files(self):
        """Unpacks images and annotations data (.jpg, .json) from raw data files (.seq, .vbb)."""
        extract_dir = os.path.join(self.data_path, 'extracted_data')
        if not os.path.exists(extract_dir):
            sets = [partition for partitions in self.sets.values() for partition in partitions]
            sets.sort()
            extract_data(self.data_path, extract_dir, sets)
        return extract_dir

    def get_set_partitions(self, is_test):
        """Returns the set partitions for the train/test set."""
        if is_test:
            return "test", self.sets["test"]
        else:
            return "train", self.sets["train"]

    def get_annotations_data(self, set_name, partitions, unpack_dir):
        """Returns the images and annotations filenames of a set from disk."""
        image_filenames, annotation_filenames = {}, {}

        if self.verbose:
            print('\n> Loading data files for the set: {}'.format(set_name))
            prgbar = progressbar.ProgressBar(max_value=len(partitions))

        for i, partition in enumerate(partitions):
            data = self.get_annotations_from_partition(unpack_dir, partition)
            image_filenames[partition] = data["images"]
            annotation_filenames[partition] = data["annotations"]
            if self.verbose:
                prgbar.update(i)  # update progressbar

        if self.verbose:
            prgbar.finish()  # reset progressbar
        return image_filenames, annotation_filenames

    def get_annotations_from_partition(self, path, partition):
        """Returns all image and annotation filenames (ordered) of a set partition from disk."""
        partition_annotations = {}
        dirs = self.get_sorted_object_names_from_dir(os.path.join(path, partition))
        for video in dirs:
            image_filenames = self.get_image_filenames_from_dir(path, partition, video)
            annotation_filenames = self.get_annotation_filenames_from_dir(path, partition, video)
            partition_annotations[video] = {
                "images": image_filenames,
                "annotations": annotation_filenames
            }
        return partition_annotations

    def get_sorted_object_names_from_dir(self, path):
        """Returns a sorted list containing the names of
        the entries in the directory given by path."""
        object_names = os.listdir(path)
        object_names.sort()
        return object_names

    def get_image_filenames_from_dir(self, path, partition, video):
        """Returns a list of ordered image filenames sampled from a directory."""
        return self.get_sample_data_from_dir(path, partition, video, 'images')

    def get_sample_data_from_dir(self, path, partition, video, type_data):
        """Returns a sampled list of ordered image / annnotation file path + names from a directory."""
        path_ = os.path.join(path, partition, video, type_data)
        filenames = self.get_sorted_object_names_from_dir(path_)
        annot_path = os.path.join(self.data_path, 'extracted_data', partition, video, type_data)
        filepaths = [os.path.join(annot_path, filename) for filename in filenames]
        sample_filepaths = self.get_sample_filenames(filepaths, self.skip_step)
        return sample_filepaths

    def get_sample_filenames(self, filenames, skip_step):
        """Returns a sample of filenames using a sampling step."""
        return [filenames[i] for i in range(skip_step - 1, len(filenames), skip_step)]

    def get_annotation_filenames_from_dir(self, path, partition, video):
        """Returns a list of ordered annotation filenames sampled from a directory."""
        return self.get_sample_data_from_dir(path, partition, video, 'annotations')

    def add_data_to_default(self, hdf5_handler, data, set_name):
        """
        Add data of a set to the default file.
        """
        object_fields = ['image_filenames', 'classes', 'boxes', 'boxesv', 'id', 'occlusion']
        image_filenames = []
        bbox = []
        bboxv = []
        lbl_id = []
        occlusion = []
        object_id = []

        list_image_filenames_per_class = []
        list_boxes_per_image = []
        list_boxesv_per_image = []
        list_object_ids_per_image = []
        list_objects_ids_per_class = []
        # list_objects_ids_per_id = []
        # list_objects_ids_per_occlusion= []

        if self.verbose:
            print('> Adding data to default file...')
            prgbar = progressbar.ProgressBar(max_value=len(data))

        img_counter = 0
        obj_counter = 0
        for i, set_data in enumerate(sorted(data)):
            for video in sorted(data[set_data]):
                img_fnames = data[set_data][video]["images"]
                annot_fnames = data[set_data][video]["annotations"]

                # cycle all images + annotations
                for j in range(0, len(img_fnames)):
                    # add image filename
                    image_filenames.append(img_fnames[j])

                    # load annotation file
                    annotation = load_json(annot_fnames[j])

                    obj_per_img = []
                    if any(annotation):
                        for obj in annotation:
                            # convert [x,y,w,h] to [xmin,ymin,xmax,ymax]
                            # discard any bbox smaller than 5px wide/high
                            if obj['pos'][2] >= 5 and obj['pos'][3] >= 5:
                                bb_correct_format = [obj['pos'][0],
                                                     obj['pos'][1],
                                                     obj['pos'][0] + obj['pos'][2] - 1,
                                                     obj['pos'][1] + obj['pos'][3] - 1]
                                bbox.append(bb_correct_format)
                                if isinstance(obj['posv'], list):
                                    # convert [x,y,w,h] to [xmin,ymin,xmax,ymax]
                                    bbv_correct_format = [obj['posv'][0],
                                                          obj['posv'][1],
                                                          obj['posv'][0] + obj['posv'][2] - 1,
                                                          obj['posv'][1] + obj['posv'][3] - 1]
                                    bboxv.append(bbv_correct_format)
                                else:
                                    bboxv.append([0, 0, 0, 0])
                                if isinstance(obj['id'], int):
                                    lbl_id.append(obj['id'])
                                else:
                                    lbl_id.append(0)
                                occlusion.append(obj['occl'])
                                class_lbl = self.classes.index(obj['lbl'])

                                # img, class, bbox, bboxv, id, occlusion
                                object_id.append([img_counter, class_lbl, obj_counter,
                                                  obj_counter, obj_counter, obj_counter])

                                obj_per_img.append(obj_counter)

                                # increment counter
                                obj_counter += 1

                    # add to lists
                    list_boxes_per_image.append(obj_per_img)
                    list_boxesv_per_image.append(obj_per_img)
                    list_object_ids_per_image.append(obj_per_img)

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
            imgs_per_class = list(set(imgs_per_class))  # get unique values
            imgs_per_class.sort()
            list_image_filenames_per_class.append(imgs_per_class)

        for i in range(len(self.classes)):
            objs_per_class = [j for j, val in enumerate(object_id) if val[1] == i]
            objs_per_class = list(set(objs_per_class))  # get unique values
            objs_per_class.sort()
            list_objects_ids_per_class.append(objs_per_class)

        # add data to hdf5 file
        hdf5_write_data(hdf5_handler, 'image_filenames', str2ascii(image_filenames),
                        dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'classes', str2ascii(self.classes),
                        dtype=np.uint8, fillvalue=0)
        hdf5_write_data(hdf5_handler, 'boxes', np.array(bbox, dtype=np.float),
                        fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'boxesv', np.array(bboxv, dtype=np.float),
                        fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'id', np.array(lbl_id, dtype=np.int32),
                        fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'occlusion', np.array(occlusion, dtype=np.float),
                        fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'object_ids', np.array(object_id, dtype=np.int32),
                        fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'object_fields', str2ascii(object_fields),
                        dtype=np.uint8, fillvalue=0)

        pad_value = -1
        hdf5_write_data(hdf5_handler, 'list_image_filenames_per_class',
                        np.array(pad_list(list_image_filenames_per_class, pad_value),
                                 dtype=np.int32),
                        fillvalue=pad_value)
        hdf5_write_data(hdf5_handler, 'list_boxes_per_image',
                        np.array(pad_list(list_boxes_per_image, pad_value), dtype=np.int32),
                        fillvalue=pad_value)
        hdf5_write_data(hdf5_handler, 'list_boxesv_per_image',
                        np.array(pad_list(list_boxesv_per_image, pad_value), dtype=np.int32),
                        fillvalue=pad_value)
        hdf5_write_data(hdf5_handler, 'list_object_ids_per_image',
                        np.array(pad_list(list_object_ids_per_image, pad_value), dtype=np.int32),
                        fillvalue=pad_value)
        hdf5_write_data(hdf5_handler, 'list_objects_ids_per_class',
                        np.array(pad_list(list_objects_ids_per_class, pad_value), dtype=np.int32),
                        fillvalue=pad_value)

        if self.verbose:
            print('> Done.')


class Detection10x(Detection):
    """ Caltech Pedestrian detection (10x data) preprocessing functions """

    skip_step = 3
    filename_h5 = 'detection_10x'


class Detection30x(Detection):
    """ Caltech Pedestrian detection (30x data) preprocessing functions """

    skip_step = 1
    filename_h5 = 'detection_30x'
