import copy
import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import math
import numpy as np
from Curve_Array_Pro_Magic_Curve.Errors.Errors import (
    show_message_box,
    CancelError,
)


def object_select(obj):

    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


class CurveData:

    def __init__(self):
        self.__curve = None
        self.__cyclic = None

    def set_curve(self, curve):
        self.__curve = curve

    def get_curve(self):
        return self.__curve

    def set_cyclic(self, cyclic):
        self.__cyclic = cyclic

    def get_cyclic(self):
        return self.__cyclic


def object_checker():

    objects = bpy.context.selected_objects

    if len(objects) == 0:

        show_message_box("Error", "Select object", 'ERROR')

        raise CancelError

    elif len(objects) > 1:

        show_message_box("Error", "Select only one object", 'ERROR')

        raise CancelError

    if objects[0].type != 'MESH':

        show_message_box("Error", "Object should be mesh", 'ERROR')

        raise CancelError

    mode = bpy.context.active_object.mode

    if mode != 'EDIT':

        show_message_box("Error", "Go to Edit Mode", 'ERROR')

        raise CancelError


def active_vertex(bm):
    try:

        act_vert = bm.select_history.active

        if act_vert is None:

            show_message_box("Error", "The active vertex must be selected", 'ERROR')

            raise CancelError

        return act_vert

    except CancelError:

        show_message_box("Error", "The active vertex must be selected", 'ERROR')

        raise CancelError


def verts_sequence(verts_count, act_vert, curve_data, split_curve: bool):

    # Функция извлечения выделенных ребер из всех принадлежащих вершине
    def selected_linked_edges(searched_vertex):

        linked_edges = searched_vertex.link_edges

        selected_linked_edges_buffer = []

        for edge in linked_edges:

            if edge.select:
                selected_linked_edges_buffer.append(edge)

        return selected_linked_edges_buffer

    # Определим циклична ли последовательность
    selected_linked_edges_buffer = selected_linked_edges(act_vert)

    if len(selected_linked_edges_buffer) == 0:

        show_message_box(
            "Error",
            "No existing edges at selected vertex",
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
            "No existing edges at selected vertex",
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

        selected_linked_edges_buffer = selected_linked_edges(searched_vertex)

        if len(selected_linked_edges_buffer) != 2:
            show_message_box(
                "Error",
                "Make sure that the sequence of vertices does not intersect or branch, and that the vertex "
                "at the beginning of the sequence is selected",
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


def merged_vertices_check(vert_sequence_array, split_curve, cyclic: bool):

    i = 0
    merged_vertices_buffer = []

    while i < len(vert_sequence_array)-1:

        if vec_equal(vert_sequence_array[i].co, vert_sequence_array[i+1].co):

            merged_vertices_buffer.append([vert_sequence_array[i].index, vert_sequence_array[i+1].index])

        i += 1

    if not split_curve or (split_curve and not cyclic):

        if vec_equal(vert_sequence_array[i].co, vert_sequence_array[0].co):

            merged_vertices_buffer.append([vert_sequence_array[i].index, vert_sequence_array[0].index])

    if len(merged_vertices_buffer) != 0:

        verts_str = ""

        for v in merged_vertices_buffer:

            verts_str += "({0},{1}) ".format(v[0], v[1])

        show_message_box(
            "Error",
            "In the sequence you have chosen, there are vertices in the same coordinates."
            " You can merge it."
            " Their indices: " + verts_str,
            'ERROR'
        )

        raise CancelError


def y_vec(vert_sequence_array):

    y_vec_arr = np.empty(len(vert_sequence_array), dtype=object)

    i = 0

    while i < len(vert_sequence_array):

        vertex_normal = copy.deepcopy(vert_sequence_array[i].normal)
        y_vec_arr[i] = vertex_normal

        i += 1

    return y_vec_arr


def vert_co(vert_sequence_array):

    vert_co_array = np.frompyfunc(lambda a: copy.deepcopy(a.co), 1, 1)

    vert_co_array = vert_co_array(vert_sequence_array)

    return vert_co_array


def duplicate(active_curve):

    switched_curve = active_curve.copy()
    switched_curve.data = active_curve.data.copy()

    if active_curve.animation_data:
        switched_curve.animation_data.action = active_curve.animation_data.action.copy()

    for i in active_curve.users_collection:

        i.objects.link(switched_curve)

    return switched_curve


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


def curve_checker():

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

    iterator = 0
    merged_points_buffer = []
    error_case = False

    for s in curve.data.splines:

        if s.type == 'POLY':

            points = s.points

        elif s.type == 'BEZIER':

            points = s.bezier_points

        else:

            show_message_box("Error", "Nurbs curves are not supported", 'ERROR')

            raise CancelError

        i = 0
        merged_points_buffer.append([])

        while i < len(points) - 1:

            if vec_equal(points[i].co, points[i+1].co):

                merged_points_buffer[iterator].append([i, i+1])
                error_case = True

            i += 1

        if s.use_cyclic_u:

            if vec_equal(points[i].co, points[0].co):

                merged_points_buffer[iterator].append([i, 0])
                error_case = True

        iterator += 1

    if error_case:

        verts_str = ""
        i = 0

        while i < len(merged_points_buffer):

            if len(merged_points_buffer[i]) != 0:

                verts_str += "Spline: {0}, Points: ".format(i)

                for p in merged_points_buffer[i]:

                    verts_str += "({0},{1}) ".format(p[0], p[1])

            i += 1

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

    # Cyclic == True; Not_Cyclic == False;
    spline_cyclic_arr = np.empty(spline_count, dtype=bool)

    # Poly == True; Bezier == False;
    spline_type_arr = np.empty(spline_count, dtype=bool)

    # Координаты правого хэндла для нулевой точки и левого для последней
    spline_start_end_handle_arr = np.empty(spline_count, dtype=object)

    i = 0
    last_index = -2  # Индекс последней нулевой вершины меша относящегося к сплайну

    while i < len(splines):

        if splines[i].type == 'POLY':

            points = splines[i].points
            spline_type = True

        else:

            points = splines[i].bezier_points
            spline_type = False
            spline_start_end_handle_arr[i] = [
                copy.deepcopy(points[0].handle_right),
                copy.deepcopy(points[-1].handle_left)
            ]

        cyclic = splines[i].use_cyclic_u
        resolution = splines[i].resolution_u

        spline_point_count_arr[i] = len(points)
        spline_verts_index_arr[i], last_index = \
            spline_verts_index(points, spline_type, cyclic, resolution, last_index)
        spline_cyclic_arr[i] = cyclic
        spline_type_arr[i] = spline_type

        i += 1

    return (
        spline_point_count_arr,
        spline_verts_index_arr,
        spline_cyclic_arr,
        spline_type_arr,
        spline_start_end_handle_arr
    )


def tilt_twist_calc(curve):

    splines = curve.data.splines
    tilt_twist_arr = np.empty(len(curve.data.splines), dtype=object)

    spline_iter = 0

    while spline_iter < len(splines):

        if splines[spline_iter].type == 'POLY':

            points = splines[spline_iter].points

        else:

            points = splines[spline_iter].bezier_points

        tilt_twist_arr[spline_iter] = np.empty(len(points)-1, dtype=int)

        i = 0

        while i < len(points)-1:

            twist = points[i+1].tilt - points[i].tilt

            if points[i].tilt > points[i+1].tilt:

                twist = -(abs(twist) // (math.pi * 2))

            elif points[i].tilt < points[i+1].tilt:

                twist = twist // (math.pi * 2)

            else:

                twist = 0

            tilt_twist_arr[spline_iter][i] = twist

            i += 1

        spline_iter += 1

    return tilt_twist_arr


def ext_vec(mesh, curve_data):

    (
        spline_point_count_arr,
        spline_verts_index_arr,
        cyclic_arr,
        spline_type_arr,
        spline_start_end_handle_arr,
    ) = curve_data

    ext_vec_arr = create_arr(spline_point_count_arr)
    verts = mesh.data.vertices
    list_iter = 0

    while list_iter < len(ext_vec_arr):

        ext_arr = ext_vec_arr[list_iter]

        spline_point_iter = 0  # Соответствует индексу поинтов одного сплайна

        while spline_point_iter < len(ext_arr):

            first_point_index = spline_verts_index_arr[list_iter][spline_point_iter]

            first_point = verts[first_point_index]
            second_point = verts[first_point_index + 1]

            ext_vec = calc_vec(first_point.co, second_point.co, True)

            ext_arr[spline_point_iter] = ext_vec

            spline_point_iter += 1

        list_iter += 1

    return ext_vec_arr


def angle_correction(angle_y_ext_arr, angle_y_test_arr):

    list_iter = 0

    while list_iter < len(angle_y_ext_arr):

        y_ext_arr = angle_y_ext_arr[list_iter]
        y_test_arr = angle_y_test_arr[list_iter]

        i = 0

        while i < len(y_ext_arr):

            if y_ext_arr[i] < y_test_arr[i]:

                y_ext_arr[i] = -y_ext_arr[i]

            i += 1

        list_iter += 1

    return angle_y_ext_arr


def tilt_correction(angle_betw_vec_arr, curve, test: bool):

    iterator = 0

    while iterator < len(curve.data.splines):

        s = curve.data.splines[iterator]

        if s.type == 'POLY':

            points = s.points

        else:

            points = s.bezier_points

        i = 0

        while i < len(points):

            angle = angle_betw_vec_arr[iterator][i]

            if test:

                if angle > math.pi/2:

                    angle = (math.pi - angle) * 0.5

                else:

                    angle = angle * 0.5

            new_angle = points[i].tilt + angle

            if new_angle > 376.992:

                show_message_box(
                    "Error",
                    (
                        'The tilt of point {0} on spline {1} has exceeded the Blender'
                        'tolerance of -21600/21600 degrees, the result of the operation will not be correct.'
                        'Reduce the point tilt on the curve and repeat the operation.'
                    ).format(i, iterator),
                    'ERROR'
                )

                raise CancelError

            points[i].tilt = new_angle

            i += 1

        iterator += 1


def twist_correction(tilt_twist_y_arr, tilt_twist_ext_arr, curve):

    splines = curve.data.splines
    spline_iter = 0

    while spline_iter < len(splines):

        if splines[spline_iter].type == 'POLY':

            points = splines[spline_iter].points

        else:

            points = splines[spline_iter].bezier_points

        i = 0

        while i < len(tilt_twist_y_arr[spline_iter]):

            diff = tilt_twist_y_arr[spline_iter][i] - tilt_twist_ext_arr[spline_iter][i]

            rad_diff = diff * math.pi * 2

            if i != len(tilt_twist_y_arr[spline_iter]) - 1:

                tilt_twist_y_arr[spline_iter][i+1] += diff

            points[i+1].tilt += rad_diff

            i += 1

        spline_iter += 1


def angle_betw_vec(y_vec_arr, ext_vec_arr, spline_point_count):

    angle_betw_vec_arr = create_arr(spline_point_count)

    list_iter = 0

    while list_iter < len(ext_vec_arr):

        angle_arr = angle_betw_vec_arr[list_iter]
        y_arr = y_vec_arr[list_iter]
        ext_arr = ext_vec_arr[list_iter]

        spline_point_iter = 0

        while spline_point_iter < len(angle_arr):

            y_vec = y_arr[spline_point_iter]
            ext_vec = ext_arr[spline_point_iter]

            angle_arr[spline_point_iter] = ext_vec.angle(y_vec)

            spline_point_iter += 1

        list_iter += 1

    return angle_betw_vec_arr


def vec_equal(vec_1, vec_2):

    return vec_1.to_tuple(4) == vec_2.to_tuple(4)


def spline_verts_index(points, spline_type, cyclic, resolution, last_index):

    arr = np.empty(len(points), dtype=object)

    vert_index = last_index + 2
    i = 0

    if cyclic and not spline_type:

        if points[-1].handle_right_type != 'VECTOR' or points[0].handle_left_type != 'VECTOR':

            vert_index += 2 * resolution

        else:

            vert_index += 2

    while i < len(points) - 1:

        arr[i] = vert_index

        if spline_type or (points[i].handle_right_type == 'VECTOR' and points[i + 1].handle_left_type == 'VECTOR'):

            vert_index += 2

        else:

            vert_index += 2 * resolution

        i += 1

    if cyclic and not spline_type:

        arr[i] = last_index + 2
        last_index = vert_index - 2

    else:
        arr[i] = vert_index
        last_index = vert_index

    return arr, last_index


def calc_vec(first_co, second_co, normalize: bool):

    vec = second_co - first_co

    if vec.length < 0.0001:

        return None

    if normalize:

        vec = vec.normalized()

    return vec


def create_arr(points_count_list):

    arr = np.empty(len(points_count_list), dtype=object)

    i = 0

    while i < len(points_count_list):

        arr[i] = np.empty(points_count_list[i], dtype=object)

        i += 1

    return arr


def vec_projection(vec, z_vec):

    projection = (vec - vec.project(z_vec)).normalized()

    return projection


def angle_calc(ext_vec, y_vec, cross_vec):

    angle = ext_vec.angle(y_vec)

    #  Определяем позитивное вращение или негативное
    if ext_vec.dot(cross_vec) > 0:

        angle = -angle

    elif ext_vec.dot(cross_vec) == 0:

        angle = 0

    #  Предотвращение перекрещивания
    if ext_vec.dot(y_vec) < 0:

        if angle < 0:

            angle = math.radians(180) + (math.radians(180) + angle)

        elif angle > 0:

            angle = math.radians(180) - (math.radians(180) - angle)

    return angle


def midle_point_calc(p_0_ind, verts):

    vec = calc_vec(verts[p_0_ind].co, verts[p_0_ind + 1].co, False)

    midle_point_co = verts[p_0_ind].co + vec/2

    return midle_point_co


def calc_z_vec(p_0_ind, prev_p_0_ind, next_p_0_ind, verts):

    start_mdidle_point_co = midle_point_calc(prev_p_0_ind, verts)
    next_mdidle_point_co = midle_point_calc(next_p_0_ind, verts)

    vec_h_1 = calc_vec(verts[p_0_ind].co, start_mdidle_point_co, True)
    vec_h_2 = calc_vec(verts[p_0_ind].co, next_mdidle_point_co, True)

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
    list_iter = 0

    while list_iter < len(z_vec_arr):

        z_arr = z_vec_arr[list_iter]

        spline_point_iter = 0  # Соответствует индексу поинтов одного сплайна

        if not cyclic_arr[list_iter]:

            point_index = spline_verts_index_arr[list_iter][spline_point_iter]

            if not spline_type_arr[list_iter]:

                z_arr[spline_point_iter] = calc_vec(
                    verts[point_index].co,
                    spline_start_end_handle_arr[list_iter][0],
                    True
                )

            else:

                z_arr[spline_point_iter] = calc_vec(
                    verts[point_index].co,
                    verts[point_index + 2].co,
                    True
                )

            spline_point_iter = 1

        while spline_point_iter < len(z_arr) - 1:

            point_index = spline_verts_index_arr[list_iter][spline_point_iter]
            prev_point_index = point_index - 2

            if prev_point_index < 0:

                prev_point_index = spline_verts_index_arr[list_iter][-1]

            next_point_index = point_index + 2

            z_arr[spline_point_iter] = calc_z_vec(point_index, prev_point_index, next_point_index, verts)

            spline_point_iter += 1

        if not cyclic_arr[list_iter]:

            point_index = spline_verts_index_arr[list_iter][spline_point_iter]

            if not spline_type_arr[list_iter]:

                z_arr[spline_point_iter] = calc_vec(
                    verts[point_index].co,
                    spline_start_end_handle_arr[list_iter][1],
                    True
                )

            else:

                z_arr[spline_point_iter] = calc_vec(
                    verts[point_index - 2].co,
                    verts[point_index].co,
                    True
                )

        else:

            point_index = spline_verts_index_arr[list_iter][spline_point_iter]
            prev_point_index = point_index - 2
            next_point_index = spline_verts_index_arr[list_iter][0]

            z_arr[spline_point_iter] = calc_z_vec(point_index, prev_point_index, next_point_index, verts)

        list_iter += 1

    return z_vec_arr
