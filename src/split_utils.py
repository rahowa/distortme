import os
import shutil
import multiprocessing as mp
from collections import defaultdict
from typing import List, Tuple, Dict

import termplotlib as tpl
from frozendict import frozendict

from src.files_utils import full_path, images, create_folders


class CopyTo:
    def __init__(self, path_to_save: str) -> None:
        self.path_to_save = path_to_save
    
    def __call__(self, file_to_copy: str) -> None:
        filename = os.path.basename(file_to_copy)
        shutil.copy(file_to_copy, os.path.join(self.path_to_save, filename))


class MoveTo:
    def __init__(self, path_to_save: str) -> None:
        self.path_to_save = path_to_save
    
    def __call__(self, file_to_copy: str) -> None:
        filename = os.path.basename(file_to_copy)
        shutil.move(file_to_copy, os.path.join(self.path_to_save, filename))
        

def copy_files_to_folders(files: List[str], path_to_save: str) -> None:
    if len(files) <= 100:
        for file in files:
            filename = os.path.basename(file)
            shutil.copy(file, os.path.join(path_to_save, filename))
    else:
        pool = mp.Pool(mp.cpu_count())
        copy_fn = CopyTo(path_to_save)
        pool.map(copy_fn, files)


def move_files_to_folders(files: List[str], path_to_save: str) -> None:
    if len(files) <= 100:
        for file in files:
            filename = file.split('/')[-1]
            shutil.move(file, os.path.join(path_to_save, filename))
    else:
        pool = mp.Pool(mp.cpu_count())
        copy_fn = MoveTo(path_to_save)
        pool.map(copy_fn, files)


def map_classes_to_files(files: Tuple[str, ...], descriptors: Tuple[str, ...], imdir: str) -> Dict[str, List[str]]:
    classes_to_files: Dict[str, List[str]] = defaultdict(list)
    for img in files:
        for current_desc in descriptors: 
            if img.find(current_desc) != -1:
                classes_to_files[current_desc].append(img)
    classes_to_files: Dict[str, List[str]] = {k: list(full_path(v, imdir)) for k, v in classes_to_files.items()}
    return frozendict(classes_to_files)


def main_split_files(imdir: str, descriptors: List[str], copy: bool = True) -> None:
    all_images = images(imdir)
    classes_folders = tuple(full_path(tuple(descriptors), imdir))
    create_folders(classes_folders)
    classes_to_files = map_classes_to_files(all_images, tuple(descriptors), imdir)
    if copy:
        for out_dir, cls_desc in zip(classes_folders, descriptors):
            copy_files_to_folders(classes_to_files[cls_desc], out_dir)
    else:
        for out_dir, cls_desc in zip(classes_folders, descriptors):
            move_files_to_folders(classes_to_files[cls_desc], out_dir)


def main_show_hist(imdir: str, descriptors: List[str]):
    folders_with_files = [os.path.join(imdir, desc) for desc in descriptors]
    num_files = tuple(len(os.listdir(files)) for files in folders_with_files)
    fig = tpl.figure()
    fig.barh(num_files, descriptors, force_ascii=False)
    fig.show()
