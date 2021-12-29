import bpy

class CRVARRPRO_PT_MainPanel(bpy.types.Panel):
    bl_label = "Settings"
    bl_idname = "CRVARRPRO_PT_main_panel"
    bl_space_type = 'VIEW_3D' 
    bl_region_type = 'UI'
    bl_category = 'CrvArrPro'
    bl_parent_id = 'CRVARRPRO_PT_curve_array_pro' 
    
    def draw(self, context):
        
        layout = self.layout
        active_scene = bpy.context.scene
        my_props = context.scene.curve_array_properties.other_props.array_settings
        active_scene = bpy.context.scene 
        props = active_scene.curve_array_properties
        rot_props = props.transform_props.rotation_trform
        loc_props = props.transform_props.location_trform
        scale_props = props.transform_props.scale_trform

        row = layout.row()
        row.label(text = "Object cloning type:", icon = 'PARTICLE_POINT')
        
        row = layout.row()
        row.prop(my_props, "cloning_type")

        if my_props.cloning_type != 'OP3':

            row = layout.row()
            row.label(text = "Enable parenting:", icon = 'LINKED')
            row.prop(my_props, "enable_parenting", text = "")
        
        row = layout.row()
        row.label(text = "Type of spacing:", icon = 'TOOL_SETTINGS')
        
        row = layout.row()
        row.prop(my_props, "spacing_type")
        
        if my_props.spacing_type == 'OP1':
                
            row = layout.row()
            row.label(text = "Count:", icon = 'MOD_ARRAY')
            row.prop(my_props, "count", text = "")
                           
        elif my_props.spacing_type == 'OP2':            
            
            row = layout.row()
            row.label(text = "Type of ofset:", icon = 'TOOL_SETTINGS')
            row.prop(my_props, "ofset_type")

            if my_props.ofset_type == 'OP1':            
            
                row = layout.row()
                row.label(text = "Constant offset:", icon = 'DRIVER_DISTANCE')
                row.prop(my_props, "constant_ofset", text = "")

            elif my_props.ofset_type == 'OP2':

                row = layout.row()
                row.label(text = "Relative offset:", icon = 'DRIVER_DISTANCE')
                row.prop(my_props, "relative_ofset", text = "")
                                
        elif my_props.spacing_type == 'OP3':
            
            row = layout.row()
            row.label(text = "Count:", icon = 'MOD_ARRAY')
            row.prop(my_props, "count", text = "")            
            
            row = layout.row()
            row.label(text = "Type of ofset:", icon = 'TOOL_SETTINGS')
            row.prop(my_props, "ofset_type")

            if my_props.ofset_type == 'OP1':            
            
                row = layout.row()
                row.label(text = "Constant offset:", icon = 'DRIVER_DISTANCE')
                row.prop(my_props, "constant_ofset", text = "")

            elif my_props.ofset_type == 'OP2':

                row = layout.row()
                row.label(text = "Relative offset:", icon = 'DRIVER_DISTANCE')
                row.prop(my_props, "relative_ofset", text = "")

        if my_props.spacing_type == 'OP1' or my_props.spacing_type == 'OP2':     

            row = layout.row()
            row.label(text = "Start ofset:", icon = 'DRIVER_DISTANCE')
            row.prop(my_props, "start_ofset", text = "")
        
            row = layout.row()
            row.label(text = "End ofset:", icon = 'DRIVER_DISTANCE')
            row.prop(my_props, "end_ofset", text = "")
            
        row = layout.row()
        row.label(text = "Track axis:", icon = 'EMPTY_AXIS')
        row.prop(my_props, "rail_axis") 
            
        row = layout.row()
        row.label(text = "Align rotation:", icon = 'CON_ROTLIKE')
        row.prop(my_props, "align_rot", text = "")
                        
        row = layout.row()
        row.label(text = "Consider size of object:", icon = 'PIVOT_BOUNDBOX')
        row.prop(my_props, "size_ofset", text = "")

        row = layout.row()
        layout.operator('crvarrpro.transform_editor', icon = 'OPTIONS')
        
        row = layout.row()
        properdelv = layout.operator('crvarrpro.make_it')
        properdelv.count = my_props.count
        properdelv.main_ofset = my_props.main_ofset
        properdelv.relative_ofset = my_props.relative_ofset
        properdelv.constant_ofset = my_props.constant_ofset
        properdelv.ofset_type = my_props.ofset_type
        properdelv.spacing_type = my_props.spacing_type
        properdelv.start_ofset = my_props.start_ofset
        properdelv.end_ofset = my_props.end_ofset
        properdelv.rail_axis = my_props.rail_axis
        properdelv.align_rot = my_props.align_rot
        properdelv.size_ofset = my_props.size_ofset
        properdelv.cloning_type = my_props.cloning_type
        properdelv.enable_parenting = my_props.enable_parenting
        properdelv.rotation_progressive_x = rot_props.rotation_progressive_x
        properdelv.rotation_min_x = rot_props.rotation_min_x
        properdelv.rotation_max_x = rot_props.rotation_max_x
        properdelv.rotation_progressive_y = rot_props.rotation_progressive_y
        properdelv.rotation_min_y = rot_props.rotation_min_y
        properdelv.rotation_max_y = rot_props.rotation_max_y
        properdelv.rotation_progressive_z = rot_props.rotation_progressive_z
        properdelv.rotation_min_z = rot_props.rotation_min_z
        properdelv.rotation_max_z = rot_props.rotation_max_z
        properdelv.location_progressive_x = loc_props.location_progressive_x
        properdelv.location_min_x = loc_props.location_min_x
        properdelv.location_max_x = loc_props.location_max_x
        properdelv.location_progressive_y = loc_props.location_progressive_y
        properdelv.location_min_y = loc_props.location_min_y
        properdelv.location_max_y = loc_props.location_max_y
        properdelv.location_progressive_z = loc_props.location_progressive_z
        properdelv.location_min_z = loc_props.location_min_z
        properdelv.location_max_z = loc_props.location_max_z
        properdelv.scale_progressive_x = scale_props.scale_progressive_x
        properdelv.scale_min_x = scale_props.scale_min_x
        properdelv.scale_max_x = scale_props.scale_max_x
        properdelv.scale_progressive_y = scale_props.scale_progressive_y
        properdelv.scale_min_y = scale_props.scale_min_y
        properdelv.scale_max_y = scale_props.scale_max_y
        properdelv.scale_progressive_z = scale_props.scale_progressive_z
        properdelv.scale_min_z = scale_props.scale_min_z
        properdelv.scale_max_z = scale_props.scale_max_z