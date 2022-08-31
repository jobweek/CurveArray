import bpy  # type: ignore


class CURVEARRAY_PT_general_panel(bpy.types.Panel):

    bl_label = 'Curve Array'
    bl_idname = 'CURVEARRAY_PT_general_panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CurveArray'

    def draw(self, _):
        pass
