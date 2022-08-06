import bpy  # type: ignore
from Curve_Array_Pro_Magic_Curve.Errors.Errors import CancelError, ShowMessageBox
from ..Engine.Curve_Array import (
    curve_array_manager,
)
import traceback


class MAGICCURVE_OT_create_smooth_curve(bpy.types.Operator):
    """Create curve from loop"""
    bl_label = "Curve from loop"
    bl_idname = 'magiccurve.create_smooth_curve'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):

        try:

            curve_array_manager()

            return {'FINISHED'}

        except CancelError:

            return {'CANCELLED'}

        except (Exception,):

            print(traceback.format_exc())
            ShowMessageBox('Unknown Error', 'Please, open console and send me report', 'ERROR')

            return {'CANCELLED'}
