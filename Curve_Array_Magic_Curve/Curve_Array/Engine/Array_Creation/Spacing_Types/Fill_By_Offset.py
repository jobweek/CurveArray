import bpy  # type: ignore
import bmesh  # type: ignore
from decimal import Decimal, getcontext
from typing import Iterator
from .Fill_By_Offset_Functions import get_object_by_name, get_demension
from ...General_Data_Classes import ItemData, ArrayPrams
from ...Path_Calculation.Calc_Path_Data_Functions import PathData
from ...Queue_Calculation.Calc_Queue_Data_Functions import QueueData


def fill_by_offset_manager(params: ArrayPrams,  path_data: PathData, queue_data: QueueData) -> Iterator[ItemData]:

    getcontext().prec = 60

    path_length = Decimal(path_data.get_path_length())
    start_offset = Decimal(params.start_offset)
    end_offset = Decimal(params.end_offset)

    if params.consider_size and params.align_rotation:

        first_obj = get_object_by_name(queue_data.get_by_index(0).object_name)
        last_obj = get_object_by_name(queue_data.get_by_index(params.count - 1).object_name)

        start_size_offset = get_demension(first_obj, params.rail_axis, False)
        end_size_offset = get_demension(last_obj, params.rail_axis, True)

        start_offset += Decimal(start_size_offset)
        end_offset += Decimal(end_size_offset)

    path_length -= (start_offset + end_offset)
    if path_length < 0:
        return

    if params.count == 1:
        step = Decimal(0)
        searched_distance = start_offset + path_length/2
    else:
        step = path_length/Decimal(params.count - 1)
        searched_distance = start_offset

    searched_distance += Decimal(params.slide)

    for i in range(params.count):

        obj_name, ghost, transform = queue_data.next()

        co, direction, normal = path_data.get_data_by_distance(
            searched_distance,
            params.smooth_normal,
            params.cyclic
        )

        item_data = ItemData(
            get_object_by_name(obj_name),
            ghost,
            co,
            direction,
            normal,
            transform,
        )

        yield item_data

        searched_distance += step
