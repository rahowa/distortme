import sys
import typer
from typing import List
from colorama import init

sys.path.append("../")

from src.aug_utils import main_apply_augmentations, SlowAugs
from src.split_utils import main_split_files, main_show_hist
from src.hdf5_utils import main_save_to_hdf5, main_extract_from_hdf5
from src.rle_utils import main_torle
app = typer.Typer()
init()

@app.command()
def augs(imdir: str = None, aug: List[SlowAugs] = None) -> None:
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
        main_apply_augmentations(imdir, aug)


@app.command()
def split(imdir: str = None, desc: List[str] = None, copy: bool = typer.Option(True)) -> None:
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
        main_split_files(imdir, desc, copy)
        main_show_hist(imdir, desc)


@app.command()
def tohd5(imdir: str = None, labels: str = typer.Option(None)) -> None:
    """
    Convert dataset into HDF5 format to speedup data loading.\n
    --imdir Directory with images to convert
    """
    if not imdir:
        typer.echo("Provide imdir to folder with images: --imdir /path/to/images")
        typer.Exit()
    else:
        main_save_to_hdf5(imdir, labels)


@app.command()
def fromhd5(file: List[str] = None) -> None:
    """
    Extract files from HDF5 dataset.\n
    --file HDF5 file to extract
    """
    if not file:
        typer.echo("Provide at least one .h5 file")
        exit()
    else:
        main_extract_from_hdf5(file)


@app.command()
def torle(imdir: str = typer.Option(None)) -> None:
    """
    Convert images with masks to .csv filr with RLE labels.\n
    --imdir Directory with images to convert.\n
    """
    if not imdir:
        typer.echo("Provide imdir to folder with images: --imdir /path/to/images")
        exit()
    else:
        main_torle(imdir)


@app.command()
def fromrle(file: List[str] = None) -> None:
    """
    Convert RLE format of masks to .PNG\n
    --file File with RLE labels
    """
    pass 


@app.command()
def label(imdir: str,
          classes: bool = typer.Option(bool),
          faces: bool = typer.Option(False),
          boxes: bool = typer.Option(False)) -> None:
    """
    Create labels for images.\n
    --imdir   Directory with images to process.\n
    --classes Classify all images according to IMAGENET dataset.\n
    --faces   Detect all faces and store boxes at normalized {xmin, ymin, xmax, ymax} format.\n
    --boxes   Detect all boxes and scores according to COCO dataset.\n
    """
    pass 


if __name__ == "__main__":
    app()
