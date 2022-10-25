import bpy  # type: ignore
from math import radians
from ..Engine.Array_Creation.Update_Array import update_array_manager
from ..Engine.Array_Creation.Create_Array import crete_array_manager
from ..Engine.General_Data_Classes import CreateArrayPrams, UpdateArrayPrams, ArrayTransform


class ArraySettings(bpy.types.PropertyGroup):

    def create_array(self, _):

        array_params = CreateArrayPrams(
                calculate_path_data=False,
                calculate_queue_data=True,
                create_object_list=True,
            )

        crete_array_manager(array_params)

    def create_array_object_update(self, _):

        array_params = CreateArrayPrams(
                calculate_path_data=False,
                calculate_queue_data=False,
                create_object_list=True,
            )

        crete_array_manager(array_params)

    def update_array(self, _):

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

        array_params = UpdateArrayPrams(
            spacing_type=self.spacing_type,
            cyclic=self.cyclic,
            smooth_normal=self.smooth_normal,
            count=self.count,
            step_offset=self.step_offset,
            size_offset=self.size_offset,
            start_offset=self.start_offset,
            end_offset=self.end_offset,
            slide=self.slide,
            consider_size=self.consider_size,
            align_rotation=self.align_rotation,
            rail_axis=self.rail_axis,
            normal_axis=self.normal_axis,
            array_transform=array_transform,
        )

        update_array_manager(array_params)

    random_seed: bpy.props.IntProperty(
        name="random_seed",
        description="Random Seed",
        default=0,
        min=0,
        update=create_array,
        )

    cloning_type: bpy.props.EnumProperty(
        name="cloning_type",
        description="Select type of cloning",
        items=[
            ('0', "Copy", "Every object is unique"),
            ('1', "Semi Instance", "All objects use main object data, but have a custom modifiers"),
            ('2', "Full Instance", "All objects use main object data"),
        ],
        update=create_array_object_update,
        )

    count: bpy.props.IntProperty(
        name="count",
        description="Count of objects on the path",
        default=10,
        min=1,
        soft_max=100,
        update=update_array,
        )

    spacing_type: bpy.props.EnumProperty(
        name="spacing_type",
        description="Type of arrangment of objects along path",
        items=[
            ('0', "Fill by Count", ""),
            ('1', "Fill by Offset", ""),
            ('2', "Fill by Size", ""),
            ('3', "Fill by Origin", ""),
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

    step_offset: bpy.props.FloatProperty(
        name="step_offset",
        description="Distance between objects in the array",
        default=1,
        min=0,
        )

    size_offset: bpy.props.FloatProperty(
        name="size_offset",
        description="Size Offset",
        default=1,
        min=0,
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
        update=update_array,
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
                ('+z', "+z", ""),
                ('+y', "+y", ""),
                ('-z', "-z", ""),
                ('-y', "-y", ""),
            ]
        elif self.rail_axis[1] == 'y':
            return [
                ('+z', "+z", ""),
                ('+x', "+x", ""),
                ('-z', "-z", ""),
                ('-x', "-x", ""),
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
        soft_min=-0.9,
        soft_max=1,
    )

    scale_y: bpy.props.FloatProperty(
        name="scale_y",
        description="Scale Y Axis",
        default=0,
        soft_min=-0.9,
        soft_max=1,
    )

    scale_z: bpy.props.FloatProperty(
        name="scale_z",
        description="Scale Z Axis",
        default=0,
        soft_min=-0.9,
        soft_max=1,
    )
