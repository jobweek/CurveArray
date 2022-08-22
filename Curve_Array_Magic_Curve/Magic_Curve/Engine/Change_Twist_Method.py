import bpy  # type: ignore
import bmesh  # type: ignore
from ...Errors.Errors import CancelError, show_message_box
from .Change_Twist_Method_Functions import (
    switch_curve_twist,
)
from ...General_Functions.Functions import (
    duplicate,
    convert_to_mesh,
    curve_methods_start_checker,
    merged_points_check, points_select,
    curve_data,
    point_direction_vec,
    angle_arr_calc,
    tilt_correction,
    z_vec,
    main_object_select,
)


def switch_twist_method_manager():

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

    # Дублируем кривую
    curve_duplicate = duplicate(curve)

    # Получим информацию о кривой
    curve_duplicate_data = curve_data(curve_duplicate)

    # Конвертируем в меш
    mesh_curve_duplicate = convert_to_mesh(curve_duplicate)

    # Получаем массив y_vec
    y_vec_arr = point_direction_vec(mesh_curve_duplicate, curve_duplicate_data)
    bpy.data.objects.remove(mesh_curve_duplicate, do_unlink=True)

    # Меняем метод скручивания
    changed_curve = switch_curve_twist(curve)

    # Дублируем кривую
    switched_curve_duplicate = duplicate(changed_curve)

    # Конвертируем в меш
    mesh_switched_curve_duplicate = convert_to_mesh(switched_curve_duplicate)

    # Получаем массив ext_vec
    ext_vec_arr = point_direction_vec(mesh_switched_curve_duplicate, curve_duplicate_data)

    # Получаем массив z_vec
    z_vec_arr = z_vec(mesh_switched_curve_duplicate, curve_duplicate_data)
    bpy.data.objects.remove(mesh_switched_curve_duplicate, do_unlink=True)

    # Получаем массив углов поврота
    angle_arr_changed_curve = angle_arr_calc(y_vec_arr, ext_vec_arr, z_vec_arr, changed_curve)

    # Корректируем тильт
    tilt_correction(angle_arr_changed_curve, changed_curve)

    # Выделяем объект
    main_object_select(changed_curve)
