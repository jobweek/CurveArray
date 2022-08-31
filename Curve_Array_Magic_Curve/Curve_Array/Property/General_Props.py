import bpy  # type: ignore
from .Path_Calculation_Props import InstantPathData
from.Set_Curve_Props import CurveName


class EnginePropsPointer(bpy.types.PropertyGroup):

    instant_path_data: bpy.props.PointerProperty(
        type=InstantPathData,
        name="Instant Path Data",
        description=""
        )


class ArrayPropsPoiner(bpy.types.PropertyGroup):

    curve_name: bpy.props.PointerProperty(
        type=CurveName,
        name="Curve Name",
        description=""
        )


class CurveArrayProps(bpy.types.PropertyGroup):

    engine_props: bpy.props.PointerProperty(
        type=EnginePropsPointer,
        name="Engine Props (Not for User's)",
        description="Dont change this data."
        )

    user_props: bpy.props.PointerProperty(
        type=EnginePropsPointer,
        name="User Array Settings",
        description="Can be edit."
        )

# Табуляция иммитирует вложенность
registaration_order = (
            InstantPathData,
        EnginePropsPointer,
    CurveArrayProps,
)
