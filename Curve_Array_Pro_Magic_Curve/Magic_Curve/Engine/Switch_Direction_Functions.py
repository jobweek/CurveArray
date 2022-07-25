import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import numpy as np
from .Errors import CancelError, ShowMessageBox
from .Smooth_Curve_Functions import (
    vec_projection,
    angle_calc,
)


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


def merged_points_check(curve):

    iterator = 0
    points_count = 0
    merged_points_buffer = []
    error_case = False

    for s in curve.data.splines:

        if s.type == 'POLY':

            points = s.points

        elif s.type == 'BEZIER':

            points = s.bezier_points

        else:

            ShowMessageBox("Error", "Nurbs curves are not supported", 'ERROR')

            raise CancelError

        points_count += len(points)
        i = 0
        merged_points_buffer.append([])

        while i < len(points) - 1:

            if points[i].co == points[i+1].co:

                merged_points_buffer[iterator].append([points[i].co, points[i+1].co])
                error_case = True

            i += 1

        if s.use_cyclic_u:

            if points[i].co == points[0].co:

                merged_points_buffer[iterator].append([points[i].co, points[0].co])
                error_case = True

        iterator += 1

    if error_case:

        verts_str = ""
        i = 0

        while i < len(merged_points_buffer):

            if len(merged_points_buffer[i]) != 0:

                verts_str += "Spline: {0}, Points: ".format(i)

                for p in merged_points_buffer[i]:

                    verts_str += "({0},{1}) ".format(p[0], p[1])

        ShowMessageBox("Error",
                       "In the curve you have chosen, there are points in the same coordinates."
                       " You can remove it."
                       " Their place: " + verts_str,
                       'ERROR')

        raise CancelError

    return points_count


def points_select(curve):

    for s in curve.data.splines:

        if s.type == 'POLY':

            for p in s.points:

                p.select = True

        elif s.type == 'BEZIER':

            for p in s.bezier_points:

                p.select_control_point = True

        else:

            ShowMessageBox("Error", "Nurbs curves are not supported", 'ERROR')

            raise CancelError


def duplicate(active_curve):

    switched_curve = active_curve.copy()
    switched_curve.data = active_curve.data.copy()

    if active_curve.animation_data:
        switched_curve.animation_data.action = active_curve.animation_data.action.copy()

    for i in active_curve.users_collection:

        i.objects.link(switched_curve)

    return switched_curve


def ext_vec(active_curve, arr_size):

    extruded_mesh_vector_array = np.empty(arr_size, dtype=object)

    active_curve.data.extrude = 0.5
    bpy.ops.object.select_all(action='DESELECT')
    active_curve.select_set(True)
    bpy.context.view_layer.objects.active = active_curve
    bpy.ops.object.convert(target='MESH')
    extruded_mesh = bpy.context.active_object

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


def z_vec(curve, array_size):

    def calc_vec(first_vertex, second_vertex):

        vec = mathutils.Vector((
            second_vertex.co[0] - first_vertex.co[0],
            second_vertex.co[1] - first_vertex.co[1],
            second_vertex.co[2] - first_vertex.co[2]
        ))

        if vec.length == 0:

            return None

        return vec.normalized()

    def prev_point_search(points, index, cyclic):

        if cyclic and index == 0:

            prev_point = points[-1]

        elif not cyclic and index == 0:

            prev_point = points[index]

        else:

            prev_point = points[index - 1]

        return prev_point

    def next_point_search(points, index, cyclic):

        if cyclic and index == len(points)-1:

            next_point = points[0]

        elif not cyclic and index == len(points)-1:

            next_point = points[index]

        else:

            next_point = points[index + 1]

        return next_point

    z_vec_arr = np.empty(array_size, dtype=object)

    iterator = 0

    for s in curve.data.splines:

        if s.type == 'POLY':

            points = s.points

        else:

            points = s.bezier_points

        i = 0

        while i < len(points):

            prev_point = prev_point_search(points, i, s.use_cyclic_u)
            next_point = next_point_search(points, i, s.use_cyclic_u)
            z_vec = calc_vec(prev_point, next_point)
            z_vec_arr[iterator] = z_vec

            iterator += 1
            i += 1

    return z_vec_arr


def tilt_correction(ext_vec_arr, y_vec_arr, z_vec_arr, curve):

    iterator = 0

    for s in curve.data.splines:

        if s.type == 'POLY':

            points = s.points

        else:

            points = s.bezier_points

        i = 0

        while i < len(points):

            if z_vec_arr[iterator] is None:

                iterator += 1
                i += 1
                continue

            ext_vec = vec_projection(ext_vec_arr[iterator], z_vec_arr[iterator])
            y_vec = vec_projection(y_vec_arr[iterator], z_vec_arr[iterator])
            cross_vec = z_vec_arr[iterator].cross(y_vec)
            angle = angle_calc(ext_vec, y_vec, cross_vec)

            points[i].tilt += angle

            if iterator == 0:

                print('ext_vec :', ext_vec)
                print('y_vec :', y_vec)
                print('cross_vec :', cross_vec)
                print('z_vec_arr :', z_vec_arr[iterator])
                print('angle :', angle)

            iterator += 1
            i += 1
