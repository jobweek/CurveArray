import bpy  # type: ignore
from typing import Iterator
from decimal import Decimal, getcontext
from ...General_Data_Classes import ItemData, ArrayPrams
from ...Path_Calculation.Calc_Path_Data_Functions import PathData
from ...Queue_Calculation.Calc_Queue_Data_Functions import QueueData
from .General_Functions import (
    get_object_by_name,
    calc_total_transform,
)


def fill_by_pivot_manager(params: ArrayPrams, path_data: PathData, queue_data: QueueData) -> Iterator[ItemData]:

    getcontext().prec = 60

    path_length = Decimal(path_data.get_path_length())
    start_offset = Decimal(params.start_offset)
    end_offset = Decimal(params.end_offset)
    max_count = params.max_count_pivot - 1

    path_length -= (start_offset + end_offset)
    if path_length < 0:
        return

    searched_distance = start_offset

    for i in range(max_count):

        if i == max_count:
            break

        obj_name, ghost, pivot, queue_transform = queue_data.next()

        obj = get_object_by_name(obj_name)

        total_transform = calc_total_transform(obj, params.array_transform, queue_transform)

        co, direction, normal, searched_distance = path_data.get_data_by_origin(
            searched_distance + Decimal(params.slide),
            pivot,
            params.cyclic,
        )

        item_data = ItemData(
            obj,
            ghost,
            co,
            direction,
            normal,
            total_transform,
        )

        yield item_data
