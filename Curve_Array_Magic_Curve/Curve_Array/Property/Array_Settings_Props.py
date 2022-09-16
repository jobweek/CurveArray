import bpy  # type: ignore


class ArraySettings(bpy.types.PropertyGroup):

    spacing_type: bpy.props.EnumProperty(
        name="spacing_type",
        description="Type of arrangment of objects along path",
        items=[
            ('0', "Fill by Count", ""),
        ]
    )

    count: bpy.props.IntProperty(
        name="count",
        description="Count of objects on the path",
        default=1,
        min=1,
        )
