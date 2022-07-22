import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import copy
import math
import numpy as np
from .Errors import CancelError, ShowMessageBox


def checker():

    objects = bpy.context.selected_objects

    if len(objects) == 0:

        ShowMessageBox("Error", "Select object", 'ERROR')

        raise CancelError

    elif len(objects) > 1:

        ShowMessageBox("Error", "Select only one object", 'ERROR')

        raise CancelError

    if objects[0].type != 'CURVE':

        ShowMessageBox("Error", "Object should be curve", 'ERROR')

        raise CancelError

    mode = bpy.context.active_object.mode

    if mode != 'OBJECT':
        ShowMessageBox("Error", "Go to Object Mode", 'ERROR')

        raise CancelError


def ext_vec(active_curve):

    pass
