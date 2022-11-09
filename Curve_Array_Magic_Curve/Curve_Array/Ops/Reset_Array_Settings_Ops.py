import bpy  # type: ignore
import traceback
from Curve_Array_Magic_Curve.Errors.Errors import CancelError, show_message_box
from .Reset_Array_Settings_Functions import reset_array_settings_manager


class CURVEARRAY_OT_reset_array_settings(bpy.types.Operator):
    bl_label = "Reset Array Settings"
    bl_idname = 'curvearray.reset_array_settings'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):
        try:

            reset_array_settings_manager()

            return {'FINISHED'}

        except CancelError:

            return {'CANCELLED'}

        except (Exception,):

            print(traceback.format_exc())
            show_message_box('Unknown Error', 'Please, open console and send me report', 'ERROR')

            return {'CANCELLED'}
