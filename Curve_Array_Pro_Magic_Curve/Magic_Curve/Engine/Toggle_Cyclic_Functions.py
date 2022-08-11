import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore


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
