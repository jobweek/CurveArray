import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import numpy as np
import math
from .Errors import CancelError, ShowMessageBox


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

    arr = np.empty(len(points_count_list), dtype=object)

    i = 0

    while i < len(points_count_list):

        arr[i] = np.empty(points_count_list[i], dtype=object)

        i += 1

    return arr


def arr_roll(arr, cyclic_list, spline_type_list, roll: int):

    i = 0

    while i < len(arr):

        if cyclic_list[i] and not spline_type_list[i]:

            arr[i] = np.roll(arr[i], roll)

        i += 1

    return arr


def arr_flip(arr):

    i = 0

    while i < len(arr):

        arr[i] = np.flip(arr[i])

        i += 1

    return arr


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


def create_profile():

    crv_mesh = bpy.data.curves.new('Curve_Profile', 'CURVE')
    crv_mesh.dimensions = '3D'
    crv_mesh.twist_mode = 'MINIMUM'

    spline = crv_mesh.splines.new(type='POLY')

    spline.points.add(2)

    spline = crv_mesh.splines[0]

    spline.points[0].co[0] = 0
    spline.points[0].co[1] = -0.5
    spline.points[0].co[2] = 0
    spline.points[0].co[3] = 0

    spline.points[1].co[0] = 0
    spline.points[1].co[1] = 0
    spline.points[1].co[2] = 0
    spline.points[1].co[3] = 0

    spline.points[2].co[0] = 0
    spline.points[2].co[1] = 0.5
    spline.points[2].co[2] = 0
    spline.points[2].co[3] = 0

    crv_obj = bpy.data.objects.new('Curve_Profile', crv_mesh)

    bpy.context.scene.collection.objects.link(crv_obj)

    return crv_obj


def duplicate(active_curve):

    switched_curve = active_curve.copy()
    switched_curve.data = active_curve.data.copy()

    if active_curve.animation_data:
        switched_curve.animation_data.action = active_curve.animation_data.action.copy()

    for i in active_curve.users_collection:

        i.objects.link(switched_curve)

    return switched_curve


def curve_data(curve):

    splines = curve.data.splines
    spline_count = len(splines)

    spline_point_count_arr = np.empty(spline_count, dtype=int)  # Количество точек на каждом сплайне
    # Массив индексов вершин меша соответствующих точкам сплайна
    spline_verts_index_arr = np.empty(spline_count, dtype=object)
    cyclic_arr = np.empty(spline_count, dtype=bool)  # Cyclic == True; Not_Cyclic == False;
    spline_type_arr = np.empty(spline_count, dtype=bool)  # Poly == True; Bezier == False;
    i = 0
    last_index = -2  # Индекс последней нулевой вершины меша относящегося к сплайну

    while i < len(splines):

        if splines[i].type == 'POLY':

            points = splines[i].points
            spline_type = True

        else:

            points = splines[i].bezier_points
            spline_type = False

        cyclic = splines[i].use_cyclic_u
        resolution = splines[i].resolution_u

        spline_point_count_arr[i] = len(points)
        spline_verts_index_arr[i], last_index = \
            spline_verts_index(points, spline_type, cyclic, resolution, last_index)
        cyclic_arr[i] = cyclic
        spline_type_arr[i] = spline_type

        i += 1

    return (
        spline_point_count_arr,
        spline_verts_index_arr,
        cyclic_arr,
        spline_type_arr,
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

                twist = -(abs(twist) // (math.pi * 2)) - 1

            elif points[i].tilt < points[i+1].tilt:

                twist = twist // (math.pi * 2) + 1

            else:

                twist = 0

            tilt_twist_arr[spline_iter][i] = twist

            i += 1

        spline_iter += 1

    return tilt_twist_arr


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


def switch_curve(curve):

    bpy.ops.object.select_all(action='DESELECT')
    curve.select_set(True)
    bpy.context.view_layer.objects.active = curve
    bpy.ops.object.editmode_toggle()
    bpy.ops.curve.switch_direction()
    curve.data.offset = -curve.data.offset
    bpy.ops.object.editmode_toggle()

    return curve


def ext_vec(mesh, curve_data):

    (
        spline_point_count_arr,
        spline_verts_index_arr,
        cyclic_arr,
        spline_type_arr,
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

            ext_vec_arr[list_iter][spline_point_iter] = ext_vec

            spline_point_iter += 1

        list_iter += 1

    return ext_vec_arr


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

                angle = angle * 0.5

            new_angle = points[i].tilt + angle

            if new_angle > 376.992:

                ShowMessageBox("Error",
                               ('The tilt of point {0} on spline {1} has exceeded the Blender'
                                'tolerance of -21600/21600 degrees, the result of the operation will not be correct. '
                                'Reduce the point tilt on the curve and repeat the operation.').format(i, iterator),
                               'ERROR')

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

            diff = +(tilt_twist_y_arr[spline_iter][i] - tilt_twist_ext_arr[spline_iter][i]) - 1

            if tilt_twist_ext_arr[spline_iter][i] < tilt_twist_y_arr[spline_iter][i]:

                points[i+1].tilt += math.pi * 2 * diff

            elif tilt_twist_ext_arr[spline_iter][i] > tilt_twist_y_arr[spline_iter][i]:

                points[i+1].tilt -= math.pi * 2 * diff

            i += 1

        spline_iter += 1
