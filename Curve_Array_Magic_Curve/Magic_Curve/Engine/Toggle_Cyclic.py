import bpy  # type: ignore
import bmesh  # type: ignore
from ...Errors.Errors import CancelError, show_message_box
from .Toggle_Cyclic_Functions import (
    end_start_point_type_correction_cyclic,
    toggle_curve_cyclic,
    angle_arr_calc_cyclic,
)
from Curve_Array_Magic_Curve.Magic_Curve.General_Functions.Functions import (
    duplicate,
    convert_to_mesh,
    curve_methods_start_checker,
    merged_points_check,
    points_select,
    MethodsCurveData,
    point_direction_vec,
    z_vec,
    tilt_correction,
    main_object_select,
)


def toggle_cyclic_manager():

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

    # Корректируем тип ручек начлаьной и конченой вершины
    end_start_point_type_correction_cyclic(curve)

    # Дублируем кривую
    curve_duplicate = duplicate(curve)

    # Получим информацию о кривой
    curve_duplicate_data = MethodsCurveData(curve_duplicate)

    # Конвертируем в меш
    mesh_curve_duplicate = convert_to_mesh(curve_duplicate)

    # Получаем массив y_vec
    y_vec_arr = point_direction_vec(mesh_curve_duplicate, curve_duplicate_data)
    bpy.data.objects.remove(mesh_curve_duplicate, do_unlink=True)

    # Меняем замкнутость
    toggled_curve = toggle_curve_cyclic(curve)

    # Дублируем кривую
    toggled_curve_duplicate = duplicate(toggled_curve)

    # Получим информацию о кривой
    toggled_curve_duplicate_data = MethodsCurveData(toggled_curve_duplicate)

    # Конвертируем в меш
    mesh_toggled_curve_duplicate = convert_to_mesh(toggled_curve_duplicate)

    # Получаем массив ext_vec
    ext_vec_arr = point_direction_vec(mesh_toggled_curve_duplicate, toggled_curve_duplicate_data)

    # Получаем массив z_vec
    z_vec_arr = z_vec(mesh_toggled_curve_duplicate, toggled_curve_duplicate_data)
    bpy.data.objects.remove(mesh_toggled_curve_duplicate, do_unlink=True)

    # Получаем массив углов поврота
    angle_arr_changed_curve = angle_arr_calc_cyclic(y_vec_arr, ext_vec_arr, z_vec_arr, toggled_curve)

    # Корректируем тильт
    tilt_correction(angle_arr_changed_curve, toggled_curve)

    # Выделяем объект
    main_object_select(toggled_curve)
