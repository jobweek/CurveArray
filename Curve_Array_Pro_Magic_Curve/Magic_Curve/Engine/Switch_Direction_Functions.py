import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import numpy as np


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


def switch_curve(curve):

    bpy.ops.object.select_all(action='DESELECT')
    curve.select_set(True)
    bpy.context.view_layer.objects.active = curve
    bpy.ops.object.editmode_toggle()
    bpy.ops.curve.switch_direction()
    curve.data.offset = -curve.data.offset
    bpy.ops.object.editmode_toggle()

    return curve
