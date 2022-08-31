import bpy  # type: ignore
from Curve_Array_Magic_Curve.Curve_Array.Engine.Core.Path_Calculation_Functions import PathData


class InstantPathData(bpy.types.PropertyGroup):
    """Содержит класс PathData, который присваивается полю path_data в начале запуска оператора Curve Array """
    path_data: PathData or None

    def set_path_data(self, path_data: PathData):

        self.path_data = path_data

    def get_path_data(self):

        return self.path_data

    def clear_path_data(self):

        self.path_data = None
