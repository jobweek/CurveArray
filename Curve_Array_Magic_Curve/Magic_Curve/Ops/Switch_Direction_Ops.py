import bpy  # type: ignore
from ...Errors.Errors import CancelError, show_message_box
from ..Engine.Switch_Direction import (
    switch_curve_direction_manager
)
import traceback


class MAGICCURVE_OT_switch_direction(bpy.types.Operator):
    """Switch curve direction and recalculate to right tilt"""
    bl_label = "Switch curve direction"
    bl_idname = 'magiccurve.switch_direction'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):
 
        try:
            
            switch_curve_direction_manager()
        
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
