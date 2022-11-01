import bpy  # type: ignore
import bmesh  # type: ignore
from math import pi, sin, asin
from mathutils import Vector  # type: ignore
from decimal import Decimal, getcontext
import numpy as np
from typing import Iterator, Union
from ...Property.Get_Property_Path import get_curve_props
from ...General_Functions.Functions import (
    midle_point_calc,
    calc_vec,
)
from....Errors.Errors import show_message_box, CancelError, LoopEnd


def _project_vec(direction: Vector, normal: Vector) -> Vector:

    dot = normal.dot(direction)

    if dot > 0.99998 or dot < -0.99998:
        raise AssertionError
    elif 0.00002 > dot > -0.00002:
        return normal
    else:
        return (normal - normal.project(direction)).normalized()


class InterpolatedSegment:

    def __init__(self, start_co: Vector, direction: Vector, length: float, normal: tuple[Vector, Vector]):

        self.start_co = start_co
        self.direction = direction
        self.direction_normalized = direction.normalized()
        self.direction_smooth: Union[Vector, None] = None
        self.length = length
        self.normal = normal

    def __str__(self):

        string = f'\nSubClass {self.__class__.__name__}:\nStart_Co: {self.start_co}' \
                 f'\nDirection_Vec: {self.direction}\nLength: {self.length}\nNormal: {self.normal}\n'

        return string

    def get_co_by_length(self, searched_length: float) -> Vector:

        ratio = searched_length / self.length
        co = self.start_co + self.direction * ratio

        return co

    def get_data_by_length(self, searched_length: float) -> tuple[Vector, Vector, Vector]:

        ratio = searched_length / self.length

        if searched_length < 0:
            normal = self.normal[0]
        elif searched_length > self.length:
            normal = self.normal[1]
        else:
            normal = self.normal[0].lerp(self.normal[1], ratio)

        co = self.start_co + self.direction * ratio

        return co, self.direction_normalized, normal

    def get_data_by_length_smooth(self, searched_length: float, cyclic: bool) -> tuple[Vector, Vector, Vector]:

        ratio = searched_length / self.length
        middle_length = self.length/2

        if searched_length < 0:
            direction = self.direction_smooth[0]
            normal = self.normal[0]
        elif searched_length > self.length:
            direction = self.direction_smooth[1]
            normal = self.normal[1]
        else:
            if searched_length < middle_length and (cyclic or not hasattr(self, "first")):
                middle_ratio = 0.5 + ((searched_length / middle_length) / 2)
                direction = self.direction_smooth[0].lerp(self.direction_normalized, middle_ratio)
            elif searched_length > middle_length and (cyclic or not hasattr(self, "last")):
                middle_ratio = ((searched_length - middle_length) / middle_length) / 2
                direction = self.direction_normalized.lerp(self.direction_smooth[1], middle_ratio)
            else:
                direction = self.direction_normalized
            normal = self.normal[0].lerp(self.normal[1], ratio)
            normal = _project_vec(direction, normal)
        co = self.start_co + self.direction * ratio

        return co, direction, normal


def _searched_distance_cyclic(searched_distance: Decimal, path_length: Decimal) -> Decimal:

    getcontext().prec = 60
    prec = Decimal('1.000000000')

    if searched_distance.quantize(prec) != path_length.quantize(prec):
        searched_distance = searched_distance % path_length
    if searched_distance < 0:
        searched_distance += path_length

    return searched_distance


def _get_path_distance(self, index: int, ratio: float, searched_length: float) -> int:

    path_distance = self.interpolated_segment_distance[index] + self.interpolated_segment[index].length * (ratio - 1)
    path_distance += searched_length

    return path_distance


def _get_index_and_ratio(index: int, element_count: int) -> tuple[int, float]:

    if index >= element_count:
        ratio = index - (element_count - 1)
        index = element_count - 1
    elif index < 0:
        ratio = -index
        index = 0
    else:
        ratio = 0

    return index, ratio


def _get_smooth_direction(
    direction_prev: Union[Vector, None], direction: Vector, direction_next: Union[Vector, None]
                          ) -> tuple[Vector, Vector]:

    if direction_prev is None:
        direction_smooth_start = direction
    else:
        direction_smooth_start = direction_prev.lerp(direction, 0.5).normalized()

    if direction_next is None:
        direction_smooth_end = direction
    else:
        direction_smooth_end = direction.lerp(direction_next, 0.5).normalized()

    return direction_smooth_start, direction_smooth_end


def _calc_length_by_pivot(a_side: Vector, b_side: Vector, pivot: float) -> float:

    dot = a_side.normalized().dot(b_side.normalized())

    if dot < -0.99998:
        return a_side.length + pivot

    elif 0.99998 < dot:
        return pivot - a_side.length

    g_side: Vector = a_side - b_side
    betta_angle = a_side.angle(g_side)
    relation = pivot / sin(betta_angle)
    alpha_angle = asin(a_side.length / relation)
    gamma_angle = pi - (alpha_angle + betta_angle)

    return relation * sin(gamma_angle)


def _get_element_and_length(self, searched_distance: Decimal, cyclic: bool) -> tuple[InterpolatedSegment, float]:

    if cyclic:
        searched_distance = _searched_distance_cyclic(
            searched_distance, Decimal(self.interpolated_segment_distance[-1])
        )
    searched_distance = float(searched_distance)

    if searched_distance < 0:

        element: InterpolatedSegment = self.interpolated_segment[0]
        searched_length: float = searched_distance

    elif searched_distance > self.interpolated_segment_distance[-1]:

        element: InterpolatedSegment = self.interpolated_segment[-1]
        element_distance: float = self.interpolated_segment_distance[-1]
        searched_length: float = searched_distance - element_distance + element.length

    else:

        index = np.searchsorted(self.interpolated_segment_distance, searched_distance, side='left')
        element: InterpolatedSegment = self.interpolated_segment[index]
        element_distance: float = self.interpolated_segment_distance[index]
        searched_length: float = element.length - (element_distance - float(searched_distance))

    return element, searched_length


def _calc_range_vec(element: InterpolatedSegment, ratio: float, start_co: Vector) -> Vector:

    vec_co = element.start_co + element.direction * ratio

    return calc_vec(start_co, vec_co, False)


def _calc_direction_vec(element: InterpolatedSegment, ratio: float, searched_length: float, start_co: Vector) -> Vector:

    vec_co = element.get_co_by_length(searched_length) + element.direction * ratio

    return calc_vec(start_co, vec_co, True)


def _get_index(self, pivot_distance: Decimal) -> int:

    searched_distance = float(pivot_distance)
    index = np.searchsorted(self.interpolated_segment_distance, searched_distance, side='left')

    return index


def _calc_normal_vec(start_normal_vec: Vector, start_direct_vec: Vector, direction_vec: Vector) -> Vector:

    dot = start_normal_vec.dot(direction_vec)

    if dot > 0.99998:
        normal_vec = -start_direct_vec
    elif dot < -0.99998:
        normal_vec = start_direct_vec
    elif 0.00002 > dot > -0.00002:
        normal_vec = start_normal_vec
    else:
        normal_vec = _project_vec(direction_vec, start_normal_vec)

    return normal_vec


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

    def get_data_by_distance(
        self, searched_distance: Decimal, smooth_normal: bool, cyclic: bool
                             ) -> tuple[Vector, Vector, Vector]:

        element, searched_length = _get_element_and_length(self, searched_distance, cyclic)

        if smooth_normal:
            return element.get_data_by_length_smooth(searched_length, cyclic)
        else:
            return element.get_data_by_length(searched_length)

    def get_data_by_origin_cyclic(
        self, searched_distance: Decimal, pivot: float
    ) -> tuple[Vector, Vector, Vector, Decimal]:

        element_count = len(self.interpolated_segment)
        path_length = Decimal(self.interpolated_segment_distance[-1])

        searched_distance = _searched_distance_cyclic(
            searched_distance, Decimal(self.interpolated_segment_distance[-1])
        )

        element, searched_length = _get_element_and_length(self, searched_distance, False)
        start_co, start_direct_vec, start_normal_vec = element.get_data_by_length(searched_length)

        pivot_distance = _searched_distance_cyclic(searched_distance + Decimal(pivot), path_length)

        if element_count == 1 and pivot_distance < searched_distance:
            raise LoopEnd

        start_index = _get_index(self, pivot_distance)
        stop_index = 0

        while True:

            if start_index >= element_count:
                index = start_index % element_count
            elif start_index < 0:
                index = element_count - (start_index % element_count)
            else:
                index = start_index

            element: InterpolatedSegment = self.interpolated_segment[index]

            try:
                first_vec = _calc_range_vec(element, 0, start_co)
            except AssertionError:
                searched_length = pivot
                direction_vec = _calc_direction_vec(element, 0, searched_length, start_co)
                path_distance = _get_path_distance(self, index, 0, searched_length)
                normal_vec = _calc_normal_vec(start_normal_vec, start_direct_vec, direction_vec)

                return start_co, direction_vec, normal_vec, Decimal(path_distance)

            try:
                second_vec = _calc_range_vec(element, 1, start_co)
            except AssertionError:
                raise LoopEnd

            if first_vec.length > pivot and (first_vec.normalized() @ second_vec.normalized() > -0.99998):
                raise LoopEnd

            if pivot < second_vec.length:
                searched_length = _calc_length_by_pivot(first_vec, second_vec, pivot)
                direction_vec = _calc_direction_vec(element, 0, searched_length, start_co)
                path_distance = _get_path_distance(self, index, 0, searched_length)
                normal_vec = _calc_normal_vec(start_normal_vec, start_direct_vec, direction_vec)

                return start_co, direction_vec, normal_vec, Decimal(path_distance)

            stop_index += 1
            if stop_index >= element_count:
                raise LoopEnd
            start_index += 1

    def get_data_by_origin(
        self, searched_distance: Decimal, pivot: float
                           ) -> tuple[Vector, Vector, Vector, Decimal]:

        element_count = len(self.interpolated_segment)
        path_length = Decimal(self.interpolated_segment_distance[-1])

        element, searched_length = _get_element_and_length(self, searched_distance, False)
        start_co, start_direct_vec, start_normal_vec = element.get_data_by_length(searched_length)

        pivot_distance = searched_distance + Decimal(pivot)

        if pivot_distance < Decimal(0) or pivot_distance > path_length:

            element, searched_length = _get_element_and_length(self, pivot_distance, False)
            direction_vec = _calc_direction_vec(element, 0, searched_length, start_co)
            normal_vec = _calc_normal_vec(start_normal_vec, start_direct_vec, direction_vec)

            return start_co, direction_vec, normal_vec, Decimal(pivot_distance)

        start_index = _get_index(self, pivot_distance)

        while True:

            if start_index >= element_count:
                ratio = start_index - (element_count - 1)
                index = element_count - 1
            elif start_index < 0:
                ratio = -start_index
                index = 0
            else:
                ratio = 0
                index = start_index

            element: InterpolatedSegment = self.interpolated_segment[index]

            try:
                first_vec = _calc_range_vec(element, ratio, start_co)
            except AssertionError:
                searched_length = pivot
                direction_vec = _calc_direction_vec(element, ratio, searched_length, start_co)
                path_distance = _get_path_distance(self, index, ratio, searched_length)
                normal_vec = _calc_normal_vec(start_normal_vec, start_direct_vec, direction_vec)

                return start_co, direction_vec, normal_vec, Decimal(path_distance)

            try:
                second_vec = _calc_range_vec(element, ratio + 1, start_co)
            except AssertionError:
                raise LoopEnd

            if first_vec.length > pivot and (first_vec.normalized() @ second_vec.normalized() > -0.99998):
                raise LoopEnd

            if pivot < second_vec.length:
                searched_length = _calc_length_by_pivot(first_vec, second_vec, pivot)
                direction_vec = _calc_direction_vec(element, ratio, searched_length, start_co)
                path_distance = _get_path_distance(self, index, ratio, searched_length)
                normal_vec = _calc_normal_vec(start_normal_vec, start_direct_vec, direction_vec)

                return start_co, direction_vec, normal_vec, Decimal(path_distance)

            start_index += 1

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


def verts_sequence_calc(curve) -> Iterator[Union[int, None]]:

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

        yield None

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

    direction = calc_vec(fisrt_point[0], second_point[0], False)

    length = direction.length

    first_normal = _project_vec(direction.normalized(), fisrt_point[1]).normalized()
    second_normal = _project_vec(direction.normalized(), second_point[1]).normalized()

    segment = InterpolatedSegment(fisrt_point[0], direction, length, (first_normal, second_normal))

    return length, segment


def arr_size_calc(verts, curve) -> int:

    size = len(verts)/2

    for s in curve.data.splines:
        if not s.use_cyclic_u:
            size -= 1

    return int(size)


def _calc_smooth_direction(interpolated_segments_arr: np.ndarray, start_range: int, end_range: int,):

    if start_range == end_range:
        interpolated_segments_arr[start_range].direction_smooth = \
            interpolated_segments_arr[start_range].direction_normalized
        return

    interpolated_segments_arr[start_range].direction_smooth = (
        interpolated_segments_arr[start_range].direction_normalized,
        interpolated_segments_arr[start_range + 1].direction_normalized
    )

    interpolated_segments_arr[end_range].direction_smooth = (
        interpolated_segments_arr[end_range - 1].direction_normalized,
        interpolated_segments_arr[end_range].direction_normalized
    )

    i = start_range + 1
    while i < end_range:
        interpolated_segments_arr[i].direction_smooth = \
            (interpolated_segments_arr[i-1].direction_normalized, interpolated_segments_arr[i+1].direction_normalized)
        i += 1


def path_data_calc(verts_sequence_generator: Iterator[Union[int, None]], verts, arr_size: int, curve_name: str
                   ) -> PathData:

    interpolated_segments_distance_arr = np.empty(arr_size, float)
    interpolated_segments_arr = np.empty(arr_size, object)

    distance = 0.0
    vert_index = next(verts_sequence_generator)
    fisrt_point = _calc_vert_data(vert_index, verts)

    i = 0
    start_range = i
    while True:
        try:
            vert_index = next(verts_sequence_generator)

            if vert_index is None:
                _calc_smooth_direction(interpolated_segments_arr, start_range, end_range=(i - 1))

                vert_index = next(verts_sequence_generator)
                fisrt_point = _calc_vert_data(vert_index, verts)
                start_range = i
                continue

            second_point = _calc_vert_data(vert_index, verts)

            length, segment = _calc_segment_data(fisrt_point, second_point)
            distance += length

            interpolated_segments_distance_arr[i] = distance
            interpolated_segments_arr[i] = segment

            fisrt_point = second_point
            i += 1

        except StopIteration:
            break

    assert i == arr_size, 'PathData, массив не заполнен'

    interpolated_segments_arr[0].first = True
    interpolated_segments_arr[0].direction_smooth = (
        interpolated_segments_arr[-1].direction_normalized,
        interpolated_segments_arr[1].direction_normalized
    )

    interpolated_segments_arr[-1].last = True
    interpolated_segments_arr[-1].direction_smooth = (
        interpolated_segments_arr[-2].direction_normalized,
        interpolated_segments_arr[0].direction_normalized
    )

    path_data = PathData(curve_name, (interpolated_segments_distance_arr, interpolated_segments_arr))

    return path_data


def get_curve():

    try:
        return bpy.context.scene.objects[get_curve_props().name]
    except KeyError:
        show_message_box("Error", f"Curve {get_curve_props().name} could not be found, "
                                  f"it has been removed from the scene or renamed.", 'ERROR')
        raise CancelError
