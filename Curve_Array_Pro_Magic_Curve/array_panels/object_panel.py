import bpy

from Curve_Array_Pro_Magic_Curve_3_0_3.props.curve_array_props import (
Obj_Stor_Draw_Count,
Obj_Stor_Draw_ObjName
)

class CRVARRPRO_PT_ObjectPanel(bpy.types.Panel):
    bl_label = "Choose object"
    bl_idname = "CRVARRPRO_PT_object_panel"
    bl_space_type = 'VIEW_3D' 
    bl_region_type = 'UI'
    bl_category = 'CrvArrPro' 
    bl_parent_id = 'CRVARRPRO_PT_curve_array_pro'
    
    def draw(self, context):
        
        active_scene = bpy.context.scene 
        props = active_scene.curve_array_properties
        #icon = props.object_props.obj_icon
        count = Obj_Stor_Draw_Count()
        layout = self.layout

        row = layout.row()
        row.operator('crvarrpro.pick_object', icon='MESH_DATA')        
        
        row = layout.row()
        row.label(text = 'Object(s) stored:')
        row.label(text = str(count))

        row = layout.box().split(factor = 0.5)
        row_l = row.column()
        row_r = row.column()

        if count == 0:

            row_l.label(text = '')            

        else:

            i = 0

            while i < count:

                row_l.label(text = Obj_Stor_Draw_ObjName(i))      

                i += 1

                try:

                    row_r.label(text = Obj_Stor_Draw_ObjName(i))    

                    i += 1 

                except:             

                    row_r.label(text = '')   
                    
        row = layout.row()
        row.operator('crvarrpro.clear_object', icon='CANCEL')

        row = layout.row()
        row.operator('crvarrpro.object_editor', icon='OPTIONS') 