import os
import cv2
import h5py
import typer
import numpy as np
import pandas as pd
import multiprocessing as mp
from typing import Sequence, Tuple

from distortme.base_types import Labels, Image
from distortme.files_utils import images, create_folders
from distortme.main_utils import print_delimiter


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
                    name=f"data_{img_name}",
                    data=img,
                    shape=(img.shape[0], img.shape[1], img.shape[2]),
                    maxshape=(img.shape[0], img.shape[1], img.shape[2]),
                    compression='gzip',
                    compression_opts=9
                )
        else:
            for img_name, img, label in zip(img_names, img_data, labels):
                compressed_data = hf.create_dataset(
                    name=f"data_{img_name}",
                    data=img,
                    shape=(img.shape[0], img.shape[1], img.shape[2]),
                    maxshape=(img.shape[0], img.shape[1], img.shape[2]),
                    compression='gzip',
                    compression_opts=9
                )
                compressed_labels = hf.create_dataset(
                    name=f"label_{img_name.split('.')[0]}",
                    data=label,
                    shape=(1, ),
                    maxshape=(None, ),
                    compression='gzip',
                    compression_opts=9
                )


def extract_from_hdf5(path: str) -> None:
    filename = os.path.basename(path)
    with h5py.File(path, 'r') as hf:
        all_instances = tuple(hf.keys())
        labels = tuple(filter(lambda x: x.split('_')[0] == 'label', all_instances))
        data = tuple(filter(lambda x: x.split('_')[0] == 'data', all_instances))
        create_folders((f'data_{filename.replace(".", "_")}', f'labels_{filename.replace(".", "_")}'))
        for image in data:
            cv2.imwrite(os.path.join(f'data_{filename.replace(".", "_")}', f'{image}'), np.array(hf[image]))

        if len(labels) == 0:
            return

        with open(f'labels_{filename.replace(".", "_")}/labels.txt', 'w') as labels_file:
            for label in labels:
                labels_file.write(f'{label}: {str(np.array(hf[label]))}')
                labels_file.write('\n')


@print_delimiter("Create HDF5 dataset from images...")
def main_save_to_hdf5(imdir: str, labels: str) -> None:
    img_names = images(imdir)
    img_locations = tuple(os.path.join(imdir, img_name) for img_name in img_names)
    img_data = load_images(img_locations)
    if labels is not None:
        try:
            labels_file = load_labels(labels)
        except NotImplementedError:
            labels_file = None
            typer.echo("Labels cant be loaded only from .CSV, .TXT or .NPY files\n")
    else:
        labels_file = None
    save_to_hdf5(imdir, img_names, img_data, labels_file)


@print_delimiter("Extract images from HDF5 dataset...")
def main_extract_from_hdf5(files: Sequence[str]):
    for filename in files:
        extract_from_hdf5(filename)
