import bpy  # type: ignore


class Curve(bpy.types.PropertyGroup):

    name: bpy.props.StringProperty(
        name="name",
        description="Name of the curve to be used to create the array",
        default=""
        )

    icon: bpy.props.StringProperty(
        name="icon",
        description="Name of the curve to be used to create the array",
        default='UNLOCKED'
        )


class CurveEditorData(bpy.types.PropertyGroup):

    curve: bpy.props.PointerProperty(
        type=Curve,
        name="curve",
        description=""
    )
