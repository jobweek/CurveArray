import bpy  # type: ignore
from .Calc_Queue_Data_Functions import (
    QueueData,
)
from ...Property.Get_Property_Path import get_instant_data_props


def calc_queue_data_manager(random_seed: int):

    queue_data = QueueData(random_seed)

    # Присваиваем экземпляр класса QueueData классу InstantPathData в атрибут __data
    get_instant_data_props().queue_data.set(queue_data)
