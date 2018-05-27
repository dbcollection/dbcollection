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
    is_clean = False  # If True, discards detection boxes smaller than 5px

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
        annotations = self.load_annotations(annotation_filenames)
        return {
            "image_filenames": image_filenames,
            "annotations": annotations
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

    def load_annotations(self, annotation_filenames):
        """Loads the annotations' files data to memory."""
        annotations = {}
        for partition in sorted(annotation_filenames):
            annotations[partition] = {}
            for video in sorted(annotation_filenames[partition]):
                annotations_video = []
                for annotation_filename in sorted(annotation_filenames[partition][video]["annotations"]):
                    annotation_data = self.load_annotation_file(annotation_filename)
                    annotations_video.append(annotation_data)
                annotations[partition][video] = annotations_video
        return annotations

    def load_annotation_file(self, path):
        """Loads the annotation's file data from disk."""
        return load_json(path)

    def process_set_metadata(self, data, set_name):
        """
        Saves the metadata of a set.
        """
        args = {
            "data": data,
            "set_name": set_name,
            "is_clean": self.is_clean,
            "hdf5_manager": self.hdf5_manager,
            "verbose": self.verbose
        }

        class_ids = ClassLabelField(**args).process(self.classes)
        image_filenames_ids = ImageFilenamesField(**args).process()
        bbox_ids = BoundingBoxField(**args).process()
        bboxv_ids = BoundingBoxvField(**args).process()
        label_ids = LabelIdField(**args).process()
        occlusion_ids = []
        object_id = []
        ObjectFieldNamesField(**args).process()

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


class BaseField(object):
    """Base class for the dataset's data fields processor."""

    def __init__(self, data, set_name, is_clean, hdf5_manager, verbose):
        self.data = data
        self.set_name = set_name
        self.is_clean = is_clean
        self.hdf5_manager = hdf5_manager
        self.verbose = verbose

    def get_annotation_objects_generator(self):
        """Returns a generator for all object annotations of the data.

        This method cycles all annotation objects for a set of partitions
        plus videos in order and returns for each object its annotation and
        two counters at specific points of the loops.

        Since most annotations of this dataset require different parameters
        at a common stage of the loop cycle(s), this generator allows to get
        such information in a flexible way by yielding the common data for
        all data fields.
        """
        img_counter = 0
        obj_counter = 0
        data = self.data["annotations"]
        for partition in sorted(data):
            for video in sorted(data[partition]):
                for annotation_data in data[partition][video]:
                    if any(annotation_data):
                        for obj in annotation_data:
                            if self.is_clean:
                                if obj['pos'][2] >= 5 and obj['pos'][3] >= 5:
                                    yield {
                                        "obj": obj,
                                        "image_counter": img_counter,
                                        "obj_counter": obj_counter
                                    }
                                    obj_counter += 1
                            else:
                                yield {
                                    "obj": obj,
                                    "image_counter": img_counter,
                                    "obj_counter": obj_counter
                                }
                                obj_counter += 1
                    img_counter += 1


    def save_field_to_hdf5(self, set_name, field, data, **kwargs):
        """Saves data of a field into the HDF% metadata file.

        Parameters
        ----------
        set_name: str
            Name of the set split.
        field : str
            Name of the data field.
        data : np.ndarray
            Numpy ndarray of the field's data.

        """
        self.hdf5_manager.add_field_to_group(
            group=set_name,
            field=field,
            data=data,
            **kwargs
        )


class ClassLabelField(BaseField):
    """Class label names' field metadata process/save class."""

    def process(self, classes):
        """Processes and saves the classes metadata to hdf5."""
        if self.verbose:
            print('> Processing the class labels metadata...')
        classes_ids = self.get_class_labels_ids(classes)
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='classes',
            data=str2ascii(classes),
            dtype=np.uint8,
            fillvalue=0
        )
        return classes_ids

    def get_class_labels_ids(self, classes):
        """Returns a list of label ids for each row of 'object_ids' field."""
        class_ids = []
        annotations_generator = self.get_annotation_objects_generator(self.data)
        for annotation in annotations_generator():
            class_ids.append(classes.index(annotation['obj']['lbl']))
        return class_ids


class ImageFilenamesField(BaseField):
    """Image filenames' field metadata process/save class."""

    def process(self):
        """Processes and saves the image filenames metadata to hdf5."""
        if self.verbose:
            print('> Processing the image filenames metadata...')
        image_filenames, image_filenames_ids = self.get_image_filenames_from_data()
        image_filenames_ids = self.get_image_filenames_obj_ids_from_data()
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='image_filenames',
            data=str2ascii(image_filenames),
            dtype=np.uint8,
            fillvalue=0
        )
        return image_filenames_ids

    def get_image_filenames_from_data(self):
        """Returns a list of sorted image filenames for a sequence of partitions + video sets."""
        image_filenames = []
        data = self.data["image_filenames"]
        for partition in sorted(data):
            for video in sorted(data[partition]):
                image_filenames += data[partition][video]
        return image_filenames

    def get_image_filenames_obj_ids_from_data(self):
        """Returns a list of image ids for each row of 'object_ids' field."""
        image_filenames_ids = []
        annotations_generator = self.get_annotation_objects_generator()
        for annotation in annotations_generator():
            image_filenames_ids.append(annotation['img_counter'])
        return image_filenames_ids


class BoundingBoxBaseField(BaseField):
    """Base class for parsing bounding box annotations."""

    def get_bboxes_from_data(self, bbox_type):
        """Returns a list of bounding boxes and a list
        of ids for each row of 'object_ids' field."""
        bbox, bbox_ids = [], []
        annotations_generator = self.get_annotation_objects_generator(self.data)
        for annotation in annotations_generator():
            bbox.append(self.get_bbox_by_type(annotation["obj"], bbox_type))
            bbox_ids.append(annotation['obj_counter'])
        return bbox, bbox_ids

    def get_bbox_by_type(self, obj, bbox_type):
        if bbox_type == 'pos':
            bbox = self.bbox_correct_format(obj['pos'])
        else:
            if isinstance(obj['posv'], list):
                bbox = self.bbox_correct_format(obj['posv'])
            else:
                bbox = [0, 0, 0, 0]
        return bbox

    def bbox_correct_format(self, bbox):
        """Converts the bounding box [x,y,wh,h] format to [x1,y1,x2,y2]."""
        x1 = bbox[0]
        y1 = bbox[1]
        x2 = bbox[0] + bbox[2] - 1
        y2 = bbox[1] + bbox[3] - 1
        return [x1, y1, x2, y2]


class BoundingBoxField(BoundingBoxBaseField):
    """Bounding boxes' field metadata process/save class."""

    def process(self):
        """Processes and saves the annotation's bounding boxes metadata to hdf5."""
        if self.verbose:
            print('> Processing the pedestrian bounding boxes metadata...')
        bboxes, bboxes_ids = self.get_bboxes_from_data('pos')
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='bboxes',
            data=np.array(bboxes, dtype=np.float32),
            dtype=np.float32,
            fillvalue=-1
        )
        return bboxes_ids


class BoundingBoxvField(BoundingBoxBaseField):
    """Bounding boxesv' field metadata process/save class."""

    def process(self):
        """Processes and saves the annotation's bounding boxes (v) metadata to hdf5."""
        if self.verbose:
            print('> Processing the pedestrian bounding boxes (v) metadata...')
        bboxesv, bboxesv_ids = self.get_bboxes_from_data('posv')
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='bboxesv',
            data=np.array(bboxesv, dtype=np.float32),
            dtype=np.float32,
            fillvalue=-1
        )
        return bboxesv_ids


class LabelIdField(BaseField):
    """Label id field metadata process/save class."""

    def process(self):
        """Processes and saves the annotation's label metadata to hdf5."""
        if self.verbose:
            print('> Processing the pedestrian labels metadata...')
        labels, label_ids = self.get_label_ids()
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='id',
            data=np.array(labels, dtype=np.float32),
            dtype=np.float32,
            fillvalue=-1
        )
        return label_ids

    def get_label_ids(self):
        """Returns a list of label ids for each row of 'object_ids' field."""
        labels, label_ids = [], []
        annotations_generator = self.get_annotation_objects_generator(self.data)
        for annotation in annotations_generator():
            labels.append(self.get_id(annotation["obj"]))
            label_ids.append(annotation['obj_counter'])
        return labels, label_ids

    def get_id(self, obj):
        """Returns the label id of an annotation obejct."""
        if isinstance(obj['id'], int):
            return obj['id']
        else:
            return 0


class ObjectFieldNamesField(BaseField):
    """Object field names' field metadata process/save class."""

    def process(self):
        """Processes and saves the classes metadata to hdf5."""
        object_fields = ['image_filenames', 'classes', 'boxes', 'boxesv', 'id', 'occlusion']
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='object_fields',
            data=str2ascii(object_fields),
            dtype=np.uint8,
            fillvalue=0
        )


class Detection10x(Detection):
    """ Caltech Pedestrian detection (10x data) preprocessing functions """

    skip_step = 3
    filename_h5 = 'detection_10x'


class Detection30x(Detection):
    """ Caltech Pedestrian detection (30x data) preprocessing functions """

    skip_step = 1
    filename_h5 = 'detection_30x'
