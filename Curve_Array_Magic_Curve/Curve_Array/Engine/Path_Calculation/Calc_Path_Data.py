import bpy  # type: ignore
import bmesh  # type: ignore

from ...Property.Get_Property_Path import get_instant_data_props
from ....General_Functions.Functions import (
    duplicate,
    convert_to_mesh,
    delete_objects,
)
from .Calc_Path_Data_Functions import (
    verts_sequence_calc,
    get_bm_verts,
    path_data_calc,
    arr_size_calc,
    get_curve,
)


def calc_path_data_manager():

    # Получаем кривую
    curve = get_curve()

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

    # Присваиваем экземпляр класса PathData классу InstantPathData в атрибут __data
    get_instant_data_props().path_data.set(path_data)
