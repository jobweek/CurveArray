import bpy  # type: ignore
from ..Engine.Errors import CancelError
from ..Engine.General_Functions import first_step, second_step, final_step
from ..Engine.Split_Curve import (
    split_curve_manager,
)


class MAGICCURVE_OT_Create_Split_Curve(bpy.types.Operator):
    """Create curve from loop"""
    bl_label = "Curve from loop"
    bl_idname = 'magiccurve.create_split_curve'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        try:

            split_curve_manager()

            return {'FINISHED'}

        except CancelError:

            return {'CANCELLED'}

        # except Exception as err:

        #     ShowMessageBox("Unknown Error, Please send me this report:", repr(err), 'ERROR')

        #     return {'CANCELLED'}
