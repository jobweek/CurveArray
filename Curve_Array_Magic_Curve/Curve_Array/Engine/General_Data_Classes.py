from typing import Any, NamedTuple
from mathutils import Vector, Matrix  # type: ignore


class ItemTransform(NamedTuple):

    rotation_x: float
    rotation_y: float
    rotation_z: float
    location_x: float
    location_y: float
    location_z: float
    scale_x: float
    scale_y: float
    scale_z: float


class QueueItem(NamedTuple):

    object_name: str
    ghost: bool
    pivot: float
    queue_transform: ItemTransform


class ItemData(NamedTuple):

    ghost: bool
    co: Vector
    direction: Vector
    normal: Vector
    total_transform: Matrix


class ArrayTransform(NamedTuple):

    rotation_x: float
    rotation_y: float
    rotation_z: float
    location_x: float
    location_y: float
    location_z: float
    scale_x: float
    scale_y: float
    scale_z: float


class ArrayPrams(NamedTuple):

    calculate_path_data: bool
    calculate_queue_data: bool
    random_seed: int
    spacing_type: str
    cloning_type: str
    cyclic: bool
    smooth_normal: bool
    count: int
    step_offset: float
    size_offset: float
    start_offset: float
    end_offset: float
    slide: float
    consider_size: bool
    align_rotation: bool
    rail_axis: str
    normal_axis: str
    array_transform: ArrayTransform
