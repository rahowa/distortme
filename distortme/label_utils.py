import os
import cv2
import typer
from typing import List
from src.nn_algorithms.utils.net_context import NetworkContext
from src.nn_algorithms.utils.serialization import save_results
from src.files_utils import images
from src.nn_models import TASK_TO_MODEL, Models
from src.main_utils import print_delimiter


@print_delimiter("Creating labels for current dataset")
def main_labels(imdir: str, tasks: List[Models], batch_size: int, output: str) -> None:
    image_locations = tuple(os.path.join(imdir, img) for img in images(imdir))
    image_data = tuple(cv2.imread(image) for image in image_locations)  # TODO: use multiprocessing
    context = NetworkContext("".join(t.value for t in tasks))
    out_basename = os.path.basename(output).split('.')[0]
    for task in tasks:
        context.model = TASK_TO_MODEL[task.value](batch_size)
        typer.echo(context)
        result_filename = f"{out_basename}_{task.value}.json"
        save_path = os.path.join(os.path.dirname(output), result_filename)
        save_results(save_path,
                     image_locations,
                     context.predict(image_data))
