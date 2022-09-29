import bpy  # type: ignore
from Curve_Array_Magic_Curve.Errors.Errors import CancelError, show_message_box
from .Reset_Transform import reset_transform_manager


import traceback


class CURVEARRAY_OT_reset_transform(bpy.types.Operator):
    """Reset Transform"""
    bl_label = "Reset Transform"
    bl_idname = 'curvearray.reset_transform'

    index: bpy.props.IntProperty(
        name="Index",
        )

    def execute(self, _):

        try:

            reset_transform_manager(self.index)

            return {'FINISHED'}

        except CancelError:

            return {'CANCELLED'}

        except (Exception,):

            print(traceback.format_exc())
            show_message_box('Unknown Error', 'Please, open console and send me report', 'ERROR')

            return {'CANCELLED'}
