import bpy  # type: ignore
from typing import Iterator
from ...General_Data_Classes import ItemData, ArrayPrams
from ...Path_Calculation.Calc_Path_Data_Functions import PathData
from ...Queue_Calculation.Calc_Queue_Data_Functions import QueueData


def fill_by_offset_manager(params: ArrayPrams, path_data: PathData, queue_data: QueueData) -> Iterator[ItemData]:

    yield ItemData
