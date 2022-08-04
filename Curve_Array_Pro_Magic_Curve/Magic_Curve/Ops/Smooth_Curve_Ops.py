import bpy  # type: ignore
from ..Engine.Errors import CancelError, ShowMessageBox
from ..Engine.Smooth_Curve import (
    smooth_curve_manager,
)
import traceback


class MAGICCURVE_OT_create_smooth_curve(bpy.types.Operator):
    """Create curve from loop"""
    bl_label = "Curve from loop"
    bl_idname = 'magiccurve.create_smooth_curve'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):

        try:

            smooth_curve_manager()

            return {'FINISHED'}

        except CancelError:

            return {'CANCELLED'}

        finally:

            tr = traceback.format_exc()
            print(tr)
            ShowMessageBox('Unknown Error', 'Please, open console and send me report', 'ERROR')

            return {'CANCELLED'}
