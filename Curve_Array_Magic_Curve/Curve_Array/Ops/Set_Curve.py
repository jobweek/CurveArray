import bpy  # type: ignore
from Curve_Array_Magic_Curve.Errors.Errors import CancelError, show_message_box

import traceback


class CURVEARRAY_OT_set_curve(bpy.types.Operator):
    """Set Curve"""
    bl_label = "Set Curve"
    bl_idname = 'curvearray.set_curve'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):

        try:

            pass

            return {'FINISHED'}

        except CancelError:

            return {'CANCELLED'}

        except (Exception,):

            print(traceback.format_exc())
            show_message_box('Unknown Error', 'Please, open console and send me report', 'ERROR')

            return {'CANCELLED'}
