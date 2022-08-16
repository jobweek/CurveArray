import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
import numpy as np
from .Smooth_Curve_Functions import (
    create_curve_smooth,
    ext_vec_smooth,
    z_vec_smooth,
    tilt_correction_smooth,
)
from ...Common_Functions.Functions import (
    curve_creation_start_check,
    active_vertex,
    verts_sequence,
    vertex_normal_vec,
    vert_co,
    duplicate,
    convert_to_mesh,
    main_object_select,
)


def smooth_curve_manager():

    # Проверям стартовые условия вызова оператора
    curve_creation_start_check()

    active_object = bpy.context.active_object
    active_mesh = active_object.data

    bm = bmesh.from_edit_mesh(active_mesh)

    # Получаем активную вершину
    act_vert = active_vertex(bm)

    # Получаем последовательность выбранных пользователем вершин
    vert_sequence_array, curve_data = verts_sequence(active_mesh.total_vert_sel, act_vert, False)

    # Получаем массив векторов y_vec
    y_vec_arr = vertex_normal_vec(vert_sequence_array)

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

    # Если кривая замкнута, сдвигаем массив на -1
    if curve_data.get_cyclic():

        ext_vec_arr = np.roll(ext_vec_arr, -1)

    # Получаем массив z_vec
    z_vec_arr = z_vec_smooth(curve_data.get_curve(), len(vert_sequence_array))

    # Корректируем тильт
    tilt_correction_smooth(ext_vec_arr, y_vec_arr, z_vec_arr, curve_data.get_curve())

    # Выделяем объект
    main_object_select(curve_data.get_curve())
