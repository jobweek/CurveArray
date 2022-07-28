import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import numpy as np
from .Switch_Direction_Functions import (
    checker,
    merged_points_check,
    points_select,
    duplicate,
    ext_z_vec,
    tilt_correction,
)


def recalculate_curve_manager():

    switched_curve = bpy.context.active_object
    checker()
    points_count = merged_points_check(switched_curve)
    points_select(switched_curve)

    extruded_curve = duplicate(switched_curve)

    bpy.ops.object.select_all(action='DESELECT')
    switched_curve.select_set(True)
    bpy.context.view_layer.objects.active = switched_curve
    bpy.ops.object.editmode_toggle()
    bpy.ops.curve.switch_direction()
    bpy.ops.object.editmode_toggle()

    y_vec_arr, _ = ext_z_vec(extruded_curve, True)
    bpy.data.objects.remove(extruded_curve, do_unlink=True)

    extruded_switched_curve = duplicate(switched_curve)

    ext_vec_arr, z_vec_arr = ext_z_vec(extruded_switched_curve, False)
    bpy.data.objects.remove(extruded_switched_curve, do_unlink=True)

    tilt_correction(ext_vec_arr, y_vec_arr, z_vec_arr, switched_curve)

    bpy.ops.object.select_all(action='DESELECT')
    switched_curve.select_set(True)
    bpy.context.view_layer.objects.active = switched_curve
