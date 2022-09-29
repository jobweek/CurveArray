import bpy  # type: ignore
from .Instant_Data_Props import (
    InstantQueueData,
    InstantPathData,
    InstantData,
)
from .Curve_Editor_Props import (
    Curve,
    CurveEditorData,
)
from .Object_Editor_Props import (
    TransformData,
    Collection,
    Queue,
    Objects,
    Groups,
    WMProperty,
    ObjectEditorData,
)
from .Array_Settings_Props import (
    ArraySettings,
)


class EngineProps(bpy.types.PropertyGroup):

    instant_data: bpy.props.PointerProperty(
        type=InstantData,
        name="instant_data",
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

    array_settings: bpy.props.PointerProperty(
        type=ArraySettings,
        name="array_settings",
        description="Array Settings"
        )


class CurveArrayProps(bpy.types.PropertyGroup):

    engine_props: bpy.props.PointerProperty(
        type=EngineProps,
        name="engine_props",
        description="Engine Props (Not for User's). Dont change this data."
        )

    array_props: bpy.props.PointerProperty(
        type=ArrayProps,
        name="array_props",
        description="User Array Settings. Can be edit."
        )

# Табуляция иммитирует вложенность (снизу вверх)
registaration_order = (
            ArraySettings,
        ArrayProps,
                Curve,
            CurveEditorData,
                    Collection,
                Groups,
                Objects,
                    TransformData,
                Queue,
                WMProperty,
            ObjectEditorData,
                InstantQueueData,
                InstantPathData,
            InstantData,
        EngineProps,
    CurveArrayProps,
)
