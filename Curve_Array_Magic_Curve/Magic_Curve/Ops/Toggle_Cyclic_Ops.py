import bpy  # type: ignore
from ...Errors.Errors import CancelError, show_message_box
from ..Engine.Toggle_Cyclic import (
    toggle_cyclic_manager
)
import traceback


class MAGICCURVE_OT_toggle_cyclic(bpy.types.Operator):
    """Switch curve direction and recalculate to right tilt"""
    bl_label = "Toggle Curve Cyclic"
    bl_idname = 'magiccurve.toggle_cyclic'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):

        try:

            toggle_cyclic_manager()

            return {'FINISHED'}

        except CancelError:

            return {'CANCELLED'}

        except AssertionError:

            print(traceback.format_exc())
            show_message_box('Programm Error', 'Please, open console and send me report', 'ERROR')

        except (Exception,):

            print(traceback.format_exc())
            show_message_box('Unknown Error', 'Please, open console and send me report', 'ERROR')

            return {'CANCELLED'}
