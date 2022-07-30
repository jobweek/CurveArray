import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore
from .Switch_Direction_Functions import (
    checker,
    merged_points_check,
    points_select,
    duplicate,
    Curve_Data,
    convert_to_mesh,
    switch_curve,
    ext_vec,
    z_vec,
    tilt_correction,
)


def recalculate_curve_manager():

    curve = bpy.context.active_object
    checker()
    merged_points_check(curve)
    points_select(curve)

    # Дублируем кривую
    curve_duplicate = duplicate(curve)

    # Получим информацию о кривой
    curve_duplicate_data = Curve_Data(curve_duplicate)

    # Конвертируем в меш
    mesh_curve_duplicate = convert_to_mesh(curve_duplicate)

    # Получаем массив y_vec
    y_vec_arr = ext_vec(mesh_curve_duplicate, curve_duplicate_data.get_curve_data())
    bpy.data.objects.remove(mesh_curve_duplicate, do_unlink=True)

    # Меняем направление
    switched_curve = switch_curve(curve)

    # Дублируем кривую
    switched_curve_duplicate = duplicate(switched_curve)

    # Получим информацию о кривой
    switched_curve_duplicate_data = Curve_Data(switched_curve_duplicate)

    # Конвертируем в меш
    mesh_switched_curve_duplicate = convert_to_mesh(switched_curve_duplicate)

    # Получаем массив ext_vec
    ext_vec_arr = ext_vec(mesh_switched_curve_duplicate, switched_curve_duplicate_data.get_curve_data())

    # Получаем массив z_vec
    z_vec_arr = z_vec(mesh_switched_curve_duplicate, switched_curve_duplicate_data.get_curve_data())
    # bpy.data.objects.remove(mesh_switched_curve_duplicate, do_unlink=True)

    # Корректируем тильт
    tilt_correction(ext_vec_arr, y_vec_arr, z_vec_arr, switched_curve)

    bpy.ops.object.select_all(action='DESELECT')
    switched_curve.select_set(True)
    bpy.context.view_layer.objects.active = switched_curve
