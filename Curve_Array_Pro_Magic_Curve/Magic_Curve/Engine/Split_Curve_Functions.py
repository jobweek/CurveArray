import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import copy
import math
import numpy as np
from .Errors import CancelError, ShowMessageBox


def checker():

    objects = bpy.context.selected_objects

    if len(objects) == 0:

        ShowMessageBox("Error", "Select object", 'ERROR')

        raise CancelError

    elif len(objects) > 1:

        ShowMessageBox("Error", "Select only one object", 'ERROR')

        raise CancelError

    if objects[0].type != 'MESH':

        ShowMessageBox("Error", "Object should be mesh", 'ERROR')

        raise CancelError

    mode = bpy.context.active_object.mode

    if mode != 'EDIT':
        ShowMessageBox("Error", "Go to Edit Mode", 'ERROR')

        raise CancelError


def active_vertex(bm):
    try:

        act_vert = bm.select_history.active

        if act_vert is None:
            ShowMessageBox("Error", "The active vertex must be selected", 'ERROR')

            raise CancelError

        return act_vert

    except CancelError:

        ShowMessageBox("Error", "The active vertex must be selected", 'ERROR')

        raise CancelError


def verts_sequence(verts_count, act_vert, curve_data):

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

        ShowMessageBox("Error",
                       "No existing edges at selected vertex",
                       'ERROR')

        raise CancelError

    elif len(selected_linked_edges_buffer) == 1:

        curve_data.set_cyclic(False)

    elif len(selected_linked_edges_buffer) == 2:

        curve_data.set_cyclic(True)

    else:

        ShowMessageBox("Error",
                       "The sequence of vertices must not overlap or branch",
                       'ERROR')

        raise CancelError

    # Создадим массив фиксированной длины
    if not curve_data.get_cyclic():

        vert_sequence_array = np.empty(verts_count, dtype=object)

    else:

        vert_sequence_array = np.empty(verts_count + 1, dtype=object)
        vert_sequence_array[-1] = act_vert

    # Наполняем массив
    vert_sequence_array[0] = act_vert

    linked_edge = selected_linked_edges_buffer[0]
    searched_vertex = linked_edge.other_vert(act_vert)

    i = 1

    while i < verts_count - 1:

        vert_sequence_array[i] = searched_vertex

        selected_linked_edges_buffer = selected_linked_edges(searched_vertex)

        if len(selected_linked_edges_buffer) != 2:
            ShowMessageBox("Error",
                           "Make sure that the sequence of vertices does not intersect or branch, and that the vertex "
                           "at the beginning of the sequence is selected",
                           'ERROR')

            raise CancelError

        if selected_linked_edges_buffer[0] != linked_edge:

            linked_edge = selected_linked_edges_buffer[0]

        else:

            linked_edge = selected_linked_edges_buffer[1]

        searched_vertex = linked_edge.other_vert(searched_vertex)

        i += 1

    vert_sequence_array[i] = searched_vertex

    return vert_sequence_array, curve_data


#  Массив усредненных нормалей каждой вершины меша
def y_normal_vector(vert_sequence_array):

    y_normal_vector_array = np.empty(len(vert_sequence_array), dtype=object)

    iterator = 0

    for i in vert_sequence_array:

        vertex_normal = copy.deepcopy(i.normal)
        y_normal_vector_array[iterator] = vertex_normal

        iterator += 1

    return y_normal_vector_array


def vert_co(vert_sequence_array):

    vert_co_array = np.frompyfunc(lambda a: copy.deepcopy(a.co), 1, 1)

    vert_co_array = vert_co_array(vert_sequence_array)

    return vert_co_array


def create_curve(vert_co_array, active_object, curve_data):

    crv_mesh = bpy.data.curves.new('Split_Curve', 'CURVE')
    crv_mesh.dimensions = '3D'
    crv_mesh.twist_mode = 'MINIMUM'

    for _ in range(len(vert_co_array)-1):

        spline = crv_mesh.splines.new(type='POLY')

        spline.points.add(1)

    i = 0

    while i < len(vert_co_array)-1:

        mesh_vertex_first_co = vert_co_array[i]
        mesh_vertex_second_co = vert_co_array[i + 1]

        spline = crv_mesh.splines[i]

        spline.points[0].co[0] = mesh_vertex_first_co[0]
        spline.points[0].co[1] = mesh_vertex_first_co[1]
        spline.points[0].co[2] = mesh_vertex_first_co[2]
        spline.points[0].co[3] = 0

        spline.points[1].co[0] = mesh_vertex_second_co[0]
        spline.points[1].co[1] = mesh_vertex_second_co[1]
        spline.points[1].co[2] = mesh_vertex_second_co[2]
        spline.points[1].co[3] = 0

        i += 1

    crv_obj = bpy.data.objects.new('Split_Curve', crv_mesh)

    crv_obj.location = active_object.location

    crv_obj.rotation_euler = active_object.rotation_euler

    crv_obj.scale = active_object.scale

    bpy.context.scene.collection.objects.link(crv_obj)

    curve_data.set_curve(crv_obj)

    return curve_data


def create_extruded_mesh(main_curve):
    extruded_curve = main_curve.copy()
    extruded_curve.data = main_curve.data.copy()
    extruded_curve.name = main_curve.name + 'Duplicate'
    extruded_curve.data.name = main_curve.data.name + 'Duplicate'
    extruded_curve.data.extrude = 0.5
    bpy.context.scene.collection.objects.link(extruded_curve)

    bpy.ops.object.select_all(action='DESELECT')
    extruded_curve.select_set(True)
    bpy.context.view_layer.objects.active = extruded_curve
    bpy.ops.object.convert(target='MESH')
    extruded_mesh = bpy.context.active_object

    return extruded_mesh


def extruded_mesh_vector(extruded_mesh, array_size):

    extruded_mesh_vector_array = np.empty(array_size, dtype=object)

    i = 0

    while i < array_size:

        first_point = extruded_mesh.data.vertices[0 + i*4]
        second_point = extruded_mesh.data.vertices[1 + i*4]

        vector = mathutils.Vector((
            second_point.co[0] - first_point.co[0],
            second_point.co[1] - first_point.co[1],
            second_point.co[2] - first_point.co[2]
        ))

        extruded_mesh_vector_array[i] = vector

        i += 1

    return extruded_mesh_vector_array


def tilt_correction(ext_vec_arr, y_vec_arr, curve):

    def z_vector(first_vertex, second_vertex):

        z_vec = mathutils.Vector((
            second_vertex.co[0] - first_vertex.co[0],
            second_vertex.co[1] - first_vertex.co[1],
            second_vertex.co[2] - first_vertex.co[2]
        ))

        return z_vec.normalized()

    def vec_projection(vec, z_vec):

        projection = (vec - vec.project(z_vec)).normalized()

        return projection

    def angle_calc(ext_vec, y_vec, cross_vec):

        try:

            angle = ext_vec.angle(y_vec)

        except ValueError:

            angle = 0

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

    i = 0

    while i < len(ext_vec_arr):

        first_point = curve.data.splines[i].points[0]
        second_point = curve.data.splines[i].points[1]
        z_vec = z_vector(first_point, second_point)
        ext_vec = vec_projection(ext_vec_arr[i], z_vec)
        first_y_vec = vec_projection(y_vec_arr[i], z_vec)
        second_y_vec = vec_projection(y_vec_arr[i + 1], z_vec)
        first_cross_vec = z_vec.cross(first_y_vec)
        second_cross_vec = z_vec.cross(second_y_vec)

        first_angle = angle_calc(ext_vec, first_y_vec, first_cross_vec)
        second_angle = angle_calc(ext_vec, second_y_vec, second_cross_vec)

        first_point.tilt = first_angle
        second_point.tilt = second_angle

        i += 1
