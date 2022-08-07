import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
from .Smooth_Curve_Functions import (
    create_curve_smooth,
    ext_vec_smooth,
    z_vec_smooth,
    tilt_correction_smooth,
)
from ...Common_Functions.Functions import (
    CurveData,
    object_checker,
    active_vertex,
    verts_sequence,
    merged_vertices_check,
    y_vec,
    vert_co,
    duplicate,
    convert_to_mesh,
    object_select,
)


def smooth_curve_manager():

    active_object = bpy.context.active_object
    active_mesh = active_object.data

    object_checker()
    curve_data = CurveData()

    bm = bmesh.from_edit_mesh(active_mesh)

    # Получаем активную вершину
    act_vert = active_vertex(bm)

    # Получаем последовательность выбранных пользователем вершин
    vert_sequence_array, curve_data = verts_sequence(active_mesh.total_vert_sel, act_vert, curve_data, False)

    # Проверяем последовательность на существование вершин с одинакеовыми координатами
    merged_vertices_check(vert_sequence_array, False, curve_data.get_cyclic())

    # Получаем массив векторов y_vec
    y_vec_arr = y_vec(vert_sequence_array)

    # Получаем массив координат каждой вершины последовательности
    vert_co_arr = vert_co(vert_sequence_array)

    bm.free()
    bpy.ops.object.editmode_toggle()

    # Создаем кривую из последовательности вершин
    curve_data = create_curve_smooth(vert_co_arr, active_object, curve_data)

    # Дублируем кривую
    curve_duplicate = duplicate(curve_data.get_curve())

    # Конвертируем в меш
    mesh_curve_duplicate = convert_to_mesh(curve_duplicate)

    # Полуаем массив ext_vec
    ext_vec_arr = ext_vec_smooth(mesh_curve_duplicate, len(vert_sequence_array))
    bpy.data.objects.remove(mesh_curve_duplicate, do_unlink=True)

    # Получаем массив z_vec
    z_vec_arr = z_vec_smooth(curve_data.get_curve(), len(vert_sequence_array))

    # Корректируем тильт
    tilt_correction_smooth(ext_vec_arr, y_vec_arr, z_vec_arr, curve_data.get_curve())

    # Выделяем объект
    object_select(curve_data.get_curve())
