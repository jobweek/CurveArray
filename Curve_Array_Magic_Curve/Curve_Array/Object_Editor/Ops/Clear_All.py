import bpy  # type: ignore
from Curve_Array_Magic_Curve.Curve_Array.Object_Editor.Ops.Clear_All_Functions import (
    clear_groups,
    clear_queue,
    clear_objects,
)
from ...Property.Get_Property_Path import set_wm_choose_group_default


def clear_all_manager():
    set_wm_choose_group_default()
    clear_queue()
    clear_groups()
    clear_objects()
