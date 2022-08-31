import bpy  # type: ignore
from Curve_Array_Magic_Curve.Errors.Errors import CancelError, show_message_box
from Curve_Array_Magic_Curve.Curve_Array.Object_Editor.Ops.Add_Objects import add_objects_manager


import traceback


class CURVEARRAY_OT_add_objects(bpy.types.Operator):
    """Add Objects"""
    bl_label = "Add objects"
    bl_idname = 'curvearray.add_objects'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):

        try:

            add_objects_manager()

            return {'FINISHED'}

        except CancelError:

            return {'CANCELLED'}

        except (Exception,):

            print(traceback.format_exc())
            show_message_box('Unknown Error', 'Please, open console and send me report', 'ERROR')

            return {'CANCELLED'}
