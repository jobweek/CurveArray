import bpy  # type: ignore
from Curve_Array_Magic_Curve.Errors.Errors import (
    show_message_box,
    CancelError,
)


def get_curve():

    if bpy.context.mode != 'OBJECT':

        show_message_box("Error", "Go to Object Mode", 'ERROR')

        raise CancelError

    objects = bpy.context.selected_objects

    if len(objects) == 0:

        show_message_box("Error", "Select object", 'ERROR')

        raise CancelError

    elif len(objects) > 1:

        show_message_box("Error", "Select only one object", 'ERROR')

        raise CancelError

    if objects[0].type != 'CURVE':

        show_message_box("Error", "Object should be curve", 'ERROR')

        raise CancelError

    return objects[0]
