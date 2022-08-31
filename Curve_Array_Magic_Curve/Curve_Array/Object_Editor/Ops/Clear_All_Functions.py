import bpy  # type: ignore
from ...Property.Get_Property_Path import (
    get_queue_props,
    get_objects_props,
    get_groups_props,
)


def clear_objects():

    objects = get_objects_props()

    for _ in objects:
        objects.remove(0)


def clear_groups():

    groups = get_groups_props()

    for _ in groups:
        groups.remove(0)


def clear_queue():

    queue = get_queue_props()

    for _ in queue:
        queue.remove(0)
