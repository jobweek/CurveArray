import bpy  # type: ignore
from Curve_Array_Magic_Curve.Errors.Errors import CancelError, show_message_box
from .Remove_Item import groups_remove_manager
import traceback


class CURVEARRAY_OT_remove_item(bpy.types.Operator):
    """Remove item for queue or group"""
    bl_label = "Remove item from Queue or Group"
    bl_idname = 'curvearray.remove_item'

    call_owner: bpy.props.BoolProperty(
        name="call_owner",
        )

    owner_id: bpy.props.IntProperty(
        name="owner_id",
        )

    item_id: bpy.props.IntProperty(
        name="item_id",
        )

    def execute(self, _):

        try:

            groups_remove_manager(self.call_owner, self.owner_id, self.item_id)

            return {'FINISHED'}

        except CancelError:

            return {'CANCELLED'}

        except (Exception,):

            print(traceback.format_exc())
            show_message_box('Unknown Error', 'Please, open console and send me report', 'ERROR')

            return {'CANCELLED'}
