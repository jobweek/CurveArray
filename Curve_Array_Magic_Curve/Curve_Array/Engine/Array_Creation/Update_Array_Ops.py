import bpy  # type: ignore
import traceback
from math import radians
from Curve_Array_Magic_Curve.Errors.Errors import CancelError, show_message_box
from .Update_Array import update_array_manager
from ..General_Data_Classes import ArrayTransform, UpdateArrayPrams
from ...Property.Get_Property_Path import get_array_settings_props


class CURVEARRAY_OT_update_array(bpy.types.Operator):
    bl_label = "Update Array"
    bl_idname = 'curvearray.update_array'
    bl_options = {'REGISTER', 'UNDO'}

    update_path_data: bpy.props.BoolProperty(
        name="update_path_data",
        description="",
        default=False
        )

    update_queue_data: bpy.props.BoolProperty(
        name="update_queue_data",
        description="",
        default=False
        )

    update_object_data: bpy.props.BoolProperty(
        name="update_object_data",
        description="",
        default=False
        )

    def execute(self, _):
        try:

            sett = get_array_settings_props()

            array_transform = ArrayTransform(
                rotation_x=radians(sett.rotation_x),
                rotation_y=radians(sett.rotation_y),
                rotation_z=radians(sett.rotation_z),
                location_x=sett.location_x,
                location_y=sett.location_y,
                location_z=sett.location_z,
                scale_x=sett.scale_x,
                scale_y=sett.scale_y,
                scale_z=sett.scale_z,
            )

            array_params = UpdateArrayPrams(
                update_path_data=self.update_path_data,
                update_queue_data=self.update_queue_data,
                update_object_data=self.update_object_data,
                random_seed=sett.random_seed,
                cloning_type=sett.cloning_type,
                spacing_type=sett.spacing_type,
                cyclic=sett.cyclic,
                smooth_normal=sett.smooth_normal,
                count=sett.count,
                step_offset=sett.step_offset,
                size_offset=sett.size_offset,
                start_offset=sett.start_offset,
                end_offset=sett.end_offset,
                slide=sett.slide,
                consider_size=sett.consider_size,
                align_rotation=sett.align_rotation,
                rail_axis=sett.rail_axis,
                normal_axis=sett.normal_axis,
                array_transform=array_transform,
            )

            update_array_manager(array_params)

            return {'FINISHED'}

        except CancelError:

            return {'CANCELLED'}

        except (Exception,):

            print(traceback.format_exc())
            show_message_box('Unknown Error', 'Please, open console and send me report', 'ERROR')

            return {'CANCELLED'}
