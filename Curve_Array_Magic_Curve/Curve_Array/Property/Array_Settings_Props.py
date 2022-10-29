import bpy  # type: ignore


class ArraySettings(bpy.types.PropertyGroup):

    def update_array(self, _):
        if self.auto_update:
            bpy.ops.curvearray.update_array()

    auto_update: bpy.props.BoolProperty(
        name="auto_update",
        description="Automatically update an array after changing properties",
        default=False,
        update=update_array,
        )

    random_seed: bpy.props.IntProperty(
        name="random_seed",
        description="Random Seed",
        default=0,
        min=0,
        update=update_array,
        )

    cloning_type: bpy.props.EnumProperty(
        name="cloning_type",
        description="Select type of cloning",
        items=[
            ('0', "Copy", "Every object is unique"),
            ('1', "Semi Instance", "All objects use main object data, but have a custom modifiers"),
            ('2', "Full Instance", "All objects use main object data"),
        ],
        update=update_array,
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
            ('3', "Fill by Pivot", ""),
        ],
        update=update_array,
    )

    cyclic: bpy.props.BoolProperty(
        name="cyclic",
        description="Is the array cyclic?",
        default=False,
        update=update_array,
        )

    smooth_normal: bpy.props.BoolProperty(
        name="smooth_normal",
        description="Smooth the direction of objects on the curve?",
        default=False,
        update=update_array,
        )

    step_offset: bpy.props.FloatProperty(
        name="step_offset",
        description="Distance between objects in the array",
        default=1,
        min=0,
        update=update_array,
        )

    size_offset: bpy.props.FloatProperty(
        name="size_offset",
        description="Size Offset",
        default=1,
        min=0,
        update=update_array,
        )

    start_offset: bpy.props.FloatProperty(
        name="start_offset",
        description="Start Offset",
        default=0,
        update=update_array,
        )

    end_offset: bpy.props.FloatProperty(
        name="end_offset",
        description="End Offset",
        default=0,
        update=update_array,
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
        default=False,
        update=update_array,
        )

    align_rotation: bpy.props.BoolProperty(
        name="align_rotation",
        description="Align objects rotation",
        default=True,
        update=update_array,
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
        ],
        update=update_array,
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
        items=_normal_axis_items,
        update=update_array,
    )

    rotation_x: bpy.props.FloatProperty(
        name="rotation_x",
        description="Rotation X Axis",
        default=0,
        soft_min=-360,
        soft_max=360,
        update=update_array,
    )

    rotation_y: bpy.props.FloatProperty(
        name="rotation_y",
        description="Rotation Y Axis",
        default=0,
        soft_min=-360,
        soft_max=360,
        update=update_array,
    )

    rotation_z: bpy.props.FloatProperty(
        name="rotation_z",
        description="Rotation Z Axis",
        default=0,
        soft_min=-360,
        soft_max=360,
        update=update_array,
    )

    location_x: bpy.props.FloatProperty(
        name="location_x",
        description="Location X Axis",
        default=0,
        update=update_array,
    )

    location_y: bpy.props.FloatProperty(
        name="location_y",
        description="Location Y Axis",
        default=0,
        update=update_array,
    )

    location_z: bpy.props.FloatProperty(
        name="location_z",
        description="Location Z Axis",
        default=0,
        update=update_array,
    )

    scale_x: bpy.props.FloatProperty(
        name="scale_x",
        description="Scale X Axis",
        default=0,
        soft_min=-0.9,
        soft_max=1,
        update=update_array,
    )

    scale_y: bpy.props.FloatProperty(
        name="scale_y",
        description="Scale Y Axis",
        default=0,
        soft_min=-0.9,
        soft_max=1,
        update=update_array,
    )

    scale_z: bpy.props.FloatProperty(
        name="scale_z",
        description="Scale Z Axis",
        default=0,
        soft_min=-0.9,
        soft_max=1,
        update=update_array,
    )
