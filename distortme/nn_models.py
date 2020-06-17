from enum import Enum
from frozendict import frozendict
from distortme.nn_algorithms.faces.wrappers.blaze_face_wrapper import BlazeFaceWrapper


class Models(str, Enum):
    faces = "faces"
    objects = "objects"
    classes = "classes"
    masks = "masks"


TASK_TO_MODEL = frozendict(
    faces=BlazeFaceWrapper
)

