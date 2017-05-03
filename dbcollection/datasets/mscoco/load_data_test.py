import os
from dbcollection.utils.file_load import load_json


def load_data_test(set_name, image_dir, annotation_path, verbose=True):
    """
    Load test data annotations.
    """
    data = {}

    # load annotation file
    if verbose:
        print('> Loading annotation file: ' + annotation_path)
    annotations = load_json(annotation_path)

    # parse annotations
    # images
    if verbose:
        print('> Processing image annotations... ')
    for i, annot in enumerate(annotations['images']):
        data[annot['id']] = {
            "width" : annot['width'],
            "height" : annot['height'],
            "filename" : os.path.join(image_dir, annot['file_name'])
        }

    # categories
    if verbose:
        print('> Processing category annotations... ')
    categories = {}
    category_list, supercategory_list = [], []
    for i, annot in enumerate(annotations['categories']):
        categories[annot['id']] = {
            "name" : annot['name'],
            "supercategory" : annot['supercategory']
        }
        category_list.append(annot['name'])
        supercategory_list.append(annot['supercategory'])
    supercategory_list = list(set(supercategory_list))

    return {set_name : [data, category_list, supercategory_list]}