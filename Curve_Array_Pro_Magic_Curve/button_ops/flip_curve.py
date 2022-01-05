import bpy

class CRVARRPRO_OT_Flip_Curve(bpy.types.Operator):
    '''Flip Curve with correct tilt'''
    bl_label = "Flip Curve"
    bl_idname = 'crvarrpro.flip_curve'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self,context):
        
        active_scene = bpy.context.scene
        my_props = active_scene.curve_array_properties.other_props.array_settings   

        return {'FINISHED'}
                