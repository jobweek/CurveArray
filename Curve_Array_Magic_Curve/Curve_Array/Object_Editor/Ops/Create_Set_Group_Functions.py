import bpy  # type: ignore
from ...Property.Get_Property_Path import (
    get_queue_props,
    get_groups_props,
)
from ....Errors.Errors import show_message_box
from typing import Any


def create_set_group(call_owner: bool, owner_id: int, item_id: int, target_id: str):

    queue = get_queue_props()
    groups = get_groups_props()

    item, item_owner = _get_item_and_owner(queue, groups, call_owner, owner_id, item_id)

    if (not item.type and item.index == int(target_id)) or (call_owner and target_id == '-2'):
        show_message_box('', "Can't Set to itself", 'NONE')
        return

    if not item.type:

        for i in groups[item.index].collection:

            if not i.type and i.index == int(target_id):
                show_message_box('', "Can't Set, cyclical dependence", 'NONE')
                return

    if target_id == '-2':

        new_item = queue.add()

    elif target_id == '-1':

        new_item = _create_group(queue, groups).collection.add()

    else:

        new_item = groups[int(target_id)].collection.add()

    new_item.index = item.index
    new_item.type = item.type

    item_owner.remove(item_id)


def _get_item_and_owner(queue: Any, groups: Any, call_owner: bool, owner_id: int, item_id: int) -> tuple[Any, Any]:

    if call_owner:
        item_owner = queue
        item = queue[item_id]
    else:
        item_owner = groups[owner_id].collection
        item = groups[owner_id].collection[item_id]

    return item, item_owner


def _create_group(queue: Any, groups: Any) -> Any:

    group_index = len(groups)
    group = groups.add()
    group.name = f'Random Group #{group_index + 1}'
    item = queue.add()
    item.index = group_index
    item.type = False

    return group
