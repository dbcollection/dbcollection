#!/usr/bin/env python
# Copyright (C) 2017, Farrajota @ https://github.com/farrajota
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


"""
Run Cifar10 download+process scripts.
"""


from . import download as cifar10_download
from . import process as cifar10_process


def main():
    """
    Runs the download script and the process scripts.
    """
    # download data
    cifar10_download.main()

    # process metadata
    cifar10_process.main()


if __name__ == '__main__':
    main()
