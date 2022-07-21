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


def extruded_mesh_vector(extruded_mesh, array_size, curve_data):

    extruded_mesh_vector_array = np.empty(array_size, dtype=object)

    i = 0

    if curve_data.get_cyclic():

        array_size -= 1

    while i < array_size:

        first_point = extruded_mesh.data.vertices[0 + i*2]
        second_point = extruded_mesh.data.vertices[1 + i*2]

        vector = mathutils.Vector((
            second_point.co[0] - first_point.co[0],
            second_point.co[1] - first_point.co[1],
            second_point.co[2] - first_point.co[2]
        ))

        extruded_mesh_vector_array[i] = vector

        i += 1

    if curve_data.get_cyclic():

        extruded_mesh_vector_array[i] = extruded_mesh_vector_array[0]

    return extruded_mesh_vector_array


def tilt_correction(ext_vec_arr, y_vec_arr, curve):

    def z_vector(first_vertex, second_vertex):

        z_vec = mathutils.Vector((
            second_vertex.co[0] - first_vertex.co[0],
            second_vertex.co[1] - first_vertex.co[1],
            second_vertex.co[2] - first_vertex.co[2]
        ))

        return z_vec.normalized()

    def vec_projection(vec, z_vec):

        projection = (vec - vec.project(z_vec)).normalized()

        return projection

    def angle_calc(ext_vec, y_vec, cross_vec):

        try:

            angle = ext_vec.angle(y_vec)

        except ValueError:

            angle = 0

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

    i = 0

    while i < len(ext_vec_arr):

        first_point = curve.data.splines[i].points[0]
        second_point = curve.data.splines[i].points[1]
        z_vec = z_vector(first_point, second_point)
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