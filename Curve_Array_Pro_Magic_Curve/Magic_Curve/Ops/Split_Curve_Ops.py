import bpy  # type: ignore
from ..Engine.Errors import CancelError, ShowMessageBox
from ..Engine.Split_Curve import (
    split_curve_manager,
)
import traceback


class MAGICCURVE_OT_create_split_curve(bpy.types.Operator):
    """Create curve from loop"""
    bl_label = "Curve from loop"
    bl_idname = 'magiccurve.create_split_curve'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):

        try:

            split_curve_manager()

            return {'FINISHED'}

        except CancelError:

            return {'CANCELLED'}

        except (Exception,):

            print(traceback.format_exc())
            ShowMessageBox('Unknown Error', 'Please, open console and send me report', 'ERROR')

            return {'CANCELLED'}
