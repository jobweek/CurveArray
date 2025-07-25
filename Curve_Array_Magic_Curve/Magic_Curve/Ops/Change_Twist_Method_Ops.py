import bpy  # type: ignore
from ...Errors.Errors import CancelError, show_message_box
from ..Engine.Change_Twist_Method import (
    switch_twist_method_manager
)
import traceback


class MAGICCURVE_OT_switch_twist_method(bpy.types.Operator):
    """Switch curve direction and recalculate to right tilt"""
    bl_label = "Change Twist Method"
    bl_idname = 'magiccurve.change_twist_method'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):

        try:

            switch_twist_method_manager()

            return {'FINISHED'}

        except CancelError:

            return {'CANCELLED'}

        except AssertionError:

            print(traceback.format_exc())
            show_message_box('Programm Error', 'Please, open console and send me report', 'ERROR')

            return {'CANCELLED'}

        except (Exception,):

            print(traceback.format_exc())
            show_message_box('Unknown Error', 'Please, open console and send me report', 'ERROR')

            return {'CANCELLED'}
