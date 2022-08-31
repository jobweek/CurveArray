import bpy  # type: ignore
from Curve_Array_Magic_Curve.Curve_Array.Engine.Path_Calculation.Path_Calculation_Functions import PathData


class InstantPathData(bpy.types.PropertyGroup):
    """Содержит класс PathData, который присваивается полю path_data в начале запуска оператора Curve Array """
    path_data: PathData or None = None

    @classmethod
    def set_path_data(cls, path_data: PathData):

        cls.path_data = path_data

    @classmethod
    def get_path_data(cls) -> PathData:

        return cls.path_data

    @classmethod
    def clear_path_data(cls):

        cls.path_data = None
