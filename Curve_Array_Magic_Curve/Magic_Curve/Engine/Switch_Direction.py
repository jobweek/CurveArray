import bpy  # type: ignore
import bmesh  # type: ignore
from Curve_Array_Magic_Curve.Errors.Errors import CancelError, show_message_box
from .Switch_Direction_Functions import (
    switch_curve_direction,
    arr_flip_direction,
)
from ...Common_Functions.Functions import (
    duplicate,
    convert_to_mesh,
    curve_checker,
    merged_points_check,
    points_select,
    curve_data,
    tilt_twist_calc,
    point_direction_vec,
    tilt_correction,
    twist_correction,
    object_select,
    z_vec,
)


def switch_curve_direction_manager():

    curve = bpy.context.active_object
    curve_checker()
    merged_points_check(curve)
    points_select(curve)

    if curve.data.twist_mode == 'Z_UP' and curve.data.twist_smooth == 0:

        switched_curve = switch_curve_direction(curve)
        object_select(switched_curve)

        return

    elif curve.data.twist_mode == 'TANGENT':

        show_message_box("Error", "Tangent twist curves are not supported", 'ERROR')

        raise CancelError

    # Дублируем кривую
    curve_duplicate = duplicate(curve)

    # Получим информацию о кривой
    curve_duplicate_data = curve_data(curve_duplicate)

    # Полуичм разницу наклонов точек прямой
    tilt_twist_y_arr = tilt_twist_calc(curve_duplicate)

    # Переворачивем массив tilt_twist_arr
    tilt_twist_y_arr = arr_flip_direction(tilt_twist_y_arr)

    # Конвертируем в меш
    mesh_curve_duplicate = convert_to_mesh(curve_duplicate)

    # Получаем массив y_vec
    y_vec_arr = point_direction_vec(mesh_curve_duplicate, curve_duplicate_data)
    bpy.data.objects.remove(mesh_curve_duplicate, do_unlink=True)

    # Переворачивем массив y_vec
    y_vec_arr = arr_flip_direction(y_vec_arr)

    # Меняем направление
    switched_curve = switch_curve_direction(curve)

    # Дублируем кривую
    switched_curve_duplicate = duplicate(switched_curve)

    # Получим информацию о кривой
    switched_curve_duplicate_data = curve_data(switched_curve_duplicate)

    # Конвертируем в меш
    mesh_switched_curve_duplicate = convert_to_mesh(switched_curve_duplicate)

    # Получаем массив ext_vec
    ext_vec_arr = point_direction_vec(mesh_switched_curve_duplicate, switched_curve_duplicate_data)

    # Получаем массив z_vec
    z_vec_arr = z_vec(mesh_switched_curve_duplicate, switched_curve_duplicate_data)
    bpy.data.objects.remove(mesh_switched_curve_duplicate, do_unlink=True)

    # Корректируем тильт
    tilt_correction(y_vec_arr, ext_vec_arr, z_vec_arr, switched_curve)

    # Получаем твист точек
    tilt_twist_ext_arr = tilt_twist_calc(switched_curve)

    # Корректируем твист
    twist_correction(tilt_twist_y_arr, tilt_twist_ext_arr, switched_curve)

    # Выделяем объект
    object_select(switched_curve)
