import bpy  # type: ignore
from ...Property.Get_Property_Path import get_instant_data_props
from ..Path_Calculation.Calc_Path_Data import calc_path_data_manager
from ..Queue_Calculation.Calc_Queue_Data import calc_queue_data_manager
from .Spacing_Types.Fill_By_Offset import fill_by_offset_manager
from .Create_Array_Functions import (
    start_check,
    create_collection,
    clone_obj,
    move_obj,
    rotate_obj,
)


def crete_array_manager(**params):

    start_check()

    if params['calculate_path_data']:
        calc_path_data_manager()
    path_data = get_instant_data_props().path_data.get()

    if params['calculate_queue_data']:
        calc_queue_data_manager(params['random_seed'])
    queue_data = get_instant_data_props().queue_data.get()

    if params['spacing_type'] == '0':
        gen = fill_by_offset_manager(params, path_data, queue_data)
    else:
        gen = fill_by_offset_manager(params, path_data, queue_data)

    collection = create_collection()

    while True:
        try:
            obj, co, direction, normal = next(gen)

            if obj is None:
                continue

            duplicate = clone_obj(obj, params['cloning_type'], collection)
            move_obj(duplicate, co)

            if params['align_rotation']:
                rotate_obj(duplicate, direction, normal, params['rail_axis'], params['normal_axis'])

        except StopIteration:
            break
