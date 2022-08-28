import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils
import numpy as np
from Curve_Array_Magic_Curve.Errors.Errors import (
    show_message_box,
    CancelError,
)


class InterpolatedPoint:

    def __init__(self, co: mathutils.Vector, normal: mathutils.Vector, distance: float, spline_point: bool):

        self.co = co
        self.normal = normal
        self.distance = distance
        self.spline_point = spline_point


class InterpolatedSpline:

    class_count = 0

    def __init__(self, spline_length: float, arrays: tuple[np.ndarray, np.ndarray]):

        self.__class__.class_count += 1
        self.points_iter = 0
        self.spline_length = spline_length
        self.interpolated_points, self.interpolated_points_distance = arrays

    def get_nearest(self, distance: float) -> InterpolatedPoint:

        index = np.searchsorted(self.interpolated_points_distance, distance)

        return self.interpolated_points[index]


class PathData:

    @staticmethod
    def _type_check(obj):

        if obj.type != 'CURVE':

            show_message_box("Error", "Object should be curve", 'ERROR')

            raise CancelError

    def __init__(self, curve, arrays: tuple[np.ndarray, np.ndarray]):

        self._type_check(curve)
        self.curve_name = curve.name
        self.interpolated_splines, self.interpolated_splines_distance = arrays

    def get_nearest(self, distance: float) -> InterpolatedPoint:

        index = np.searchsorted(self.interpolated_splines_distance, distance)

        return self.interpolated_splines[index]


def _spline_verts_index(points, spline_type, cyclic, resolution, last_index) -> tuple[int, int, tuple[int, int]]:

    vert_index = last_index + 2
    start_range = vert_index

    if cyclic and not spline_type:

        if points[-1].handle_right_type != 'VECTOR' or points[0].handle_left_type != 'VECTOR':

            shift = 2 * resolution

        else:

            shift = 2

        vert_index += shift

    else:

        shift = 0

    for i in range(len(points)-1):

        if spline_type or (points[i].handle_right_type == 'VECTOR' and points[i + 1].handle_left_type == 'VECTOR'):

            vert_index += 2

        else:

            vert_index += 2 * resolution

    if cyclic and not spline_type:

        vert_index -= 2

    end_range = vert_index

    return end_range, shift, (start_range, end_range)


def spline_range_calc(curve) -> np.ndarray:

    last_index = -2  # Индекс последней нулевой вершины меша относящегося к сплайну

    def __func(spline) -> tuple[bool, int, tuple[int, int]]:

        nonlocal last_index

        if spline.type == 'POLY':

            points = spline.points
            spline_type = True

        else:

            points = spline.bezier_points
            spline_type = False

        cyclic = spline.use_cyclic_u
        resolution = spline.resolution_u

        last_index, shift, verts_range = _spline_verts_index(points, spline_type, cyclic, resolution, last_index)

        res = (spline_type, shift, verts_range)

        return res

    spline_range_arr = np.frompyfunc(__func, 1, 1)
    spline_range_arr = spline_range_arr(curve.data.splines)

    return spline_range_arr
