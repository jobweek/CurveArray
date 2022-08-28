import bpy  # type: ignore
from ..Engine.Core.Path_Calculation import path_calculation_manager


class CURVEARRAY_OT_path_calc(bpy.types.Operator):
    """Create curve from loop"""
    bl_label = "Test"
    bl_idname = 'magiccurve.path_calc'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):

        path_calculation_manager(bpy.context.active_object)

