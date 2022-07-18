import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import copy
import numpy as np
from .Errors import CancelError, ShowMessageBox
from .Classes import (
    checker,
    CurveData,
)
from .Split_Curve_Functions import (
    active_vertex,
    verts_sequence
)


def split_curve_manager():

    active_object = bpy.context.active_object
    active_mesh = active_object.data

    checker()
    curve_data = CurveData()

    bm = bmesh.from_edit_mesh(active_mesh)

    act_vert = active_vertex(bm)

    vert_sequence_array, curve_data = verts_sequence(active_mesh.total_vert_sel, act_vert, curve_data)

    print(vert_sequence_array)
