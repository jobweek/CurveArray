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
from ..Path_Calculation.Calc_Path_Data import calc_path_data_manager
from ..Queue_Calculation.Calc_Queue_Data import calc_queue_data_manager
from ..Object_Creation.Create_Objects_Functions import ObjectsList
from ....Errors.Errors import CancelError


def update_array_manager(params: UpdateArrayPrams):

    path_data: PathData = get_instant_data_props().path_data.get()
    queue_data: QueueData = get_instant_data_props().queue_data.get()
    object_list: ObjectsList = get_instant_data_props().object_list.get()

    if path_data is None:
        raise CancelError

    if params.update_path_data:
        calc_path_data_manager()
        path_data: PathData = get_instant_data_props().path_data.get()

    if params.random_seed != queue_data.random_seed or params.update_queue_data:
        calc_queue_data_manager(params.random_seed)
        queue_data: QueueData = get_instant_data_props().queue_data.get()
        object_list.update_object_list(params.cloning_type, params.count)

    if params.cloning_type != object_list.cloning_type:
        object_list.update_object_list(params.cloning_type, params.count)
    else:
        object_list.check_count(params.count)

    if params.spacing_type == '0':
        gen = fill_by_count_manager(params, path_data, queue_data, object_list)
    elif params.spacing_type == '1':
        gen = fill_by_offset_manager(params, path_data, queue_data, object_list)
    elif params.spacing_type == '2':
        gen = fill_by_size_manager(params, path_data, queue_data, object_list)
    else:
        gen = fill_by_pivot_manager(params, path_data, queue_data, object_list)

    i = 0
    while True:
        try:
            item_data: ItemData = next(gen)
            if item_data.ghost:
                object_list.move_obj_to_coll(i, item_data.ghost)
            obj: bpy.types.Object = object_list.get_obj_by_index(i)
            move_obj(obj, item_data.co)

            total_transform_matrix = item_data.total_transform

            if params.align_rotation:
                align_matrix = align_obj(item_data.direction, item_data.normal, params.rail_axis, params.normal_axis)
                total_transform_matrix = align_matrix @ total_transform_matrix

            trasnform_obj(obj,  total_transform_matrix)
            i += 1

        except StopIteration:
            break
