import bpy  # type: ignore
from Curve_Array_Pro_Magic_Curve.Errors.Errors import CancelError, show_message_box
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
            show_message_box('Unknown Error', 'Please, open console and send me report', 'ERROR')

            return {'CANCELLED'}
