import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils
import numpy as np
from Curve_Array_Magic_Curve.Errors.Errors import (
    show_message_box,
    CancelError,
)
from ....General_Functions.Functions import (
    duplicate,
    convert_to_mesh,
    delete_objects,
)
from .Path_Calculation_Functions import (
    verts_sequence_calc,
)


def path_calculation_manager(curve):

    verts_sequence_generator = verts_sequence_calc(curve)
    duplicated_curve = duplicate(curve)
    extruded_mesh = convert_to_mesh(duplicated_curve)
    bm = bmesh.new()
    bm.from_mesh(extruded_mesh.data, face_normals=False, vertex_normals=False)
    bmesh.ops.transform(bm, matrix=curve.matrix_world, verts=bm.verts)
    delete_objects(extruded_mesh)


