import bpy  # type: ignore
from typing import Iterator
from decimal import Decimal, getcontext
from ...General_Data_Classes import ItemData, UpdateArrayPrams, ItemTransform
from ...Path_Calculation.Calc_Path_Data_Functions import PathData
from ...Queue_Calculation.Calc_Queue_Data_Functions import QueueData
from ...Object_Creation.Create_Objects_Functions import ObjectsList
from .....Errors.Errors import show_message_box, CancelError
from .General_Functions import (
    get_object_by_name,
    calc_total_transform,
)
from .....Errors.Errors import LoopEnd


def pivot_correction(pivot: float, params: UpdateArrayPrams, queue_transform: ItemTransform) -> float:

    if params.rail_axis[1] == 'x':
        pivot += pivot * params.array_transform.scale_x
        pivot += pivot * queue_transform.scale_x
    elif params.rail_axis[1] == 'y':
        pivot += pivot * params.array_transform.scale_y
        pivot += pivot * queue_transform.scale_y
    else:
        pivot += pivot * params.array_transform.scale_z + queue_transform.scale_z
        pivot += pivot * queue_transform.scale_z

    return pivot


def fill_by_pivot_manager(
    params: UpdateArrayPrams, path_data: PathData, queue_data: QueueData, object_list: ObjectsList
        ) -> Iterator[ItemData]:

    getcontext().prec = 60

    searched_distance = Decimal(params.slide)

    for i in range(params.count):

        obj_name, ghost, pivot, queue_transform = queue_data.get_by_index(i)

        if pivot < 0.00002:
            show_message_box("Error", f"Pivot of object {obj_name} is zero", 'ERROR')
            raise CancelError

        pivot = pivot_correction(pivot, params, queue_transform)

        obj = get_object_by_name(obj_name)
        object_list.move_obj_to_coll(i, False)

        total_transform = calc_total_transform(obj, params.array_transform, queue_transform)

        try:
            if params.cyclic:
                co, direction, normal, searched_distance = path_data.get_data_by_origin_cyclic(
                    searched_distance,
                    pivot,
                )
            else:
                co, direction, normal, searched_distance = path_data.get_data_by_origin(
                    searched_distance,
                    pivot,
                )
        except LoopEnd:
            while i < params.count:
                object_list.move_obj_to_coll(i, True)
                i += 1
            return

        item_data = ItemData(
            ghost,
            co,
            direction,
            normal,
            total_transform,
        )

        yield item_data
