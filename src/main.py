import typer 
from typing import List
from colorama import init

from src.aug_utils import main_apply_augmentations, SlowAugs
from src.split_utils import main_split_files, main_show_hist

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
        exit()
    if not aug:
        typer.echo("Provide augmentations: --aug reisze224 --aug rotate etc.")
        exit()
    else:
        typer.echo("="*80)
        typer.echo("Porocess images: ... \n")
        main_apply_augmentations(imdir, aug)
        typer.echo("DONE!\n")
        typer.echo("="*80)


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
        exit()
    if not desc:
        typer.echo("Provide descriptor of class in file name:  IMG001_cls_0.jpg -> --desc cls_0.")
        exit()
    else:
        main_split_files(imdir, desc, copy)
        typer.echo("="*80)
        typer.echo("Historgramm of classes:\n")
        main_show_hist(imdir, desc)
        typer.echo("="*80)


@app.command()
def tohd5() -> None:
    pass 

@app.command()
def fromhd5() -> None:
    pass 

@app.command()
def torle() -> None:
    pass

@app.command()
def fromrle() -> None:
    pass 

if __name__ == "__main__":
    app()