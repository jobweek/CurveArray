import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import numpy as np
from ...Errors.Errors import show_message_box
from ...General_Functions.Functions import (
    vec_projection,
    angle_calc,
)


def end_start_point_type_correction_cyclic(curve):

    for spline in curve.data.splines:

        if spline.type == 'POLY':

            return

        else:

            points = spline.bezier_points

        if points[0].handle_left_type == 'AUTO':

            points[0].handle_left_type = 'FREE'
            points[0].handle_right_type = 'FREE'

        if points[-1].handle_left_type == 'AUTO':

            points[-1].handle_left_type = 'FREE'
            points[-1].handle_right_type = 'FREE'


def toggle_curve_cyclic(curve):

    bpy.ops.object.select_all(action='DESELECT')
    curve.select_set(True)
    bpy.context.view_layer.objects.active = curve
    bpy.ops.object.editmode_toggle()
    bpy.ops.curve.cyclic_toggle()
    bpy.ops.object.editmode_toggle()

    return curve


def angle_arr_calc_cyclic(y_vec_arr, ext_vec_arr, z_vec_arr, curve):

    # Возвращает массив содержащий углы поворта кажждой точки для одного сплайна
    def __func(spline_iter):

        splines = curve.data.splines

        if splines[spline_iter].type == 'POLY':

            points = splines[spline_iter].points

        else:

            points = splines[spline_iter].bezier_points

        y_arr = y_vec_arr[spline_iter]
        ext_arr = ext_vec_arr[spline_iter]
        z_arr = z_vec_arr[spline_iter]

        # Возвращает угл поворта точки
        def __under_func(point_iter):

            y_vec = y_arr[point_iter]
            ext_vec = ext_arr[point_iter]
            z_vec = z_arr[point_iter]

            if point_iter == 0 or point_iter == len(y_arr) - 1:

                y_vec = vec_projection(y_vec, z_vec)
                ext_vec = vec_projection(ext_vec, z_vec)

            cross_vec = z_vec.cross(y_vec)
            angle = angle_calc(ext_vec, y_vec, cross_vec)

            new_angle = points[point_iter].tilt + angle

            if new_angle > 376.992:

                show_message_box(
                    "Error",
                    (
                        'The tilt of point {0} on spline {1} has exceeded the Blender'
                        'tolerance of -21600|+21600 degrees, the result of the operation will not be correct.'
                        'Reduce the point tilt on the curve and repeat the operation.'
                    ).format(point_iter, spline_iter),
                    'ERROR'
                )

            return new_angle

        spline_angle_arr = np.frompyfunc(__under_func, 1, 1)
        spline_angle_arr = spline_angle_arr(range(len(y_arr)))

        return spline_angle_arr

    angle_arr = np.frompyfunc(__func, 1, 1)
    angle_arr = angle_arr(range(len(ext_vec_arr)))

    return angle_arr
