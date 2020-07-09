from enum import Enum
from frozendict import frozendict


class Datasets(str, Enum):
    MNIST = "MNIST"
    CIFAR10 = "CIFAR10"
    CIFAR100 = "CIFAR100"
    COCO = "COCO"
    PASCAL_VOC2012 = 'PASCAL_VOC2012'
    STL10 = "STL10"
    SVHN = "SVHN"
    PHOTOTOUR = "PHOTOTOUR"
    SBD = "SBD"
    USPS = "USPS"
    HMDB51 = "HMDB51"


DATASET_DOWNLOAD_LINKS = frozendict(
    MNIST          = {"train": "http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz",
                      "train_labels": "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz",
                      "test": "http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz",
                      "test_labels": "http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz"},
    CIFAR10        = {"train/val" : "https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"},
    CIFAR100       = {"train/val" : "https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz"},
    COCO           = {"train": "http://images.cocodataset.org/zips/train2017.zip",
                      "val": "http://images.cocodataset.org/zips/val2017.zip",
                      "annotations": "http://images.cocodataset.org/annotations/annotations_trainval2017.zip"},
    PASCAL_VOC2012 = {"train/val":  "http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar"},
    STL10          = {"train/val":  "http://ai.stanford.edu/~acoates/stl10/stl10_binary.tar.gz"},
    SVHN_FULL      = {"train": "http://ufldl.stanford.edu/housenumbers/train.tar.gz",
                      "test": "http://ufldl.stanford.edu/housenumbers/test.tar.gz",
                      "extra": "http://ufldl.stanford.edu/housenumbers/extra.tar.gz"},
    SVHN           = {"train": "http://ufldl.stanford.edu/housenumbers/train_32x32.mat",
                      "test": "http://ufldl.stanford.edu/housenumbers/test_32x32.mat",
                      "extra": "http://ufldl.stanford.edu/housenumbers/extra_32x32.mat"},
    PHOTOTOUR      = {"train/val": "http://phototour.cs.washington.edu/datasets/NotreDame.zip"},
    SBD            = {"train": "http://www.eecs.berkeley.edu/Research/Projects/CS/vision/grouping/semantic_contours/benchmark.tgz"},
    USPS           = {"train": "https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/multiclass/usps.bz2",
                      "test": "https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/multiclass/usps.t.bz2"},
    HMDB51         = {"train/val": "http://serre-lab.clps.brown.edu/wp-content/uploads/2013/10/hmdb51_org.rar"}
)

