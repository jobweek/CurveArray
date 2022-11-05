import bpy  # type: ignore


def get_pivot_distance(obj: bpy.types.Object) -> float:

    origin_co = obj.location
    pivot_co = bpy.context.scene.cursor.location
    vec = pivot_co - origin_co

    return vec.length
