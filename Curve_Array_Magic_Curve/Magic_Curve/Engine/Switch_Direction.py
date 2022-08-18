import bpy  # type: ignore
import bmesh  # type: ignore
from ...Errors.Errors import CancelError, show_message_box
from .Switch_Direction_Functions import (
    switch_curve_direction,
    arr_flip_direction,
)
from ...General_Functions.Functions import (
    duplicate,
    convert_to_mesh,
    curve_methods_start_checker,
    merged_points_check,
    points_select,
    curve_data,
    angle_arr_get,
    point_direction_vec,
    angle_arr_calc,
    tilt_correction,
    main_object_select,
    z_vec,
)


def switch_curve_direction_manager():

    # Проверям стартовые условия вызова оператора
    curve_methods_start_checker()

    curve = bpy.context.active_object
    if curve.data.twist_mode == 'TANGENT':

        show_message_box("Error", "Tangent twist curves are not supported", 'ERROR')

        raise CancelError

    # Проверяем кривую на существование слитых точек
    merged_points_check(curve)

    # Выделяем все точки на кривой
    points_select(curve)

    if curve.data.twist_mode == 'Z_UP' and curve.data.twist_smooth == 0:

        switched_curve = switch_curve_direction(curve)
        main_object_select(switched_curve)

        return

    # Дублируем кривую
    curve_duplicate = duplicate(curve)

    # Получим информацию о кривой
    curve_duplicate_data = curve_data(curve_duplicate)

    # Полуичм углы наклона точек кривой
    angle_arr_curve = angle_arr_get(curve_duplicate)

    # Переворачивем массив angle_arr_curve
    angle_arr_curve = arr_flip_direction(angle_arr_curve)

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

    # Получаем массив углов поврота
    angle_arr_switched_curve = angle_arr_calc(y_vec_arr, ext_vec_arr, z_vec_arr, switched_curve)
    print(f'angle_arr_curve: {angle_arr_curve}\nangle_arr_switched_curve: {angle_arr_switched_curve}')
    # Корректируем тильт
    tilt_correction(angle_arr_curve, angle_arr_switched_curve, switched_curve)

    # Выделяем объект
    main_object_select(switched_curve)
