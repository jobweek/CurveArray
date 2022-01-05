import bpy

class CRVARRPRO_PT_CurveArrayPro(bpy.types.Panel):
    bl_label = "Curve Array Pro"
    bl_idname = "CRVARRPRO_PT_curve_array_pro"
    bl_space_type = 'VIEW_3D' 
    bl_region_type = 'UI'
    bl_category = 'CrvArrPro' 

    def draw(self, context):
        layout = self.layout              
        row = layout.row()