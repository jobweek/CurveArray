import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import numpy as np
from .Errors import CancelError, ShowMessageBox
from .Smooth_Curve_Functions import (
    vec_projection,
    angle_calc,
)


def vec_equal(vec_1, vec_2):

    return vec_1.to_tuple(4) == vec_2.to_tuple(4)


def calc_vec(first_vertex, second_vertex, normalize: bool):

    vec = second_vertex - first_vertex

    if vec.length < 0.0001:

        return None

    if normalize:

        vec = vec.normalized()

    return vec


def create_arr(points_count_list):

    arr = []

    i = 0

    while i < len(points_count_list):

        arr.append(np.empty(len(points_count_list[i]), dtype=object))

        i += 1

    return arr


def checker():

    objects = bpy.context.selected_objects

    if len(objects) == 0:

        ShowMessageBox("Error", "Select object", 'ERROR')

        raise CancelError

    elif len(objects) > 1:

        ShowMessageBox("Error", "Select only one object", 'ERROR')

        raise CancelError

    if objects[0].type != 'CURVE':

        ShowMessageBox("Error", "Object should be curve", 'ERROR')

        raise CancelError

    mode = bpy.context.active_object.mode

    if mode != 'OBJECT':
        ShowMessageBox("Error", "Go to Object Mode", 'ERROR')

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

            ShowMessageBox("Error", "Nurbs curves are not supported", 'ERROR')

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

        ShowMessageBox("Error",
                       "In the curve you have chosen, there are points in the same coordinates."
                       " You can remove it."
                       " Their place: " + verts_str,
                       'ERROR')

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

            ShowMessageBox("Error", "Nurbs curves are not supported", 'ERROR')

            raise CancelError


def duplicate(active_curve):

    switched_curve = active_curve.copy()
    switched_curve.data = active_curve.data.copy()

    if active_curve.animation_data:
        switched_curve.animation_data.action = active_curve.animation_data.action.copy()

    for i in active_curve.users_collection:

        i.objects.link(switched_curve)

    return switched_curve


class Curve_Data:

    def __init__(self, curve):

        self.spline_point_count = []  # Количество точек на каждом сплайне
        self.cyclic_list = []  # Cyclic == True; Not_Cyclic == False;
        self.spline_type_list = []  # Poly == True; Bezier == False;
        self.spline_range_list = []  # Каждый элемент - список из начальной и конечной "нулевой" вершины меша сплайна
        self.curve_resolution = curve.data.resolution_u

        for s in curve.data.splines:

            if s.type == 'POLY':

                points = s.points
                self.spline_type_list.append(True)

                if len(self.spline_range_list) == 0:

                    start_range = 0

                else:

                    start_range = self.spline_range_list[-1][1] + 2

                end_range = start_range + (len(points) - 1) * 2

                self.spline_range_list.append([start_range, end_range])

            else:

                points = s.bezier_points
                self.spline_type_list.append(False)

                if len(self.spline_range_list) == 0:

                    start_range = 0

                else:

                    start_range = self.spline_range_list[-1][1] + 2

                if s.use_cyclic_u:

                    end_range = (start_range + (len(points) * 2 * self.curve_resolution)) - 2

                else:

                    end_range = start_range + ((len(points) - 1) * 2 * self.curve_resolution)

                self.spline_range_list.append([start_range, end_range])

            self.spline_point_count.append(len(points))

            self.cyclic_list.append(s.use_cyclic_u)

    def get_curve_data(self):

        return (
            self.spline_point_count,
            self.cyclic_list,
            self.spline_type_list,
            self.spline_range_list,
            self.curve_resolution
        )


def convert_to_mesh(curve):

    curve.data.extrude = 0.5
    bpy.ops.object.select_all(action='DESELECT')
    curve.select_set(True)
    bpy.context.view_layer.objects.active = curve
    bpy.ops.object.convert(target='MESH')
    mesh = bpy.context.active_object

    return mesh


def switch_curve(curve):

    bpy.ops.object.select_all(action='DESELECT')
    curve.select_set(True)
    bpy.context.view_layer.objects.active = curve
    bpy.ops.object.editmode_toggle()
    bpy.ops.curve.switch_direction()
    bpy.ops.object.editmode_toggle()

    return curve


def ext_vec(mesh, curve_data):

    (
        spline_point_count,
        cyclic_list,
        spline_type_list,
        spline_range_list,
        curve_resolution
    ) = curve_data

    ext_vec_arr = create_arr(spline_point_count)
    verts = mesh.data.vertices
    list_iter = 0

    while list_iter < len(ext_vec_arr):

        ext_arr = ext_vec_arr[list_iter]
        verts_range = spline_range_list[list_iter]

        spline_point_iter = 0  # Соответствует индексу поинтов одного сплайна

        if spline_type_list[list_iter]:

            resol = 1

        else:

            resol = curve_resolution

        while spline_point_iter < len(ext_arr):

            first_point = verts[0 + curve_iter * 2 * resol]
            second_point = verts[first_point.index + 1]

            ext_vec = calc_vec(first_point.co, second_point.co, True)

            ext_arr[spline_point_iter] = ext_vec

            spline_point_iter += 1

        list_iter += 1

    return ext_vec_arr


def ext_z_vec(curve, flip: bool):  # Если flip == false, вычисляем z_vec_arr, не переворачиев массив ext_vec_arr

    def calc_vec(first_vertex, second_vertex, normalize: bool):

        vec = second_vertex - first_vertex

        if vec.length < 0.0001:

            return None

        if normalize:

            vec = vec.normalized()

        return vec

    def midle_point(first_vertex, second_vertex):

        vec = first_vertex.co + calc_vec(first_vertex.co, second_vertex.co, False)/2

        return vec

    def prev_point_search(verts, index_0, cyclic: bool, verts_range):

        # Example
        # index_0 = 45, verts_range = [(45,_),(52,_)]
        if cyclic and index_0 == verts_range[0]:

            prev_point_0 = verts[verts_range[1]]
        #  prev_point_0 = 52

        elif not cyclic and index_0 == verts_range[0]:

            prev_point_0 = verts[index_0]

        else:

            prev_point_0 = verts[index_0 - 2]

        prev_point_1 = verts[prev_point_0.index + 1]

        res = midle_point(prev_point_0, prev_point_1)

        return res

    def next_point_search(verts, index_0, cyclic: bool, verts_range):

        # Example
        # index_0 = 52, verts_range = [(45,_),(52,_)]
        if cyclic and index_0 == verts_range[1]:

            next_point_0 = verts[verts_range[0]]
        # next_point_0 = 45

        elif not cyclic and index_0 == verts_range[1]:

            next_point_0 = verts[index_0]

        else:

            next_point_0 = verts[index_0 + 2]

        next_point_1 = verts[next_point_0.index + 1]

        res = midle_point(next_point_0, next_point_1)

        return res

    ext_mesh_vec_arr = []
    z_vec_arr = []
    cyclic_list = []  # Cyclic == True; Not_Cyclic == False;
    spline_type_list = []  # Poly == True; Bezier == False;
    spline_range_list = []  # Каждый элемент - список из начальной и конечной "нулевой" вершины меша сплайна
    curve_resolution = curve.data.resolution_u

    for s in curve.data.splines:

        if s.type == 'POLY':

            points = s.points
            spline_type_list.append(True)

            if len(spline_range_list) == 0:

                start_range = 0

            else:

                start_range = spline_range_list[-1][1] + 2

            end_range = start_range + (len(points) - 1) * 2

            spline_range_list.append([start_range, end_range])

        else:

            points = s.bezier_points
            spline_type_list.append(False)

            if len(spline_range_list) == 0:

                start_range = 0

            else:

                start_range = spline_range_list[-1][1] + 2

            if s.use_cyclic_u:

                end_range = (start_range + (len(points) * 2 * curve_resolution)) - 2

            else:

                end_range = start_range + ((len(points) - 1) * 2 * curve_resolution)

            spline_range_list.append([start_range, end_range])

        print('RANGE: ', start_range, ', ', end_range)

        ext_mesh_vec_arr.append(np.empty(len(points), dtype=object))

        if not flip:

            z_vec_arr.append(np.empty(len(points), dtype=object))

        cyclic_list.append(s.use_cyclic_u)

    curve.data.extrude = 0.5
    bpy.ops.object.select_all(action='DESELECT')
    curve.select_set(True)
    bpy.context.view_layer.objects.active = curve
    bpy.ops.object.convert(target='MESH')
    extruded_mesh = bpy.context.active_object

    list_iter = 0  # Соответствует сплайну и принадлежащим им спискам/массивам
    curve_iter = 0  # Соответствует индексу поинтов всей кривой
    verts = extruded_mesh.data.vertices

    while list_iter < len(ext_mesh_vec_arr):

        ext_arr = ext_mesh_vec_arr[list_iter]

        verts_range = spline_range_list[list_iter]

        spline_iter = 0  # Соответствует индексу поинтов одного сплайна

        if spline_type_list[list_iter]:

            resol = 1

        else:

            resol = curve_resolution

        while spline_iter < len(ext_arr):

            first_point = verts[0 + curve_iter * 2 * resol]
            second_point = verts[1 + curve_iter * 2 * resol]

            ext_vec = calc_vec(first_point.co, second_point.co, True)

            ext_arr[spline_iter] = ext_vec

            if not flip:

                z_arr = z_vec_arr[list_iter]

                prev_point = prev_point_search(verts, first_point.index, cyclic_list[list_iter], verts_range)
                next_point = next_point_search(verts, first_point.index, cyclic_list[list_iter], verts_range)

                z_vec = calc_vec(prev_point, next_point, True)

                z_arr[spline_iter] = z_vec

            spline_iter += 1
            curve_iter += 1

        list_iter += 1

    i = 0

    while i < len(ext_mesh_vec_arr):

        if cyclic_list[i] and not spline_type_list[i]:  # Если сплайн цикличен и Bezier, то сдвигаем на -1

            ext_mesh_vec_arr[i] = np.roll(ext_mesh_vec_arr[i], -1)

            if not flip:

                z_vec_arr[i] = np.roll(z_vec_arr[i], -1)

        if flip:

            ext_mesh_vec_arr[i] = np.flip(ext_mesh_vec_arr[i])

        i += 1

    return ext_mesh_vec_arr, z_vec_arr


def tilt_correction(ext_vec_arr, y_vec_arr, z_vec_arr, curve):

    iterator = 0

    for s in curve.data.splines:

        if s.type == 'POLY':

            points = s.points

        else:

            points = s.bezier_points

        i = 0

        while i < len(points):

            if z_vec_arr[iterator][i] is None:

                i += 1
                continue

            ext_vec = vec_projection(ext_vec_arr[iterator][i], z_vec_arr[iterator][i])
            y_vec = vec_projection(y_vec_arr[iterator][i], z_vec_arr[iterator][i])
            cross_vec = z_vec_arr[iterator][i].cross(y_vec)
            angle = angle_calc(ext_vec, y_vec, cross_vec)

            points[i].tilt += angle

            if iterator == 0 and i == 0:

                print('ext_vec:', ext_vec)
                print('z_vec:', z_vec_arr[iterator][i])
                print('y_vec:', y_vec)

            i += 1

        iterator += 1
