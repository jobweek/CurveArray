import bpy  # type: ignore
from Curve_Array_Magic_Curve.Errors.Errors import CancelError, show_message_box
from .Create_Set_Group import create_set_group_manager
import traceback


class CURVEARRAY_OT_create_set_group(bpy.types.Operator):
    """Set or Create and Set"""
    bl_label = "Set/Create Group"
    bl_idname = 'curvearray.create_set_group'

    call_owner: bpy.props.BoolProperty(
        name="call_owner",
        )

    owner_id: bpy.props.IntProperty(
        name="owner_id",
        )

    item_id: bpy.props.IntProperty(
        name="item_id",
        )

    target_id: bpy.props.StringProperty(
        name="target",
        )

    def execute(self, _):

        try:

            create_set_group_manager(self.call_owner, self.owner_id, self.item_id, self.target_id)

            return {'FINISHED'}

        except CancelError:

            return {'CANCELLED'}

        except (Exception,):

            print(traceback.format_exc())
            show_message_box('Unknown Error', 'Please, open console and send me report', 'ERROR')

            return {'CANCELLED'}
