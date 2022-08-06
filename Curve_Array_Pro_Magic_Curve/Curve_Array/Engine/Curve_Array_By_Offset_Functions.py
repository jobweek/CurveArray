import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore


def get_point_on_spline(distance, spline_segment):

    interpolated_segment = mathutils.geometry.interpolate_bezier(*spline_segment)

    print(interpolated_segment)
