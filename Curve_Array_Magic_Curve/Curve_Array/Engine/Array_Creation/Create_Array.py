import bpy  # type: ignore
from math import radians
from .Create_Array_Functions import start_check
from ..General_Data_Classes import CreateArrayPrams, ArrayTransform, UpdateArrayPrams
from ...Property.Get_Property_Path import get_array_settings_props
from ..Path_Calculation.Calc_Path_Data import calc_path_data_manager
from ..Queue_Calculation.Calc_Queue_Data import calc_queue_data_manager
from ..Object_Creation.Create_Objects import create_objects_manager
from .Update_Array import update_array_manager


def crete_array_manager(params: CreateArrayPrams):
    print(f'CREATE ARRAY')
    settings = get_array_settings_props()
    start_check()

    if params.calculate_path_data:
        calc_path_data_manager()

    if params.calculate_queue_data:
        calc_queue_data_manager(settings.random_seed)

    if params.create_object_list:
        create_objects_manager(settings.count, settings.cloning_type)

    array_transform = ArrayTransform(
        rotation_x=radians(settings.rotation_x),
        rotation_y=radians(settings.rotation_y),
        rotation_z=radians(settings.rotation_z),
        location_x=settings.location_x,
        location_y=settings.location_y,
        location_z=settings.location_z,
        scale_x=settings.scale_x,
        scale_y=settings.scale_y,
        scale_z=settings.scale_z,
    )

    array_params = UpdateArrayPrams(
        update_path_data=False,
        update_queue_data=False,
        update_object_data=False,
        random_seed=settings.random_seed,
        cloning_type=settings.cloning_type,
        spacing_type=settings.spacing_type,
        cyclic=settings.cyclic,
        smooth_normal=settings.smooth_normal,
        count=settings.count,
        step_offset=settings.step_offset,
        size_offset=settings.size_offset,
        start_offset=settings.start_offset,
        end_offset=settings.end_offset,
        slide=settings.slide,
        consider_size=settings.consider_size,
        align_rotation=settings.align_rotation,
        rail_axis=settings.rail_axis,
        normal_axis=settings.normal_axis,
        array_transform=array_transform,
    )

    update_array_manager(array_params)
