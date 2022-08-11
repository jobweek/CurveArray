import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import numpy as np
from ...Common_Functions.Functions import (
    vec_projection,
    angle_calc,
    calc_vec,
)


def create_curve_smooth(vert_co_array, active_object, curve_data):

    crv_mesh = bpy.data.curves.new('Smooth_Curve', 'CURVE')
    crv_mesh.dimensions = '3D'
    crv_mesh.twist_mode = 'MINIMUM'
    spline = crv_mesh.splines.new(type='POLY')

    spline.points.add(len(vert_co_array) - 1)

    if curve_data.get_cyclic():

        spline.use_cyclic_u = True

    i = 0

    while i < len(vert_co_array):

        spline.points[i].co = vert_co_array[i].to_4d()

        i += 1

    main_curve = bpy.data.objects.new('Smooth_Curve', crv_mesh)
    main_curve.location = active_object.location
    main_curve.rotation_euler = active_object.rotation_euler
    main_curve.scale = active_object.scale
    bpy.context.scene.collection.objects.link(main_curve)
    spline.type = 'BEZIER'

    curve_data.set_curve(main_curve)

    return curve_data


def ext_vec_smooth(extruded_mesh, array_size):

    ext_vec_arr = np.empty(array_size, dtype=object)

    i = 0

    while i < array_size:

        first_point = extruded_mesh.data.vertices[0 + i*2]
        second_point = extruded_mesh.data.vertices[1 + i*2]

        vector = calc_vec(first_point.co, second_point.co, True)

        ext_vec_arr[i] = vector

        i += 1

    return ext_vec_arr


def z_vec_smooth(curve, array_size):

    z_vec_arr = np.empty(array_size, dtype=object)
    points = curve.data.splines[0].bezier_points

    i = 0

    while i < len(z_vec_arr):

        h_1 = points[i].handle_left
        h_2 = points[i].handle_right

        vec_h_1 = calc_vec(h_1, points[i].co, True)
        vec_h_2 = calc_vec(h_2, points[i].co, True)

        vec = calc_vec(vec_h_2, vec_h_1, True)

        z_vec_arr[i] = vec

        i += 1

    return z_vec_arr


def tilt_correction_smooth(ext_vec_arr, y_vec_arr, z_vec_arr, curve):

    i = 0
    points = curve.data.splines[0].bezier_points

    while i < len(ext_vec_arr):

        z_vec = z_vec_arr[i]
        ext_vec = vec_projection(ext_vec_arr[i], z_vec)
        y_vec = vec_projection(y_vec_arr[i], z_vec)
        cross_vec = z_vec.cross(y_vec)
        angle = angle_calc(ext_vec, y_vec, cross_vec)

        points[i].tilt = angle

        i += 1