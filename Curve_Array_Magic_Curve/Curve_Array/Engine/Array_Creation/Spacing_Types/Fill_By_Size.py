import bpy  # type: ignore
from typing import Iterator
from decimal import Decimal, getcontext
from ...General_Data_Classes import ItemData, ArrayPrams
from ...Path_Calculation.Calc_Path_Data_Functions import PathData
from ...Queue_Calculation.Calc_Queue_Data_Functions import QueueData
from .General_Functions import (
    get_object_by_name,
    calc_total_transform,
    get_dimension_offset,
)


def fill_by_size_manager(params: ArrayPrams, path_data: PathData, queue_data: QueueData) -> Iterator[ItemData]:

    getcontext().prec = 60

    path_length = Decimal(path_data.get_path_length())
    start_offset = Decimal(params.start_offset)
    end_offset = Decimal(params.end_offset)
    size_offset = Decimal(params.size_offset)

    path_length -= (start_offset + end_offset)
    if path_length < 0 or size_offset == 0:
        return

    searched_distance = start_offset
    prev_pos_dim = Decimal(0)

    for i in range(params.max_count):

        obj_name, ghost, queue_transform = queue_data.next()

        obj = get_object_by_name(obj_name)

        total_transform = calc_total_transform(obj, params.array_transform, queue_transform)

        neg_dim, pos_dim = get_dimension_offset(obj, total_transform, params.rail_axis)

        dimension = (Decimal(neg_dim) + prev_pos_dim) * size_offset

        prev_pos_dim = Decimal(pos_dim)

        if params.consider_size:
            searched_distance += dimension
            if searched_distance + prev_pos_dim > path_length:
                break
        else:
            if i != 0:
                searched_distance += dimension

        if searched_distance > path_length:
            break

        co, direction, normal = path_data.get_data_by_distance(
            searched_distance + Decimal(params.slide),
            params.smooth_normal,
            params.cyclic
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
