import bpy  # type: ignore
from .Create_Array_Functions import (
    trasnform_obj,
    align_obj,
    move_obj,
    clone_obj,
    create_collection,
    start_check
)
from ...Property.Get_Property_Path import get_instant_data_props
from ..Path_Calculation.Calc_Path_Data import calc_path_data_manager
from ..Queue_Calculation.Calc_Queue_Data import calc_queue_data_manager
from .Spacing_Types.Fill_By_Count import fill_by_count_manager
from .Spacing_Types.Fill_By_Offset import fill_by_offset_manager
from .Spacing_Types.Fill_By_Size import fill_by_size_manager
from ..General_Data_Classes import (
    ItemData,
    ArrayPrams
)


def crete_array_manager(params: ArrayPrams):

    start_check()

    if params.calculate_path_data:
        calc_path_data_manager()
    path_data = get_instant_data_props().path_data.get()

    if params.calculate_queue_data:
        calc_queue_data_manager(params.random_seed)
    queue_data = get_instant_data_props().queue_data.get()

    if params.spacing_type == '0':
        gen = fill_by_count_manager(params, path_data, queue_data)
    elif params.spacing_type == '1':
        gen = fill_by_offset_manager(params, path_data, queue_data)
    elif params.spacing_type == '2':
        gen = fill_by_size_manager(params, path_data, queue_data)
    else:
        gen = fill_by_offset_manager(params, path_data, queue_data)

    main_collection = create_collection()
    ghost_collection = None

    while True:
        try:
            item_data: ItemData = next(gen)

            if item_data.ghost:

                if ghost_collection is None:
                    ghost_collection = create_collection(main_collection)

                duplicate = clone_obj(item_data.obj, params.cloning_type, ghost_collection)
            else:
                duplicate = clone_obj(item_data.obj, params.cloning_type, main_collection)

            move_obj(duplicate, item_data.co)
            trasnform_obj(duplicate,  item_data.total_transform)

            if params.align_rotation:
                align_obj(duplicate, item_data.direction, item_data.normal, params.rail_axis, params.normal_axis)

        except StopIteration:
            break
