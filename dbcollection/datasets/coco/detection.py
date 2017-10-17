"""
COCO Detection 2015/2016 process functions.
"""


from __future__ import print_function, division
import os
from collections import OrderedDict
import numpy as np
import progressbar

from dbcollection.datasets import BaseTask

from dbcollection.utils.string_ascii import convert_str_to_ascii as str2ascii
from dbcollection.utils.pad import pad_list, squeeze_list
from dbcollection.utils.file_load import load_json
from dbcollection.utils.hdf5 import hdf5_write_data

from .load_data_test import load_data_test


class Detection2015(BaseTask):
    """COCO Detection (2015) preprocessing functions."""

    # metadata filename
    filename_h5 = 'detection_2015'

    image_dir_path = {
        "train": 'train2014',
        "val": 'val2014',
        "test": 'test2014'
    }

    annotation_path = {
        "train": os.path.join('annotations', 'instances_train2014.json'),
        "val": os.path.join('annotations', 'instances_val2014.json'),
        "test": os.path.join('annotations', 'image_info_test2014.json')
    }

    def parse_image_annotations(self, image_dir, annotations):
        """
        Parse image annotations data to a dictionary and  lists
        """
        filename_ids = {}
        for i, annot in enumerate(annotations['images']):
            filename_ids[annot['file_name']] = i

        # order image data by file name
        images_annot_by_fname = {}
        for i, annot in enumerate(annotations['images']):
            images_annot_by_fname[annot['file_name']] = {
                "file_name": os.path.join(image_dir, annot['file_name']),
                "width": annot['width'],
                "height": annot['height'],
                "id": annot['id'],
                "coco_url": annot['coco_url'],
            }
        # order image data by file id
        images_fname_by_id = {}
        for i, annot in enumerate(annotations['images']):
            images_fname_by_id[annot['id']] = annot['file_name']

        return filename_ids, images_annot_by_fname, images_fname_by_id

    def parse_category_annotations(self, annotations):
        """
        Parse category annotations data to a dictionary and  lists
        """
        categories = {}
        category_list, supercategory_list, category_id = [], [], []
        for i, annot in enumerate(annotations['categories']):
            categories[annot['id']] = {
                "name": annot['name'],
                "supercategory": annot['supercategory'],
                "id": annot['id']
            }
            category_id.append(annot['id'])
            category_list.append(annot['name'])
            supercategory_list.append(annot['supercategory'])
        supercategory_list = list(set(supercategory_list))

        return categories, category_list, supercategory_list, category_id

    def load_data_trainval(self, set_name, image_dir, annotation_path):
        """
        Load train+val data
        """
        data = {}

        # load annotations file
        if self.verbose:
            print('  > Loading annotation file: ' + annotation_path)
        annotations = load_json(annotation_path)

        # progressbar
        if self.verbose:
            prgbar = progressbar.ProgressBar(max_value=len(annotations['annotations']))

        # ---------------------------------------------------------
        #  parse annotations
        # ---------------------------------------------------------

        if self.verbose:
            print('  > Processing image annotations... ')
        # get all image filenames + ids into a list
        filename_ids, images_annot_by_fname, images_fname_by_id = self.parse_image_annotations(
            image_dir, annotations)

        if self.verbose:
            print('  > Processing category annotations... ')
        parsed_annots = self.parse_category_annotations(annotations)
        categories, category_list, supercategory_list, category_id = parsed_annots

        if self.verbose:
            print('  > Processing object annotations... ')
        # group annotations by file name
        annotation_id_dict = {}
        for i, annot in enumerate(annotations['annotations']):
            filename = images_fname_by_id[annot['image_id']]
            category_annot = categories[annot['category_id']]
            obj_id = annot["id"]
            annotation_id_dict[obj_id] = i

            if isinstance(annot["segmentation"], list):
                segmentation = squeeze_list(annot["segmentation"], -1)  # squeeze list
            elif isinstance(annot["segmentation"]['counts'], list):
                segmentation = annot["segmentation"]["counts"]
            else:
                segmentation = annot["segmentation"]

            # convert from [x,y,w,h] to [xmin,ymin,xmax,ymax]
            bbox = [annot['bbox'][0],  # xmin
                    annot['bbox'][1],  # ymin
                    annot['bbox'][0] + annot['bbox'][2] - 1,  # ymax
                    annot['bbox'][1] + annot['bbox'][3] - 1]  # ymax

            obj = {
                "category": category_annot['name'],
                "supercategory": category_annot['supercategory'],
                "area": annot['area'],
                "iscrowd": annot['iscrowd'],
                "segmentation": segmentation,
                "bbox": bbox,
                "image_id": annot['image_id'],
                "category_id": annot['category_id'],
                "id": annot["id"],
                "annotation_id": i
            }

            # add annotations to the image data
            try:
                images_annot_by_fname[filename]["object"].update({obj_id: obj})
            except KeyError:
                images_annot_by_fname[filename]["object"] = {obj_id: obj}

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # reset progressbar
        if self.verbose:
            prgbar.finish()

        return {set_name: [OrderedDict(sorted(images_annot_by_fname.items())),
                           annotations,
                           annotation_id_dict,
                           category_list,
                           supercategory_list,
                           category_id,
                           filename_ids,
                           images_fname_by_id]}

    def load_data(self):
        """
        Load data of the dataset (create a generator).
        """
        for set_name in self.image_dir_path:
            if self.verbose:
                print('\n> Loading data files for the set: ' + set_name)

            # image dir
            image_dir = os.path.join(self.data_path, self.image_dir_path[set_name])

            # annotation file path
            annot_filepath = os.path.join(self.data_path, self.annotation_path[set_name])

            if 'test' in set_name:
                yield load_data_test(set_name, image_dir, annot_filepath, self.verbose)
            else:
                yield self.load_data_trainval(set_name, image_dir, annot_filepath)

    def add_data_to_source(self, hdf5_handler, data, set_name):
        """
        Store classes + filenames as a nested tree.
        """
        image_dir = os.path.join(self.data_path, self.image_dir_path[set_name])
        if 'test' in set_name:
            is_test = True
            data_ = data[0]
            annotations = data[2]
        else:
            is_test = False
            data_ = data[0]
            annotations = data[1]

        if self.verbose:
            print('> Adding data to source group...')

        if self.verbose:
            print('>>> Adding data to group: images')
            prgbar = progressbar.ProgressBar(max_value=len(annotations['images']))

        # images - original
        image_grp = hdf5_handler.create_group('images')
        for i, annot in enumerate(annotations['images']):
            file_grp = image_grp.create_group(str(i))
            file_grp['file_name'] = str2ascii(os.path.join(image_dir, annot["file_name"]))
            file_grp['coco_url'] = str2ascii(annot["coco_url"])
            file_grp['width'] = np.array(annot["width"], dtype=np.int32)
            file_grp['height'] = np.array(annot["height"], dtype=np.int32)
            file_grp['id'] = np.array(annot["id"], dtype=np.int32)

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        if self.verbose:
            prgbar.finish()
            print('>>> Adding data to group: categories')
            prgbar = progressbar.ProgressBar(max_value=len(annotations['categories']))

        # categories - original
        cat_grp = hdf5_handler.create_group('categories')
        for i, annot in enumerate(annotations['categories']):
            file_grp = cat_grp.create_group(str(i))
            file_grp['supercategory'] = str2ascii(annot["supercategory"])
            file_grp['name'] = str2ascii(annot["name"])
            file_grp['id'] = np.array(annot["id"], dtype=np.int32)

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # annotations - original
        if not is_test:
            if self.verbose:
                prgbar.finish()
                print('>>> Adding data to group: annotations')
                prgbar = progressbar.ProgressBar(max_value=len(annotations['annotations']))

            annot_grp = hdf5_handler.create_group('annotations')
            for i, annot in enumerate(annotations['annotations']):
                file_grp = annot_grp.create_group(str(i))
                file_grp['iscrowd'] = np.array(annot["iscrowd"], dtype=np.int32)
                file_grp['area'] = np.array(annot["area"], dtype=np.float)
                file_grp['id'] = np.array(annot["id"], dtype=np.int32)
                file_grp['category_id'] = np.array(annot["category_id"], dtype=np.int32)
                file_grp['image_id'] = np.array(annot["image_id"], dtype=np.int32)
                file_grp['bbox'] = np.array(annot["bbox"], dtype=np.float)
                file_grp['segmentation'] = np.array(annot["segmentation"], dtype=np.float)

                # update progressbar
                if self.verbose:
                    prgbar.update(i)

        if self.verbose:
            prgbar.finish()
            print('>>> Adding data to group: grouped')
            prgbar = progressbar.ProgressBar(max_value=len(data_))

        # grouped/combined data - parsed by me
        grouped_grp = hdf5_handler.create_group('grouped')
        for i, key in enumerate(data_):
            file_grp = grouped_grp.create_group(str(i))
            file_grp['image_filename'] = str2ascii(data_[key]["file_name"])
            file_grp['coco_url'] = str2ascii(data_[key]["coco_url"])
            file_grp['width'] = np.array(data_[key]["width"], dtype=np.int32)
            file_grp['height'] = np.array(data_[key]["height"], dtype=np.int32)
            file_grp['id'] = np.array(data_[key]["id"], dtype=np.int32)

            if 'object' in data_[key]:
                for j, obj_id in enumerate(data_[key]["object"]):
                    obj_grp = file_grp.create_group(str(j))
                    obj = data_[key]["object"][obj_id]
                    obj_grp['id'] = np.array(obj["id"], dtype=np.int32)
                    obj_grp['image_id'] = np.array(obj["image_id"], dtype=np.int32)
                    obj_grp['category_id'] = np.array(obj["category_id"], dtype=np.int32)
                    obj_grp['category'] = str2ascii(obj["category"])
                    obj_grp['supercategory'] = str2ascii(obj["supercategory"])
                    obj_grp['area'] = np.array(obj["area"], dtype=np.int32)
                    obj_grp['iscrowd'] = np.array(obj["iscrowd"], dtype=np.int32)
                    obj_grp['bbox'] = np.array(obj["bbox"], dtype=np.float)
                    obj_grp['segmentation'] = np.array(obj["segmentation"], dtype=np.float)

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # update progressbar
        if self.verbose:
            prgbar.finish()

    def add_data_to_default(self, hdf5_handler, data, set_name):
        """
        Add data of a set to the default group.
        """
        image_dir = os.path.join(self.data_path, self.image_dir_path[set_name])
        if 'test' in set_name:
            is_test = True
            data_ = data[0]
            filename_ids = data[1]
            annotations = data[2]
            category = data[3]
            supercategory = data[4]
            category_id = data[5]
        else:
            is_test = False
            data_ = data[0]
            annotations = data[1]
            annotation_id_dict = data[2]
            category = data[3]
            supercategory = data[4]
            category_id = data[5]
            filename_ids = data[6]
            images_fname_by_id = data[7]

        image_filenames = []
        coco_urls = []
        width = []
        height = []
        image_id = []

        annotation_id = []
        area = []
        iscrowd = [0, 1]
        segmentation = []
        bbox = []
        object_id = []

        # coco id lists
        # These are order by entry like in the annotation files.
        # I.e., coco_images_ids[0] has the object_id with the file_name, id, height, etc.
        # as coco_annotation_file[set_name]["images"][0]
        coco_images_ids = []
        coco_categories_ids = []
        coco_annotations_ids = []

        if is_test:
            object_fields = ["image_filenames", "coco_urls", "width", "height"]
        else:
            object_fields = ["image_filenames", "coco_urls", "width", "height",
                             "category", "supercategory", "boxes", "area",
                             "iscrowd", "segmentation",
                             "image_id", "category_id", "annotation_id"]

        list_image_filenames_per_category = []
        list_image_filenames_per_supercategory = []
        list_boxes_per_image = []
        list_object_ids_per_image = []
        list_objects_ids_per_category = []
        list_objects_ids_per_supercategory = []

        if self.verbose:
            print('> Adding data to default group:')
            prgbar = progressbar.ProgressBar(max_value=len(data[0]))

        counter = 0
        segmentation_t1_counter, segmentation_t2_counter = 0, 0
        tmp_coco_annotations_ids = {}

        for i, fname_idx in enumerate(data_):
            # fetch annotation
            annotation = data_[fname_idx]

            # add fields
            image_filenames.append(annotation["file_name"])
            width.append(annotation["width"])
            height.append(annotation["height"])
            coco_urls.append(annotation["coco_url"])
            image_id.append(annotation["id"])

            if is_test:
                # *** object_id ***
                # [filename, coco_url, width, height]
                object_id.append([i, i, i, i])
                list_object_ids_per_image.append([i])
            else:
                boxes_per_image = []

                if "object" in annotation:
                    for j, obj_idx in enumerate(annotation["object"]):
                        obj = annotation["object"][obj_idx]
                        area.append(obj["area"])
                        bbox.append(obj["bbox"])
                        annotation_id.append(obj["id"])
                        segmentation.append(obj["segmentation"])

                        # *** object_id ***
                        # [filename, coco_url, width, height,
                        # category, supercategory,
                        # bbox, area, iscrowd, segmentation,
                        # "image_id", "category_id", "annotation_id"]
                        object_id.append([i, i, i, i,
                                          category.index(obj["category"]), supercategory.index(
                                              obj["supercategory"]),
                                          counter, counter, obj["iscrowd"], counter,
                                          i, category.index(obj["category"]), counter])

                        boxes_per_image.append(counter)

                        # temporary var
                        tmp_coco_annotations_ids[obj["id"]] = counter

                        # update counter
                        counter += 1

                list_boxes_per_image.append(boxes_per_image)
                list_object_ids_per_image.append(boxes_per_image)

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # update progressbar
        if self.verbose:
            prgbar.finish()

        if self.verbose:
            print('> Processing coco lists:')
            prgbar = progressbar.ProgressBar(max_value=len(annotations['images']))

        # set coco id lists
        for i, annot in enumerate(annotations['images']):
            fname_id = image_filenames.index(os.path.join(image_dir, annot['file_name']))
            coco_images_ids.append(fname_id)

            # update progressbar
            if self.verbose:
                prgbar.update(i)

        # update progressbar
        if self.verbose:
            prgbar.finish()

        coco_categories_ids = list(range(len(category)))

        if not is_test:
            if self.verbose:
                prgbar = progressbar.ProgressBar(max_value=len(annotations['annotations']))
            for i, annot in enumerate(annotations['annotations']):
                annot_id = tmp_coco_annotations_ids[annot['id']]
                coco_annotations_ids.append(annot_id)

                # update progressbar
                if self.verbose:
                    prgbar.update(i)

            # update progressbar
            if self.verbose:
                prgbar.finish()

        # process lists
        if not is_test:
            if self.verbose:
                print('> Processing lists...')

            for i in range(len(category)):
                imgs_per_category = [val[0] for _, val in enumerate(object_id) if val[4] == i]
                imgs_per_category = list(set(imgs_per_category))  # get unique values
                imgs_per_category.sort()
                list_image_filenames_per_category.append(imgs_per_category)

            for i in range(len(supercategory)):
                imgs_per_supercategory = [val[0] for _, val in enumerate(object_id) if val[5] == i]
                imgs_per_supercategory = list(set(imgs_per_supercategory))  # get unique values
                imgs_per_supercategory.sort()
                list_image_filenames_per_supercategory.append(imgs_per_supercategory)

            for i in range(len(category)):
                obj_per_category = [j for j, val in enumerate(object_id) if val[4] == i]
                obj_per_category = list(set(obj_per_category))  # get unique values
                obj_per_category.sort()
                list_objects_ids_per_category.append(obj_per_category)

            for i in range(len(supercategory)):
                obj_per_supercategory = [j for j, val in enumerate(object_id) if val[5] == i]
                obj_per_supercategory = list(set(obj_per_supercategory))  # get unique values
                obj_per_supercategory.sort()
                list_objects_ids_per_supercategory.append(obj_per_supercategory)

            if self.verbose:
                print('> Done.')

        hdf5_write_data(hdf5_handler, 'image_filenames',
                        str2ascii(image_filenames), dtype=np.uint8,
                        fillvalue=0)
        hdf5_write_data(hdf5_handler, 'coco_urls',
                        str2ascii(coco_urls), dtype=np.uint8,
                        fillvalue=0)
        hdf5_write_data(hdf5_handler, 'width',
                        np.array(width, dtype=np.int32),
                        fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'height',
                        np.array(height, dtype=np.int32),
                        fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'category',
                        str2ascii(category), dtype=np.uint8,
                        fillvalue=0)
        hdf5_write_data(hdf5_handler, 'supercategory',
                        str2ascii(supercategory), dtype=np.uint8,
                        fillvalue=0)
        hdf5_write_data(hdf5_handler, 'image_id',
                        np.array(image_id, dtype=np.int32),
                        fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'category_id',
                        np.array(category_id, dtype=np.int32),
                        fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'object_ids',
                        np.array(object_id, dtype=np.int32),
                        fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'object_fields',
                        str2ascii(object_fields), dtype=np.uint8,
                        fillvalue=0)
        hdf5_write_data(hdf5_handler, 'coco_images_ids',
                        np.array(coco_images_ids, dtype=np.int32),
                        fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'coco_categories_ids',
                        np.array(coco_categories_ids, dtype=np.int32),
                        fillvalue=-1)
        hdf5_write_data(hdf5_handler, 'list_object_ids_per_image',
                        np.array(pad_list(list_object_ids_per_image, -1), dtype=np.int32),
                        fillvalue=-1)

        if not is_test:
            hdf5_write_data(hdf5_handler, 'annotation_id',
                            np.array(annotation_id, dtype=np.int32),
                            fillvalue=-1)
            hdf5_write_data(hdf5_handler, 'boxes',
                            np.array(bbox, dtype=np.float),
                            fillvalue=-1)
            hdf5_write_data(hdf5_handler, 'iscrowd',
                            np.array(iscrowd, dtype=np.uint8),
                            fillvalue=0)

            nrows = len(segmentation)
            ncols = max([len(l) for l in segmentation])
            dset = hdf5_handler.create_dataset('segmentation',
                                               (nrows, ncols),
                                               dtype=np.float,
                                               chunks=True,
                                               compression="gzip",
                                               compression_opts=4,
                                               fillvalue=-1)
            if self.verbose:
                print('   -- Saving segmentation masks to disk (this will take some time)')
                prgbar = progressbar.ProgressBar(max_value=nrows)
            for i in range(nrows):
                dset[i, :len(segmentation[i])] = np.array(segmentation[i], dtype=np.float)
                if self.verbose:
                    prgbar.update(i)

            if self.verbose:
                prgbar.finish()

            hdf5_write_data(hdf5_handler, 'area',
                            np.array(area, dtype=np.int32),
                            fillvalue=-1)
            hdf5_write_data(hdf5_handler, 'coco_annotations_ids',
                            np.array(coco_annotations_ids, dtype=np.int32),
                            fillvalue=-1)

            pad_value = -1
            hdf5_write_data(hdf5_handler, 'list_image_filenames_per_category',
                            np.array(pad_list(list_image_filenames_per_category,
                                              pad_value), dtype=np.int32),
                            fillvalue=pad_value)
            hdf5_write_data(hdf5_handler, 'list_image_filenames_per_supercategory',
                            np.array(pad_list(list_image_filenames_per_supercategory,
                                              pad_value), dtype=np.int32),
                            fillvalue=pad_value)
            hdf5_write_data(hdf5_handler, 'list_boxes_per_image',
                            np.array(pad_list(list_boxes_per_image, pad_value), dtype=np.int32),
                            fillvalue=pad_value)
            hdf5_write_data(hdf5_handler, 'list_objects_ids_per_category',
                            np.array(pad_list(list_objects_ids_per_category,
                                              pad_value), dtype=np.int32),
                            fillvalue=pad_value)
            hdf5_write_data(hdf5_handler, 'list_objects_ids_per_supercategory',
                            np.array(pad_list(list_objects_ids_per_supercategory,
                                              pad_value), dtype=np.int32),
                            fillvalue=pad_value)


# ---------------------------------------------------------
#  Detection 2016
# ---------------------------------------------------------

class Detection2016(Detection2015):
    """COCO Detection (2016) preprocessing functions."""

    # metadata filename
    filename_h5 = 'detection_2016'

    image_dir_path = {
        "train": 'train2014',
        "val": 'val2014',
        "test": 'test2015',
        "test_dev": "test2015"
    }

    annotation_path = {
        "train": os.path.join('annotations', 'instances_train2014.json'),
        "val": os.path.join('annotations', 'instances_val2014.json'),
        "test": os.path.join('annotations', 'image_info_test2015.json'),
        "test_dev": os.path.join('annotations', 'image_info_test-dev2015.json')
    }
