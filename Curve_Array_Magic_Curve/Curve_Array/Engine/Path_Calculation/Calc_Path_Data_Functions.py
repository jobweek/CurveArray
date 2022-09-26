import bpy  # type: ignore
import bmesh  # type: ignore
from mathutils import Vector
import numpy as np
from typing import Iterator, Union
from ...Property.Get_Property_Path import get_curve_props
from Curve_Array_Magic_Curve.General_Functions.Functions import (
    midle_point_calc,
    calc_vec,
)
from....Errors.Errors import show_message_box, CancelError


def _get_smooth_direction(direction_prev: Union[Vector, None], direction: Vector, direction_next: Union[Vector, None])\
        -> tuple[Vector, Vector]:

    if direction_prev is None:
        direction_smooth_start = direction
    else:
        direction_smooth_start = direction_prev.lerp(direction, 0.5).normalized()

    if direction_next is None:
        direction_smooth_end = direction
    else:
        direction_smooth_end = direction.lerp(direction_next, 0.5).normalized()

    return direction_smooth_start, direction_smooth_end


class InterpolatedSegment:

    class_count = 0

    def __init__(self, start_co: Vector, direction: Vector, length: float, normal: tuple[Vector, Vector]):

        self.__class__.class_count += 1
        self.start_co = start_co
        self.direction = direction
        self.length = length
        self.normal = normal

    def __str__(self):

        string = f'\nSubClass {self.__class__.__name__}:\nStart_Co: {self.start_co}' \
                 f'\nDirection_Vec: {self.direction}\nLength: {self.length}\nNormal: {self.normal}\n'

        return string

    def get_data_by_length(self, searched_length: float) -> tuple[Vector, Vector, Vector]:
        """Searched_length = distance between 'start distance' and searched point"""
        ratio = searched_length / self.length

        if searched_length < 0:
            normal = self.normal[0]
        elif searched_length > self.length:
            normal = self.normal[1]
        else:
            normal = self.normal[0].lerp(self.normal[1], ratio).normalized()

        co = self.start_co + self.direction * ratio

        return co, self.direction.normalized(), normal

    def get_data_by_length_smooth(self, searched_length: float, direction_smooth_start: Vector,
                                  direction_smooth_end: Vector) -> tuple[Vector, Vector, Vector]:
        """Searched_length = distance between 'start distance' and searched point"""
        ratio = searched_length / self.length

        if searched_length < 0:
            normal = self.normal[0]
            direction = self.direction.normalized()
        elif searched_length > self.length:
            normal = self.normal[1]
            direction = self.direction.normalized()
        else:
            normal = self.normal[0].lerp(self.normal[1], ratio).normalized()
            direction = direction_smooth_start.lerp(direction_smooth_end, ratio).normalized()

        co = self.start_co + self.direction * ratio

        return co, direction, normal


class PathData:

    def __init__(self, curve_name: str, arrays: tuple[np.ndarray, np.ndarray]):

        self.curve_name = curve_name
        self.interpolated_segment_distance, self.interpolated_segment = arrays

    def __str__(self):

        string = f'Class {self.__class__.__name__}:'

        for i, _ in enumerate(self.interpolated_segment_distance):

            part = f'\nIndex: {i}, Distance: {self.interpolated_segment_distance[i]}\n{self.interpolated_segment[i]}'

            string += part

        return string

    def get_data_by_distance(self, searched_distance: float, smooth_normal: bool) -> tuple[Vector, Vector, Vector]:

        if searched_distance < 0:

            element: InterpolatedSegment = self.interpolated_segment[0]
            searched_length = searched_distance

        elif searched_distance > self.interpolated_segment_distance[-1]:

            element: InterpolatedSegment = self.interpolated_segment[-1]
            element_distance = self.interpolated_segment_distance[-1]
            searched_length = searched_distance - element_distance + element.length

        else:

            index = np.searchsorted(self.interpolated_segment_distance, searched_distance, side='left')
            element: InterpolatedSegment = self.interpolated_segment[index]
            element_distance = self.interpolated_segment_distance[index]
            searched_length = element.length - (element_distance - searched_distance)

            if smooth_normal:
                if index == 0:
                    direction_prev = None
                    direction_next = self.interpolated_segment[index+1].direction.normalized()
                elif index == len(self.interpolated_segment_distance) - 1:
                    direction_prev = self.interpolated_segment[index-1].direction.normalized()
                    direction_next = None
                else:
                    direction_prev = self.interpolated_segment[index-1].direction.normalized()
                    direction_next = self.interpolated_segment[index+1].direction.normalized()

                direction_smooth_start, direction_smooth_end = \
                    _get_smooth_direction(direction_prev, element.direction.normalized(), direction_next)

                return element.get_data_by_length_smooth(searched_length, direction_smooth_start, direction_smooth_end)

        return element.get_data_by_length(searched_length)

    def get_path_length(self) -> float:
        return self.interpolated_segment_distance[-1]


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


def __project_vec(direction: Vector, normal: Vector) -> Vector:

    dot = normal.dot(direction)

    if dot > 0.99998 or dot < -0.99998:

        raise AssertionError

    elif 0.00002 > dot > -0.00002:

        return normal

    else:

        return (normal - normal.project(direction)).normalized()


def _calc_segment_data(fisrt_point: tuple[Vector, Vector], second_point: tuple[Vector, Vector]
                       ) -> tuple[float, InterpolatedSegment]:

    direction = calc_vec(fisrt_point[0], second_point[0], False)

    length = direction.length

    first_normal = __project_vec(direction, fisrt_point[1])
    second_normal = __project_vec(direction, second_point[1])

    segment = InterpolatedSegment(fisrt_point[0], direction, length, (first_normal, second_normal))

    return length, segment


def arr_size_calc(verts, curve) -> int:

    size = len(verts)/2 - 1

    for s in curve.data.splines:

        if s.use_cyclic_u:

            size += 1

    return int(size)


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


def get_curve():

    try:
        return bpy.context.scene.objects[get_curve_props().name]
    except KeyError:
        show_message_box("Error", f"Curve {get_curve_props().name} could not be found, "
                                  f"it has been removed from the scene or renamed.", 'ERROR')
        raise CancelError
