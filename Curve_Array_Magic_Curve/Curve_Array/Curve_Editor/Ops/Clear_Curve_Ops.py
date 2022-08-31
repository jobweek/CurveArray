import bpy  # type: ignore
from Curve_Array_Magic_Curve.Errors.Errors import CancelError, show_message_box
from Curve_Array_Magic_Curve.Curve_Array.Curve_Editor.Ops.Clear_Curve import clear_curve_manager


import traceback


class CURVEARRAY_OT_clear_curve(bpy.types.Operator):
    """Clear Curve"""
    bl_label = "Clear Curve"
    bl_idname = 'curvearray.clear_curve'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):

        try:

            clear_curve_manager()

            return {'FINISHED'}

        except CancelError:

            return {'CANCELLED'}

        except (Exception,):

            print(traceback.format_exc())
            show_message_box('Unknown Error', 'Please, open console and send me report', 'ERROR')

            return {'CANCELLED'}
