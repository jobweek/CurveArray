import bpy  # type: ignore
from .Path_Calculation_Props import InstantPathData
from .Curve_Editor_Props import (
    Curve,
    CurveEditorData,
)
from .Object_Editor_Props import (
    Collection,
    Queue,
    Objects,
    Groups,
    WMProperty,
    ObjectEditorData,
)


class EngineProps(bpy.types.PropertyGroup):

    instant_path_data: bpy.props.PointerProperty(
        type=InstantPathData,
        name="instant_path_data",
        description=""
        )

    object_editor_data: bpy.props.PointerProperty(
        type=ObjectEditorData,
        name="object_editor_data",
        description=""
        )

    curve_editor_data: bpy.props.PointerProperty(
        type=CurveEditorData,
        name="curve_editor_data",
        description=""
        )


class ArrayProps(bpy.types.PropertyGroup):

    pass


class CurveArrayProps(bpy.types.PropertyGroup):

    engine_props: bpy.props.PointerProperty(
        type=EngineProps,
        name="Engine Props (Not for User's)",
        description="Dont change this data."
        )

    array_props: bpy.props.PointerProperty(
        type=ArrayProps,
        name="User Array Settings",
        description="Can be edit."
        )

# Табуляция иммитирует вложенность (снизу вверх)
registaration_order = (
        ArrayProps,
                Curve,
            CurveEditorData,
                    Collection,
                Groups,
                Objects,
                Queue,
                WMProperty,
            ObjectEditorData,
            InstantPathData,
        EngineProps,
    CurveArrayProps,
)
