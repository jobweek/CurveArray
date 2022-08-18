import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
from ...Errors.Errors import show_message_box
from ...General_Functions.Functions import (
    vec_projection,
    angle_calc,
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


def tilt_correction_cyclic(y_vec_arr, ext_vec_arr, z_vec_arr, curve):

    splines = curve.data.splines
    spline_iter = 0

    while spline_iter < len(ext_vec_arr):

        if splines[spline_iter].type == 'POLY':

            points = splines[spline_iter].points

        else:

            points = splines[spline_iter].bezier_points

        y_arr = y_vec_arr[spline_iter]
        ext_arr = ext_vec_arr[spline_iter]
        z_arr = z_vec_arr[spline_iter]

        point_iter = 0

        while point_iter < len(y_arr):

            y_vec = y_arr[point_iter]
            ext_vec = ext_arr[point_iter]
            z_vec = z_arr[point_iter]

            if point_iter == 0 or point_iter == len(y_arr) - 1:

                y_vec = vec_projection(y_vec, z_vec)
                ext_vec = vec_projection(ext_vec, z_vec)

                if y_vec is None or ext_vec is None:

                    point_iter += 1

                    continue

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

            points[point_iter].tilt = new_angle

            point_iter += 1

        spline_iter += 1
