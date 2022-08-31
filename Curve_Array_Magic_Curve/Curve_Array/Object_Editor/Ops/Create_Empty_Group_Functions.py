import bpy  # type: ignore

from ...Property.Get_Property_Path import (
    get_queue_props,
    get_groups_props,
)


def create_group():

    groups = get_groups_props()
    queue = get_queue_props()

    index = len(groups)
    item = groups.add()
    item.name = f'Random Group #{index+1}'

    item = queue.add()
    item.index = index
    item.type = False
