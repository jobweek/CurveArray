import bpy

class CRVARRPRO_PT_CurvePanel(bpy.types.Panel):
    bl_label = "Pick Path"
    bl_idname = "CRVARRPRO_PT_curve_panel"
    bl_space_type = 'VIEW_3D' 
    bl_region_type = 'UI'
    bl_category = 'CrvArrPro' 
    bl_parent_id = 'CRVARRPRO_PT_curve_array_pro'
    
    def draw(self, context):
        
        active_scene = bpy.context.scene 
        props = active_scene.curve_array_properties
        path = props.path_props.path_main.path_name
        icon = props.path_props.path_main.path_icon

        
        layout = self.layout
                
        row = layout.row()
        row.operator('crvarrpro.pick_curve', icon='CURVE_DATA')
        
        row = layout.row()
        row.label(text = "", icon = icon)
        
        if path != '':

            row.label(text = path)

        else:

            row.label(text = "'''Empty'''")            
            
        row.operator('crvarrpro.clear_curve', icon='CANCEL')