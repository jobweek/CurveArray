import bpy

class CRVARRPRO_PT_ButtonPanel(bpy.types.Panel):
    bl_label = "Useful buttons"
    bl_idname = "CRVARRPRO_PT_button_panel"
    bl_space_type = 'VIEW_3D' 
    bl_region_type = 'UI'
    bl_category = 'CrvArrPro' 
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):

        active_scene = bpy.context.scene
        my_props = active_scene.curve_array_properties.other_props.array_settings   
        layout = self.layout

        row = layout.row()
        row.operator('crvarrpro.delete_last_array', icon='CANCEL')        

        row = layout.row()
        row.operator('crvarrpro.reset_settings', icon='OPTIONS')   

        #row = layout.row()
        #row.operator('crvarrpro.flip_curve', icon='FILE_REFRESH')   