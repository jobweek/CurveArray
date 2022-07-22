import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import copy
import math
import numpy as np
from .Errors import CancelError, ShowMessageBox


def checker():

    objects = bpy.context.selected_objects

    if len(objects) == 0:

        ShowMessageBox("Error", "Select object", 'ERROR')

        raise CancelError

    elif len(objects) > 1:

        ShowMessageBox("Error", "Select only one object", 'ERROR')

        raise CancelError

    if objects[0].type != 'CURVE':

        ShowMessageBox("Error", "Object should be curve", 'ERROR')

        raise CancelError

    mode = bpy.context.active_object.mode

    if mode != 'OBJECT':
        ShowMessageBox("Error", "Go to Object Mode", 'ERROR')

        raise CancelError


def duplicate(active_curve):

    switched_curve = active_curve.copy()
    switched_curve.data = active_curve.data.copy()

    if active_curve.animation_data:
        switched_curve.animation_data.action = active_curve.animation_data.action.copy()

    for i in active_curve.users_collection:

        i.objects.link(switched_curve)

    return switched_curve


def ext_vec(active_curve):

    active_curve.data.extrude = 0.5
    bpy.ops.object.select_all(action='DESELECT')
    active_curve.select_set(True)
    bpy.context.view_layer.objects.active = active_curve
    bpy.ops.object.convert(target='MESH')
    extruded_mesh = bpy.context.active_object
    arr_size = int(len(extruded_mesh.data.vertices) / 2)
    extruded_mesh_vector_array = np.empty(arr_size, dtype=object)

    i = 0

    while i < arr_size:

        first_point = extruded_mesh.data.vertices[0 + i*2]
        second_point = extruded_mesh.data.vertices[1 + i*2]

        vector = mathutils.Vector((
            second_point.co[0] - first_point.co[0],
            second_point.co[1] - first_point.co[1],
            second_point.co[2] - first_point.co[2]
        ))

        extruded_mesh_vector_array[i] = vector

        i += 1

    return extruded_mesh_vector_array
