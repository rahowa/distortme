import numpy as np
from typing import Union
from nptyping import Array
from albumentations import BasicIAATransform, BasicTransform

Image = Array[np.uint8]
BaseAug = Union[BasicTransform, BasicIAATransform]