import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
from .Curve_Array_By_Offset_Functions import (
    get_point_on_spline,
)


def curve_array_by_offset_manager(curve, objects, params):

    spline_segment = (
        curve.data.splines[0].bezier_points[0],
        curve.data.splines[0].bezier_points[0].handle_right.co,
        curve.data.splines[0].bezier_points[1],
        curve.data.splines[0].bezier_points[1].handle_left.co,
        curve.data.splines[0].resolution_u
    )

    get_point_on_spline(0, spline_segment)

    pass
