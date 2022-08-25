import copy
import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import math
import numpy as np
from typing import Final
from ..Errors.Errors import (
    show_message_box,
    CancelError,
)

RAD_CIRCLE_CONST: Final = math.pi * 2


class CreationCurveData:

    def __init__(self):
        self.__curve = None
        self.__cyclic = None

    def __repr__(self):
        return f'{self.__class__.__name__}{self.__curve!r}, {self.__cyclic!r}'

    def set_curve(self, curve):
        self.__curve = curve

    def get_curve(self):
        return self.__curve

    def set_cyclic(self, cyclic):
        self.__cyclic = cyclic

    def get_cyclic(self):
        return self.__cyclic


def curve_creation_start_check():

    objects = bpy.context.selected_objects

    if len(objects) == 0:

        show_message_box("Error", "Select object.", 'ERROR')

        raise CancelError

    elif len(objects) > 1:

        show_message_box("Error", "Select only one object.", 'ERROR')

        raise CancelError

    if objects[0].type != 'MESH':

        show_message_box("Error", "Object should be mesh.", 'ERROR')

        raise CancelError

    if bpy.context.active_object.mode != 'EDIT':

        show_message_box("Error", "Go to Edit Mode", 'ERROR')

        raise CancelError


def active_vertex(bm):

    act_vert = bm.select_history.active

    if act_vert is None:

        show_message_box("Error", "The active vertex must be selected.", 'ERROR')

        raise CancelError

    return act_vert


def _merged_vertices_check(selected_linked_edges_buffer, searched_vertex):

    for edge in selected_linked_edges_buffer:

        if vec_equal(edge.other_vert(searched_vertex).co, searched_vertex.co):

            show_message_box(
                "Error",
                "In the sequence you have chosen, there are vertices in the same coordinates."
                " You can merge it. Their indices: "
                f"({edge.other_vert(searched_vertex).index}, {searched_vertex.index})",
                'ERROR'
            )

            raise CancelError


def _selected_linked_edges(searched_vertex):

    linked_edges = searched_vertex.link_edges

    selected_linked_edges_buffer = []

    for edge in linked_edges:

        if edge.select:
            selected_linked_edges_buffer.append(edge)

    _merged_vertices_check(selected_linked_edges_buffer, searched_vertex)

    return selected_linked_edges_buffer


def verts_sequence(verts_count: int, act_vert, split_curve: bool):

    # Класс содержащий информацию о кривой
    curve_data = CreationCurveData()

    # Определим циклична ли последовательность
    selected_linked_edges_buffer = _selected_linked_edges(act_vert)

    if len(selected_linked_edges_buffer) == 0:

        show_message_box(
            "Error",
            "No existing edges at selected sequence.",
            'ERROR'
        )

        raise CancelError

    elif len(selected_linked_edges_buffer) == 1:

        curve_data.set_cyclic(False)

    elif len(selected_linked_edges_buffer) == 2:

        curve_data.set_cyclic(True)

    else:

        show_message_box(
            "Error",
            "Make sure that the sequence of vertices does not intersect or branch.",
            'ERROR'
        )

        raise CancelError

    # Создадим массив фиксированной длины
    if split_curve and curve_data.get_cyclic():

        vert_sequence_array = np.empty(verts_count + 1, dtype=object)
        vert_sequence_array[-1] = act_vert

    else:

        vert_sequence_array = np.empty(verts_count, dtype=object)

    # Наполняем массив
    vert_sequence_array[0] = act_vert

    linked_edge = selected_linked_edges_buffer[0]
    searched_vertex = linked_edge.other_vert(act_vert)

    i = 1

    while i < verts_count - 1:

        vert_sequence_array[i] = searched_vertex

        selected_linked_edges_buffer = _selected_linked_edges(searched_vertex)

        if len(selected_linked_edges_buffer) != 2:
            show_message_box(
                "Error",
                "Make sure that the sequence of vertices does not intersect or branch, "
                "and that the vertex at the beginning of the sequence is selected.",
                'ERROR'
            )

            raise CancelError

        if selected_linked_edges_buffer[0] != linked_edge:

            linked_edge = selected_linked_edges_buffer[0]

        else:

            linked_edge = selected_linked_edges_buffer[1]

        searched_vertex = linked_edge.other_vert(searched_vertex)

        i += 1

    vert_sequence_array[i] = searched_vertex

    return vert_sequence_array, curve_data


def vertex_normal_vec(vert_sequence_array):

    y_vec_arr = np.frompyfunc(lambda v: copy.deepcopy(v.normal), 1, 1)

    y_vec_arr = y_vec_arr(vert_sequence_array)

    return y_vec_arr


def vert_co(vert_sequence_array):

    vert_co_array = np.frompyfunc(lambda v: copy.deepcopy(v.co), 1, 1)

    vert_co_array = vert_co_array(vert_sequence_array)

    return vert_co_array


def duplicate(active_curve):

    duplicate_curve = active_curve.copy()
    duplicate_curve.data = active_curve.data.copy()

    if active_curve.animation_data:
        duplicate_curve.animation_data.action = active_curve.animation_data.action.copy()

    for i in active_curve.users_collection:

        i.objects.link(duplicate_curve)

    return duplicate_curve


def convert_to_mesh(curve):

    curve.data.extrude = 0.5
    curve.data.offset = 0.0
    curve.data.taper_object = None
    curve.data.bevel_depth = 0.0
    curve.data.bevel_object = None
    bpy.ops.object.select_all(action='DESELECT')
    curve.select_set(True)
    bpy.context.view_layer.objects.active = curve
    bpy.ops.object.convert(target='MESH')
    mesh = bpy.context.active_object

    return mesh


def ext_vec_curve_creation(extruded_mesh, array_size: int, step: int):

    def __func(i):

        first_point = extruded_mesh.data.vertices[i]
        second_point = extruded_mesh.data.vertices[i + 1]

        vector = calc_vec(first_point.co, second_point.co, True)

        return vector

    ext_vec_arr = np.frompyfunc(__func, 1, 1)
    ext_vec_arr = ext_vec_arr(range(0, array_size*step, step))

    return ext_vec_arr


def curve_methods_start_checker():

    objects = bpy.context.selected_objects

    if len(objects) == 0:

        show_message_box("Error", "Select object", 'ERROR')

        raise CancelError

    elif len(objects) > 1:

        show_message_box("Error", "Select only one object", 'ERROR')

        raise CancelError

    if objects[0].type != 'CURVE':

        show_message_box("Error", "Object should be curve", 'ERROR')

        raise CancelError

    mode = bpy.context.active_object.mode

    if mode != 'OBJECT':
        show_message_box("Error", "Go to Object Mode", 'ERROR')

        raise CancelError


def merged_points_check(curve):

    merged_points_buffer = []
    error_case = False

    for spline_iter, spline in enumerate(curve.data.splines):

        if spline.type == 'POLY':

            points = spline.points

        elif spline.type == 'BEZIER':

            points = spline.bezier_points

        else:

            show_message_box("Error", "Nurbs curves are not supported", 'ERROR')

            raise CancelError

        merged_points_buffer.append([])

        for i in range(len(points)-1):

            if vec_equal(points[i].co, points[i+1].co):

                merged_points_buffer[spline_iter].append([i, i+1])
                error_case = True

        if spline.use_cyclic_u:

            if vec_equal(points[-1].co, points[0].co):

                merged_points_buffer[spline_iter].append([-1, 0])
                error_case = True

    if error_case:

        verts_str = ""

        for i, item in enumerate(merged_points_buffer):

            if len(item) != 0:

                verts_str += "Spline: {0}, Points: ".format(i)

                for p in item:

                    verts_str += "({0},{1}) ".format(p[0], p[1])

        show_message_box(
            "Error",
            "In the curve you have chosen, there are points in the same coordinates."
            " You can remove it."
            " Their place: " + verts_str,
            'ERROR'
        )

        raise CancelError


def points_select(curve):

    for s in curve.data.splines:

        if s.type == 'POLY':

            for p in s.points:

                p.select = True

        elif s.type == 'BEZIER':

            for p in s.bezier_points:

                p.select_control_point = True

        else:

            show_message_box("Error", "Nurbs curves are not supported", 'ERROR')

            raise CancelError


def curve_data(curve):

    splines = curve.data.splines
    spline_count = len(splines)

    # Количество точек на каждом сплайне
    spline_point_count_arr = np.empty(spline_count, dtype=int)

    # Массив индексов вершин меша соответствующих точкам сплайна
    spline_verts_index_arr = np.empty(spline_count, dtype=object)

    # Cyclic == True; Non_Cyclic == False;
    spline_cyclic_arr = np.empty(spline_count, dtype=bool)

    # Poly == True; Bezier == False;
    spline_type_arr = np.empty(spline_count, dtype=bool)

    # Координаты правого хэндла для нулевой точки и левого для последней
    spline_start_end_handle_arr = np.empty(spline_count, dtype=object)

    last_index = -2  # Индекс последней нулевой вершины меша относящегося к сплайну

    for spline_iter, spline in enumerate(splines):

        if spline.type == 'POLY':

            points = spline.points
            spline_type = True

        else:

            points = spline.bezier_points
            spline_type = False
            spline_start_end_handle_arr[spline_iter] = [
                copy.deepcopy(points[0].handle_right),
                copy.deepcopy(points[-1].handle_left)
            ]

        cyclic = spline.use_cyclic_u
        resolution = spline.resolution_u

        spline_point_count_arr[spline_iter] = len(points)
        spline_verts_index_arr[spline_iter], last_index = \
            _spline_verts_index(points, spline_type, cyclic, resolution, last_index)
        spline_cyclic_arr[spline_iter] = cyclic
        spline_type_arr[spline_iter] = spline_type

    return (
        spline_point_count_arr,
        spline_verts_index_arr,
        spline_cyclic_arr,
        spline_type_arr,
        spline_start_end_handle_arr
    )


def angle_arr_get(curve):

    splines = curve.data.splines

    # Возвращает массив содержащий углы поворта кажждой точки для одного сплайна
    def __func(spline_iter):

        if splines[spline_iter].type == 'POLY':

            points = splines[spline_iter].points

        else:

            points = splines[spline_iter].bezier_points

        # Возвращает угл поворта точки
        def __under_func(point_iter):

            angle = points[point_iter].tilt

            return angle

        spline_angle_arr = np.frompyfunc(__under_func, 1, 1)
        spline_angle_arr = spline_angle_arr(range(len(points)))

        return spline_angle_arr

    angle_arr = np.frompyfunc(__func, 1, 1)
    angle_arr = angle_arr(range(len(splines)))

    return angle_arr


def point_direction_vec(mesh, curve_data):

    (
        spline_point_count_arr,
        spline_verts_index_arr,
        cyclic_arr,
        spline_type_arr,
        spline_start_end_handle_arr,
    ) = curve_data

    ext_vec_arr = create_arr(spline_point_count_arr)
    verts = mesh.data.vertices

    for spline_iter, ext_arr in enumerate(ext_vec_arr):

        for point_iter in range(len(ext_arr)):

            first_point_index = spline_verts_index_arr[spline_iter][point_iter]

            first_point = verts[first_point_index]
            second_point = verts[first_point_index + 1]

            ext_vec = calc_vec(first_point.co, second_point.co, True)

            ext_arr[point_iter] = ext_vec

    return ext_vec_arr


def _tilt_twist_calc(fist_angle, second_angle):

    twist = second_angle - fist_angle

    if fist_angle > second_angle:

        twist = -(abs(twist) // RAD_CIRCLE_CONST)

    elif fist_angle < second_angle:

        twist = twist // RAD_CIRCLE_CONST

    else:

        twist = 0

    return twist


def _twist_levelling(points_tilt_arr):

    min_tilt = int(np.amin(points_tilt_arr)/(math.pi * 2))
    max_tilt = int(np.amax(points_tilt_arr)/(math.pi * 2))

    tilt_range_diff = (max_tilt - min_tilt)

    if tilt_range_diff > 1:

        min_range = -tilt_range_diff//2

        global_tilt_diff = min_range - min_tilt

        for i, _ in enumerate(points_tilt_arr):

            points_tilt_arr[i] += global_tilt_diff * RAD_CIRCLE_CONST

    return points_tilt_arr


def _twist_correction(twist_old, twist_new):

    diff = twist_old - twist_new

    rad_diff = diff * RAD_CIRCLE_CONST

    return rad_diff


def tilt_correction(curve_angle_arr_new, curve):

    splines = curve.data.splines

    for spline_iter, spline in enumerate(splines):

        if spline.type == 'POLY':

            points = spline.points

        else:

            points = spline.bezier_points

        curve_angle_arr_new[spline_iter] = _twist_levelling(curve_angle_arr_new[spline_iter])

        for point_iter, point in enumerate(points):

            point.tilt = curve_angle_arr_new[spline_iter][point_iter]


def angle_arr_calc(y_vec_arr, ext_vec_arr, z_vec_arr, curve):

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


def vec_equal(vec_1, vec_2):

    return vec_1.to_tuple(4) == vec_2.to_tuple(4)


def _spline_verts_index(points, spline_type, cyclic, resolution, last_index):

    arr = np.empty(len(points), dtype=int)

    vert_index = last_index + 2

    if cyclic and not spline_type:

        if points[-1].handle_right_type != 'VECTOR' or points[0].handle_left_type != 'VECTOR':

            vert_index += 2 * resolution

        else:

            vert_index += 2

    for i in range(len(points)-1):

        arr[i] = vert_index

        if spline_type or (points[i].handle_right_type == 'VECTOR' and points[i + 1].handle_left_type == 'VECTOR'):

            vert_index += 2

        else:

            vert_index += 2 * resolution

    if cyclic and not spline_type:

        arr[-1] = last_index + 2
        last_index = vert_index - 2

    else:

        arr[-1] = vert_index
        last_index = vert_index

    return arr, last_index


def calc_vec(first_co, second_co, normalize: bool):

    vec = second_co - first_co

    if vec.length < 0.00002:

        return None

    if normalize:

        vec = vec.normalized()

    return vec


def create_arr(points_count_list):

    arr = np.empty(len(points_count_list), dtype=object)

    for i, item in enumerate(points_count_list):

        arr[i] = np.empty(item, dtype=object)

    return arr


def vec_projection(vec, z_vec):

    dot = vec.dot(z_vec)

    if dot > 0.99998 or dot < -0.99998:

        return None

    elif 0.00002 > dot > -0.00002:

        return vec

    else:

        return (vec - vec.project(z_vec)).normalized()


def angle_calc(ext_vec, y_vec, cross_vec):

    angle = ext_vec.angle(y_vec)
    ext_cross_dot = ext_vec.dot(cross_vec)
    ext_y_dot = ext_vec.dot(y_vec)

    # Вектор ext перпендикулярен y
    if -0.00002 > ext_y_dot < 0.00002:

        angle = math.pi/2

        # Вектор ext соноправлен cross
        if ext_cross_dot > 0:

            angle = -angle

    # Вектор ext параллелен и соноправлен y
    elif ext_y_dot > 0.99998:

        angle = 0

    # Вектор ext параллелен и противонаправлен y
    elif ext_y_dot < -0.99998:

        angle = math.pi

    # Вектор ext соноправлен y
    elif ext_y_dot > 0.00002:

        angle = ext_vec.angle(y_vec)

        # Вектор ext соноправлен cross
        if ext_cross_dot > 0:

            angle = -angle

    # Вектор ext противонаправлен y
    elif ext_y_dot < -0.00002:

        angle = ext_vec.angle(y_vec)

        # Вектор ext соноправлен cross
        if ext_cross_dot > 0:

            angle = RAD_CIRCLE_CONST - abs(angle)

        # Вектор ext противонаправлен cross
        elif ext_cross_dot < 0:

            angle = math.pi - (math.pi - abs(angle))

    else:

        assert False, f'Невозможное условие angle_calc, {ext_y_dot}'

    # print(f'angle: {math.degrees(angle)}, ext: {ext_vec}, y: {y_vec}, cross_vec: {cross_vec}')
    return angle


def midle_point_calc(p_0_ind, verts):

    vec = calc_vec(verts[p_0_ind].co, verts[p_0_ind + 1].co, False)

    midle_point_co = verts[p_0_ind].co + vec/2

    return midle_point_co


def calc_z_vec(p_0_ind, prev_p_0_ind, next_p_0_ind, verts):

    mdidle_point_co = midle_point_calc(p_0_ind, verts)
    prev_mdidle_point_co = midle_point_calc(prev_p_0_ind, verts)
    next_mdidle_point_co = midle_point_calc(next_p_0_ind, verts)

    vec_h_1 = calc_vec(mdidle_point_co, prev_mdidle_point_co, True)
    vec_h_2 = calc_vec(mdidle_point_co, next_mdidle_point_co, True)

    z_vec = calc_vec(vec_h_1, vec_h_2, True)

    return z_vec


def z_vec(mesh, curve_data):

    (
        spline_point_count_arr,
        spline_verts_index_arr,
        cyclic_arr,
        spline_type_arr,
        spline_start_end_handle_arr,
    ) = curve_data

    z_vec_arr = create_arr(spline_point_count_arr)
    verts = mesh.data.vertices

    for spline_iter, z_arr in enumerate(z_vec_arr):

        max_index = np.amax(spline_verts_index_arr[spline_iter])
        min_index = np.amin(spline_verts_index_arr[spline_iter])

        point_iter = 0  # Соответствует индексу поинтов одного сплайна

        if not cyclic_arr[spline_iter]:

            point_index = spline_verts_index_arr[spline_iter][point_iter]
            mid_point = midle_point_calc(point_index, verts)

            if not spline_type_arr[spline_iter]:

                z_arr[point_iter] = calc_vec(
                    mid_point,
                    spline_start_end_handle_arr[spline_iter][0],
                    True
                )

            else:

                next_mid_point = midle_point_calc(point_index+2, verts)

                z_arr[point_iter] = calc_vec(
                    mid_point,
                    next_mid_point,
                    True
                )

            point_iter = 1

        while point_iter < len(z_arr) - 1:

            point_index = spline_verts_index_arr[spline_iter][point_iter]

            prev_point_index = point_index - 2
            if prev_point_index < min_index:
                prev_point_index = max_index

            next_point_index = point_index + 2
            if next_point_index > max_index:
                next_point_index = min_index

            z_arr[point_iter] = calc_z_vec(point_index, prev_point_index, next_point_index, verts)

            point_iter += 1

        if not cyclic_arr[spline_iter]:

            point_index = spline_verts_index_arr[spline_iter][point_iter]
            mid_point = midle_point_calc(point_index, verts)

            if not spline_type_arr[spline_iter]:

                z_arr[point_iter] = calc_vec(
                    spline_start_end_handle_arr[spline_iter][1],
                    mid_point,
                    True
                )

            else:

                prev_mid_point = midle_point_calc(point_index-2, verts)

                z_arr[point_iter] = calc_vec(
                    prev_mid_point,
                    mid_point,
                    True
                )

        else:

            point_index = spline_verts_index_arr[spline_iter][point_iter]

            prev_point_index = point_index - 2
            if prev_point_index < min_index:
                prev_point_index = max_index

            next_point_index = point_index + 2
            if next_point_index > max_index:
                next_point_index = min_index

            z_arr[point_iter] = calc_z_vec(point_index, prev_point_index, next_point_index, verts)

    return z_vec_arr


def main_object_select(obj):

    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
