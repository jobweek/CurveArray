import bpy  # type: ignore
from ...Property.Get_Property_Path import (
    get_queue_props,
)


def reset_transform(index: int):

    transform_data = get_queue_props()[index].transform_data

    transform_data.rotation_progressive_x = 0
    transform_data.rotation_progressive_y = 0
    transform_data.rotation_progressive_z = 0
    transform_data.rotation_random_min_x = 0
    transform_data.rotation_random_min_y = 0
    transform_data.rotation_random_min_z = 0
    transform_data.rotation_random_max_x = 0
    transform_data.rotation_random_max_y = 0
    transform_data.rotation_random_max_z = 0

    transform_data.location_progressive_x = 0
    transform_data.location_progressive_y = 0
    transform_data.location_progressive_z = 0
    transform_data.location_random_min_x = 0
    transform_data.location_random_min_y = 0
    transform_data.location_random_min_z = 0
    transform_data.location_random_max_x = 0
    transform_data.location_random_max_y = 0
    transform_data.location_random_max_z = 0

    transform_data.scale_progressive_x = 0
    transform_data.scale_progressive_y = 0
    transform_data.scale_progressive_z = 0
    transform_data.scale_random_min_x = 0
    transform_data.scale_random_min_y = 0
    transform_data.scale_random_min_z = 0
    transform_data.scale_random_max_x = 0
    transform_data.scale_random_max_y = 0
    transform_data.scale_random_max_z = 0
    transform_data.scale_random_min_xyz = 0
    transform_data.scale_random_max_xyz = 0
