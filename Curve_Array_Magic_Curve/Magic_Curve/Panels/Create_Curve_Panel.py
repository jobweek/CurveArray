import bpy  # type: ignore


class MAGICCURVE_PT_create_curve_panel(bpy.types.Panel):
    bl_label = "Create Curve"
    bl_idname = "MAGICCURVE_PT_create_curve_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = 'MAGICCURVE_PT_general_panel'

    def draw(self, _):
        layout = self.layout

        row = layout.row(align=True)
        row.operator('magiccurve.create_smooth_curve', text="Smooth")
        row.operator('magiccurve.create_split_curve', text="Split")
