"""
Caltech Pedestrian detection process functions.
"""


from __future__ import print_function, division
import os
import numpy as np
import progressbar

from dbcollection.datasets import BaseTaskNew

from dbcollection.utils.decorators import display_message_processing
from dbcollection.utils.file_load import load_json
from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list
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
        loader = DatasetLoader(
            skip_step=self.skip_step,
            classes=self.classes,
            sets=self.sets,
            is_clean=self.is_clean,
            data_path=self.data_path,
            cache_path=self.cache_path,
            verbose=self.verbose
        )
        yield {"train": loader.load_train_data()}
        yield {"test": loader.load_test_data()}

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

        # Fields
        if self.verbose:
            print('\n==> Setting up the data fields:')
        class_ids, classes_unique_ids = ClassLabelField(**args).process(self.classes)
        image_filenames_ids, image_filenames_unique_ids = ImageFilenamesField(**args).process()
        bbox_ids = BoundingBoxField(**args).process()
        bboxv_ids = BoundingBoxvField(**args).process()
        label_ids = LabelIdField(**args).process()
        occlusion_ids = OcclusionField(**args).process()
        ObjectFieldNamesField(**args).process()
        object_ids = ObjectIdsField(**args).process(
            image_filenames_ids=image_filenames_ids,
            class_ids=class_ids,
            bbox_ids=bbox_ids,
            bboxv_ids=bboxv_ids,
            label_ids=label_ids,
            occlusion_ids=occlusion_ids
        )

        # Lists
        if self.verbose:
            print('\n==> Setting up ordered lists:')
        ImageFilenamesPerClassList(**args).process(image_filenames_unique_ids, classes_unique_ids)
        BoundingBoxPerImageList(**args).process(object_ids, image_filenames_unique_ids)
        BoundingBoxvPerImageList(**args).process(object_ids, image_filenames_unique_ids)
        ObjectsPerImageList(**args).process(object_ids, image_filenames_unique_ids)
        ObjectsPerClassList(**args).process(object_ids, classes_unique_ids)


# -----------------------------------------------------------
# Data load / set up
# -----------------------------------------------------------

class DatasetLoader(object):
    """Annotation's data loader for the caltech's dataset (train/test)."""

    def __init__(self, skip_step, classes, sets, is_clean, data_path, cache_path, verbose):
        self.skip_step = skip_step
        self.classes = classes
        self.sets = sets
        self.is_clean = is_clean
        self.data_path = data_path
        self.cache_path = cache_path
        self.verbose = verbose

    def load_train_data(self):
        """Loads the train set annotation data from disk and returns
        a dictionary with the data."""
        return self.load_data_set(is_test=False)

    def load_test_data(self):
        """Loads the test set annotation data from disk and returns
        a dictionary with the data."""
        return self.load_data_set(is_test=True)

    def load_data_set(self, is_test):
        """Fetches the train/test data from disk."""
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
        image_filenames = {}
        annotation_filenames = {}
        dirs = self.get_sorted_object_names_from_dir(os.path.join(path, partition))
        for video in dirs:
            image_filenames[video] = self.get_image_filenames_from_dir(path, partition, video)
            annotation_filenames[video] = self.get_annotation_filenames_from_dir(path, partition, video)
        return {
            "images": image_filenames,
            "annotations": annotation_filenames
        }

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
                for annotation_filename in sorted(annotation_filenames[partition][video]):
                    annotation_data = self.load_annotation_file(annotation_filename)
                    annotations_video.append(annotation_data)
                annotations[partition][video] = annotations_video
        return annotations

    def load_annotation_file(self, path):
        """Loads the annotation's file data from disk."""
        return load_json(path)


# -----------------------------------------------------------
# Metadata fields
# -----------------------------------------------------------

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

    @display_message_processing('class labels')
    def process(self, classes):
        """Processes and saves the classes metadata to hdf5."""
        class_names, class_ids, class_unique_ids = self.get_class_labels_ids(classes)
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='classes',
            data=str2ascii(class_names),
            dtype=np.uint8,
            fillvalue=0
        )
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='classes_unique',
            data=str2ascii(classes),
            dtype=np.uint8,
            fillvalue=0
        )
        return class_ids, class_unique_ids

    def get_class_labels_ids(self, classes):
        """Returns a list of label ids for each row of 'object_ids' field."""
        class_names, class_ids, class_unique_ids = [], [], []
        annotations_generator = self.get_annotation_objects_generator()
        for annotation in annotations_generator:
            class_ids.append(annotation['obj_counter'])
            class_names.append(annotation['obj']['lbl'])
            class_unique_ids.append(classes.index(annotation['obj']['lbl']))
        return class_names, class_ids, class_unique_ids


class ImageFilenamesField(BaseField):
    """Image filenames' field metadata process/save class."""

    @display_message_processing('image filenames')
    def process(self):
        """Processes and saves the image filenames metadata to hdf5."""
        image_filenames_unique = self.get_image_filenames_from_data()
        image_filenames_unique_ids = self.get_image_filenames_obj_ids_from_data()
        image_filenames = [image_filenames_unique[id] for id in image_filenames_unique_ids]
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='image_filenames',
            data=str2ascii(image_filenames),
            dtype=np.uint8,
            fillvalue=0
        )
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='image_filenames_unique',
            data=str2ascii(image_filenames_unique),
            dtype=np.uint8,
            fillvalue=0
        )
        image_filenames_ids = list(range(len(image_filenames_unique_ids)))
        return image_filenames_ids, image_filenames_unique_ids

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
        for annotation in annotations_generator:
            image_filenames_ids.append(annotation['image_counter'])
        return image_filenames_ids


class BoundingBoxBaseField(BaseField):
    """Base class for parsing bounding box annotations."""

    def get_bboxes_from_data(self, bbox_type):
        """Returns a list of bounding boxes and a list
        of ids for each row of 'object_ids' field."""
        bbox, bbox_ids = [], []
        annotations_generator = self.get_annotation_objects_generator()
        for annotation in annotations_generator:
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

    @display_message_processing('bounding boxes')
    def process(self):
        """Processes and saves the annotation's bounding boxes metadata to hdf5."""
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

    @display_message_processing('bounding boxes (v)')
    def process(self):
        """Processes and saves the annotation's bounding boxes (v) metadata to hdf5."""
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

    @display_message_processing('labels')
    def process(self):
        """Processes and saves the annotation's label metadata to hdf5."""
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
        annotations_generator = self.get_annotation_objects_generator()
        for annotation in annotations_generator:
            labels.append(self.get_id(annotation["obj"]))
            label_ids.append(annotation['obj_counter'])
        return labels, label_ids

    def get_id(self, obj):
        """Returns the label id of an annotation obejct."""
        if isinstance(obj['id'], int):
            return obj['id']
        else:
            return 0


class OcclusionField(BaseField):
    """Occlusion field metadata process/save class."""

    @display_message_processing('occlusion')
    def process(self):
        """Processes and saves the annotation's occlusion metadata to hdf5."""
        occlusions, occlusion_ids = self.get_occlusion_ids()
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='occlusion',
            data=np.array(occlusions, dtype=np.float32),
            dtype=np.float32,
            fillvalue=-1
        )
        return occlusion_ids

    def get_occlusion_ids(self):
        """Returns a list of occlusion labels and ids for each row of 'object_ids' field."""
        occlusions, occlusion_ids = [], []
        annotations_generator = self.get_annotation_objects_generator()
        for annotation in annotations_generator:
            occlusions.append(annotation["obj"]["occl"])
            occlusion_ids.append(annotation['obj_counter'])
        return occlusions, occlusion_ids


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


class ObjectIdsField(BaseField):
    """Object ids' field metadata process/save class."""

    def process(self, image_filenames_ids, class_ids, bbox_ids,
                bboxv_ids, label_ids, occlusion_ids):
        """Processes and saves the object ids metadata to hdf5."""
        # img, class, bbox, bboxv, id, occlusion
        object_ids = [[image_filenames_ids[i], class_ids[i], bbox_ids[i],
                      bboxv_ids[i], label_ids[i], occlusion_ids[i]]
                      for i in range(len(bbox_ids))]
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='object_ids',
            data=np.array(object_ids, dtype=np.int32),
            dtype=np.int32,
            fillvalue=-1
        )
        return object_ids


# -----------------------------------------------------------
# Metadata lists
# -----------------------------------------------------------

class ImageFilenamesPerClassList(BaseField):
    """Images per class list metadata process/save class."""

    @display_message_processing('image filenames per class list')
    def process(self, image_unique_ids, class_unique_ids):
        """Processes and saves the list ids metadata to hdf5."""
        image_filenames_per_class = self.get_image_filename_ids_per_class(image_unique_ids, class_unique_ids)
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='list_image_filenames_per_class',
            data=np.array(pad_list(image_filenames_per_class, val=-1), dtype=np.int32),
            dtype=np.int32,
            fillvalue=-1
        )

    def get_image_filename_ids_per_class(self, image_unique_ids, class_unique_ids):
        """Returns a list of lists of image filename ids per class id."""
        images_per_class_ids = []
        classes = list(set(class_unique_ids))
        for i in range(len(classes)):
            imgs_per_class = [image_unique_ids[j] for j, val in enumerate(class_unique_ids) if val == i]
            imgs_per_class = sorted(list(set(imgs_per_class)))  # get unique values
            images_per_class_ids.append(imgs_per_class)
        return images_per_class_ids


class BoundingBoxPerImageList(BaseField):
    """Bounding boxes per image list metadata process/save class."""

    @display_message_processing('bounding boxes per image list')
    def process(self, object_ids, image_unique_ids):
        """Processes and saves the list ids metadata to hdf5."""
        bboxes_per_image = self.get_bbox_ids_per_image(object_ids, image_unique_ids)
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='list_boxes_per_image',
            data=np.array(pad_list(bboxes_per_image, val=-1), dtype=np.int32),
            dtype=np.int32,
            fillvalue=-1
        )

    def get_bbox_ids_per_image(self, object_ids, image_unique_ids):
        """Returns a list of lists of bounding boxes ids per image id."""
        bboxes_per_image_ids = []
        unique_ids = list(set(image_unique_ids))
        for i, image_id in enumerate(unique_ids):
            bboxes_per_image = [obj[2] for j, obj in enumerate(object_ids) if image_unique_ids[obj[0]] == image_id]
            bboxes_per_image = list(set(bboxes_per_image))  # get unique values
            bboxes_per_image.sort()
            bboxes_per_image_ids.append(bboxes_per_image)
        return bboxes_per_image_ids


class BoundingBoxvPerImageList(BaseField):
    """Bounding boxes (v) per image list metadata process/save class."""

    @display_message_processing('bounding boxes (v) per image list')
    def process(self, object_ids, image_unique_ids):
        """Processes and saves the list ids metadata to hdf5."""
        bboxesv_per_image = self.get_bboxv_ids_per_image(object_ids, image_unique_ids)
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='list_boxesv_per_image',
            data=np.array(pad_list(bboxesv_per_image, val=-1), dtype=np.int32),
            dtype=np.int32,
            fillvalue=-1
        )

    def get_bboxv_ids_per_image(self, object_ids, image_unique_ids):
        """Returns a list of lists of bounding boxes (v) ids per image id."""
        bboxesv_per_image_ids = []
        unique_ids = list(set(image_unique_ids))
        for i, image_id in enumerate(unique_ids):
            bboxesv_per_image = [obj[3] for j, obj in enumerate(object_ids) if image_unique_ids[obj[0]] == image_id]
            bboxesv_per_image = list(set(bboxesv_per_image))  # get unique values
            bboxesv_per_image.sort()
            bboxesv_per_image_ids.append(bboxesv_per_image)
        return bboxesv_per_image_ids


class ObjectsPerImageList(BaseField):
    """Objects per image list metadata process/save class."""

    @display_message_processing('objects per image list')
    def process(self, object_ids, image_unique_ids):
        """Processes and saves the list ids metadata to hdf5."""
        object_ids_per_image = self.get_object_ids_per_image(object_ids, image_unique_ids)
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='list_object_ids_per_image',
            data=np.array(pad_list(object_ids_per_image, val=-1), dtype=np.int32),
            dtype=np.int32,
            fillvalue=-1
        )

    def get_object_ids_per_image(self, object_ids, image_unique_ids):
        """Returns a list of lists of object ids per image id."""
        objects_per_image_ids = []
        unique_ids = list(set(image_unique_ids))
        for i, image_id in enumerate(unique_ids):
            objects_per_image = [j for j, obj in enumerate(object_ids) if image_unique_ids[obj[0]] == image_id]
            objects_per_image = list(set(objects_per_image))  # get unique values
            objects_per_image.sort()
            objects_per_image_ids.append(objects_per_image)
        return objects_per_image_ids


class ObjectsPerClassList(BaseField):
    """Objects per class list metadata process/save class."""

    @display_message_processing('objects per class list')
    def process(self, object_ids, classes_unique_ids):
        """Processes and saves the list ids metadata to hdf5."""
        objects_ids_per_class = self.get_object_ids_per_class(object_ids, classes_unique_ids)
        self.save_field_to_hdf5(
            set_name=self.set_name,
            field='list_objects_ids_per_class',
            data=np.array(pad_list(objects_ids_per_class, val=-1), dtype=np.int32),
            dtype=np.int32,
            fillvalue=-1
        )

    def get_object_ids_per_class(self, object_ids, class_unique_ids):
        """Returns a list of lists of object ids per class id."""
        objects_per_class_ids = []
        classes = list(set(class_unique_ids))
        for i in range(len(classes)):
            objects_per_class = [j for j, val in enumerate(class_unique_ids) if val == i]
            objects_per_class = sorted(list(set(objects_per_class)))  # get unique values
            objects_per_class_ids.append(objects_per_class)
        return objects_per_class_ids


# -----------------------------------------------------------
# Additional tasks
# -----------------------------------------------------------

class DetectionClean(Detection):
    """Caltech Pedestrian detection (clean) preprocessing functions."""

    filename_h5 = 'detection_clean'
    is_clean = True  # If True, discards detection boxes smaller than 5px


class Detection10x(Detection):
    """Caltech Pedestrian detection (10x data) preprocessing functions """

    skip_step = 3
    filename_h5 = 'detection_10x'


class Detection10xClean(Detection):
    """Caltech Pedestrian detection (clean, 10x data) preprocessing functions """

    skip_step = 3
    filename_h5 = 'detection_10x_clean'
    is_clean = True  # If True, discards detection boxes smaller than 5px


class Detection30x(Detection):
    """Caltech Pedestrian detection (30x data) preprocessing functions """

    skip_step = 1
    filename_h5 = 'detection_30x'


class Detection30xClean(Detection):
    """Caltech Pedestrian detection (clean, 30x data) preprocessing functions """

    skip_step = 1
    filename_h5 = 'detection_30x_clean'
    is_clean = True  # If True, discards detection boxes smaller than 5px
