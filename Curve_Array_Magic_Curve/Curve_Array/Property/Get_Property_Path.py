import bpy  # type: ignore


def get_main_props():
    return bpy.context.scene.curve_array_properties


def get_array_props():
    return bpy.context.scene.curve_array_properties.array_props


def get_engine_props():
    return bpy.context.scene.curve_array_properties.engine_props


def get_obj_editor_props():
    return bpy.context.scene.curve_array_properties.engine_props.object_editor_data


def get_queue_props():
    return bpy.context.scene.curve_array_properties.engine_props.object_editor_data.queue


def get_objects_props():
    return bpy.context.scene.curve_array_properties.engine_props.object_editor_data.objects


def get_groups_props():
    return bpy.context.scene.curve_array_properties.engine_props.object_editor_data.groups


def get_curve_props():
    return bpy.context.scene.curve_array_properties.engine_props.curve_editor_data.curve


def get_wm_props():
    return bpy.context.scene.curve_array_properties.engine_props.object_editor_data.wm_property


def get_wm_choose_group_props():
    return bpy.context.scene.curve_array_properties.engine_props.object_editor_data.wm_property.choose_group


def set_wm_choose_group_default():
    bpy.context.scene.curve_array_properties.engine_props.object_editor_data.wm_property.choose_group = '-1'


def get_array_settings_props():
    return bpy.context.scene.curve_array_properties.array_props.array_settings


def get_instant_data_props():
    return bpy.context.scene.curve_array_properties.engine_props.instant_data
