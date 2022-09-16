import bpy  # type: ignore
from ..Property.Get_Property_Path import (
    get_array_settings_props
)


class CURVEARRAY_PT_array_settings_panel(bpy.types.Panel):

    bl_label = 'Array Settings'
    bl_idname = 'CURVEARRAY_PT_array_settings_panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CrvArrMgcCrv'
    bl_parent_id = 'CURVEARRAY_PT_general_panel'

    def draw(self, _):

        array_set_props = get_array_settings_props()
        layout = self.layout

        layout.label(text='Spacing Type:', icon='TOOL_SETTINGS')
        layout.prop(array_set_props, 'spacing_type', text='')

        settings_box = layout.box()

        row = settings_box.row()
        row.label(text="Count:", icon='MOD_ARRAY')
        row.prop(array_set_props, "count", text="")

        oper = layout.row().operator('curvearray.create_array')
        oper.calculate_path_data = True
        oper.calculate_queue_data = True
        oper.spacing_type = array_set_props.spacing_type
        oper.count = array_set_props.count


