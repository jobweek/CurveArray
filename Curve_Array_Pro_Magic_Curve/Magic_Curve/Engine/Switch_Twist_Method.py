import bpy  # type: ignore
import bmesh  # type: ignore
from Curve_Array_Pro_Magic_Curve.Errors.Errors import CancelError, ShowMessageBox
from .Switch_Twist_Method_Functions import (
    switch_curve_twist,
)
from ...Common_Functions.Functions import (
    duplicate,
    convert_to_mesh,
    curve_checker,
    merged_points_check, points_select,
    curve_data,
    tilt_twist_calc,
    ext_vec,
    angle_correction,
    tilt_correction,
    twist_correction,
    angle_betw_vec,
    object_select,
)


def switch_twist_method_manager():

    curve = bpy.context.active_object
    curve_checker()
    merged_points_check(curve)
    points_select(curve)

    if curve.data.twist_mode == 'TANGENT':

        ShowMessageBox("Error", "Tangent twist curves are not supported", 'ERROR')

        raise CancelError

    # Дублируем кривую
    curve_duplicate = duplicate(curve)

    # Получим информацию о кривой
    curve_duplicate_data = curve_data(curve_duplicate)

    # Полуичм разницу наклонов точек прямой
    tilt_twist_y_arr = tilt_twist_calc(curve_duplicate)

    # Конвертируем в меш
    mesh_curve_duplicate = convert_to_mesh(curve_duplicate)

    # Получаем массив y_vec
    y_vec_arr = ext_vec(mesh_curve_duplicate, curve_duplicate_data)
    bpy.data.objects.remove(mesh_curve_duplicate, do_unlink=True)

    # Меняем метод скручивания
    switched_curve = switch_curve_twist(curve)

    # Дублируем кривую
    switched_curve_duplicate = duplicate(switched_curve)

    # Конвертируем в меш
    mesh_switched_curve_duplicate = convert_to_mesh(switched_curve_duplicate)

    # Получаем массив ext_vec
    ext_vec_arr = ext_vec(mesh_switched_curve_duplicate, curve_duplicate_data)
    bpy.data.objects.remove(mesh_switched_curve_duplicate, do_unlink=True)

    # Получаем угол между векторами
    angle_y_ext_arr = angle_betw_vec(y_vec_arr, ext_vec_arr, curve_duplicate_data[0])

    # Дублируем кривую
    test_curve = duplicate(switched_curve)

    # Тестово поворачиваем точки на половину угла
    tilt_correction(angle_y_ext_arr, test_curve, True)

    # Конвертируем в меш
    mesh_test_curve = convert_to_mesh(test_curve)

    # Получаем массив test_vec
    test_vec_arr = ext_vec(mesh_test_curve, curve_duplicate_data)
    bpy.data.objects.remove(mesh_test_curve, do_unlink=True)

    # Получаем угол между векторами после поворота
    angle_y_test_arr = angle_betw_vec(y_vec_arr, test_vec_arr, curve_duplicate_data[0])

    # Корректируем углы
    angle_y_ext_arr = angle_correction(angle_y_ext_arr, angle_y_test_arr)

    # Корректируем тильт
    tilt_correction(angle_y_ext_arr, switched_curve, False)

    # Корректируем направление вращения
    tilt_twist_ext_arr = tilt_twist_calc(switched_curve)
    print(tilt_twist_y_arr)
    print(tilt_twist_ext_arr)
    # Корректируем твист
    twist_correction(tilt_twist_y_arr, tilt_twist_ext_arr, switched_curve)

    # Выделяем объект
    object_select(switched_curve)
