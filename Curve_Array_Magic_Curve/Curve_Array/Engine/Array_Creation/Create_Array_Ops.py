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

    def update_func_random_seed(self, _):
        self.calculate_queue_data = True

    def update_func_cloning_type(self, _):
        self.create_object_list = True

    calculate_path_data: bpy.props.BoolProperty(
        name="calculate_path_data",
        description="",
        default=False
        )

    calculate_queue_data: bpy.props.BoolProperty(
        name="calculate_queue_data",
        description="",
        default=False
        )

    create_object_list: bpy.props.BoolProperty(
        name="create_object_list",
        description="",
        default=False
        )

    random_seed: bpy.props.IntProperty(
        name="random_seed",
        description="Random Seed",
        default=0,
        min=0,
        update=update_func_random_seed,
        )

    cloning_type: bpy.props.EnumProperty(
        name="cloning_type",
        description="Select type of cloning",
        items=[
            ('0', "Copy", "Every object is unique"),
            ('1', "Semi Instance", "All objects use main object data, but have a custom modifiers"),
            ('2', "Full Instance", "All objects use main object data"),
        ],
        update=update_func_cloning_type,
        )

    def draw(self, _):

        layout = self.layout

        row = layout.row()
        row.prop(self, 'random_seed', text='')
        row = layout.row()
        row.prop(self, 'cloning_type', text='')

    def execute(self, _):
        try:

            array_params = CreateArrayPrams(
                calculate_path_data=self.calculate_path_data,
                calculate_queue_data=self.calculate_queue_data,
                create_object_list=self.create_object_list,
                random_seed=self.random_seed,
                cloning_type=self.cloning_type,
            )

            crete_array_manager(array_params)

            self.calculate_path_data = False
            self.calculate_queue_data = False

            return {'FINISHED'}

        except CancelError:

            return {'CANCELLED'}

        except (Exception,):

            print(traceback.format_exc())
            show_message_box('Unknown Error', 'Please, open console and send me report', 'ERROR')

            return {'CANCELLED'}
