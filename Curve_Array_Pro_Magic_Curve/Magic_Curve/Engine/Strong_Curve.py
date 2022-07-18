import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import math
import numpy as np
from .Errors import CancelError, ShowMessageBox
from .Classes import checker, CurveData
from .General_Functions import (
    active_vertex,
    direction_vector,
    vert_co,
)


def verts_sequence(verts_count, act_vert, curve_data):

    def selected_linked_edges(searched_vertex):

        linked_edges = searched_vertex.link_edges

        selected_linked_edges_buffer = []

        for edge in linked_edges:

            if edge.select:
                selected_linked_edges_buffer.append(edge)

        return selected_linked_edges_buffer

    vert_sequence_array = np.empty(verts_count, dtype=object)
    edge_sequence_array = np.empty(verts_count - 1, dtype=object)

    vert_sequence_array[0] = act_vert

    selected_linked_edges_buffer = selected_linked_edges(act_vert)

    if len(selected_linked_edges_buffer) < 1 or len(selected_linked_edges_buffer) > 2:

        ShowMessageBox("Error",
                       "An intersection has been detected",
                       "ERROR")

        raise CancelError

    linked_edge = selected_linked_edges_buffer[0]

    edge_sequence_array[0] = linked_edge

    searched_vertex = linked_edge.other_vert(act_vert)

    i = 1

    while i < verts_count - 1:

        vert_sequence_array[i] = searched_vertex

        selected_linked_edges_buffer = selected_linked_edges(searched_vertex)

        if len(selected_linked_edges_buffer) != 2:

            ShowMessageBox("Error",
                           "The sequence of vertices must be connected and must not overlap",
                           'ERROR')

            raise CancelError

        if selected_linked_edges_buffer[0] != linked_edge:

            linked_edge = selected_linked_edges_buffer[0]

        else:

            linked_edge = selected_linked_edges_buffer[1]

        edge_sequence_array[0] = linked_edge

        searched_vertex = linked_edge.other_vert(searched_vertex)

        i += 1

    vert_sequence_array[i] = searched_vertex

    selected_linked_edges_buffer = selected_linked_edges(searched_vertex)

    if len(selected_linked_edges_buffer) == 2:

        curve_data.set_cyclic(True)

    else:

        curve_data.set_cyclic(False)

    return vert_sequence_array, edge_sequence_array


def x_vector(edge_sequence_array):

    for edge in edge_sequence_array:

        if edge.link_faces > 2:

            ShowMessageBox("Error",
                           "Invalid mesh, an edge forming three or more faces is detected",
                           "ERROR")

            raise CancelError

    return x_vector_array


def cyclic_correction(vert_co_array, curve_data):

    if curve_data.get_cyclic():

        arr = np.empty(1, dtype=object)

        arr[0] = vert_co_array[0]

        vert_co_array = np.append(vert_co_array, arr, axis=0)

    return vert_co_array


def create_curve(vert_co_array, active_object, curve_data):

    def create_spline(crv_mesh, vert_co_array):

        for _ in range(len(vert_co_array)-1):

            spline = crv_mesh.splines.new(type='POLY')

            spline.points.add(1)

    crv_mesh = bpy.data.curves.new('MgCrv_curve_strong', 'CURVE')
    crv_mesh.dimensions = '3D'
    crv_mesh.twist_mode = 'MINIMUM'
    create_spline(crv_mesh, vert_co_array)

    i = 0

    while i < len(vert_co_array) - 1:

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

    crv_obj = bpy.data.objects.new('MgCrv_curve_strong', crv_mesh)

    crv_obj.location = active_object.location

    crv_obj.rotation_euler = active_object.rotation_euler

    crv_obj.scale = active_object.scale

    bpy.context.scene.collection.objects.link(crv_obj)

    curve_data.set_curve(crv_obj)

    return curve_data


def extruded_mesh_vector(extruded_mesh, vector_count):

    extruded_mesh_vector_array = np.empty(vector_count, dtype=object)

    i = 0

    while i < vector_count:

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


def curve_correction(curve_data):

    main_curve = curve_data.get_curve()

    for spline in main_curve.data.splines:

        spline.type = 'BEZIER'

        spline.bezier_points[0].handle_left_type = 'FREE'
        spline.bezier_points[0].handle_right_type = 'FREE'

        spline.bezier_points[1].handle_left_type = 'FREE'
        spline.bezier_points[1].handle_right_type = 'FREE'

    return curve_data


def angle_between_vector(extruded_mesh_vector_array, active_mesh_vector_array, direction_vector_array):

    def angle_correction(angle, cross_vector, vec_active_mesh):

        direction_angle = cross_vector.angle(vec_active_mesh)

        if direction_angle < math.radians(90):

            return angle

        elif direction_angle > math.radians(90):

            return angle * (-1)

        else:

            return angle

    def correct_vec(vec, vec_direction):

        projection = vec.project(vec_direction)
        correct_vec = vec - projection

        return correct_vec

    def rotation_correction(angle, cross_vector, vec_active_mesh):

        if angle > math.radians(90):

            angle = math.pi - angle

            angle = angle_correction(angle, cross_vector, vec_active_mesh)

            angle += math.pi

        else:

            angle = angle_correction(angle, cross_vector, vec_active_mesh)

        return angle

    angle_array = np.empty(len(extruded_mesh_vector_array), dtype=object)

    i = 0

    while i < len(extruded_mesh_vector_array):

        vec_extruded_mesh = extruded_mesh_vector_array[i]
        vec_active_mesh_first = active_mesh_vector_array[i]
        vec_active_mesh_second = active_mesh_vector_array[i + 1]
        vec_direction = direction_vector_array[i]

        correct_vec_active_mesh_first = correct_vec(vec_active_mesh_first, vec_direction)
        correct_vec_active_mesh_second = correct_vec(vec_active_mesh_second, vec_direction)

        correct_vec_extruded_mesh = correct_vec(vec_extruded_mesh, vec_direction)

        angle_first = correct_vec_extruded_mesh.angle(correct_vec_active_mesh_first)
        angle_second = correct_vec_extruded_mesh.angle(correct_vec_active_mesh_second)

        cross_vector = vec_direction.cross(correct_vec_extruded_mesh)

        angle_first = rotation_correction(angle_first, cross_vector, vec_active_mesh_first)
        angle_second = rotation_correction(angle_second, cross_vector, vec_active_mesh_second)

        # if math.fabs(angle_first - angle_second) > math.pi:

        #     if angle_second < 0:

        #         angle_second = (math.pi*2 - math.fabs(angle_second))

        #     else:

        #         angle_second = (math.pi*2 - math.fabs(angle_second)) * (-1)

        angle_array[i] = [angle_first, angle_second]

        i += 1

    return angle_array


def tilt_correction(angle_array, curve_data):

    i = 0

    while i < len(curve_data.get_curve().data.splines):

        spline = curve_data.get_curve().data.splines[i]

        angle_spine_list = angle_array[i]

        spline.bezier_points[0].tilt = angle_spine_list[0]

        spline.bezier_points[1].tilt = angle_spine_list[1]

        i += 1


def strong_curve_manager():

    active_object = bpy.context.active_object
    active_mesh = active_object.data

    Checker.checker()
    curve_data = CurveData()

    bm = bmesh.from_edit_mesh(active_mesh)

    act_vert = active_vertex(bm)

    vert_sequence_array, edge_sequence_array = verts_sequence(active_mesh.total_vert_sel, act_vert, curve_data)

    vert_co_array = vert_co(vert_sequence_array)

    z_vector_array = direction_vector(vert_sequence_array)

    x_vector_array = x_vector(edge_sequence_array)

