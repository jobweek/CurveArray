import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore


def switch_curve_twist(curve):

    if curve.data.twist_mode == 'Z_UP':

        curve.data.twist_mode = 'MINIMUM'

    else:

        curve.data.twist_mode = 'Z_UP'

    return curve
