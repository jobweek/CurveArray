import bpy  # type: ignore
from Curve_Array_Magic_Curve.Curve_Array.Curve_Editor.Ops.Set_Curve_Functions import (
    get_curve,
)
from ...Property.Get_Property_Path import get_curve_props


def set_curve_manager():

    curve = get_curve()

    get_curve_props().name = curve.name
    get_curve_props().icon = 'LOCKED'
