#!/usr/bin/env python
# Copyright (C) 2017, Farrajota @ https://github.com/farrajota
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""
Cifar10 data download script.
"""

DATASET_NAME = 'cifar10'


def main():
    """
    Main function
    """
   
   # get save path
   store_data_path = get_save_path()

   # define files to download
   url = {'https://www.cs.toronto.edu/~kriz/cifar-10-matlab.tar.gz'}



   url1 = 'https://www.cs.toronto.edu/~kriz/cifar-10-matlab.tar.gz'
dataset = 'cifar10'
save_path = '/home/mf/tmp/data/' + dataset + '/'
fname_save = 'cifar-10-matlab.tar.gz'

#---------------------------------------------------------
# Main function call 
#---------------------------------------------------------

if __name__ == "__main__":
    main()