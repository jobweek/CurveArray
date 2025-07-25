import bpy  # type: ignore


class Curve(bpy.types.PropertyGroup):

    name: bpy.props.StringProperty(
        name="Curve name",
        description="Name of the curve to be used to create the array",
        default=""
        )

    icon: bpy.props.StringProperty(
        name="Curve icon",
        description="Name of the curve to be used to create the array",
        default='UNLOCKED'
        )
