from enum import Enum
from frozendict import frozendict
from albumentations import (Rotate, ShiftScaleRotate, RandomContrast,
                            HueSaturationValue, Equalize, RandomCrop,
                            Resize, RandomBrightness, ToGray)

class SlowAugs(str, Enum):
    rotate = "rotate"
    shift_scale_rotate = "shift_scale_rotate"
    shift_hsv = "shift_hsv"
    equalize = "equalize"
    to_gray =  "to_gray"
    resize512 = "resize512"
    resize300 = "resize300"
    resize256 = "resize256"
    resize224 = "resize224"
    contrast = "contrast"
    crop = "crop",
    bright = "bright"

SLOW_AUGS_DICT = frozendict(
    rotate=Rotate(always_apply=True),
    shift_scale_rotate=ShiftScaleRotate(always_apply=True),
    shift_hsv=HueSaturationValue(always_apply=True),
    equalize=Equalize(always_apply=True),
    to_gray=ToGray(always_apply=True),
    resize512=Resize(512, 512, always_apply=True),
    resize300=Resize(300, 300, always_apply=True),
    resize256=Resize(256, 256, always_apply=True),
    resiz224=Resize(224, 224, always_apply=True),
    contrast=RandomContrast(always_apply=True),
    crop=RandomCrop(64, 64, always_apply=True),
    bright=RandomBrightness(always_apply=True)
)


