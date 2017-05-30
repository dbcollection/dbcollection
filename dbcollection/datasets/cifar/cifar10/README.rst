.. _cifar_10_readme:

CIFAR-10
========

The CIFAR-10 dataset consists of 60000 32x32 colour images in 10 classes,
with 6000 images per class. There are 50000 training images and 10000 test images.

The dataset is divided into five training batches and one test batch, each with 10000
images. The test batch contains exactly 1000 randomly-selected images from each class.
The training batches contain the remaining images in random order, but some training
batches may contain more images from one class than another. Between them, the training
batches contain exactly 5000 images from each class.

Here are the classes in the dataset, as well as 10 random images from each:



airplane    |airplane1| |airplane2| |airplane3| |airplane4| |airplane5| |airplane6| |airplane7| |airplane8| |airplane9| |airplane10|

automobile

bird

cat

deer

dog

frog

horse

ship

truck


Name
----

String to load the dataset: ``cifar10``

Tasks
-----

The following tasks are available for this dataset:

- classification: (``default task``)
- classification_d:


Data structure
--------------



Disclaimer
----------

All rights reserved to the original creators of ``CIFAR-10``.

For information about the dataset and its terms of use, please see the `original website <https://www.cs.toronto.edu/~kriz/cifar.html/>`_.


.. |airplane1| image:: https://www.cs.toronto.edu/~kriz/cifar-10-sample/airplane1.png
.. |airplane2| image:: https://www.cs.toronto.edu/~kriz/cifar-10-sample/airplane2.png
.. |airplane3| image:: https://www.cs.toronto.edu/~kriz/cifar-10-sample/airplane3.png
.. |airplane4| image:: https://www.cs.toronto.edu/~kriz/cifar-10-sample/airplane4.png
.. |airplane5| image:: https://www.cs.toronto.edu/~kriz/cifar-10-sample/airplane5.png
.. |airplane6| image:: https://www.cs.toronto.edu/~kriz/cifar-10-sample/airplane6.png
.. |airplane7| image:: https://www.cs.toronto.edu/~kriz/cifar-10-sample/airplane7.png
.. |airplane8| image:: https://www.cs.toronto.edu/~kriz/cifar-10-sample/airplane8.png
.. |airplane9| image:: https://www.cs.toronto.edu/~kriz/cifar-10-sample/airplane9.png
.. |airplane10| image:: https://www.cs.toronto.edu/~kriz/cifar-10-sample/airplane10.png