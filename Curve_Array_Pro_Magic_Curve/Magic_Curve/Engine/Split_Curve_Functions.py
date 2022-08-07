import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import math
import numpy as np


def calc_vec(first_vertex, second_vertex, normalize: bool):

    vec = second_vertex - first_vertex

    if vec.length < 0.0001:

        return None

    if normalize:

        vec = vec.normalized()

    return vec


def create_curve(vert_co_array, active_object, curve_data):

    crv_mesh = bpy.data.curves.new('Split_Curve', 'CURVE')
    crv_mesh.dimensions = '3D'
    crv_mesh.twist_mode = 'MINIMUM'

    for _ in range(len(vert_co_array)-1):

        spline = crv_mesh.splines.new(type='POLY')

        spline.points.add(1)

    i = 0

    while i < len(vert_co_array)-1:

        mesh_vertex_first_co = vert_co_array[i]
        mesh_vertex_second_co = vert_co_array[i + 1]

        spline = crv_mesh.splines[i]

        spline.points[0].co[0] = mesh_vertex_first_co[0]
        spline.points[0].co[1] = mesh_vertex_first_co[1]
        spline.points[0].co[2] = mesh_vertex_first_co[2]
        spline.points[0].co[3] = 0

        spline.points[1].co[0] = mesh_vertex_second_co[0]
        spline.points[1].co[1] = mesh_vertex_second_co[1]
        spline.points[1].co[2] = mesh_vertex_second_co[2]
        spline.points[1].co[3] = 0

        i += 1

    crv_obj = bpy.data.objects.new('Split_Curve', crv_mesh)

    crv_obj.location = active_object.location

    crv_obj.rotation_euler = active_object.rotation_euler

    crv_obj.scale = active_object.scale

    bpy.context.scene.collection.objects.link(crv_obj)

    curve_data.set_curve(crv_obj)

    return curve_data


def ext_vec(extruded_mesh, array_size):

    ext_vec_arr = np.empty(array_size, dtype=object)

    i = 0

    while i < array_size:

        first_point = extruded_mesh.data.vertices[0 + i*4]
        second_point = extruded_mesh.data.vertices[1 + i*4]

        vector = mathutils.Vector((
            second_point.co[0] - first_point.co[0],
            second_point.co[1] - first_point.co[1],
            second_point.co[2] - first_point.co[2]
        ))

        ext_vec_arr[i] = vector

        i += 1

    return ext_vec_arr


def tilt_correction(ext_vec_arr, y_vec_arr, curve):

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
