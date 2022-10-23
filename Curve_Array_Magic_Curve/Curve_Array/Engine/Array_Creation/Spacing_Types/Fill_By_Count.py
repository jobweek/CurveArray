import bpy  # type: ignore
from decimal import Decimal, getcontext
from typing import Iterator
from .General_Functions import get_object_by_name, calc_total_transform, get_bb_offset
from ...General_Data_Classes import ItemData, ArrayPrams
from ...Path_Calculation.Calc_Path_Data_Functions import PathData
from ...Queue_Calculation.Calc_Queue_Data_Functions import QueueData


def fill_by_count_manager(params: ArrayPrams, path_data: PathData, queue_data: QueueData) -> Iterator[ItemData]:

    getcontext().prec = 60

    path_length = Decimal(path_data.get_path_length())
    start_offset = Decimal(params.start_offset)
    end_offset = Decimal(params.end_offset)

    if params.consider_size:

        first_item = queue_data.get_by_index(0)
        last_item = queue_data.get_by_index(params.count - 1)

        first_obj = get_object_by_name(first_item.object_name)
        last_obj = get_object_by_name(last_item.object_name)

        start_size_offset = get_bb_offset(
            first_obj, params.array_transform, first_item.queue_transform, params.rail_axis, False
        )
        end_size_offset = get_bb_offset(
            last_obj, params.array_transform, last_item.queue_transform, params.rail_axis, True
        )

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

        obj_name, ghost, _, queue_transform = queue_data.get_by_index(i)
        obj = get_object_by_name(obj_name)

        total_transform = calc_total_transform(obj, params.array_transform, queue_transform)

        co, direction, normal = path_data.get_data_by_distance(
            searched_distance,
            params.smooth_normal,
            params.cyclic
        )

        item_data = ItemData(
            ghost,
            co,
            direction,
            normal,
            total_transform,
        )

        yield item_data

        searched_distance += step
