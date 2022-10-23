import bpy  # type: ignore
from .Create_Objects_Functions import (
    ObjectsList,
)
from ...Property.Get_Property_Path import get_instant_data_props


def create_objects_manager(count: int, cloning_type: str):

    objects_list = ObjectsList(count, cloning_type)

    get_instant_data_props().object_list.set(objects_list)

