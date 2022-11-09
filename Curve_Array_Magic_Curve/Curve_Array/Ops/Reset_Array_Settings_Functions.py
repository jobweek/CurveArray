import bpy  # type: ignore
from ..Property.Get_Property_Path import (
    get_array_settings_props
)


def reset_array_settings_manager():
    sett = get_array_settings_props()

    sett.property_unset("random_seed")
    sett.property_unset("cloning_type")
    sett.property_unset("count")
    sett.property_unset("spacing_type")
    sett.property_unset("cyclic")
    sett.property_unset("smooth_normal")
    sett.property_unset("step_offset")
    sett.property_unset("size_offset")
    sett.property_unset("start_offset")
    sett.property_unset("end_offset")
    sett.property_unset("step_offset")
    sett.property_unset("slide")
    sett.property_unset("step")
    sett.property_unset("consider_size")
    sett.property_unset("align_rotation")
    sett.property_unset("rail_axis")
    sett.property_unset("normal_axis")
    sett.property_unset("rotation_x")
    sett.property_unset("rotation_y")
    sett.property_unset("rotation_z")
    sett.property_unset("location_x")
    sett.property_unset("location_y")
    sett.property_unset("location_z")
    sett.property_unset("scale_x")
    sett.property_unset("scale_y")
    sett.property_unset("scale_z")
    sett.property_unset("scale_xyz")
