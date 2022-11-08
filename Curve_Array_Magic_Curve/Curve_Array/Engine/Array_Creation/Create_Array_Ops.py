import bpy  # type: ignore
import traceback
from Curve_Array_Magic_Curve.Errors.Errors import CancelError, show_message_box
from .Create_Array import crete_array_manager
from ..General_Data_Classes import CreateArrayPrams


class CURVEARRAY_OT_create_array(bpy.types.Operator):
    """Create curve along path"""
    bl_label = "Create Array"
    bl_idname = 'curvearray.create_array'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, _):
        try:

            array_params = CreateArrayPrams(
                calculate_path_data=True,
                calculate_queue_data=True,
                create_object_list=True,
            )
            crete_array_manager(array_params)
            return {'FINISHED'}

        except CancelError:
            return {'CANCELLED'}

        except (Exception,):

            print(traceback.format_exc())
            show_message_box('Unknown Error', 'Please, open console and send me report', 'ERROR')
            return {'CANCELLED'}
