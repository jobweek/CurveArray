import bpy  # type: ignore


class CurveName(bpy.types.PropertyGroup):

    curve_name: bpy.props.StringProperty(
        name="Curve name",
        description="Name of the curve to be used to create the array"
        )
