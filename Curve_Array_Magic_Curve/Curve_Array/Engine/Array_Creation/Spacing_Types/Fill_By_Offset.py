import bpy  # type: ignore
import bmesh  # type: ignore
from mathutils import Vector
from typing import Any, Iterator
from...Path_Calculation.Calc_Path_Data_Functions import PathData
from...Queue_Calculation.Calc_Queue_Data_Functions import QueueData


def get_demension(obj: Any, axis: str, direction: bool) -> float:

    bb = obj.bound_box

    def _positive_x(bb):
        points = (bb[4][0], bb[5][0], bb[6][0], bb[7][0])
        offset = max(points)
        return offset

    def _negative_x(bb):
        points = (bb[0][0], bb[1][0], bb[2][0], bb[3][0])
        offset = min(points)
        return -offset

    def _positive_y(bb):
        points = (bb[2][1], bb[3][1], bb[6][1], bb[7][1])
        offset = max(points)
        return offset

    def _negative_y(bb):
        points = (bb[0][1], bb[1][1], bb[4][1], bb[5][1])
        offset = min(points)
        return -offset

    def _positive_z(bb):
        points = (bb[1][2], bb[2][2], bb[5][2], bb[6][2])
        offset = max(points)
        return offset

    def _negative_z(bb):
        points = (bb[0][2], bb[3][2], bb[4][2], bb[7][2])
        offset = min(points)
        return -offset

    if axis == '+x':
        if direction:
            return _positive_x(bb)
        else:
            return _negative_x(bb)
    elif axis == '-x':
        if direction:
            return _negative_x(bb)
        else:
            return _positive_x(bb)
    elif axis == '+y':
        if direction:
            return _positive_y(bb)
        else:
            return _negative_y(bb)
    elif axis == '-y':
        if direction:
            return _negative_y(bb)
        else:
            return _positive_y(bb)
    elif axis == '+z':
        if direction:
            return _positive_z(bb)
        else:
            return _negative_z(bb)
    elif axis == '-z':
        if direction:
            return _negative_z(bb)
        else:
            return _positive_z(bb)


def fill_by_offset_manager(params,  path_data: PathData, queue_data: QueueData) \
        -> Iterator[tuple[Any, Vector, Vector, Vector]]:

    path_length = path_data.get_path_length()
    start_offset = params['start_offset']
    end_offset = params['end_offset']

    if params['consider_size'] and params['align_rotation']:

        start_size_offset = get_demension(queue_data.get_by_index(0), params['rail_axis'], False)
        end_size_offset = get_demension(queue_data.get_by_index(params['count']-1), params['rail_axis'], True)

        start_offset += start_size_offset
        end_offset += end_size_offset

    path_length -= (start_offset + end_offset)
    if path_length < 0:
        return

    if params['count'] == 1:
        step = 0
        searched_distance = start_offset + path_length/2
    else:
        step = path_length/(params['count'] - 1)
        searched_distance = start_offset

    searched_distance += params['slide']

    for _ in range(params['count']):

        obj = queue_data.next()
        co, direction, normal = path_data.get_data_by_distance(searched_distance)

        yield obj, co, direction, normal

        searched_distance += step
