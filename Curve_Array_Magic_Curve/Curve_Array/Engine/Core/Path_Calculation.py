import bpy  # type: ignore
import bmesh  # type: ignore


from ....General_Functions.Functions import (
    duplicate,
    convert_to_mesh,
    delete_objects,
)
from .Path_Calculation_Functions import (
    verts_sequence_calc,
    get_bm_verts,
    path_data_calc,
)


def path_calculation_manager(curve):

    verts_sequence_generator = verts_sequence_calc(curve)
    duplicated_curve = duplicate(curve)
    extruded_mesh = convert_to_mesh(duplicated_curve)
    bm = get_bm_verts(extruded_mesh)
    delete_objects(extruded_mesh)

    path_data = path_data_calc(verts_sequence_generator, bm.verts, len(bm.faces), curve.name)

    print(path_data)
