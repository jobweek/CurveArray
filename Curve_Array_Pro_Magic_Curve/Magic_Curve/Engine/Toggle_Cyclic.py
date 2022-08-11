import bpy  # type: ignore
import bmesh  # type: ignore
from Curve_Array_Pro_Magic_Curve.Errors.Errors import CancelError, show_message_box
from .Toggle_Cyclic_Functions import (
    end_start_point_type_correction_cyclic,
    toggle_curve_cyclic,
)
from ...Common_Functions.Functions import (
    duplicate,
    convert_to_mesh,
    curve_checker,
    merged_points_check,
    points_select,
    curve_data,
    tilt_twist_calc,
    ext_vec,
    z_vec,
    tilt_correction,
    twist_correction,
    object_select,
)


def toggle_cyclic_manager():

    curve = bpy.context.active_object
    curve_checker()
    merged_points_check(curve)
    points_select(curve)

    # Корректируем тип ручек начлаьной и конченой вершины
    end_start_point_type_correction_cyclic(curve)

    if curve.data.twist_mode == 'Z_UP':

        toggled_curve = toggle_curve_cyclic(curve)
        object_select(toggled_curve)

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

    # Конвертируем в меш
    mesh_curve_duplicate = convert_to_mesh(curve_duplicate)

    # Получаем массив y_vec
    y_vec_arr = ext_vec(mesh_curve_duplicate, curve_duplicate_data)
    bpy.data.objects.remove(mesh_curve_duplicate, do_unlink=True)

    # Меняем замкнутость
    toggled_curve = toggle_curve_cyclic(curve)

    # Дублируем кривую
    toggled_curve_duplicate = duplicate(toggled_curve)

    # Получим информацию о кривой
    toggled_curve_duplicate_data = curve_data(toggled_curve_duplicate)

    # Конвертируем в меш
    mesh_toggled_curve_duplicate = convert_to_mesh(toggled_curve_duplicate)

    # Получаем массив ext_vec
    ext_vec_arr = ext_vec(mesh_toggled_curve_duplicate, toggled_curve_duplicate_data)

    # Получаем массив z_vec
    z_vec_arr = z_vec(mesh_toggled_curve_duplicate, toggled_curve_duplicate_data)
    bpy.data.objects.remove(mesh_toggled_curve_duplicate, do_unlink=True)

    # Корректируем тильт
    tilt_correction(y_vec_arr, ext_vec_arr, z_vec_arr, toggled_curve)

    # Получаем твист точек
    tilt_twist_ext_arr = tilt_twist_calc(toggled_curve)

    # Корректируем твист
    twist_correction(tilt_twist_y_arr, tilt_twist_ext_arr, toggled_curve)

    # Выделяем объект
    object_select(toggled_curve)
