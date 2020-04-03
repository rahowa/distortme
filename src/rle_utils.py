import os
from typing import Sequence, Tuple

import cv2
import numpy as np
import pandas as pd
import multiprocessing as mp

from src.base_types import Image, ImageShape
from src.files_utils import images
from src.main_utils import print_delimiter


def rle2mask(mask_rle: str, shape: ImageShape) -> Image:
    if mask_rle != mask_rle:
        return np.zeros_like(shape)

    s = mask_rle.split()
    starts, lengths = [np.asarray(x, dtype=int) for x in (s[0:][::2], s[1:][::2])]
    starts -= 1
    ends = starts + lengths
    img = np.zeros(shape[0]*shape[1], dtype=np.uint8)
    for lo, hi in zip(starts, ends):
        img[lo:hi] = 1
    return img.reshape(shape).T


def mask2rle(image: Image) -> str:
    image = image.T > 0.5
    pixels = image.flatten()
    pixels = np.concatenate([[0], pixels, [0]])
    runs = np.where(pixels[1:] != pixels[:-1])[0] + 1
    runs[1::2] -= runs[::2]
    return ' '.join(str(x) for x in runs)


def convert_to_rle(img_data: Sequence[Image]) -> Tuple[str, ...]:
    if len(img_data) < 100:
        return tuple(mask2rle(img) for img in img_data)

    pool = mp.Pool(mp.cpu_count())
    return tuple(pool.map(mask2rle, img_data))


@print_delimiter("Convert masks to rle...")
def main_torle(imdir: str) -> None:
    img_names = images(imdir)
    img_locations = (os.path.join(imdir, img) for img in img_names)
    img_data = tuple(cv2.imread(img) for img in img_locations)
    img_sizes = (img.shape[:2] for img in img_data)
    rles = convert_to_rle(img_data)
    rle_result = pd.DataFrame(tuple(zip(img_names, rles, img_sizes)), columns=["image", 'rle', 'shape'])
    rle_result.to_csv(f"rle_of_{imdir}.csv", index=False)


@print_delimiter
def main_frommrle(filename: str) -> None:
    pass
