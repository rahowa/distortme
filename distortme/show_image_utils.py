import sys
import cv2
import typer
import numpy as np
from PIL import Image

from distortme.main_utils import print_delimiter


def get_ansi_color_code(r: int, g: int, b: int) -> int:
    if r == g and g == b:
        if r < 8:
            return 16
        if r > 248:
            return 231
        return round(((r - 8) / 247) * 24) + 232
    return 16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5)


def get_color(r: int, g: int, b: int) -> str:
    return "\x1b[48;5;{}m \x1b[0m".format(int(get_ansi_color_code(r, g, b)))


def show_image(img_path: str, height: int) -> None:
    try:
        img = Image.open(img_path)
    except FileNotFoundError:
        typer.echo("Image no found")
        typer.Exit()

    width = int((img.width / img.height) * height)

    img = img.resize((width, height), Image.ANTIALIAS)
    img_arr = np.asarray(img)

    if len(img_arr.shape) != 3:
        img_arr = cv2.cvtColor(img_arr, cv2.COLOR_GRAY2RGB)

    h, w, c = img_arr.shape

    for x in range(h):
        for y in range(w):
            pix = img_arr[x][y]
            print(get_color(pix[0], pix[1], pix[2]), sep='', end='')
        print()


@print_delimiter("Showing image")
def main_show_image(impath: str, height: int) -> None:
    show_image(impath, height)
