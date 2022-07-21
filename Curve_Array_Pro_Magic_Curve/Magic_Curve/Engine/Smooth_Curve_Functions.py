import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import copy
import math
import numpy as np
from .Errors import CancelError, ShowMessageBox


def create_curve(vert_co_array, active_object, curve_data):
    crv_mesh = bpy.data.curves.new('MgCrv_curve_smooth', 'CURVE')
    crv_mesh.dimensions = '3D'
    crv_mesh.twist_mode = 'MINIMUM'
    spline = crv_mesh.splines.new(type='POLY')

    spline.points.add(len(vert_co_array) - 1)

    if curve_data.get_cyclic():

        spline.use_cyclic_u = True

    iterator = 0

    for i in vert_co_array:
        spline.points[iterator].co[0] = i[0]
        spline.points[iterator].co[1] = i[1]
        spline.points[iterator].co[2] = i[2]
        spline.points[iterator].co[3] = 0

        iterator += 1

    main_curve = bpy.data.objects.new('MgCrv_curve_smooth', crv_mesh)

    main_curve.location = active_object.location

    main_curve.rotation_euler = active_object.rotation_euler

    main_curve.scale = active_object.scale

    bpy.context.scene.collection.objects.link(main_curve)

    spline.type = 'BEZIER'

    curve_data.set_curve(main_curve)

    return curve_data
