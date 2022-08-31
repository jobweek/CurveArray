import bpy  # type: ignore
from ...Property.Get_Property_Path import get_curve_props


def clear_curve():

    curve = get_curve_props()

    curve.name = ''
    curve.icon = 'UNLOCKED'
