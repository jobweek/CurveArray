import bpy  # type: ignore
from .Duplicate_Item_Functions import duplicate_item


def duplicate_item_manager(call_owner: bool, owner_id: int, item_id: int):

    duplicate_item(call_owner, owner_id, item_id)
