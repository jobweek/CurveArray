import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import numpy as np


def arr_flip_direction(arr):

    i = 0

    while i < len(arr):

        arr[i] = np.flip(arr[i])

        i += 1

    return arr


def switch_curve_direction(curve):

    bpy.ops.object.select_all(action='DESELECT')
    curve.select_set(True)
    bpy.context.view_layer.objects.active = curve
    bpy.ops.object.editmode_toggle()
    bpy.ops.curve.switch_direction()
    curve.data.offset = -curve.data.offset
    bpy.ops.object.editmode_toggle()

    return curve
