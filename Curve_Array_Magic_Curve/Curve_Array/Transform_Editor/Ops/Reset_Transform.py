import bpy  # type: ignore
from .Reset_tranform_Functions import reset_transform

from typing import Any


def reset_transform_manager(index: int):

    reset_transform(index)
