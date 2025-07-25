import bpy  # type: ignore
from Curve_Array_Magic_Curve.Errors.Errors import (
    show_message_box,
    CancelError,
)
from ...Property.Get_Property_Path import (
    get_queue_props,
    get_objects_props,
)
from .Catch_Pivot_Functions import get_pivot_distance


def get_objects():

    if bpy.context.mode != 'OBJECT':

        show_message_box("Error", "Go to Object Mode", 'ERROR')

        raise CancelError

    objects = bpy.context.selected_objects

    if len(objects) == 0:

        show_message_box("Error", "Select object", 'ERROR')

        raise CancelError

    return objects


def add_object(obj: bpy.types.Object):

    objects = get_objects_props()
    queue = get_queue_props()

    index = len(objects)
    item = objects.add()
    item.name = obj.name
    item.pivot = get_pivot_distance(obj)

    item = queue.add()
    item.index = index
