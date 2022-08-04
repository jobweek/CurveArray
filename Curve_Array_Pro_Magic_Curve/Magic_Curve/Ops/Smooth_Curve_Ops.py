import bpy  # type: ignore
from ..Engine.Errors import CancelError, ShowMessageBox
from ..Engine.Smooth_Curve import (
    smooth_curve_manager,
)


class MAGICCURVE_OT_create_smooth_curve(bpy.types.Operator):
    """Create curve from loop"""
    bl_label = "Curve from loop"
    bl_idname = 'magiccurve.create_smooth_curve'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):

        try:

            smooth_curve_manager()

            return {'FINISHED'}

        except CancelError:

            return {'CANCELLED'}

        except Exception as err:

            ShowMessageBox("Unknown Error, Please send me this report:", repr(err), 'ERROR')

            return {'CANCELLED'}
