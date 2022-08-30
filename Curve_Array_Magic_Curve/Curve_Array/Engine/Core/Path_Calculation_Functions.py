import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils
import numpy as np

from Curve_Array_Magic_Curve.General_Functions.Functions import (
    midle_point_calc,
    calc_vec,
)
from typing import Iterator
Vector = mathutils.Vector


class InterpolatedSegment:

    class_count = 0

    def __init__(self, start_co: Vector, direction_vec: Vector, length: float, normal: tuple[Vector, Vector]):

        self.__class__.class_count += 1
        self.start_co = start_co
        self.direction_vec = direction_vec
        self.length = length
        self.normal = normal

    def __str__(self):

        string = f'SubClass {self.__class__.__name__}:\nStart_Co: {self.start_co}' \
                 f'\nDirection_Vec: {self.direction_vec}\nLength: {self.length}\nNormal: {self.normal}'

        return string


class PathData:

    def __init__(self, curve_name: str, arrays: tuple[np.ndarray, np.ndarray]):

        self.curve_name = curve_name
        self.interpolated_splines_distance, self.interpolated_splines = arrays

    def __str__(self):

        string = f'Class {self.__class__.__name__}:'

        for i, _ in enumerate(self.interpolated_splines_distance):

            part = f'\nIndex: {i}, Distance: {self.interpolated_splines_distance[i]}\n{self.interpolated_splines[i]}'

            string += part

        return string

    def get_nearest(self, distance: float) -> InterpolatedSegment:

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

    return bm


def _calc_vert_data(index: int, verts) -> tuple[Vector, Vector]:

    p_0 = verts[index]
    p_1 = verts[index + 1]
    mid_point_co = midle_point_calc(p_0.co, p_1.co)
    normal = calc_vec(p_0.co, p_1.co, True)

    return mid_point_co, normal


def _calc_segment_data(fisrt_point: tuple[Vector, Vector], second_point: tuple[Vector, Vector]
                       ) -> tuple[float, InterpolatedSegment]:

    direction_vec = calc_vec(fisrt_point[0], second_point[0], False)

    length = direction_vec.length

    segment = InterpolatedSegment(fisrt_point[0], direction_vec, length, (fisrt_point[1], second_point[1]))

    return length, segment


def path_data_calc(verts_sequence_generator: Iterator[int], verts, arr_size: int, curve_name: str) -> PathData:

    interpolated_splines_distance_arr = np.empty(arr_size, float)
    interpolated_splines_arr = np.empty(arr_size, object)

    distance = 0.0
    fisrt_point = _calc_vert_data(next(verts_sequence_generator), verts)

    i = 0

    while True:

        try:

            second_point = _calc_vert_data(next(verts_sequence_generator), verts)

            length, segment = _calc_segment_data(fisrt_point, second_point)
            distance += length

            interpolated_splines_distance_arr[i] = distance
            interpolated_splines_arr[i] = segment

            fisrt_point = second_point
            i += 1

        except StopIteration:

            break

    assert i == arr_size, 'PathData, массив не заполнен'

    path_data = PathData(curve_name, (interpolated_splines_distance_arr, interpolated_splines_arr))

    return path_data
