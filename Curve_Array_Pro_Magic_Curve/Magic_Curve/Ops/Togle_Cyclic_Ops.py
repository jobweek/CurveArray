import bpy  # type: ignore
from ..Engine.Errors import CancelError, ShowMessageBox
from ..Engine.Switch_Direction import (
    recalculate_curve_manager
)


class MAGICCURVE_OT_togle_cyclic(bpy.types.Operator):
    """Switch curve direction and recalculate to right tilt"""
    bl_label = "Togle Curve Cyclic"
    bl_idname = 'magiccurve.togle_cyclic'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):

        try:

            recalculate_curve_manager()

            return {'FINISHED'}

        except CancelError:

            return {'CANCELLED'}

        except Exception as err:

            ShowMessageBox("Unkown Error, Please send me this report:", repr(err), 'ERROR')

            return {'CANCELLED'}
