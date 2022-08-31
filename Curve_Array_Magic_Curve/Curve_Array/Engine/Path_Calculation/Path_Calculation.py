import bpy  # type: ignore
import bmesh  # type: ignore


from ....General_Functions.Functions import (
    duplicate,
    convert_to_mesh,
    delete_objects,
)
from .Path_Calculation_Functions import (
    verts_sequence_calc,
    get_bm_verts,
    path_data_calc,
    arr_size_calc,
)


def path_calculation_manager(curve):

    # Генератор последовательности вершин кривой
    verts_sequence_generator = verts_sequence_calc(curve)

    # Дублируем кривую
    duplicated_curve = duplicate(curve)

    # Превращаем в меш
    extruded_mesh = convert_to_mesh(duplicated_curve)

    # Получаем bmesh
    bm = get_bm_verts(extruded_mesh)

    # Удаляем меш
    delete_objects(extruded_mesh)

    # Вычисляем размер массива
    arr_size = arr_size_calc(bm.verts, curve)

    # Получаем класс Path Data
    path_data = path_data_calc(verts_sequence_generator, bm.verts, arr_size, curve.name)

    # Присваиваем класс Path Data классу InstantPathData в атрибут data
    bpy.context.scene.curve_array_properties.engine_props.instant_path_data.set_data(path_data)
