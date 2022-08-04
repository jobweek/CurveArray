import math

import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import numpy as np
from .Errors import CancelError, ShowMessageBox


def toggle_cyclic(curve):

    bpy.ops.object.select_all(action='DESELECT')
    curve.select_set(True)
    bpy.context.view_layer.objects.active = curve
    bpy.ops.object.editmode_toggle()
    bpy.ops.curve.cyclic_toggle()
    bpy.ops.object.editmode_toggle()

    return curve
