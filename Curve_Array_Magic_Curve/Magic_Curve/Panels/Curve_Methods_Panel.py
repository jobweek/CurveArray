import bpy  # type: ignore


class MAGICCURVE_PT_curve_methods_panel(bpy.types.Panel):
    bl_label = "Curve Methods"
    bl_idname = "MAGICCURVE_PT_curve_methods_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CrvArrPro'
    bl_parent_id = 'MAGICCURVE_PT_main_panel'

    def draw(self, _):
        layout = self.layout

        row = layout.row()
        row.operator('magiccurve.switch_direction', text="Switch Сurve direction")

        row = layout.row()
        row.operator('magiccurve.toggle_cyclic', text="Toggle Cyclic")

        row = layout.row()
        row.operator('magiccurve.switch_twist_method', text="Switch Twist Method")
