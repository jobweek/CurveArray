import bpy  # type: ignore
import traceback
from Curve_Array_Magic_Curve.Errors.Errors import CancelError, show_message_box
from .Create_Array import crete_array_manager
from ..General_Data_Classes import CreateArrayPrams
from ...Property.Get_Property_Path import get_array_settings_props


class CURVEARRAY_OT_create_array(bpy.types.Operator):
    """Create curve along path"""
    bl_label = "Create Array"
    bl_idname = 'curvearray.create_array'
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, _):

        layout = self.layout
        sett = get_array_settings_props()

        split = layout.box().split(factor=0.5)
        left_side = split.column()
        right_side = split.column()

        left_side.row().label(text='Random Seed:')
        right_side.row().prop(sett, 'random_seed', text='')

        left_side.row().label(text='Cloning Type:')
        right_side.row().prop(sett, 'cloning_type', text='')

        left_side.row().label(text='Count:')
        right_side.row().prop(sett, 'count', text='')

        left_side.row().label(text='Slide:')
        right_side.row().prop(sett, 'slide', text='')

    def execute(self, _):
        return {'FINISHED'}

    def invoke(self, context, _):

        try:

            array_params = CreateArrayPrams(
                calculate_path_data=True,
                calculate_queue_data=True,
                create_object_list=True,
            )

            crete_array_manager(array_params)

        except CancelError:
            pass

        except (Exception,):

            print(traceback.format_exc())
            show_message_box('Unknown Error', 'Please, open console and send me report', 'ERROR')

        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=216)
