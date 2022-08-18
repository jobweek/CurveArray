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
    crv_mesh.twist_mode = 'Z_UP'
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


def z_vec_smooth(curve, array_size):

    points = curve.data.splines[0].bezier_points

    def __func(i):

        h_1 = points[i].handle_left
        h_2 = points[i].handle_right

        vec_h_1 = calc_vec(points[i].co.to_3d(), h_1, True)
        vec_h_2 = calc_vec(points[i].co.to_3d(), h_2, True)

        z_vec = calc_vec(vec_h_1, vec_h_2, True)
        assert z_vec is not None, 'z_vec is None'

        return z_vec

    z_vec_arr = np.frompyfunc(__func, 1, 1)
    z_vec_arr = z_vec_arr(range(array_size))

    return z_vec_arr


def angle_arr_calc_smooth(ext_vec_arr, y_vec_arr, z_vec_arr):

    def __func(i):

        z_vec = z_vec_arr[i]
        ext_vec = vec_projection(ext_vec_arr[i], z_vec)
        y_vec = vec_projection(y_vec_arr[i], z_vec)

        cross_vec = z_vec.cross(y_vec)
        angle = angle_calc(ext_vec, y_vec, cross_vec)

        return angle

    angle_arr = np.frompyfunc(__func, 1, 1)

    angle_arr = angle_arr(range(len(ext_vec_arr)))

    return angle_arr


def tilt_correction_smooth(angle_arr, curve):

    points = curve.data.splines[0].bezier_points

    for i in range(len(points)):

        points[i].tilt = angle_arr[i]
