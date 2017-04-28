import os
from dbcollection.utils.file_load import load_json


def load_data_test(set_name, image_dir, annotation_path):
    """
    Load test data annotations.
    """
    data = {}

    # load annotation file
    annotations = load_json(annotation_path)

    # parse annotations
    # images
    for i, annot in enumerate(annotations['images']):
        data[annot['id']] = {
            "width" : annot['width'],
            "height" : annot['height'],
            "file_name" : os.path.join(image_dir, annot['file_name'])
        }

    # categories
    categories = {}
    category_list, supercategory_list = [], []
    for i, annot in enumerate(annotations['categories']):
        categories[annot['id']] = {
            "name" : annot['name'],
            "supercategory" : annot['supercategory']
        }
        category_list[i] = annot['name']
        supercategory_list[i] = annot['supercategory']
    supercategory_list = list(set(supercategory_list))

    return {set_name : [data, category_list, supercategory_list]}