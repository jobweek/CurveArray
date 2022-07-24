import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import math
import numpy as np


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


def tilt_correction(ext_vec_arr, y_vec_arr, curve, cyclic):

    def z_vector(first_vertex, second_vertex):

        z_vec = mathutils.Vector((
            second_vertex.co[0] - first_vertex.co[0],
            second_vertex.co[1] - first_vertex.co[1],
            second_vertex.co[2] - first_vertex.co[2]
        ))

        return z_vec.normalized()

    i = 0
    spline_point = curve.data.splines[0].bezier_points

    #  Если кривая циклична, последнюю точку не считаем
    if not cyclic:

        cycle_lenth = len(ext_vec_arr)

    else:

        cycle_lenth = len(ext_vec_arr) - 1

    while i < cycle_lenth:

        if not cyclic:

            if i == 0:

                z_vec = z_vector(spline_point[i], spline_point[i+1])

            elif i == cycle_lenth - 1:

                z_vec = z_vector(spline_point[i-1], spline_point[i])

            else:

                z_vec = z_vector(spline_point[i-1], spline_point[i+1])

        else:

            if i == 0:

                z_vec = z_vector(spline_point[i-2], spline_point[i+1])

            else:

                z_vec = z_vector(spline_point[i-1], spline_point[i+1])

        ext_vec = vec_projection(ext_vec_arr[i], z_vec)
        y_vec = vec_projection(y_vec_arr[i], z_vec)
        cross_vec = z_vec.cross(y_vec)
        angle = angle_calc(ext_vec, y_vec, cross_vec)

        spline_point[i].tilt = angle

        i += 1

    if cyclic:

        spline_point[-1].tilt = spline_point[0].tilt
