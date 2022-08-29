import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils
import numpy as np
from Curve_Array_Magic_Curve.Errors.Errors import (
    show_message_box,
    CancelError,
)
from Curve_Array_Magic_Curve.General_Functions.Functions import (
    midle_point_calc,
    calc_vec,
)
from typing import Iterator


class InterpolatedPoint:

    def __init__(self, co: mathutils.Vector, normal: mathutils.Vector, distance: float, spline_point: bool):

        self.co = co
        self.normal = normal
        self.distance = distance
        self.spline_point = spline_point


class InterpolatedSegment:

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


def _spline_range_calc(points, spline_type, cyclic, resolution, last_index) -> tuple[int, int, tuple[int, int]]:

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


def _verts_range_generator(verts_range: tuple[bool, int, tuple[int, int]]):

    cyclic = verts_range[0]
    shift = verts_range[1]
    start = verts_range[2][0]
    end = verts_range[2][1]
    p = start + shift

    def __func(p, end):

        while p <= end:
            yield p
            p += 2

    for y in __func(p, end):
        yield y

    if shift != 0:

        p = start
        end = start + shift - 2

        for y in __func(p, end):
            yield y

    if cyclic:

        yield start + shift


def verts_sequence_calc(curve) -> Iterator[int]:

    last_index = -2  # Индекс последней нулевой вершины меша относящегося к сплайну

    def __func(spline):

        nonlocal last_index

        if spline.type == 'POLY':

            points = spline.points
            spline_type = True

        else:

            points = spline.bezier_points
            spline_type = False

        cyclic = spline.use_cyclic_u
        resolution = spline.resolution_u

        last_index, shift, verts_range = _spline_range_calc(points, spline_type, cyclic, resolution, last_index)

        spline_verts_generator = _verts_range_generator((cyclic, shift, verts_range))

        for i in spline_verts_generator:

            yield i

    for spline in curve.data.splines:

        for i in __func(spline):

            yield i


def get_bm_verts(mesh):

    bm = bmesh.new()
    bm.from_mesh(mesh.data, face_normals=False, vertex_normals=False)
    bm.verts.ensure_lookup_table()
    bmesh.ops.transform(bm, matrix=mesh.matrix_world, verts=bm.verts)

    return bm.verts


def _calc_vert_data(index: int, verts) -> tuple[mathutils.Vector, mathutils.Vector]:

    p_0 = verts[index]
    p_1 = verts[index + 1]
    mid_point_co = midle_point_calc(p_0.co, p_1.co)
    normal = calc_vec(p_0.co, p_1.co, True)

    return mid_point_co, normal


def func(verts_sequence_generator: Iterator[int], verts):

    fisrt_point = _calc_vert_data(next(verts_sequence_generator), verts)

    while True:

        try:

            second_point = _calc_vert_data(next(verts_sequence_generator), verts)

            print(f'{fisrt_point}\n{second_point}')

            fisrt_point = second_point

        except StopIteration:

            break
