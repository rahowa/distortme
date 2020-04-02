import numpy as np
from typing import Union, Tuple, List
from nptyping import Array
from albumentations import BasicIAATransform, BasicTransform

Image = Array[Union[np.uint8, np.float]]
ImageShape = Union[Tuple[int, int], Tuple[int, int, int]]
BaseAug = Union[BasicTransform, BasicIAATransform]
Labels = Array[int]
Box = Tuple[float, float, float, float, float]
Boxes = List[Box]
