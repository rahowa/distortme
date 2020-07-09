# `distortme`

CLI utility for augmentation and preprocessing images.

Possible operations are given below under 'Commands: '

To get more info type 'distortme <command> --help'

**Usage**:

```console
$ distortme [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `augs`: Apply provided augmentations to all images in...
* `coco2voc`: [[IN PROGRESS]] Convert any dataset in COCO...
* `convert`: Convert images to certain extension as .jpg...
* `download`: Asynchronously download packed datasets in...
* `fromhd5`: Extract files from HDF5 dataset.
* `fromrle`: Convert RLE format of masks to .PNG.
* `info`: [[IN PROGRESS]] Print all info about dataset...
* `label`: [[IN PROGRESS]] Create labels for images.
* `map`: Apply csutom processing to all files in...
* `show`: Allow to show image inside terminal Original...
* `split`: Split images into follders according to...
* `tohd5`: Convert dataset into HDF5 format to speedup...
* `torle`: Convert images with masks to .csv filr with...
* `unpack`: Unpack any archive file into folder with the...
* `voc2coco`: Convert any dataset in PASCAL VOC format to...

## `distortme augs`

Apply provided augmentations to all images in imdir and copy them to 
different folders with name corresponded to augmentation.

Possible augmentations:

[rotate|shift_scale_rotate|shift_hsv|equalize|resize512|resize300|resize256|resize224|to_gray|
crop|contrast|bright]


--imdir Directory with images to process

--aug   Augmentation to apply. You may specify as mach augmentations as you want. 

**Usage**:

```console
$ distortme augs [OPTIONS]
```

**Options**:

* `--imdir PATH`
* `--aug [rotate|shift_scale_rotate|shift_hsv|equalize|to_gray|resize512|resize300|resize256|resize224|contrast|crop|bright]`
* `--help`: Show this message and exit.

## `distortme coco2voc`

[[IN PROGRESS]]

Convert any dataset in COCO format ot PASCAL VOC format.

Original implementation at https://gist.github.com/jinyu121/a222492405890ce912e95d8fb5367977 

--anns   Path to COCO annotation .json file

--dstdir Directory to save results

**Usage**:

```console
$ distortme coco2voc [OPTIONS]
```

**Options**:

* `--anns PATH`
* `--dstdir TEXT`
* `--help`: Show this message and exit.

## `distortme convert`

Convert images to certain extension as .jpg .png etc.


--imdir Directory with images to process

--orig  Formats of files that will be concerted

--to    Target format

**Usage**:

```console
$ distortme convert [OPTIONS]
```

**Options**:

* `--imdir PATH`
* `--orig TEXT`
* `--to TEXT`
* `--help`: Show this message and exit.

## `distortme download`

Asynchronously download packed datasets in original format


--dataset Dataset name from available variants

--to      Folder to save datasets

**Usage**:

```console
$ distortme download [OPTIONS]
```

**Options**:

* `--dataset [MNIST|CIFAR10|CIFAR100|COCO|PASCAL_VOC2012|STL10|SVHN|PHOTOTOUR|SBD|USPS|HMDB51]`
* `--to PATH`
* `--help`: Show this message and exit.

## `distortme fromhd5`

Extract files from HDF5 dataset.

--file HDF5 file to extract

**Usage**:

```console
$ distortme fromhd5 [OPTIONS]
```

**Options**:

* `--file PATH`
* `--help`: Show this message and exit.

## `distortme fromrle`

Convert RLE format of masks to .PNG. 

--file    File with RLE labels

--colrle  Column in dataframe with rles

--colsize Column in dataframe with size for each mask

--colimg  Column in dataframe with name of corresponding image

**Usage**:

```console
$ distortme fromrle [OPTIONS]
```

**Options**:

* `--file PATH`
* `--colrle TEXT`
* `--colsize TEXT`
* `--colimg TEXT`
* `--help`: Show this message and exit.

## `distortme info`

[[IN PROGRESS]]

Print all info about dataset in console

**Usage**:

```console
$ distortme info [OPTIONS]
```

**Options**:

* `--imdir PATH`
* `--file PATH`
* `--help`: Show this message and exit.

## `distortme label`

[[IN PROGRESS]]

Create labels for images.

--imdir Directory with images to process.

--bs    Batch size

--task  Classify all images according to IMAGENET dataset or

        Detect all faces and store boxes at normalized {xmin, ymin, xmax, ymax} format or

        Detect all boxes and scores according to COCO dataset.

--out   Json file with results for each task

**Usage**:

```console
$ distortme label [OPTIONS]
```

**Options**:

* `--imdir PATH`
* `--task [faces|objects|classes|masks]`
* `--bs INTEGER`
* `--out PATH`
* `--help`: Show this message and exit.

## `distortme map`

Apply csutom processing to all files in folder

--imdir  Path to folder with files to process

--fun    Path to script.py file with function 'process' with only one argument

--resdir Path to dir with modified images

**Usage**:

```console
$ distortme map [OPTIONS]
```

**Options**:

* `--imdir PATH`
* `--fun PATH`
* `--resdir PATH`
* `--help`: Show this message and exit.

## `distortme show`

Allow to show image inside terminal
Original implementation at https://github.com/nikhilkumarsingh/terminal-image-viewer
--impath Path to image

--height Number of terminal rows used to show image

**Usage**:

```console
$ distortme show [OPTIONS]
```

**Options**:

* `--impath PATH`
* `--height INTEGER`
* `--help`: Show this message and exit.

## `distortme split`

Split images into follders according to provided descriptor in file name.

--imdir Directory with files (e.g. images) to process

--desc  Descriptor of each class in file name

--copy  Copy files if enabled. Else move them to corresponding folder.

**Usage**:

```console
$ distortme split [OPTIONS]
```

**Options**:

* `--imdir PATH`
* `--desc TEXT`
* `--copy / --no-copy`
* `--help`: Show this message and exit.

## `distortme tohd5`

Convert dataset into HDF5 format to speedup data loading.

--imdir Directory with images to convert

**Usage**:

```console
$ distortme tohd5 [OPTIONS]
```

**Options**:

* `--imdir PATH`
* `--labels TEXT`
* `--help`: Show this message and exit.

## `distortme torle`

Convert images with masks to .csv filr with RLE labels.

--imdir Directory with images to convert.

**Usage**:

```console
$ distortme torle [OPTIONS]
```

**Options**:

* `--imdir PATH`
* `--help`: Show this message and exit.

## `distortme unpack`

Unpack any archive file into folder with the name of archive.

--file Path to archive to unpack

**Usage**:

```console
$ distortme unpack [OPTIONS]
```

**Options**:

* `--file PATH`
* `--help`: Show this message and exit.

## `distortme voc2coco`

Convert any dataset in PASCAL VOC format to COCO format.

Original implementation at https://github.com/yukkyo/voc2coco 

--anndir Directory with PASCAL VOC annotations im .xml format

--annids Path to file with annotations list in annotations/ids/

--labels Path to labels e.g labels.txt

--output Name for annotations.json result file

**Usage**:

```console
$ distortme voc2coco [OPTIONS]
```

**Options**:

* `--anndir PATH`
* `--annids PATH`
* `--labels PATH`
* `--output PATH`
* `--help`: Show this message and exit.
