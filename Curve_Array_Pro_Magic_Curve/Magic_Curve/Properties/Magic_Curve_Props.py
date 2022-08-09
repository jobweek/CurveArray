import bpy  # type: ignore


class Magic_Curve_Props(bpy.types.PropertyGroup):

    precision: bpy.props.FloatProperty(
        name="precision",
        description="Smooth of curve tangent calculation",
        default=0,
        min=0,
        max=100
    )
