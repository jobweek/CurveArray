import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
from .Classes import (
    CurveData,
)
from .Smooth_Curve_Functions import (
    create_curve,
    extruded_mesh_vector,
)
from .Split_Curve_Functions import (
    checker,
    active_vertex,
    verts_sequence,
    merged_vertices_check,
    y_normal_vector,
    vert_co,
    create_extruded_mesh,
)
from .Switch_Direction_Functions import (
    #  z_vec,
    tilt_correction,
)


def smooth_curve_manager():

    active_object = bpy.context.active_object
    active_mesh = active_object.data

    checker()
    curve_data = CurveData()

    bm = bmesh.from_edit_mesh(active_mesh)

    act_vert = active_vertex(bm)

    vert_sequence_array, curve_data = verts_sequence(active_mesh.total_vert_sel, act_vert, curve_data, False)
    merged_vertices_check(vert_sequence_array, False, curve_data.get_cyclic())

    y_vec_arr = y_normal_vector(vert_sequence_array)

    vert_co_arr = vert_co(vert_sequence_array)

    bm.free()
    bpy.ops.object.editmode_toggle()

    curve_data = create_curve(vert_co_arr, active_object, curve_data)
    #  z_vec_arr = z_vec(curve_data.get_curve(), len(vert_sequence_array))

    extruded_mesh = create_extruded_mesh(curve_data.get_curve())

    ext_vec_arr = extruded_mesh_vector(extruded_mesh, len(vert_sequence_array), curve_data)

    bpy.data.objects.remove(extruded_mesh, do_unlink=True)

    #  tilt_correction(ext_vec_arr, y_vec_arr, z_vec_arr, curve_data.get_curve())

    bpy.ops.object.select_all(action='DESELECT')
    curve_data.get_curve().select_set(True)
    bpy.context.view_layer.objects.active = curve_data.get_curve()
