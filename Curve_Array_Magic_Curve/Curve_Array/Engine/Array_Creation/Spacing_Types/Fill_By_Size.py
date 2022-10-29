import bpy  # type: ignore
from typing import Iterator
from decimal import Decimal, getcontext
from ...General_Data_Classes import ItemData, UpdateArrayPrams
from ...Path_Calculation.Calc_Path_Data_Functions import PathData
from ...Queue_Calculation.Calc_Queue_Data_Functions import QueueData
from ...Object_Creation.Create_Objects_Functions import ObjectsList
from .General_Functions import (
    get_object_by_name,
    calc_total_transform,
    get_dimension_offset,
)


def fill_by_size_manager(
    params: UpdateArrayPrams, path_data: PathData, queue_data: QueueData, object_list: ObjectsList
        ) -> Iterator[ItemData]:

    getcontext().prec = 60

    path_length = Decimal(path_data.get_path_length())
    slide = Decimal(params.slide)
    start_offset = Decimal(params.start_offset) + slide
    end_offset = Decimal(params.end_offset) - slide
    size_offset = Decimal(params.size_offset)

    if size_offset < 0.00002:
        for i in range(params.count):
            object_list.move_obj_to_coll(i, True)
        return

    searched_distance = slide
    prev_pos_dim = Decimal(0)

    for i in range(params.count):

        obj_name, ghost, _, queue_transform = queue_data.get_by_index(i)
        obj = get_object_by_name(obj_name)

        total_transform = calc_total_transform(obj, params.array_transform, queue_transform)

        neg_dim, pos_dim = get_dimension_offset(obj, total_transform, params.rail_axis)
        dimension = (Decimal(neg_dim) + prev_pos_dim) * size_offset
        prev_pos_dim = Decimal(pos_dim)

        if i == 0:
            if params.consider_size:
                searched_distance += dimension
        else:
            searched_distance += dimension

        if searched_distance < start_offset or searched_distance > (path_length - end_offset):
            object_list.move_obj_to_coll(i, True)
        else:
            object_list.move_obj_to_coll(i, False)

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
