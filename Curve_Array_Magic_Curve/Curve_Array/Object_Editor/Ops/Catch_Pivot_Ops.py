import bpy  # type: ignore
from Curve_Array_Magic_Curve.Errors.Errors import CancelError, show_message_box
from Curve_Array_Magic_Curve.Curve_Array.Object_Editor.Ops.Catch_Pivot import catch_pivot_manager


import traceback


class CURVEARRAY_OT_catch_pivot(bpy.types.Operator):
    """Clear all objects in Object Editor"""
    bl_label = "Clear All"
    bl_idname = 'curvearray.catch_pivot'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):

        try:

            catch_pivot_manager()

            return {'FINISHED'}

        except CancelError:

            return {'CANCELLED'}

        except (Exception,):

            print(traceback.format_exc())
            show_message_box('Unknown Error', 'Please, open console and send me report', 'ERROR')

            return {'CANCELLED'}
