import bpy  # type: ignore
from .Remove_Item_Functions import (
    groups_remove,
)


def groups_remove_manager(call_owner: bool, owner_id: int, item_id: int):

    groups_remove(call_owner, owner_id, item_id)
