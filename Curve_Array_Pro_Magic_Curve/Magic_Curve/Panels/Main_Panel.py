import bpy  # type: ignore


class MAGICCURVE_PT_panel(bpy.types.Panel):
    bl_label = "Magic Curve"
    bl_idname = "MAGICCURVE_PT_mgcrv_panel"
    bl_space_type = 'VIEW_3D' 
    bl_region_type = 'UI'
    bl_category = 'CrvArrPro' 
    
    def draw(self, _):

        props = bpy.context.scene.magic_curve_properties

        layout = self.layout
                            
        row = layout.row()
        row.operator('magiccurve.create_split_curve', text="Split Curve")
        row = layout.row()
        row.operator('magiccurve.create_smooth_curve', text="Smooth Curve")
        row = layout.row()
        row.operator('magiccurve.switch_twist_method', text="Switch Twist Method")
        row = layout.row()
        row.operator('magiccurve.switch_direction', text="Switch Сurve direction")
        row = layout.row()
        row.operator('magiccurve.toggle_cyclic', text="Toggle Cyclic")
        row = layout.row()
        row.prop(props, "precision", text="Precision")
