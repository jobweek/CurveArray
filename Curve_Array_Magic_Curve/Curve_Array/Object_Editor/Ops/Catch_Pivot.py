import bpy  # type: ignore
from .Catch_Pivot_Functions import get_pivot_distance
from Curve_Array_Magic_Curve.Errors.Errors import CancelError, show_message_box


def catch_pivot_manager():

    obj = bpy.context.active_object

    if obj is None:
        show_message_box('Error', 'No Active Object!', 'ERROR')
        raise CancelError

    distance = str(get_pivot_distance(obj))

    bpy.context.window_manager.clipboard = distance

    show_message_box('Success', f"Distance = '{distance}' copied to the clipboard.", 'DRIVER_DISTANCE')
