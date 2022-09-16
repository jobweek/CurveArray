import bpy  # type: ignore
import numpy as np
from typing import Any
from itertools import cycle
from...Property.Get_Property_Path import (
    get_queue_props,
    get_objects_props,
    get_groups_props,
)
from....Errors.Errors import show_message_box, CancelError


class QueueData:

    def __init__(self, random_seed: int):
        self.queue_list = _get_queue_data(random_seed)
        self.queue_loop = None

    def prepare_queue_loop(self):
        self.queue_loop = cycle(self.queue_list)

    def next(self):

        return _get_object_by_name(next(self.queue_loop))

    def get_by_index(self, index):
        try:
            return _get_object_by_name(self.queue_list[index])
        except IndexError:
            return _get_object_by_name(self.queue_list[index % len(self.queue_list)])

    def __str__(self):
        return f'\nClass {self.__class__.__name__}:\nQueue_List: {self.queue_list}\n'


def _get_sum_element_count(group: Any) -> int:

    sum_count = 0

    for coll in group.collection:

        sum_count += coll.count

    return sum_count


def _get_cahnce_list(group: Any) -> tuple[list, list] or None:

    index_list = []
    chance_list = []

    sum_count = _get_sum_element_count(group)

    if sum_count == 0:
        return None

    for i, coll in enumerate(group.collection):

        index_list.append(i)
        chance_list.append(float(coll.count)/float(sum_count))

    return index_list, chance_list


def _get_object_by_name(name: str) -> Any:

    try:
        obj = bpy.context.scene.objects[name]
    except KeyError:
        show_message_box("Error", f"Object '{name}' could not be found, "
                                  f"it has been removed from the scene or renamed.", 'ERROR')
        raise CancelError

    return obj


def _get_random_coll(index: int, groups: Any, objects: Any) -> Any or None:

    group = groups[index]
    index_list, chance_list = _get_cahnce_list(group)

    if chance_list is None:
        return None

    rand_index = np.random.choice(a=index_list, size=1, p=chance_list)[0]

    coll = group.collection[rand_index]

    if not coll.type:
        coll = _get_random_coll(coll.index, groups, objects)

    return coll


def _get_object_name(q: Any) -> str or None:

    groups = get_groups_props()
    objects = get_objects_props()

    if q.type:
        name: str = objects[q.index].name
    else:
        coll = _get_random_coll(q.index, groups, objects)
        if coll is None:
            return None
        name: str = objects[coll.index].name

    return name


def _get_queue_data(random_seed: int):

    queue = get_queue_props()
    queue_list = []
    np.random.seed(random_seed)

    for q in queue:

        if q.count == 0:
            continue

        for i in range(q.count):

            if q.ghost_percentage == 100:
                queue_list.append(None)

            elif q.ghost_percentage == 0:
                obj_name = _get_object_name(q)
                queue_list.append(obj_name)
            else:
                if np.random.uniform(0, 100) < q.ghost_percentage:
                    queue_list.append(None)
                else:
                    obj_name = _get_object_name(q)
                    queue_list.append(obj_name)

    return queue_list
