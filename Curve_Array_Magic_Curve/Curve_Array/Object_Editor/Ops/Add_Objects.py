import bpy  # type: ignore
from Curve_Array_Magic_Curve.Curve_Array.Object_Editor.Ops.Add_Objects_Functions import (
    get_objects,
    add_object,
)


def add_objects_manager():

    objects = get_objects()

    for obj in objects:

        add_object(obj)

