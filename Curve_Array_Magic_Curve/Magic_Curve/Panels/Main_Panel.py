import bpy  # type: ignore


class MAGICCURVE_PT_main_panel(bpy.types.Panel):
    bl_label = "Magic Curve"
    bl_idname = "MAGICCURVE_PT_main_panel"
    bl_space_type = 'VIEW_3D' 
    bl_region_type = 'UI'
    bl_category = 'CrvArrPro' 

    def draw(self, _):

        pass
