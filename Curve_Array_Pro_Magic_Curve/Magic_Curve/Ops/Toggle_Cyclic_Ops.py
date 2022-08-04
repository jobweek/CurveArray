import bpy  # type: ignore
from ..Engine.Errors import CancelError, ShowMessageBox
from ..Engine.Toggle_Cyclic import (
    toggle_cyclic_manager
)


class MAGICCURVE_OT_togle_cyclic(bpy.types.Operator):
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

        except Exception as err:

            ShowMessageBox("Unkown Error, Please send me this report:", repr(err), 'ERROR')

            return {'CANCELLED'}
