from importlib import import_module
import os
import importlib
from typing import Callable

from distortme.base_types import Image
from distortme.main_utils import print_delimiter


def apply_preprocessing(imdir: str,
                        functoin: Callable[[Image], None]) -> None:
    pass


@print_delimiter("Apply custom preprosessing...")
def main_custom_map(imdir: str, module: str) -> None:
    module_name = os.path.basename(module)
    module_location = os.path.dirname(module)
    custom_map_module = importlib.import_module(module_name, module_location)
    apply_preprocessing(imdir, custom_map_module.process)