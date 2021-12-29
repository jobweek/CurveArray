import bpy

class CRVARRPRO_OT_Reset_Settings(bpy.types.Operator):
    '''Reset all settings to default'''
    bl_label = "Reset All Settings"
    bl_idname = 'crvarrpro.reset_settings'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self,context):
        
        active_scene = bpy.context.scene
        my_props = active_scene.curve_array_properties
        array_props = my_props.other_props.array_settings
        rot_props = my_props.transform_props.rotation_trform
        loc_props = my_props.transform_props.location_trform
        scale_props = my_props.transform_props.scale_trform
        
        array_props.slide = 0
        array_props.count = 1
        array_props.relative_ofset = 1
        array_props.constant_ofset = 1
        array_props.ofset_type = 'OP1'
        array_props.cloning_type = 'OP3'
        array_props.enable_parenting = False
        array_props.spacing_type = 'OP1'
        array_props.start_ofset = 0
        array_props.end_ofset = 0
        array_props.size_ofset = False
        array_props.rail_axis = '+x'
        array_props.align_rot = True

        rot_props.rotation_progressive_x = 0
        rot_props.rotation_progressive_y = 0
        rot_props.rotation_progressive_z = 0
        rot_props.rotation_min_x = 0
        rot_props.rotation_min_y = 0
        rot_props.rotation_min_z = 0
        rot_props.rotation_max_x = 0
        rot_props.rotation_max_y = 0
        rot_props.rotation_max_z = 0
        loc_props.location_progressive_x = 0
        loc_props.location_progressive_y = 0
        loc_props.location_progressive_z = 0
        loc_props.location_min_x = 0
        loc_props.location_min_y = 0
        loc_props.location_min_z = 0
        loc_props.location_max_x = 0
        loc_props.location_max_y = 0
        loc_props.location_max_z = 0
        scale_props.scale_progressive_x = 0
        scale_props.scale_progressive_y = 0
        scale_props.scale_progressive_z = 0
        scale_props.scale_min_x = 0
        scale_props.scale_min_y = 0
        scale_props.scale_min_z = 0
        scale_props.scale_max_x = 0
        scale_props.scale_max_y = 0
        scale_props.scale_max_z = 0

        return {'FINISHED'}
                