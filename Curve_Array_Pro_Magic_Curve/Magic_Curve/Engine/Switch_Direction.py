import bpy  # type: ignore
import bmesh  # type: ignore
from Curve_Array_Pro_Magic_Curve.Errors.Errors import CancelError, ShowMessageBox
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
    curve_data, tilt_twist_calc,
    ext_vec,
    angle_correction,
    tilt_correction,
    twist_correction,
    angle_betw_vec,
    object_select,
)


def recalculate_curve_manager():

    curve = bpy.context.active_object
    curve_checker()
    merged_points_check(curve)
    points_select(curve)

    if curve.data.twist_mode == 'Z_UP':

        switched_curve = switch_curve_direction(curve)
        object_select(switched_curve)

        return

    elif curve.data.twist_mode == 'TANGENT':

        ShowMessageBox("Error", "Tangent twist curves are not supported", 'ERROR')

        raise CancelError

    else:

        curve.data.twist_smooth = 100

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
    y_vec_arr = ext_vec(mesh_curve_duplicate, curve_duplicate_data)
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
    ext_vec_arr = ext_vec(mesh_switched_curve_duplicate, switched_curve_duplicate_data)
    bpy.data.objects.remove(mesh_switched_curve_duplicate, do_unlink=True)

    # Получаем угол между векторами
    angle_y_ext_arr = angle_betw_vec(y_vec_arr, ext_vec_arr, switched_curve_duplicate_data[0])

    # Дублируем кривую
    test_curve = duplicate(switched_curve)

    # Тестово поворачиваем точки на половину угла
    tilt_correction(angle_y_ext_arr, test_curve, True)

    # Конвертируем в меш
    mesh_test_curve = convert_to_mesh(test_curve)

    # Получаем массив test_vec
    test_vec_arr = ext_vec(mesh_test_curve, switched_curve_duplicate_data)
    bpy.data.objects.remove(mesh_test_curve, do_unlink=True)

    # Получаем угол между векторами после поворота
    angle_y_test_arr = angle_betw_vec(y_vec_arr, test_vec_arr, switched_curve_duplicate_data[0])

    # Корректируем углы
    angle_y_ext_arr = angle_correction(angle_y_ext_arr, angle_y_test_arr)

    # Корректируем тильт
    tilt_correction(angle_y_ext_arr, switched_curve, False)

    tilt_twist_ext_arr = tilt_twist_calc(switched_curve)

    # Корректируем твист
    twist_correction(tilt_twist_y_arr, tilt_twist_ext_arr, switched_curve)

    # Выделяем объект
    object_select(switched_curve)
