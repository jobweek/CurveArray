import bpy  # type: ignore
from ...Property.Get_Property_Path import (
    get_queue_props,
    get_groups_props,
    get_objects_props,
)

from typing import Any


def duplicate_item(call_owner: bool, owner_id: int, item_id: int):

    queue = get_queue_props()
    groups = get_groups_props()
    objects = get_objects_props()

    item, item_owner = _get_item_and_owner(queue, groups, call_owner, owner_id, item_id)

    if item.type:

        index = _duplicate_object(objects, item)

        index_in_owner = _add_to_owner(item_owner, call_owner, item, index)

    else:

        index = _duplicate_group(queue, objects, groups, item)

        index_in_owner = _add_to_owner(item_owner, call_owner, item, index)

    _move_in_owner(item_owner, index_in_owner, item_id)


def _move_in_owner(item_owner: Any, index_in_owner: int, item_id: int):

    if index_in_owner == item_id + 1:

        return

    item_owner.move(index_in_owner, item_id + 1)


def _add_to_owner(item_owner: Any, call_owner: bool, item: Any, index: int):

    index_in_owner = len(item_owner)
    new_item = item_owner.add()

    if call_owner:

        new_item.index = index
        new_item.type = item.type
        new_item.count = item.count
        new_item.ghost = item.ghost
        new_item.ghost_percentage = item.ghost_percentage

    else:

        new_item.index = index
        new_item.type = item.type
        new_item.count = item.count

    return index_in_owner


def _get_item_and_owner(queue: Any, groups: Any, call_owner: bool, owner_id: int, item_id: int) -> tuple[Any, Any]:

    if call_owner:
        item_owner = queue
        item = queue[item_id]
    else:
        item_owner = groups[owner_id].collection
        item = groups[owner_id].collection[item_id]

    return item, item_owner


def _duplicate_object(objects: Any, item: Any) -> int:

    new_object_index = len(objects)
    new_object = objects.add()
    new_object.name = objects[item.index].name

    return new_object_index


def _duplicate_group(queue: Any, objects: Any, groups: Any, item: Any) -> Any:

    new_group_index = len(groups)
    new_group = groups.add()
    new_group.name = f'{groups[item.index].name}_Copy'

    for coll in groups[item.index].collection:

        new_coll = new_group.collection.add()

        if coll.type:
            index = _duplicate_object(objects, coll)
        else:
            index = _duplicate_group(queue, objects, groups, coll)

        new_coll.index = index
        new_coll.count = coll.count
        new_coll.type = coll.type

    return new_group_index
