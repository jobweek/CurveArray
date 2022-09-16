import bpy  # type: ignore
from Curve_Array_Magic_Curve.Curve_Array.Engine.Path_Calculation.Calc_Path_Data_Functions import PathData
from Curve_Array_Magic_Curve.Curve_Array.Engine.Queue_Calculation.Calc_Queue_Data_Functions import QueueData


class InstantPathData(bpy.types.PropertyGroup):

    __data: PathData or None = None

    @classmethod
    def set(cls, path_data: PathData):

        cls.__data = path_data

    @classmethod
    def get(cls) -> PathData:

        return cls.__data

    @classmethod
    def clear(cls):

        cls.__data = None


class InstantQueueData(bpy.types.PropertyGroup):

    __data: QueueData or None = None

    @classmethod
    def set(cls, queue_data: QueueData):
        cls.__data = queue_data

    @classmethod
    def get(cls) -> PathData:
        cls.__data.prepare_queue_loop()
        return cls.__data

    @classmethod
    def clear(cls):
        cls.__data = None


class InstantData(bpy.types.PropertyGroup):

    path_data: bpy.props.PointerProperty(
        type=InstantPathData,
        name="path_data",
        description=""
        )

    queue_data: bpy.props.PointerProperty(
        type=InstantQueueData,
        name="queue_data",
        description=""
        )
