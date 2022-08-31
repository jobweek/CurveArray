import bpy  # type: ignore
from ...Property.Get_Property_Path import (
    get_queue_props,
)


def move_up(index: int):

    if index == 0:

        return

    queue = get_queue_props()

    queue.move(index, index-1)


def move_down(index: int):

    queue = get_queue_props()

    if index == len(queue)-1:

        return

    queue.move(index, index+1)
