import bpy  # type: ignore
from Curve_Array_Magic_Curve.Curve_Array.Engine.Path_Calculation.Path_Calculation_Functions import PathData


class InstantPathData(bpy.types.PropertyGroup):
    """Содержит класс PathData, который присваивается полю data в начале запуска оператора Curve Array """
    data: PathData or None = None

    @classmethod
    def set_data(cls, path_data: PathData):

        cls.data = path_data

    @classmethod
    def get_data(cls) -> PathData:

        return cls.data

    @classmethod
    def clear_data(cls):

        cls.data = None
