import bpy  # type: ignore
from Curve_Array_Pro_Magic_Curve.Errors.Errors import CancelError, show_message_box
from ..Engine.Curve_Array_By_Offset import (
    curve_array_by_offset_manager,
)
import traceback


class CURVEARRAY_OT_create_array_by_offset(bpy.types.Operator):
    """Create curve from loop"""
    bl_label = "Create Array along Curve"
    bl_idname = 'curvearray.create_array_by_offset'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):

        try:

            curve_array_by_offset_manager(bpy.context.active_object, None, None)

            return {'FINISHED'}

        except CancelError:

            return {'CANCELLED'}

        except (Exception,):

            print(traceback.format_exc())
            show_message_box('Unknown Error', 'Please, open console and send me report', 'ERROR')

            return {'CANCELLED'}
