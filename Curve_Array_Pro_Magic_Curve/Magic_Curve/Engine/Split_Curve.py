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
    verts_sequence,
    y_normal_vector,
    vert_co,
    create_curve,
)


def split_curve_manager():

    active_object = bpy.context.active_object
    active_mesh = active_object.data

    checker()
    curve_data = CurveData()

    bm = bmesh.from_edit_mesh(active_mesh)

    act_vert = active_vertex(bm)

    vert_sequence_array, curve_data = verts_sequence(active_mesh.total_vert_sel, act_vert, curve_data)

    y_normal_vector_array = y_normal_vector(vert_sequence_array)

    vert_co_array = vert_co(vert_sequence_array)

    bm.free()
    bpy.ops.object.editmode_toggle()

    #  Создаем кривую
    curve_data = create_curve(vert_co_array, active_object, curve_data)
