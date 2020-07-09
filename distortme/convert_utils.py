import os
import cv2
import multiprocessing as mp
from typing import List, Sequence
from tqdm.contrib.concurrent import process_map

from distortme.files_utils import images
from distortme.main_utils import print_delimiter


def convert(imdir: str, orig_ext: Sequence[str], target_ext: str) -> None:

    if not target_ext.startswith('.'):
        target_ext = "." + target_ext

    if len(orig_ext) == 0:
        original_images = images(imdir)
    else:
        original_images = images(imdir, tuple(orig_ext))

    new_images = (img_name.replace(os.path.splitext(img_name)[1], target_ext)
                  for img_name in original_images)
    image_locations = tuple(os.path.join(imdir, img)
                            for img in original_images)
    orig_locations = tuple(os.path.join(imdir, img)
                           for img in original_images)
    new_locations = tuple(os.path.join(imdir, img)
                          for img in new_images)

    if len(image_locations) < 2:
        image_data = tuple(cv2.imread(img) for img in image_locations)
    else:
        image_data = process_map(cv2.imread, image_locations,
                                 max_workers=mp.cpu_count(), ncols=80)

    for orig_loc in orig_locations:
        os.remove(orig_loc)  # TODO : process with MP

    for orig_data, new_loc in zip(image_data, new_locations):
        cv2.imwrite(new_loc, orig_data)  # TODO : process with MP



@print_delimiter("Converting files...")
def main_convert(imdir: str, orig: List[str], to: str) -> None:
    convert(imdir, orig, to)
