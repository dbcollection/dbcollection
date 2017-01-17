#!/usr/bin/env python
# Copyright (C) 2017, Farrajota @ https://github.com/farrajota
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""
Cifar10 data download script.
"""

from .. import utils, data


def main(verbose=False, clean_cache=False):
    """
    Download and extract cifar10's files. 
    """

    dataset = {
        "name": "cifar10",
        "url":['https://www.cs.toronto.edu/~kriz/cifar-10-matlab.tar.gz']
    }
    
    # get path to store data
    cache_manager = data.CacheManager()
    dir_save = cache_manager.get_cache_path(dataset["name"])

    # download + extract data and remove temporary files
    utils.download_all(dataset['url'], dir_save, clean_cache, verbose)


#---------------------------------------------------------
# Main function call 
#---------------------------------------------------------

if __name__ == "__main__":
    main()