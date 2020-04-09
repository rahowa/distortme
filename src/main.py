import sys
import typer
import asyncio
from typing import List, Tuple
from pathlib import Path
from colorama import init

sys.path.append("../")

from src.datasets import Datasets
from src.aug_utils import main_apply_augmentations, SlowAugs
from src.split_utils import main_split_files, main_show_hist
from src.hdf5_utils import main_save_to_hdf5, main_extract_from_hdf5
from src.rle_utils import main_torle, main_frommrle
from src.main_utils import not_implemented
from src.datasets_download_utils import main_download
from src.unpack_utils import main_unpack

app = typer.Typer()
init()


@app.callback()
def callback() -> None:
    """
    CLI utility for augmentation and preprocessing images.

    Possible operations are given below under 'Commands: '

    """

@app.command()
def augs(imdir: Path = None, aug: List[SlowAugs] = None) -> None:
    """
    Apply provided augmentations to all images in imdir and copy them to 
    different folders with name corresponded to augmentation.\n
    Possible augmentations:\n 
    [rotate|shift_scale_rotate|shift_hsv|equalize|resize512|resize300|resize256|resize224|to_gray|
    crop|contrast|bright]

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
        exit()
    else:
        main_extract_from_hdf5(tuple(map(lambda x: str(x), file)))


@app.command()
def torle(imdir: Path = typer.Option(None)) -> None:
    """
    Convert images with masks to .csv filr with RLE labels.\n
    --imdir Directory with images to convert.\n
    """

    if not imdir:
        typer.echo("Provide imdir to folder with images: --imdir /path/to/images")
        exit()
    else:
        main_torle(str(imdir))


@app.command()
@not_implemented
def fromrle(file: Path = None,
            size: Tuple[int, int] = typer.Option(None),
            imdir: Path = typer.Option(None),
            colimg: str = typer.Option("image"),
            colsize: str = typer.Option("size")) -> None:
    """
    [[NOT IMPLEMENTED]]\n
    Convert RLE format of masks to .PNG\n
    --file    File with RLE labels
    --size    One size for all mask in file. If size is unknown, provide 'imdir' and 'colimg'
    --imdir   Directory with images. Provide if size is unknown or column with sizes is dropped
    --colimg  Column in dataframe with name of corresponding image
    --colsize Column in dataframe with size for each mask
    """

    pass


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
def unpack(file: List[Path] = None) -> None:
    """
    Unpack any archive file into folder with the name of archive.
    --file Path to archive to unpack
    """

    if not file:
        typer.echo("Provide file to unpack:  --file /path/to/archive")
        typer.Exit()
    else:
        main_unpack(tuple(str(file_path) for file_path in file))


@app.command()
@not_implemented
def ext() -> None:
    """
    [[NOT IMPLEMENTED]]\n
    Convert images to certain extension as .jpg .png etc.
    :return:
    """
    pass


@app.command()
@not_implemented
def label(imdir: Path = None,
          classes: bool = typer.Option(bool),
          faces: bool = typer.Option(False),
          boxes: bool = typer.Option(False)) -> None:
    """
    [[NOT IMPLEMENTED]]\n
    Create labels for images.\n
    --imdir   Directory with images to process.\n
    --classes Classify all images according to IMAGENET dataset.\n
    --faces   Detect all faces and store boxes at normalized {xmin, ymin, xmax, ymax} format.\n
    --boxes   Detect all boxes and scores according to COCO dataset.\n
    """
    pass


@app.command()
@not_implemented
def info(imdir: Path = typer.Option(Path), file: Path = typer.Option(Path)) -> None:
    """
    [[NOT IMPLEMENTED]]\n
    Print all info about dataset in console
    """
    pass


@app.command()
@not_implemented
def voc2coco() -> None:
    """
    [[NOT IMPLEMENTED]]\n
    Convert any dataset in PASCAL VOC format to COCO format.
    :return:
    """
    pass


@app.command()
@not_implemented
def coco2voc() -> None:
    """
    [[NOT IMPLEMENTED]]\n
    Convert any dataset in COCO format ot PASCAL VOC format.
    """
    pass


if __name__ == "__main__":
    app()
