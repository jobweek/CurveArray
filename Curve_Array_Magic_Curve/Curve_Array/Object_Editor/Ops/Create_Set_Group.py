import bpy  # type: ignore
from .Create_Set_Group_Functions import (
    create_set_group,
)


# call_owner: True = Queue, False = Group
def create_set_group_manager(call_owner: bool, owner_id: int, item_id: int, target_id: str):

    create_set_group(call_owner, owner_id, item_id, target_id)
