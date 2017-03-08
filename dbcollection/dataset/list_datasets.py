"""
Datasets list.

All available datasets must be added in this file.
"""


from . import cifar, pascal_voc, mnist, imagenet


datasets = {
    "cifar10" : cifar.cifar10.Cifar10,
    "cifar100" : cifar.cifar100.Cifar100,
    "ilsvrc2012": imagenet.ilsvrc2012.ILSVRC2012,
    'mnist': mnist.mnist.MNIST,
    "pascal_voc_2007" : pascal_voc.voc_2007.PascalVOC2007
}

available_datasets = list(datasets.keys())