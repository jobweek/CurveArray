import bpy # type: ignore

class MAGICCURVE_PT_mgcrv_panel(bpy.types.Panel):
    bl_label = "Magic Curve"
    bl_idname = "MAGICCURVE_PT_mgcrv_panel"
    bl_space_type = 'VIEW_3D' 
    bl_region_type = 'UI'
    bl_category = 'CrvArrPro' 
    
    def draw(self, context):    
                
        layout = self.layout
                            
        row = layout.row()
        properdelv = row.operator('magiccurve.mgcrv_ops', text = "Smooth Curve")
        properdelv.curve_type = False
        properdelv = row.operator('magiccurve.mgcrv_ops', text = "Strong Curve")
        properdelv.curve_type = True