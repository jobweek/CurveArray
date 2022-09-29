import bpy  # type: ignore
import traceback
from math import radians
from Curve_Array_Magic_Curve.Errors.Errors import CancelError, show_message_box
from .Create_Array import crete_array_manager
from ..General_Data_Classes import ArrayPrams, ArrayTransform


class CURVEARRAY_OT_create_array(bpy.types.Operator):
    """Create curve along path"""
    bl_label = "Create Array along Curve"
    bl_idname = 'curvearray.create_array'
    bl_options = {'REGISTER', 'UNDO'}

    def update_func(self, _):
        self.calculate_queue_data = True

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

    random_seed: bpy.props.IntProperty(
        name="random_seed",
        description="Random Seed",
        default=0,
        min=0,
        update=update_func,
        )

    spacing_type: bpy.props.EnumProperty(
        name="spacing_type",
        description="Type of arrangment of objects along path",
        items=[
            ('0', "Fill by Count", ""),
        ]
    )

    cloning_type: bpy.props.EnumProperty(
        name="cloning_type",
        description="Select type of cloning",
        items=[
            ('0', "Copy", "Every object is unique"),
            ('1', "Semi Instance", "All objects use main object data, but have a custom transform"),
            ('2', "Full Instance", "All objects use main object data, and copy transform"),
        ]
        )

    cyclic: bpy.props.BoolProperty(
        name="cyclic",
        description="Is the array cyclic?",
        default=False
        )

    smooth_normal: bpy.props.BoolProperty(
        name="smooth_normal",
        description="Smooth the direction of objects on the curve?",
        default=False
        )

    count: bpy.props.IntProperty(
        name="count",
        description="Count of objects on the path",
        default=1,
        min=1,
        )

    start_offset: bpy.props.FloatProperty(
        name="start_offset",
        description="Start Offset",
        default=0,
        )

    end_offset: bpy.props.FloatProperty(
        name="end_offset",
        description="End Offset",
        default=0,
        )

    slide: bpy.props.FloatProperty(
        name="slide",
        description="Slide objects along path",
        default=0,
        )

    consider_size: bpy.props.BoolProperty(
        name="consider_size",
        description="Take into account the size of the object",
        default=False
        )

    align_rotation: bpy.props.BoolProperty(
        name="align_rotation",
        description="Align objects rotation",
        default=True
        )

    rail_axis: bpy.props.EnumProperty(
        name="rail_axis",
        description="Select rail axis",
        items=[
            ('+x', "+x", ""),
            ('+y', "+y", ""),
            ('+z', "+z", ""),
            ('-x', "-x", ""),
            ('-y', "-y", ""),
            ('-z', "-z", ""),
        ]
        )

    def _normal_axis_items(self, _):

        if self.rail_axis[1] == 'x':
            return [
                ('+y', "+y", ""),
                ('+z', "+z", ""),
                ('-y', "-y", ""),
                ('-z', "-z", ""),
            ]
        elif self.rail_axis[1] == 'y':
            return [
                ('+x', "+x", ""),
                ('+z', "+z", ""),
                ('-x', "-x", ""),
                ('-z', "-z", ""),
            ]
        else:
            return [
                ('+x', "+x", ""),
                ('+y', "+y", ""),
                ('-x', "-x", ""),
                ('-y', "-y", ""),
            ]

    normal_axis: bpy.props.EnumProperty(
        name="normal_axis",
        description="Select normal axis",
        items=_normal_axis_items
    )

    rotation_x: bpy.props.FloatProperty(
        name="rotation_x",
        description="Rotation X Axis",
        default=0,
        soft_min=-360,
        soft_max=360,
        )

    rotation_y: bpy.props.FloatProperty(
        name="rotation_y",
        description="Rotation Y Axis",
        default=0,
        soft_min=-360,
        soft_max=360,
        )
    
    rotation_z: bpy.props.FloatProperty(
        name="rotation_z",
        description="Rotation Z Axis",
        default=0,
        soft_min=-360,
        soft_max=360,
        )

    location_x: bpy.props.FloatProperty(
        name="location_x",
        description="Location X Axis",
        default=0,
    )

    location_y: bpy.props.FloatProperty(
        name="location_y",
        description="Location Y Axis",
        default=0,
    )

    location_z: bpy.props.FloatProperty(
        name="location_z",
        description="Location Z Axis",
        default=0,
    )

    scale_x: bpy.props.FloatProperty(
        name="scale_x",
        description="Scale X Axis",
        default=0,
        soft_min=-1,
        soft_max=1,
    )

    scale_y: bpy.props.FloatProperty(
        name="scale_y",
        description="Scale Y Axis",
        default=0,
        soft_min=-1,
        soft_max=1,
    )

    scale_z: bpy.props.FloatProperty(
        name="scale_z",
        description="Scale Z Axis",
        default=0,
        soft_min=-1,
        soft_max=1,
    )

    def execute(self, _):
        try:

            array_transform = ArrayTransform(
                rotation_x=radians(self.rotation_x),
                rotation_y=radians(self.rotation_y),
                rotation_z=radians(self.rotation_z),
                location_x=self.location_x,
                location_y=self.location_y,
                location_z=self.location_z,
                scale_x=self.scale_x,
                scale_y=self.scale_y,
                scale_z=self.scale_z,
            )

            array_params = ArrayPrams(
                calculate_path_data=self.calculate_path_data,
                calculate_queue_data=self.calculate_queue_data,
                random_seed=self.random_seed,
                spacing_type=self.spacing_type,
                cloning_type=self.cloning_type,
                cyclic=self.cyclic,
                smooth_normal=self.smooth_normal,
                count=self.count,
                start_offset=self.start_offset,
                end_offset=self.end_offset,
                slide=self.slide,
                consider_size=self.consider_size,
                align_rotation=self.align_rotation,
                rail_axis=self.rail_axis,
                normal_axis=self.normal_axis,
                array_transform=array_transform,
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
