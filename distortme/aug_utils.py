import os
import cv2
from tqdm import tqdm
import multiprocessing as mp
from typing import Sequence, List


from distortme.base_types import Image, BaseAug
from distortme.augmentations import SLOW_AUGS_DICT, SlowAugs
from distortme.files_utils import create_folders, full_path, images
from distortme.main_utils import print_delimiter


class ApplyAugmentation:
    def __init__(self, output_folder: str, aug: BaseAug) -> None:
        self.aug = aug
        self.output_folder = output_folder

    def _apply_aug(self, image: Image, current_aug: BaseAug) -> Image:
        return current_aug(image=image)["image"]

    def _save_image(self, image: Image, path: str) -> None:
        cv2.imwrite(path, image)

    def __call__(self, img_path: str) -> None:
        img_name = img_path.split('/')[-1]
        self._save_image(self._apply_aug(cv2.imread(img_path), self.aug),
                         os.path.join(self.output_folder, img_name))


def augment_all_images(images: Sequence[str], output_folder: str, aug: BaseAug) -> None:
    process_one_image = ApplyAugmentation(output_folder, aug)
    pool = mp.Pool(mp.cpu_count())
    pool.map(process_one_image, images)


@print_delimiter("Applying augmentations to images")
def main_apply_augmentations(imdir: str, augs: List[SlowAugs]) -> None:
    all_images = tuple(map(lambda x: os.path.join(imdir, x), images(imdir)))
    used_augs = tuple(SLOW_AUGS_DICT[aug.value] for aug in augs)
    aug_folders = tuple(full_path(tuple(aug.value for aug in augs), imdir))
    create_folders(aug_folders)
    pbar = tqdm(zip(aug_folders, used_augs, augs), ncols=80)
    for out_dir, out_aug, aug_name in pbar:
        augment_all_images(all_images, out_dir, out_aug)
        pbar.set_description(f"Augmetation: [{aug_name}]")
