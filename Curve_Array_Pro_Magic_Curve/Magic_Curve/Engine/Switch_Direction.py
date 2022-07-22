import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
from .Switch_Direction_Functions import (
    checker,
    ext_vec,
)


def recalculate_curve_manager():

    active_curve = bpy.context.active_object

    checker()

    ext_vec_arr = ext_vec(active_curve)

