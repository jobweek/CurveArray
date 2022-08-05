import bpy  # type: ignore
import bmesh  # type: ignore
from .Errors import CancelError, ShowMessageBox
from .Toggle_Cyclic_Functions import (
    toggle_cyclic,
    angle_betw_vec,
    z_vec,
    create_z_arr,
)
from .Switch_Direction_Functions import (
    checker,
    merged_points_check,
    points_select,
    duplicate,
    curve_data,
    tilt_twist_calc,
    convert_to_mesh,
    ext_vec,
    angle_correction,
    tilt_correction,
    twist_correction,
)


def toggle_cyclic_manager():

    curve = bpy.context.active_object
    checker()
    merged_points_check(curve)
    points_select(curve)

    if curve.data.twist_mode == 'Z_UP':

        switched_curve = toggle_cyclic(curve)

        bpy.ops.object.select_all(action='DESELECT')
        switched_curve.select_set(True)
        bpy.context.view_layer.objects.active = switched_curve

        return

    elif curve.data.twist_mode == 'TANGENT':

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

    # Создадим массив z_vec для каждой начальной и конечной точки незамкнутого сплайна
    z_vec_arr = create_z_arr(curve_duplicate_data[0])

    # Получаем массив y_vec
    y_vec_arr = ext_vec(mesh_curve_duplicate, curve_duplicate_data)

    # Наполним z_vec_arr
    z_vec_arr = z_vec(z_vec_arr, mesh_curve_duplicate, curve_duplicate_data)
    bpy.data.objects.remove(mesh_curve_duplicate, do_unlink=True)

    # Меняем замкнутость
    toggled_curve = toggle_cyclic(curve)

    # Дублируем кривую
    toggled_curve_duplicate = duplicate(toggled_curve)

    # Получим информацию о кривой
    toggled_curve_duplicate_data = curve_data(toggled_curve_duplicate)

    # Конвертируем в меш
    mesh_toggled_curve_duplicate = convert_to_mesh(toggled_curve_duplicate)

    # Получаем массив ext_vec
    ext_vec_arr = ext_vec(mesh_toggled_curve_duplicate, toggled_curve_duplicate_data)

    # Наполним z_vec_arr
    z_vec_arr = z_vec(z_vec_arr, mesh_toggled_curve_duplicate, toggled_curve_duplicate_data)
    bpy.data.objects.remove(mesh_toggled_curve_duplicate, do_unlink=True)

    # Получаем угол между векторами
    angle_y_ext_arr = angle_betw_vec(y_vec_arr, ext_vec_arr, toggled_curve_duplicate_data[0], z_vec_arr)

    # Дублируем кривую
    test_curve = duplicate(toggled_curve)

    # Тестово поворачиваем точки на половину угла
    tilt_correction(angle_y_ext_arr, test_curve, True)

    # Конвертируем в меш
    mesh_test_curve = convert_to_mesh(test_curve)

    # Получаем массив test_vec
    test_vec_arr = ext_vec(mesh_test_curve, toggled_curve_duplicate_data)
    bpy.data.objects.remove(mesh_test_curve, do_unlink=True)

    # Получаем угол между векторами после поворота
    angle_y_test_arr = angle_betw_vec(y_vec_arr, test_vec_arr, toggled_curve_duplicate_data[0], z_vec_arr)

    # Корректируем углы
    angle_y_ext_arr = angle_correction(angle_y_ext_arr, angle_y_test_arr)

    # Корректируем тильт
    tilt_correction(angle_y_ext_arr, toggled_curve, False)

    tilt_twist_ext_arr = tilt_twist_calc(toggled_curve)

    # Корректируем твист
    twist_correction(tilt_twist_y_arr, tilt_twist_ext_arr, toggled_curve)

    bpy.ops.object.select_all(action='DESELECT')
    toggled_curve.select_set(True)
    bpy.context.view_layer.objects.active = toggled_curve
