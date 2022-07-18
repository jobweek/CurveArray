import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import copy
import numpy as np
from .Errors import CancelError, ShowMessageBox
from .Classes import checker
from Split_Curve import (
    curve_data,
)


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

    if len(linked_edges) == 0:

        ShowMessageBox("Error",
                       "No existing edges at selected vertex",
                       'ERROR')

        raise CancelError

    elif len(linked_edges) == 1:

        curve_data.set_cyclic(False)

    elif len(linked_edges) == 2:

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

    # Наполняем массив
    vert_sequence_array[0] = act_vert

    searched_vertex = linked_edges[0].other_vert(act_vert)

    i = 1

    while i < verts_count - 1:

        vert_sequence_array[i] = searched_vertex

        i += 1

    return vert_sequence_array
