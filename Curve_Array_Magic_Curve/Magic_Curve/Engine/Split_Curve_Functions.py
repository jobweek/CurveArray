import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import numpy as np
import math
from Curve_Array_Magic_Curve.Magic_Curve.General_Functions.Functions import (
    vec_projection,
    angle_calc,
    calc_vec,
    RAD_CIRCLE_CONST,
)


def create_curve_split(vert_co_array, active_object, curve_data):

    crv_mesh = bpy.data.curves.new('Split_Curve', 'CURVE')
    crv_mesh.dimensions = '3D'
    crv_mesh.twist_mode = 'Z_UP'

    for i in range(len(vert_co_array)-1):

        spline = crv_mesh.splines.new(type='POLY')
        spline.points.add(1)

        spline.points[0].co = vert_co_array[i].to_4d()
        spline.points[1].co = vert_co_array[i + 1].to_4d()

        spline.type = 'BEZIER'

    crv_obj = bpy.data.objects.new('Split_Curve', crv_mesh)
    crv_obj.location = active_object.location
    crv_obj.rotation_euler = active_object.rotation_euler
    crv_obj.scale = active_object.scale
    bpy.context.scene.collection.objects.link(crv_obj)

    curve_data.set_curve(crv_obj)

    return curve_data


def _twist_correction_split(first_angle, second_angle):

    diff = second_angle - first_angle

    if abs(diff) > math.pi:

        if diff > 0:

            angle_tuple = (first_angle, second_angle - RAD_CIRCLE_CONST)

        else:

            angle_tuple = (first_angle, second_angle + RAD_CIRCLE_CONST)

    else:

        angle_tuple = (first_angle, second_angle)

    return angle_tuple


def angle_arr_calc_split(ext_vec_arr, y_vec_arr, curve):

    def __func(i):

        first_point = curve.data.splines[i].bezier_points[0]
        second_point = curve.data.splines[i].bezier_points[1]

        z_vec = calc_vec(first_point.co.to_3d(), second_point.co.to_3d(), True)
        assert z_vec is not None, 'z_vec is None'

        ext_vec = vec_projection(ext_vec_arr[i], z_vec)

        first_y_vec = vec_projection(y_vec_arr[i], z_vec)
        second_y_vec = vec_projection(y_vec_arr[i + 1], z_vec)

        first_cross_vec = z_vec.cross(first_y_vec)
        second_cross_vec = z_vec.cross(second_y_vec)

        first_angle = angle_calc(ext_vec, first_y_vec, first_cross_vec)
        second_angle = angle_calc(ext_vec, second_y_vec, second_cross_vec)

        angle_tuple = _twist_correction_split(first_angle, second_angle)

        return angle_tuple

    angle_arr = np.frompyfunc(__func, 1, 1)

    angle_arr = angle_arr(range(len(ext_vec_arr)))

    return angle_arr


def tilt_correction_split(angle_arr, curve):

    for i, spline in enumerate(curve.data.splines):

        spline.bezier_points[0].tilt = angle_arr[i][0]
        spline.bezier_points[1].tilt = angle_arr[i][1]
