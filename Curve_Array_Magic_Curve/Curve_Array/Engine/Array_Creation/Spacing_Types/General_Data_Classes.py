from typing import Any, NamedTuple
from ...Queue_Calculation.Calc_Queue_Data_Functions import ItemTransform
from mathutils import Vector


class ItemData(NamedTuple):

    obj: Any
    ghost: bool
    co: Vector
    direction: Vector
    normal: Vector
    transform: ItemTransform
