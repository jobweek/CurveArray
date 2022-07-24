import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
from .Switch_Direction_Functions import (
    checker,
    duplicate,
    ext_vec,
    z_vec,
)


def recalculate_curve_manager():

    switched_curve = bpy.context.active_object
    checker()

    extruded_curve = duplicate(switched_curve)

    bpy.ops.object.select_all(action='DESELECT')
    switched_curve.select_set(True)
    bpy.context.view_layer.objects.active = switched_curve
    bpy.ops.object.editmode_toggle()
    bpy.ops.curve.switch_direction()
    bpy.ops.object.editmode_toggle()

    ext_vec_arr = ext_vec(extruded_curve)

    z_vec_arr = z_vec(switched_curve, len(extruded_curve))

    bpy.data.objects.remove(extruded_curve, do_unlink=True)


