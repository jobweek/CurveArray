import bpy  # type: ignore
from ...Property.Get_Property_Path import (
    get_groups_props,
    get_objects_props,
    get_queue_props,
)
from ...Property.Get_Property_Path import set_wm_choose_group_default
from typing import Any


def groups_remove(call_owner: bool, owner_id: int, item_id: int):

    queue = get_queue_props()
    groups = get_groups_props()
    objects = get_objects_props()

    remove_queue = ([], [])

    item, item_owner = _get_item_and_owner(call_owner, owner_id, item_id, queue, groups)

    if item.type:
        remove_queue[0].append(item.index)

    else:
        set_wm_choose_group_default()
        _remove_group(item.index, remove_queue, groups)

    item_owner.remove(item_id)

    _run_remove_queue_clear(remove_queue, queue, groups, objects)


def _get_item_and_owner(call_owner: bool, owner_id: int, item_id: int, queue: Any, groups: Any,) -> tuple[Any, Any]:

    if call_owner:
        item_owner = queue
        item = queue[item_id]
    else:
        item_owner = groups[owner_id].collection
        item = groups[owner_id].collection[item_id]

    return item, item_owner


def _run_remove_queue_clear(remove_queue: tuple[list, list], queue: Any, groups: Any, objects: Any):

    objets_remove_queue = remove_queue[0]

    objets_remove_queue.sort(reverse=True)

    for i in objets_remove_queue:

        objects.remove(i)

        _object_links_update(i, queue, groups)

    groups_remove_queue = remove_queue[1]

    groups_remove_queue.sort(reverse=True)

    for i in groups_remove_queue:

        groups.remove(i)

        _group_links_update(i, queue, groups)


def _remove_group(index: int, remove_queue: Any, groups: Any):

    for coll in groups[index].collection:

        if coll.type:
            remove_queue[0].append(index)
        else:
            _remove_group(coll.index, remove_queue, groups)

    remove_queue[1].append(index)


def _object_links_update(index: int, queue: Any, groups: Any):

    for q in queue:
        if q.type and q.index > index:
            q.index -= 1

    for g in groups:
        for coll in g.collection:
            if coll.type and coll.index > index:
                coll.index -= 1


def _group_links_update(index: int, queue: Any, groups: Any):

    for q in queue:
        if not q.type and q.index > index:
            q.index -= 1

    for g in groups:
        for coll in g.collection:
            if not coll.type and coll.index > index:
                coll.index -= 1
