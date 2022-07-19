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
    create_extruded_mesh,
    extruded_mesh_vector,
)


def split_curve_manager():

    active_object = bpy.context.active_object
    active_mesh = active_object.data

    checker()
    curve_data = CurveData()

    bm = bmesh.from_edit_mesh(active_mesh)

    act_vert = active_vertex(bm)

    vert_sequence_array, curve_data = verts_sequence(active_mesh.total_vert_sel, act_vert, curve_data)

    y_vec_arr = y_normal_vector(vert_sequence_array)

    vert_co_arr = vert_co(vert_sequence_array)

    bm.free()
    bpy.ops.object.editmode_toggle()

    curve_data = create_curve(vert_co_arr, active_object, curve_data)

    extruded_mesh = create_extruded_mesh(curve_data.get_curve())

    ext_vec_arr = extruded_mesh_vector(extruded_mesh, len(vert_sequence_array)-1)

    bpy.data.objects.remove(extruded_mesh, do_unlink=True)