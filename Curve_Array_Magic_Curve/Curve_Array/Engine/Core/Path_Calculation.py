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
    spline_range_calc,
)


def path_calculation_manager(curve):

    spline_range_arr = spline_range_calc(curve)
    print(spline_range_arr)
    duplicated_curve = duplicate(curve)

    extruded_mesh = convert_to_mesh(duplicated_curve)
    bm = bmesh.new()
    bm.from_mesh(extruded_mesh.data, face_normals=False, vertex_normals=False)
    bmesh.ops.transform(bm, matrix=curve.matrix_world, verts=bm.verts)
    delete_objects(duplicated_curve, extruded_mesh)

    for i in bm.verts:

        print(i.index, i.co)

