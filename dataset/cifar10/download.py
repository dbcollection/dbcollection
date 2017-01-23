#!/usr/bin/env python
# Copyright (C) 2017, Farrajota @ https://github.com/farrajota
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


"""
Cifar10 data download script.

This script downloads the necessary files to disk from the owners website and then extracts them.
"""


if __name__ == "__main__":
    import os
    import sys

    dir_path = os.path.dirname(os.path.realpath(__file__))
    lib_path = os.path.abspath(os.path.join(dir_path, '..', '..'))
    sys.path.append(lib_path)
    from dataset import utils, data


def main(verbose=False, clean_cache=False):
    """
    Download and extract cifar10's files.
    """

    dataset_info = {
        "name": "cifar10",
        "url":[
            ['https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz', "c58f30108f718f92721af3b95e74349a"]
        ]
    }

    # get path to store data
    cache_manager = data.CacheManager() # Cache manager
    data_paths = cache_manager.get_dataset_storage_paths(dataset_info["name"])
    dir_save = data_paths["data_path"]

    # download + extract data and remove temporary files
    utils.download_extract_all(dataset_info['url'][0], dataset_info['url'][1], dir_save, clean_cache, verbose)


#---------------------------------------------------------
# Main function call
#---------------------------------------------------------

if __name__ == "__main__":
    main(True, False)
