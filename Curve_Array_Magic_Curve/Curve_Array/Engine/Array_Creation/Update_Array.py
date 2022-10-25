import bpy  # type: ignore
from .Create_Array_Functions import (
    trasnform_obj,
    align_obj,
    move_obj,
)
from ..General_Data_Classes import (
    ItemData,
    UpdateArrayPrams,
)
from ...Property.Get_Property_Path import get_instant_data_props
from ..Path_Calculation.Calc_Path_Data_Functions import PathData
from ..Queue_Calculation.Calc_Queue_Data_Functions import QueueData
from .Spacing_Types.Fill_By_Count import fill_by_count_manager
from .Spacing_Types.Fill_By_Offset import fill_by_offset_manager
from .Spacing_Types.Fill_By_Size import fill_by_size_manager
from .Spacing_Types.Fill_By_Pivot import fill_by_pivot_manager
from ..Object_Creation.Create_Objects_Functions import ObjectsList


def update_array_manager(params: UpdateArrayPrams):
    print(f'UPDATE ARRAY')
    path_data: PathData = get_instant_data_props().path_data.get()
    queue_data: QueueData = get_instant_data_props().queue_data.get()
    object_list: ObjectsList = get_instant_data_props().object_list.get()

    object_list.check_count(params.count)

    if params.spacing_type == '0':
        gen = fill_by_count_manager(params, path_data, queue_data)
    elif params.spacing_type == '1':
        gen = fill_by_offset_manager(params, path_data, queue_data)
    elif params.spacing_type == '2':
        gen = fill_by_size_manager(params, path_data, queue_data)
    else:
        gen = fill_by_pivot_manager(params, path_data, queue_data)

    i = 0
    while True:
        try:
            item_data: ItemData = next(gen)

            obj: bpy.types.Object = object_list.get_obj_by_index(i)

            move_obj(obj, item_data.co)
            trasnform_obj(obj,  item_data.total_transform)

            if params.align_rotation:
                align_obj(obj, item_data.direction, item_data.normal, params.rail_axis, params.normal_axis)

            i += 1

        except StopIteration:
            break
