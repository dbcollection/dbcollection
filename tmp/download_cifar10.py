#!/usr/bin/env python
# Copyright (C) 2017, Farrajota @ https://github.com/farrajota 
# All rights reserved.
# 
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import download as dl


# Download cifar 10
url1 = 'https://www.cs.toronto.edu/~kriz/cifar-10-matlab.tar.gz'
dataset = 'cifar10'
save_path = '/home/mf/tmp/data/' + dataset + '/'
fname_save = 'cifar-10-matlab.tar.gz'

# download file
dl.download_file(url1, save_path, fname_save, True)
#print('download file')
#dl.download_file_v1(url1, save_path, fname_save, True)

# extract file
dl.extract_file(save_path, fname_save,True)

print('Done.')