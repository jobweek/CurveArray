import bpy  # type: ignore
from Curve_Array_Magic_Curve.Errors.Errors import CancelError, show_message_box
from Curve_Array_Magic_Curve.Curve_Array.Object_Editor.Ops.Create_Empty_Group import create_group_manager


import traceback


class CURVEARRAY_OT_create_empty_group(bpy.types.Operator):
    """Create Random Group"""
    bl_label = "Create Group"
    bl_idname = 'curvearray.create_empty_group'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):

        try:

            create_group_manager()

            return {'FINISHED'}

        except CancelError:

            return {'CANCELLED'}

        except (Exception,):

            print(traceback.format_exc())
            show_message_box('Unknown Error', 'Please, open console and send me report', 'ERROR')

            return {'CANCELLED'}
