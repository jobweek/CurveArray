import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import copy
import math
import numpy as np
from .Errors import CancelError, ShowMessageBox


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

        while i < len(points) - 1:

            if points[i].co == points[i+1].co:

                ShowMessageBox("Error",
                               "In the curve you have chosen, there are points in the same coordinates."
                               " You can remove it."
                               " Their indices: "
                               "Spline: " + str(iterator) +
                               ", Points: " + str(i) + "," + str(i+1)
                               , 'ERROR')

                raise CancelError

            i += 1

        if s.use_cyclic_u:

            if points[i].co == points[0].co:

                ShowMessageBox("Error",
                               "In the curve you have chosen, there are points in the same coordinates."
                               " You can remove it."
                               " Their indices: "
                               "Spline: " + str(iterator) +
                               ", Points: " + str(i) + "," + str(0)
                               , 'ERROR')

                raise CancelError

        iterator += 1

    return points_count


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

    def prev_point_search(points, index):

        while index > 0:

            if points[index].co == points[index - 1].co:

                index -= 1
                continue

            else:

                return points[index - 1]

        return points[index]

    def next_point_search(points, index):

        while index < len(points)-1:

            if points[index].co == points[index + 1].co:

                index += 1
                continue

            else:

                return points[index + 1]

        return points[index]

    def prev_point_search_cyclic(points, index):

        stop_point = points[index + 1]

        while points[index] != stop_point:

            if points[index].co == points[index - 1].co:

                index -= 1
                continue

            else:

                return points[index - 1]

        return points[index]

    def next_point_search_cyclic(points, index):

        stop_point = points[index - 1]

        while points[index] != stop_point:

            if index + 1 == len(points):

                next_point = points[0]

            else:

                next_point = points[index + 1]

            if points[index].co == next_point.co:

                index += 1

                if index == len(points):

                    index = 0

                continue

            else:

                return next_point

        return points[index]

    z_vec_arr = np.empty(array_size, dtype=object)

    iterator = 0

    for s in curve.data.splines:

        if s.type == 'POLY':

            points = s.points

        elif s.type == 'BEZIER':

            points = s.bezier_points

        else:

            ShowMessageBox("Error", "Nurbs curves are not supported", 'ERROR')

            raise CancelError

        if not s.use_cyclic_u:

            i = 0

            next_point = next_point_search(points, i)
            z_vec = calc_vec(points[i], next_point)
            z_vec_arr[iterator] = z_vec
            iterator += 1
            i += 1

            while i < len(points)-1:

                if points[i].co == points[i+1].co:

                    z_vec_arr[iterator] = None
                    iterator += 1
                    continue

                prev_point = prev_point_search(points, i)
                next_point = next_point_search(points, i)
                z_vec = calc_vec(prev_point, next_point)
                z_vec_arr[iterator] = z_vec
                iterator += 1

                i += 1

            prev_point = prev_point_search(points, i)
            z_vec = calc_vec(prev_point, points[i])
            z_vec_arr[iterator] = z_vec
            iterator += 1

        else:

            i = 0

            while i < len(points):

                if points[i].co == points[i+1].co:

                    z_vec_arr[iterator] = None
                    iterator += 1
                    continue

                prev_point = prev_point_search_cyclic(points, i)
                next_point = next_point_search_cyclic(points, i)
                z_vec = calc_vec(prev_point, next_point)
                z_vec_arr[iterator] = z_vec
                iterator += 1

                i += 1

    return z_vec_arr
