import os
import cv2
import typer
from tqdm import tqdm
import importlib.util
from tqdm.contrib.concurrent import process_map
from typing import Callable, Optional, Any, Sequence, Tuple

from distortme.base_types import Image
from distortme.main_utils import print_delimiter
from distortme.files_utils import images, create_folders


def apply_custom_map(images: Sequence[Image],
                     function: Callable[[Image], Image]) -> Tuple[Image, ...]:
    if len(images) < 100:
        modified_images = []
        for img in tqdm(images, ncols=80):
            modified_images.append(function(img))
        return tuple(modified_images)
    else:
        return tuple(process_map(function, images))


def load_custom_module(path_to_module: str) -> Optional[Any]:
    module_name = os.path.basename(path_to_module)
    module_location = os.path.abspath(path_to_module)
    module_spec = importlib.util.spec_from_file_location(
        module_name, module_location
    )
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


def save_result(resdir: str,
                img_names: Sequence[str],
                ready_images: Sequence[Image]) -> None:
    result_image_locations = tuple(os.path.join(resdir, img_name)
                                   for img_name in img_names)
    if len(ready_images) < 100:
        for res_path, img in tqdm(zip(result_image_locations, ready_images), ncols=80):
            cv2.imwrite(res_path, img)
    else:
        process_map(cv2.imwrite, result_image_locations, ready_images)


@print_delimiter("Apply custom preprosessing")
def main_custom_map(imdir: str, module_path: str, resdir: str) -> None:
    module = load_custom_module(module_path)
    if not module:
        typer.echo("Module not found")
        typer.echo("Please check path to your custom module")
        typer.Exit()

    create_folders((resdir, ))
    module = load_custom_module(module_path)
    img_names = tuple(images(imdir))
    img_locations = tuple(os.path.join(imdir, img) for img in img_names)
    loaded_images = tuple(cv2.imread(img) for img in img_locations)
    modified_images = apply_custom_map(loaded_images, module.map_fn)
    save_result(resdir, img_names, modified_images)
