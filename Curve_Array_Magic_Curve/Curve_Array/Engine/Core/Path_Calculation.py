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
    get_bm_verts,
    func,
)


def path_calculation_manager(curve):

    verts_sequence_generator = verts_sequence_calc(curve)
    duplicated_curve = duplicate(curve)
    extruded_mesh = convert_to_mesh(duplicated_curve)
    verts = get_bm_verts(extruded_mesh)
    delete_objects(extruded_mesh)

    func(verts_sequence_generator, verts)


