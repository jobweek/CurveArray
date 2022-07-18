import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import copy
import numpy as np
from .Errors import CancelError, ShowMessageBox


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
