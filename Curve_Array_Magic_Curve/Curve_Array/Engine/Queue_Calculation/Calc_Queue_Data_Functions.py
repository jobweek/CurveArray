import bpy  # type: ignore
import numpy as np
from typing import Any, NamedTuple
from itertools import cycle
from...Property.Get_Property_Path import (
    get_queue_props,
    get_objects_props,
    get_groups_props,
    get_wm_queue_repetitions,
)


class ItemTransform(NamedTuple):
    rotation_x: float
    rotation_y: float
    rotation_z: float
    location_x: float
    location_y: float
    location_z: float
    scale_x: float
    scale_y: float
    scale_z: float


class QueueItem(NamedTuple):
    object_name: str
    ghost: bool
    item_transform: ItemTransform


class BaseTransform:

    def __init__(self):

        self.rotation_x = [0.0]
        self.rotation_y = [0.0]
        self.rotation_z = [0.0]
        self.location_x = [0.0]
        self.location_y = [0.0]
        self.location_z = [0.0]
        self.scale_x = [0.0]
        self.scale_y = [0.0]
        self.scale_z = [0.0]


class QueueData:

    def __init__(self, random_seed: int):
        self.queue_list = _get_queue_data(random_seed)
        self.queue_loop = None

    def prepare_queue_loop(self):
        self.queue_loop = cycle(self.queue_list)

    def next(self) -> QueueItem:
        return next(self.queue_loop)

    def get_by_index(self, index) -> QueueItem:
        try:
            return self.queue_list[index]
        except IndexError:
            return self.queue_list[index % len(self.queue_list)]

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


def __calc_transform(base_trform: list[float], progressive_trform: float, random_trform: tuple[float, float]) -> float:

    base_trform[0] += progressive_trform

    transform = base_trform[0] + np.random.uniform(random_trform[0], random_trform[1])

    return transform


def _get_queue_data(random_seed: int) -> list[QueueItem]:

    queue = get_queue_props()
    queue_repit = get_wm_queue_repetitions()
    np.random.seed(random_seed)

    queue_list = []

    base_transform = [BaseTransform() for _ in range(len(queue))]

    queue_len = 0

    while queue_len < queue_repit:

        for queue_index, q in enumerate(queue):

            transofrm_data = q.transform_data

            if q.count == 0:
                continue

            for i in range(q.count):

                rotation_x = __calc_transform(
                    base_transform[queue_index].rotation_x,
                    transofrm_data.rotation_progressive_x,
                    (transofrm_data.rotation_random_min_x, transofrm_data.rotation_random_max_x)
                )
                rotation_y = __calc_transform(
                    base_transform[queue_index].rotation_y,
                    transofrm_data.rotation_progressive_y,
                    (transofrm_data.rotation_random_min_y, transofrm_data.rotation_random_max_y)
                )
                rotation_z = __calc_transform(
                    base_transform[queue_index].rotation_z,
                    transofrm_data.rotation_progressive_z,
                    (transofrm_data.rotation_random_min_z, transofrm_data.rotation_random_max_z)
                )
                location_x = __calc_transform(
                    base_transform[queue_index].location_x,
                    transofrm_data.location_progressive_x,
                    (transofrm_data.location_random_min_x, transofrm_data.location_random_max_x)
                )
                location_y = __calc_transform(
                    base_transform[queue_index].location_y,
                    transofrm_data.location_progressive_y,
                    (transofrm_data.location_random_min_y, transofrm_data.location_random_max_y)
                )
                location_z = __calc_transform(
                    base_transform[queue_index].location_z,
                    transofrm_data.location_progressive_z,
                    (transofrm_data.location_random_min_z, transofrm_data.location_random_max_z)
                )
                scale_x = __calc_transform(
                    base_transform[queue_index].scale_x,
                    transofrm_data.scale_progressive_x,
                    (transofrm_data.scale_random_min_x, transofrm_data.scale_random_max_x)
                )
                scale_y = __calc_transform(
                    base_transform[queue_index].scale_y,
                    transofrm_data.scale_progressive_y,
                    (transofrm_data.scale_random_min_y, transofrm_data.scale_random_max_y)
                )
                scale_z = __calc_transform(
                    base_transform[queue_index].scale_z,
                    transofrm_data.scale_progressive_z,
                    (transofrm_data.scale_random_min_z, transofrm_data.scale_random_max_z)
                )

                obj_name = _get_object_name(q)

                if np.random.uniform(0, 100) < q.ghost_percentage:
                    ghost = True
                else:
                    ghost = False

                queue_list.append(QueueItem(
                    obj_name,
                    ghost,
                    ItemTransform(
                        rotation_x,
                        rotation_y,
                        rotation_z,
                        location_x,
                        location_y,
                        location_z,
                        scale_x,
                        scale_y,
                        scale_z,
                    )
                ))

                queue_len += 1

    return queue_list
