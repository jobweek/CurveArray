import bpy  # type: ignore
from Curve_Array_Magic_Curve.Errors.Errors import CancelError, show_message_box
from Curve_Array_Magic_Curve.Curve_Array.Object_Editor.Ops.Queue_Move import queue_move_manager


import traceback


class CURVEARRAY_OT_queue_move(bpy.types.Operator):
    """Move Queue"""
    bl_label = "Move queue"
    bl_idname = 'curvearray.queue_move'

    index: bpy.props.IntProperty(
        name="Index",
        )

    direction: bpy.props.BoolProperty(
        name="Direction",
        )

    def execute(self, _):

        try:

            queue_move_manager(self.index, self.direction)

            return {'FINISHED'}

        except CancelError:

            return {'CANCELLED'}

        except (Exception,):

            print(traceback.format_exc())
            show_message_box('Unknown Error', 'Please, open console and send me report', 'ERROR')

            return {'CANCELLED'}
