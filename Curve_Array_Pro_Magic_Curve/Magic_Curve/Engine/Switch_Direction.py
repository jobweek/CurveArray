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
    ext_z_vec,
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

    # Меняем направление
    switched_curve = switch_curve(curve)

    y_vec_arr, _ = ext_z_vec(extruded_curve, True)
    bpy.data.objects.remove(extruded_curve, do_unlink=True)

    extruded_switched_curve = duplicate(switched_curve)

    ext_vec_arr, z_vec_arr = ext_z_vec(extruded_switched_curve, False)
    bpy.data.objects.remove(extruded_switched_curve, do_unlink=True)

    tilt_correction(ext_vec_arr, y_vec_arr, z_vec_arr, switched_curve)

    bpy.ops.object.select_all(action='DESELECT')
    switched_curve.select_set(True)
    bpy.context.view_layer.objects.active = switched_curve
