import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import copy
import numpy as np
from .Errors import CancelError, ShowMessageBox
from .Classes import checker
from .General_Functions import (
    active_vertex,
)


def split_curve_manager():

    active_object = bpy.context.active_object
    active_mesh = active_object.data

    checker.start_checker()
    curve_data = CurveData()

    bm = bmesh.from_edit_mesh(active_mesh)

    act_vert = active_vertex(bm)

    vert_sequence_array = verts_sequence(active_mesh.total_vert_sel, act_vert, curve_data)