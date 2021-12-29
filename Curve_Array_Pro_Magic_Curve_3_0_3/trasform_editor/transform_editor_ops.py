import bpy

class CRVARRPRO_OT_TransformEditor(bpy.types.Operator):
    '''Editing Objects Transformation'''
    bl_label = "Transform Editor"
    bl_idname = 'crvarrpro.transform_editor'
    bl_options = {'UNDO'}

    def draw(self, context):    
        active_scene = bpy.context.scene 
        props = active_scene.curve_array_properties
        rot_props = props.transform_props.rotation_trform
        loc_props = props.transform_props.location_trform
        scale_props = props.transform_props.scale_trform
        layout = self.layout

        col = layout.box().column()
        row_1 = col.row()
        split = row_1.split(factor = 0.2)
        split_1 = split.row()
        split = split.split(factor = 0.333)
        split_2 = split.row()
        split_3 = split.row(align = True)

        split_1.label(text= '')
        split_2.label(text= '  Progressive')
        split_3.label(text= '   Rand Min ')
        split_3.label(text= '   Rand Max ')

        col = layout.box().column()
        row_1 = col.row()
        row_2 = col.row()
        row_3 = col.row()

        split = row_1.split(factor = 0.2)
        split_1 = split.row()
        split = split.split(factor = 0.333)
        split_2 = split.row()
        split_3 = split.row(align = True)

        split_1.label(text= 'Rotation X')
        split_2.prop(rot_props, "rotation_progressive_x", text = "")
        split_3.prop(rot_props, "rotation_min_x", text = "")
        split_3.prop(rot_props, "rotation_max_x", text = "")

        split = row_2.split(factor = 0.2)
        split_1 = split.row()
        split = split.split(factor = 0.333)
        split_2 = split.row()
        split_3 = split.row(align = True)

        split_1.label(text= 'Rotation Y')
        split_2.prop(rot_props, "rotation_progressive_y", text = "")
        split_3.prop(rot_props, "rotation_min_y", text = "")
        split_3.prop(rot_props, "rotation_max_y", text = "")

        split = row_3.split(factor = 0.2)
        split_1 = split.row()
        split = split.split(factor = 0.333)
        split_2 = split.row()
        split_3 = split.row(align = True)

        split_1.label(text= 'Rotation Z')
        split_2.prop(rot_props, "rotation_progressive_z", text = "")
        split_3.prop(rot_props, "rotation_min_z", text = "")
        split_3.prop(rot_props, "rotation_max_z", text = "")

        col = layout.box().column()
        row_1 = col.row()
        row_2 = col.row()
        row_3 = col.row()

        split = row_1.split(factor = 0.2)
        split_1 = split.row()
        split = split.split(factor = 0.333)
        split_2 = split.row()
        split_3 = split.row(align = True)

        split_1.label(text= 'Location X')
        split_2.prop(loc_props, "location_progressive_x", text = "")
        split_3.prop(loc_props, "location_min_x", text = "")
        split_3.prop(loc_props, "location_max_x", text = "")

        split = row_2.split(factor = 0.2)
        split_1 = split.row()
        split = split.split(factor = 0.333)
        split_2 = split.row()
        split_3 = split.row(align = True)

        split_1.label(text= 'Location Y')
        split_2.prop(loc_props, "location_progressive_y", text = "")
        split_3.prop(loc_props, "location_min_y", text = "")
        split_3.prop(loc_props, "location_max_y", text = "")

        split = row_3.split(factor = 0.2)
        split_1 = split.row()
        split = split.split(factor = 0.333)
        split_2 = split.row()
        split_3 = split.row(align = True)

        split_1.label(text= 'Location Z')
        split_2.prop(loc_props, "location_progressive_z", text = "")
        split_3.prop(loc_props, "location_min_z", text = "")
        split_3.prop(loc_props, "location_max_z", text = "")

        col = layout.box().column()
        row_1 = col.row()
        row_2 = col.row()
        row_3 = col.row()

        split = row_1.split(factor = 0.2)
        split_1 = split.row()
        split = split.split(factor = 0.333)
        split_2 = split.row()
        split_3 = split.row(align = True)

        split_1.label(text= 'Scale X')
        split_2.prop(scale_props, "scale_progressive_x", text = "")
        split_3.prop(scale_props, "scale_min_x", text = "")
        split_3.prop(scale_props, "scale_max_x", text = "")

        split = row_2.split(factor = 0.2)
        split_1 = split.row()
        split = split.split(factor = 0.333)
        split_2 = split.row()
        split_3 = split.row(align = True)

        split_1.label(text= 'Scale Y')
        split_2.prop(scale_props, "scale_progressive_y", text = "")
        split_3.prop(scale_props, "scale_min_y", text = "")
        split_3.prop(scale_props, "scale_max_y", text = "")

        split = row_3.split(factor = 0.2)
        split_1 = split.row()
        split = split.split(factor = 0.333)
        split_2 = split.row()
        split_3 = split.row(align = True)

        split_1.label(text= 'Scale Z')
        split_2.prop(scale_props, "scale_progressive_z", text = "")
        split_3.prop(scale_props, "scale_min_z", text = "")
        split_3.prop(scale_props, "scale_max_z", text = "")

    def execute(self,context):
        
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=300)
        
                
        return {'FINISHED'}
