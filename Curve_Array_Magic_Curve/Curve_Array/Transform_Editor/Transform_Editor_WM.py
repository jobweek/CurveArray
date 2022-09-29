import bpy  # type: ignore
from typing import Any
from ..Property.Get_Property_Path import (
    get_queue_props,
    get_objects_props,
    get_groups_props,
    get_wm_props,
    get_wm_choose_group_props,
)


class CURVEARRAY_OT_open_transform_editor(bpy.types.Operator):
    """Editing Objects which will be used for array creation"""
    bl_label = "Transform Editor"
    bl_idname = 'curvearray.open_transform_editor'
    bl_options = {'UNDO'}

    def draw(self, _):

        groups = get_groups_props()
        objects = get_objects_props()
        queue = get_queue_props()
        wm_props = get_wm_props()
        wm_choose_group = get_wm_choose_group_props()

        layout = self.layout

    def execute(self, _):

        for area in bpy.context.window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()

        return {'FINISHED'}

    def invoke(self, context, _):
        wm = context.window_manager

        return wm.invoke_props_dialog(self, width=540)

