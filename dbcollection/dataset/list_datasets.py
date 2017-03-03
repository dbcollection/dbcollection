"""
Datasets list.

All available datasets must be added in this file.
"""


from . import cifar, pascal_voc


datasets = {
    "cifar10" : cifar.cifar10.Cifar10,
    "cifar100" : cifar.cifar100.Cifar100,

    "pascal_voc_2007" : pascal_voc.voc_2007.PascalVOC2007
}