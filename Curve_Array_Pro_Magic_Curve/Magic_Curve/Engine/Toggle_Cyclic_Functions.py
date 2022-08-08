import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import numpy as np
from ...Common_Functions.Functions import (
    calc_vec,
    create_arr,
    vec_projection,
)


def end_start_point_type_correction_cyclic(curve):

    iterator = 0

    while iterator < len(curve.data.splines):

        s = curve.data.splines[iterator]

        if s.type == 'POLY':

            points = s.points

        else:

            points = s.bezier_points

        if points[0].handle_left_type == 'AUTO':

            points[0].handle_left_type = 'FREE'
            points[0].handle_right_type = 'FREE'

        if points[-1].handle_left_type == 'AUTO':

            points[-1].handle_left_type = 'FREE'
            points[-1].handle_right_type = 'FREE'

        iterator += 1


def toggle_curve_cyclic(curve):

    bpy.ops.object.select_all(action='DESELECT')
    curve.select_set(True)
    bpy.context.view_layer.objects.active = curve
    bpy.ops.object.editmode_toggle()
    bpy.ops.curve.cyclic_toggle()
    bpy.ops.object.editmode_toggle()

    return curve


def create_z_arr_cyclic(points_count_list):

    z_vec_arr = np.empty(len(points_count_list), dtype=object)

    i = 0

    while i < len(points_count_list):

        z_vec_arr[i] = np.empty(2, dtype=object)

        i += 1

    return z_vec_arr


def midle_point_calc_cyclic(p_0_ind, verts):

    vec = calc_vec(verts[p_0_ind].co, verts[p_0_ind + 1].co, False)

    midle_point_co = verts[p_0_ind].co + vec/2

    return midle_point_co


def z_vec_cyclic(z_vec_arr, mesh, curve_data):

    (
        spline_point_count_arr,
        spline_verts_index_arr,
        cyclic_arr,
        spline_type_arr,
    ) = curve_data

    verts = mesh.data.vertices
    list_iter = 0

    while list_iter < len(z_vec_arr):

        if cyclic_arr[list_iter]:

            list_iter += 1
            continue

        z_arr = z_vec_arr[list_iter]

        start_point_index = spline_verts_index_arr[list_iter][0]
        next_point_index = start_point_index + 2
        start_mdidle_point_co = midle_point_calc_cyclic(start_point_index, verts)
        next_mdidle_point_co = midle_point_calc_cyclic(next_point_index, verts)
        z_arr[0] = calc_vec(start_mdidle_point_co, next_mdidle_point_co, True)

        end_point_index = spline_verts_index_arr[list_iter][-1]
        prev_point_index = end_point_index - 2
        end_mdidle_point_co = midle_point_calc_cyclic(end_point_index, verts)
        prev_mdidle_point_co = midle_point_calc_cyclic(prev_point_index, verts)

        z_arr[1] = calc_vec(prev_mdidle_point_co, end_mdidle_point_co, True)

        list_iter += 1

    return z_vec_arr


def angle_betw_vec_cyclic(y_vec_arr, ext_vec_arr, spline_point_count, z_vec_arr):

    angle_betw_vec_arr = create_arr(spline_point_count)

    list_iter = 0

    while list_iter < len(ext_vec_arr):

        angle_arr = angle_betw_vec_arr[list_iter]
        y_arr = y_vec_arr[list_iter]
        ext_arr = ext_vec_arr[list_iter]
        z_arr = z_vec_arr[list_iter]

        spline_point_iter = 0

        while spline_point_iter < len(angle_arr):

            if spline_point_iter == 0 or spline_point_iter == len(angle_arr) - 1:

                if spline_point_iter == 0:
                    z_vec = z_arr[0]

                else:
                    z_vec = z_arr[1]

                y_vec = vec_projection(y_arr[spline_point_iter], z_vec)
                ext_vec = vec_projection(ext_arr[spline_point_iter], z_vec)

            else:

                y_vec = y_arr[spline_point_iter]
                ext_vec = ext_arr[spline_point_iter]

            angle_arr[spline_point_iter] = ext_vec.angle(y_vec)

            spline_point_iter += 1

        list_iter += 1

    return angle_betw_vec_arr
