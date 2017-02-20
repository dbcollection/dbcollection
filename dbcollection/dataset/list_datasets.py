"""
Datasets list.

All available datasets must be added in this file.
"""


from . import cifar


datasets = {
    "cifar10" : cifar.cifar10.Cifar10,
}