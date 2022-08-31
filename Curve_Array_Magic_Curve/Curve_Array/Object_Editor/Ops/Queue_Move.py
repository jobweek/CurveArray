import bpy  # type: ignore
from .Queue_Move_Functions import move_up, move_down


#  True = 'Up', False = 'Down'
def queue_move_manager(index: int, direction: bool):

    if direction:
        move_up(index)
    else:
        move_down(index)
