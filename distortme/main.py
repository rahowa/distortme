import typer
import asyncio
import colorama
from typing import List
from pathlib import Path
from distortme.nn_models import Models
from distortme.datasets import Datasets
from distortme.label_utils import main_labels
from distortme.unpack_utils import main_unpack
from distortme.convert_utils import main_convert
from distortme.main_utils import not_implemented
from distortme.voc2coco_utils import main_voc2coco
from distortme.coco2voc_utils import main_coco2voc
from distortme.cusom_map_utils import main_custom_map
from distortme.show_image_utils import main_show_image
from distortme.rle_utils import main_torle, main_frommrle
from distortme.datasets_download_utils import main_download
from distortme.aug_utils import main_apply_augmentations, SlowAugs
from distortme.split_utils import main_split_files, main_show_hist
from distortme.hdf5_utils import main_save_to_hdf5, main_extract_from_hdf5

app = typer.Typer()
colorama.init()


@app.callback()
def callback() -> None:
    """
    CLI utility for augmentation and preprocessing images.

    Possible operations are given below under 'Commands: '

    To get more info type 'distortme <command> --help'
    """


@app.command()
def augs(imdir: Path = None, aug: List[SlowAugs] = None) -> None:
    """
    Apply provided augmentations to all images in imdir and copy them to 
    different folders with name corresponded to augmentation.\n
    Possible augmentations:\n 
    [rotate|shift_scale_rotate|shift_hsv|equalize|resize512|resize300|resize256|resize224|to_gray|
    crop|contrast|bright]\n

    --imdir Directory with images to process\n
    --aug   Augmentation to apply. You may specify as mach augmentations as you want. 
    """

    if not imdir:
        typer.echo("Provide path to folder with images: --imdir path/to/folder")
        typer.Exit()
    if not aug:
        typer.echo("Provide augmentations: --aug reisze224 --aug rotate etc.")
        typer.Exit()
    else:
        main_apply_augmentations(str(imdir), aug)


@app.command()
def split(imdir: Path = None, desc: List[str] = None, copy: bool = typer.Option(True)) -> None:
    """
    Split images into follders according to provided descriptor in file name.\n
    --imdir Directory with files (e.g. images) to process\n
    --desc  Descriptor of each class in file name\n
    --copy  Copy files if enabled. Else move them to corresponding folder.
    """

    if not imdir:
        typer.echo("Provide path to folder with files: --imdir path/to/folder")
        typer.Exit()
    if not desc:
        typer.echo("Provide descriptor of class in file name:  IMG001_cls_0.jpg -> --desc cls_0.")
        typer.Exit()
    else:
        main_split_files(str(imdir), desc, copy)
        main_show_hist(str(imdir), desc)


@app.command()
def tohd5(imdir: Path = None, labels: str = typer.Option(None)) -> None:
    """
    Convert dataset into HDF5 format to speedup data loading.\n
    --imdir Directory with images to convert
    """

    if not imdir:
        typer.echo("Provide imdir to folder with images: --imdir /path/to/images")
        typer.Exit()
    else:
        main_save_to_hdf5(str(imdir), labels)


@app.command()
def fromhd5(file: List[Path] = None) -> None:
    """
    Extract files from HDF5 dataset.\n
    --file HDF5 file to extract
    """

    if not file:
        typer.echo("Provide at least one .h5 file")
        typer.Exit()
    else:
        main_extract_from_hdf5(tuple(map(lambda x: str(x), file)))


@app.command()
def download(dataset: List[Datasets] = None, to: Path = typer.Option(None)) -> None:
    """
    Asynchronously download packed datasets in original format\n

    --dataset Dataset name from available variants\n
    --to      Folder to save datasets\n
    """

    if not dataset:
        typer.echo("Provide name of dataset like --dataset MNIST to download PACKED (archived) data")
        typer.Exit()
    else:
        asyncio.run(main_download(dataset, str(to)))


@app.command()
def torle(imdir: Path = typer.Option(None)) -> None:
    """
    Convert images with masks to .csv filr with RLE labels.\n
    --imdir Directory with images to convert.\n
    """

    if not imdir:
        typer.echo("Provide imdir to folder with images: --imdir /path/to/images")
        typer.Exit()
    else:
        main_torle(str(imdir))


@app.command()
def fromrle(file: Path = None,
            colrle: str = typer.Option("rle"),
            colsize: str = typer.Option("size"),
            colimg: str = typer.Option("image_name")) -> None:
    """
    Convert RLE format of masks to .PNG. \n
    --file    File with RLE labels\n
    --colrle  Column in dataframe with rles\n
    --colsize Column in dataframe with size for each mask\n
    --colimg  Column in dataframe with name of corresponding image\n
    """

    if not file:
        typer.echo("Provide path to .csv file with encoded masks")
        typer.Exit()
    else:
        main_frommrle(str(file), colrle, colsize, colimg)


@app.command()
def unpack(file: List[Path] = None) -> None:
    """
    Unpack any archive file into folder with the name of archive.\n
    --file Path to archive to unpack\n
    """

    if not file:
        typer.echo("Provide file to unpack:  --file /path/to/archive")
        typer.Exit()
    else:
        main_unpack(tuple(str(file_path) for file_path in file))


@app.command()
def convert(imdir: Path = None,
            orig: List[str] = typer.Option(None),
            to: str = None) -> None:
    """
    Convert images to certain extension as .jpg .png etc.\n

    --imdir Directory with images to process\n
    --orig  Formats of files that will be concerted\n
    --to    Target format\n
    """
    if not imdir:
        typer.echo("Provide imdir to folder with images: --imdir /path/to/images")
        typer.Exit()
    if not to:
        typer.echo("Provide target format of images: img.orig -> img.to")
        typer.Exit()
    else:
        main_convert(str(imdir), orig, to)


@app.command()
@not_implemented
def label(imdir: Path = None,
          task: List[Models] = None,
          bs: int = typer.Option(4),
          out: Path = typer.Option("result.json")) -> None:
    """
    [[IN PROGRESS]]\n
    Create labels for images.\n

    Original implementations:
        * Face detection: https://github.com/hollance/BlazeFace-PyTorch
    --imdir Directory with images to process.\n
    --bs    Batch size\n
    --task  Classify all images according to IMAGENET dataset or\n
            Detect all faces and store boxes at normalized {xmin, ymin, xmax, ymax} format or\n
            Detect all boxes and scores according to COCO dataset.\n
    --out   Json file with results for each task
    """

    if not imdir:
        typer.echo("Provide imdir to folder with images: --imdir /path/to/images")
        typer.Exit()
    else:
        main_labels(str(imdir), task, bs, str(out))


@app.command()
@not_implemented
def info(imdir: Path = typer.Option(Path),
         file: Path = typer.Option(Path)) -> None:
    """
    [[IN PROGRESS]]\n
    Print all info about dataset in console
    """
    if (not imdir) and (not file):
        typer.echo("Provide imdir or path to .csv file with data to get dataset info")
        typer.Exit()

@app.command()
def voc2coco(anndir: Path = None,
             annids: Path = None,
             labels: Path = None,
             output: Path = typer.Option(Path)) -> None:
    """
    Convert any dataset in PASCAL VOC format to COCO format.\n
    Original implementation at https://github.com/yukkyo/voc2coco \n
    --anndir Directory with PASCAL VOC annotations im .xml format\n
    --annids Path to file with annotations list in annotations/ids/\n
    --labels Path to labels e.g labels.txt\n
    --output Name for annotations.json result file
    """

    if not anndir:
        typer.echo("Provide path to directory with annottaions like /path/to/annotation/dir")
        typer.Exit()
    if not annids:
        typer.echo("Provide path to file with ids like /path/to/annotations/ids/list.txt")
        typer.Exit()
    if not labels:
        typer.echo("Provide path to file with labels like /path/to/labels.txt")
        typer.Exit()
    else:
        main_voc2coco(str(anndir),
                      str(annids),
                      str(labels),
                      str(output) if output is not None else None)


@app.command()
def coco2voc(anns: Path = None, dstdir = typer.Option(None)) -> None:
    """
    [[IN PROGRESS]]\n
    Convert any dataset in COCO format ot PASCAL VOC format.\n
    Original implementation at https://gist.github.com/jinyu121/a222492405890ce912e95d8fb5367977 \n
    --anns   Path to COCO annotation .json file\n
    --dstdir Directory to save results\n
    """
    if not anns:
        typer.echo("Provide path to COCO annotation .json file")
        typer.Exit()
    else:
        main_coco2voc(str(anns), 
                      str(dstdir) if dstdir is not None else None)


@app.command()
def map(imdir: Path = None, fun: Path = None, resdir: Path = None) -> None:
    """
    Apply csutom processing to all files in folder\n
    --imdir  Path to folder with files to process\n
    --fun    Path to script.py file with function 'process' with only one argument\n
    --resdir Path to dir with modified images\n
    """

    if not imdir:
        typer.echo("Provide path to directory with images to apply map function")
        typer.Exit()
    if not fun:
        typer.echo("Provide path to .py file with your own custom map")
        typer.Exit()
    if not resdir:
        typer.echo("Provide path to result directory")
    else:
        main_custom_map(str(imdir), str(fun), str(resdir))


@app.command()
def show(impath: Path = None, height: int = typer.Option(35)) -> None:
    """
    Allow to show image inside terminal
    Original implementation at https://github.com/nikhilkumarsingh/terminal-image-viewer
    --impath Path to image\n
    --height Number of terminal rows used to show image\n
    """

    if not impath:
        typer.echo("Provide path to image to show")
        typer.Exit()
    else:
        main_show_image(str(impath), height)
