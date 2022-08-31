import bpy  # type: ignore
from .Core_Props import InstantPathData


class EnginePropsPointer(bpy.types.PropertyGroup):
    path_data: bpy.props.PointerProperty(
        type=InstantPathData,
        name="Instant Path Data",
        description=""
        )


class CurveArrayProps(bpy.types.PropertyGroup):

    engine_props: bpy.props.PointerProperty(
        type=EnginePropsPointer,
        name="Engine Props (Not for User's)",
        description="Dont change this data."
        )

# Табуляция иммитирует вложенность
registaration_order = (
            InstantPathData,
        EnginePropsPointer,
    CurveArrayProps,
)
