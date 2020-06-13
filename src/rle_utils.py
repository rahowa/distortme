import os
from typing import Any, Sequence, Tuple, Callable

import cv2
import numpy as np
import pandas as pd
import multiprocessing as mp

from src.base_types import Image
from src.files_utils import images
from src.main_utils import print_delimiter


def rle2mask(mask_and_shape: Tuple[str, Image]) -> Image:
    mask_rle, shape = *mask_and_shape
    if mask_rle != mask_rle:
        return np.zeros_like(shape)

    s = mask_rle.split()
    starts, lengths = [np.asarray(x, dtype=int)
                       for x in (s[0:][::2], s[1:][::2])]
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


def save_mask(image_data: Tuple[str, Image]) -> None:
    cv2.imwrite(image_data[0], image_data[1])


def proces_async(data: Sequence[Any],
                 function: Callable[[Tuple[Any, ...]], Any]) -> Tuple[Any, ...]:
    if len(data) < 100:
        return tuple(function(data_sample) for data_sample in data)

    pool = mp.Pool(mp.cpu_count())
    return tuple(pool.map(function, data))


@print_delimiter("Convert masks to rle's...")
def main_torle(imdir: str) -> None:
    img_names = images(imdir)
    img_locations = (os.path.join(imdir, img) for img in img_names)
    img_data = tuple(cv2.imread(img) for img in img_locations)
    img_sizes = (img.shape[:2] for img in img_data)
    rles = proces_async(img_data, mask2rle)
    rle_result = pd.DataFrame(tuple(zip(img_names, rles, img_sizes)),
                              columns=["image_name", 'rle', 'size'])
    rle_result.to_csv(f"rle_of_{imdir}.csv", index=False)


@print_delimiter("Convert rle's to masks...")
def main_frommrle(filename: str,
                  rle_column: str,
                  size_column: str,
                  name_column: str) -> None:
    data = pd.read_csv(filename)
    rles = data[rle_column].value.tolist()
    shapes = data[size_column].value.tolist()
    images_names = data[name_column].value.tolist()
    rle_and_shapes = tuple((rle, shape) for rle, shape in zip(rles, shapes))
    images = proces_async(rle_and_shapes, rle2mask)
    proces_async(zip(images_names, images), save_mask)
