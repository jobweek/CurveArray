import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import math
import numpy as np


def create_curve(vert_co_array, active_object, curve_data):
    crv_mesh = bpy.data.curves.new('Smooth_Curve', 'CURVE')
    crv_mesh.dimensions = '3D'
    crv_mesh.twist_mode = 'MINIMUM'
    spline = crv_mesh.splines.new(type='POLY')

    spline.points.add(len(vert_co_array) - 1)

    if curve_data.get_cyclic():

        spline.use_cyclic_u = True

    i = 0

    while i < len(vert_co_array):

        spline.points[i].co[0] = vert_co_array[i][0]
        spline.points[i].co[1] = vert_co_array[i][1]
        spline.points[i].co[2] = vert_co_array[i][2]
        spline.points[i].co[3] = 0

        i += 1

    main_curve = bpy.data.objects.new('Smooth_Curve', crv_mesh)

    main_curve.location = active_object.location

    main_curve.rotation_euler = active_object.rotation_euler

    main_curve.scale = active_object.scale

    bpy.context.scene.collection.objects.link(main_curve)

    spline.type = 'BEZIER'

    curve_data.set_curve(main_curve)

    return curve_data


def ext_vec(extruded_mesh, array_size):

    ext_vec_arr = np.empty(array_size, dtype=object)

    i = 0

    while i < array_size:

        first_point = extruded_mesh.data.vertices[0 + i*2]
        second_point = extruded_mesh.data.vertices[1 + i*2]

        vector = (second_point.co - first_point.co).normalized()

        ext_vec_arr[i] = vector

        i += 1

    return ext_vec_arr


def z_vec(curve, array_size):

    z_vec_arr = np.empty(array_size, dtype=object)

    i = 0

    while i < len(z_vec_arr):

        point = curve.data.splines[0].bezier_points[i]

        h_1 = point.handle_left
        h_2 = point.handle_right

        vec_h_1 = (h_1 - point.co).normalized()
        vec_h_2 = (h_2 - point.co).normalized()

        vec = (vec_h_2 - vec_h_1).normalized()

        z_vec_arr[i] = vec

        i += 1

    return z_vec_arr


def vec_projection(vec, z_vec):

    projection = (vec - vec.project(z_vec)).normalized()

    return projection


def angle_calc(ext_vec, y_vec, cross_vec):

    angle = ext_vec.angle(y_vec)

    #  Определяем позитивное вращение или негативное
    if ext_vec.dot(cross_vec) > 0:

        angle = -angle

    elif ext_vec.dot(cross_vec) == 0:

        angle = 0

    #  Предотвращение перекрещивания
    if ext_vec.dot(y_vec) < 0:

        if angle < 0:

            angle = math.radians(180) + (math.radians(180) + angle)

        elif angle > 0:

            angle = math.radians(180) - (math.radians(180) - angle)

    return angle


def tilt_correction(ext_vec_arr, y_vec_arr, z_vec_arr, curve):

    i = 0
    spline_point = curve.data.splines[0].bezier_points

    while i < len(ext_vec_arr):

        z_vec = z_vec_arr[i]

        ext_vec = vec_projection(ext_vec_arr[i], z_vec)
        y_vec = vec_projection(y_vec_arr[i], z_vec)
        cross_vec = z_vec.cross(y_vec)
        angle = angle_calc(ext_vec, y_vec, cross_vec)

        spline_point[i].tilt = angle

        i += 1
