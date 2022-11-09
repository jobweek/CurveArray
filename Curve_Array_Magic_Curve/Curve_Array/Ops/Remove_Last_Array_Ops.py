import bpy  # type: ignore
import traceback
from Curve_Array_Magic_Curve.Errors.Errors import CancelError, show_message_box
from .Remove_Last_Array_Functions import remove_last_array_manager


class CURVEARRAY_OT_remove_last_array(bpy.types.Operator):
    bl_label = "Remove Last Array"
    bl_idname = 'curvearray.remove_last_array'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):
        try:

            remove_last_array_manager()

            return {'FINISHED'}

        except CancelError:

            return {'CANCELLED'}

        except (Exception,):

            print(traceback.format_exc())
            show_message_box('Unknown Error', 'Please, open console and send me report', 'ERROR')

            return {'CANCELLED'}
