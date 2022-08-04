import bpy  # type: ignore
from ..Engine.Errors import CancelError, ShowMessageBox
from ..Engine.Switch_Direction import (
    recalculate_curve_manager
)
import traceback


class MAGICCURVE_OT_switch_direction(bpy.types.Operator):
    """Switch curve direction and recalculate to right tilt"""
    bl_label = "Switch curve direction"
    bl_idname = 'magiccurve.switch_direction'
    bl_options = {'REGISTER', 'UNDO'}
        
    def execute(self, _):
 
        try:
            
            recalculate_curve_manager()
        
            return {'FINISHED'}
        
        except CancelError:
            
            return {'CANCELLED'}

        except (Exception,):

            print(traceback.format_exc())
            ShowMessageBox('Unknown Error', 'Please, open console and send me report', 'ERROR')

            return {'CANCELLED'}
