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
    get_bb_offset,
)


def fill_by_offset_manager(
    params: UpdateArrayPrams, path_data: PathData, queue_data: QueueData, object_list: ObjectsList
        ) -> Iterator[ItemData]:

    getcontext().prec = 60

    path_length = Decimal(path_data.get_path_length())
    slide = Decimal(params.slide)
    start_offset = Decimal(params.start_offset) + slide
    end_offset = Decimal(params.end_offset) - slide
    step = Decimal(params.step_offset)

    if step < 0.00002:
        for i in range(params.count):
            object_list.move_obj_to_coll(i, True)
        return

    if params.consider_size:

        first_item = queue_data.get_by_index(0)

        first_obj = get_object_by_name(first_item.object_name)

        start_size_offset = get_bb_offset(
            first_obj, params.array_transform, first_item.queue_transform, params.rail_axis, False
        )

        start_offset += Decimal(start_size_offset)

    searched_distance = slide + start_offset

    for i in range(params.count):

        if not params.cyclic:
            if searched_distance < slide + start_offset or searched_distance > slide + (path_length - end_offset):
                object_list.move_obj_to_coll(i, True)
            else:
                object_list.move_obj_to_coll(i, False)
        else:
            object_list.move_obj_to_coll(i, False)

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
