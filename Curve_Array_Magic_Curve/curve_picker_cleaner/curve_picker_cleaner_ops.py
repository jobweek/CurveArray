import bpy

def ShowMessageBox(title, message, icon):

    def draw(self, context):
        self.layout.label(text = message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

class CRVARRPRO_OT_CurvePicker(bpy.types.Operator):
    '''Select Curve, witch be used for array, and press "Store"'''
    bl_label = "Store selected curve"
    bl_idname = 'crvarrpro.pick_curve'
    bl_options = {'REGISTER', 'UNDO'}
           
    def execute(self,context):
        
        selected_objects = bpy.context.selected_objects
        active_object = bpy.context.active_object
        object_type = active_object.type
        active_scene = bpy.context.scene     
        path_props = active_scene.curve_array_properties.path_props.path_main
        
        if active_object in selected_objects and len(selected_objects) == 1:
        
            if object_type == 'CURVE':
                
                splines_curve = active_object.data.splines
                
                if len(splines_curve)==1:
                                            
                    path_props.path_name  = bpy.context.active_object.name
                    bpy.ops.object.select_all(action='DESELECT')
                    path_props.path_icon = 'LOCKED'
       
                    return {'FINISHED'}
                                    
                else:
                    
                    ShowMessageBox("Error","Сurve should have only one spline", 'ERROR')
            
                    return {'CANCELLED'}
            
            else:
                
                ShowMessageBox("Error","Select Curve", 'ERROR')
            
                return {'CANCELLED'}
    
        else:
        
            ShowMessageBox("Error","Select only one curve", 'ERROR')
            
            return {'CANCELLED'}


class CRVARRPRO_OT_CurveCleaner(bpy.types.Operator):
    '''Clear selected curve'''
    bl_label = "Clear"
    bl_idname = 'crvarrpro.clear_curve'
        
    def execute(self,context):
        
        active_scene = bpy.context.scene
        path_props = active_scene.curve_array_properties.path_props.path_main
            
        path_props.path_icon = 'UNLOCKED'
        path_props.path_name = ''

        return {'FINISHED'}