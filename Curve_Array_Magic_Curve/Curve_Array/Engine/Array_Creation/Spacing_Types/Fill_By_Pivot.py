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
from .....Errors.Errors import LoopEnd


def fill_by_pivot_manager(params: ArrayPrams, path_data: PathData, queue_data: QueueData) -> Iterator[ItemData]:

    getcontext().prec = 60

    searched_distance = Decimal(params.slide)

    for i in range(params.max_count_pivot):

        if i == params.max_count_pivot:
            break

        obj_name, ghost, pivot, queue_transform = queue_data.next()

        obj = get_object_by_name(obj_name)

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
            print(f'LOOP_END')
            return

        item_data = ItemData(
            obj,
            ghost,
            co,
            direction,
            normal,
            total_transform,
        )

        yield item_data
