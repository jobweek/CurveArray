import bpy  # type: ignore


class CURVEARRAY_PT_main_panel(bpy.types.Panel):
    bl_label = "Settings"
    bl_idname = "CRVARRPRO_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Curve_Array'
    bl_parent_id = 'CRVARRPRO_PT_curve_array_pro'

    def draw(self, context):

        pass
