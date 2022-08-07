import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import numpy as np

from Curve_Array_Pro_Magic_Curve.Common_Functions.Functions import (
    vec_projection,
    angle_calc,
    calc_vec,
)


def create_curve_split(vert_co_array, active_object, curve_data):

    crv_mesh = bpy.data.curves.new('Split_Curve', 'CURVE')
    crv_mesh.dimensions = '3D'
    crv_mesh.twist_mode = 'MINIMUM'

    for _ in range(len(vert_co_array)-1):

        spline = crv_mesh.splines.new(type='POLY')

        spline.points.add(1)

    i = 0

    while i < len(vert_co_array)-1:

        points = crv_mesh.splines[i].points

        points[0].co = vert_co_array[i].to_4d()
        points[1].co = vert_co_array[i + 1].to_4d()

        i += 1

    crv_obj = bpy.data.objects.new('Split_Curve', crv_mesh)
    crv_obj.location = active_object.location
    crv_obj.rotation_euler = active_object.rotation_euler
    crv_obj.scale = active_object.scale
    bpy.context.scene.collection.objects.link(crv_obj)

    curve_data.set_curve(crv_obj)

    return curve_data


def ext_vec_split(extruded_mesh, array_size):

    ext_vec_arr = np.empty(array_size, dtype=object)

    i = 0

    while i < array_size:

        first_point = extruded_mesh.data.vertices[0 + i*4]
        second_point = extruded_mesh.data.vertices[1 + i*4]

        vector = calc_vec(first_point.co, second_point.co, True)

        ext_vec_arr[i] = vector

        i += 1

    return ext_vec_arr


def tilt_correction_split(ext_vec_arr, y_vec_arr, curve):

    i = 0

    while i < len(ext_vec_arr):

        first_point = curve.data.splines[i].points[0]
        second_point = curve.data.splines[i].points[1]

        z_vec = (second_point.co - first_point.co).to_3d().normalized()
        ext_vec = vec_projection(ext_vec_arr[i], z_vec)

        first_y_vec = vec_projection(y_vec_arr[i], z_vec)
        second_y_vec = vec_projection(y_vec_arr[i + 1], z_vec)

        first_cross_vec = z_vec.cross(first_y_vec)
        second_cross_vec = z_vec.cross(second_y_vec)

        first_angle = angle_calc(ext_vec, first_y_vec, first_cross_vec)
        second_angle = angle_calc(ext_vec, second_y_vec, second_cross_vec)

        first_point.tilt = first_angle
        second_point.tilt = second_angle

        i += 1
