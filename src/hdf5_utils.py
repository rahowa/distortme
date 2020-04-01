import os
import typer
import h5py
import pandas as pd
import numpy as np
from typing import List, Tuple
import multiprocessing as mp
import cv2

from src.base_types import Labels, Image
from src.files_utils import  images

def read_labels_npy(path: str) -> Labels:
    return np.load(path).reshape(-1, 1)


def read_labels_txt(path: str) -> Labels:
    return np.asanyarray(np.loadtxt(path)).reshape(-1, 1)


def read_labels_csv(path: str) -> Labels:
    return pd.read_csv(path).values.reshape(-1, 1)


def load_images(img_locations: Tuple[str, ...]) -> Tuple[Image, ...]:
    pool = mp.Pool(mp.cpu_count())
    return tuple(pool.map(cv2.imread, img_locations))


def load_labels(path: str) -> Labels:
    filename = os.path.basename(path)
    if filename.endswith('.csv'):
        return read_labels_csv(path)
    elif filename.endswith('.txt'):
        return read_labels_txt(path)
    elif filename.endswith('.npy'):
        return read_labels_npy(path)
    else:
        raise NotImplementedError


def save_to_hdf5(result_name: str,
                 img_names: Tuple[str, ...],
                 img_data: Tuple[Image, ...],
                 labels: Labels = None) -> None:
    with h5py.File(f'{result_name}.h5', 'w') as hf:
        if labels is None:
            for img_name, img in zip(img_names, img_data):
                compressed_data = hf.create_dataset(
                    name=f"data_{img_name.split('.')[0]}",
                    data=img,
                    shape=(img.shape[0], img.shape[1], img.shape[2]),
                    maxshape=(img.shape[0], img.shape[1], img.shape[2]),
                    compression='gzip',
                    compression_opts=9
                )
        else:
            for img_name, img, label in zip(img_names, img_data, labels):
                compressed_data = hf.create_dataset(
                    name=f"data_{img_name.split('.')[0]}",
                    data=img,
                    shape=(img.shape[0], img.shape[1], img.shape[2]),
                    maxshape=(img.shape[0], img.shape[1], img.shape[2]),
                    compression='gzip',
                    compression_opts=9
                )
                compressed_labels = hf.create_dataset(
                    name=f"label_{img_name}",
                    data=label,
                    shape=(1, ),
                    maxshape=(None, ),
                    compressin='gzip',
                    compression_opts=9
                )


def extract_from_hdft(path: str) -> None:
    with h5py.File(path, 'r') as hf:



def main_save_to_hdf5(imdir: str, labels: str = None) -> None:
    img_names = images(imdir)
    img_locations = tuple(os.path.join(imdir, img_name) for img_name in img_names)
    img_data = load_images(img_locations)
    if labels is not None:
        try:
            labels_file = load_labels(labels)
        except NotImplementedError:
            typer.echo("Labels cant be loaded only from .CSV, .TXT or .NPY files\n")
    else:
        labels_file = None
    save_to_hdf5(imdir, img_names, img_data, labels_file)
