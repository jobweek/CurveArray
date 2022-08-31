"""
Copyright (C) 2021 JobWeek
5236131@mail.ru

Created by JobWeek

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import bpy  # type: ignore

from .Curve_Array.Property.General_Props import (
    registaration_order,
    CurveArrayProps,
)
from .Curve_Array.Ops.Curve_Array_By_Offset_Ops import (
    CURVEARRAY_OT_create_array_by_offset
)
from .Curve_Array.Ops.Test_Core_ops import (
    CURVEARRAY_OT_path_calc
)
from .Curve_Array.Panels.General_Panel import (
    CURVEARRAY_PT_general_panel
)


from .Magic_Curve.Ops.Smooth_Curve_Ops import (
    MAGICCURVE_OT_create_smooth_curve
)
from .Magic_Curve.Ops.Split_Curve_Ops import (
    MAGICCURVE_OT_create_split_curve
)
from .Magic_Curve.Ops.Change_Twist_Method_Ops import (
    MAGICCURVE_OT_switch_twist_method
)
from .Magic_Curve.Ops.Switch_Direction_Ops import (
    MAGICCURVE_OT_switch_direction
)
from .Magic_Curve.Ops.Toggle_Cyclic_Ops import (
    MAGICCURVE_OT_toggle_cyclic
)


from .Magic_Curve.Panels.General_Panel import (
    MAGICCURVE_PT_general_panel
)
from .Magic_Curve.Panels.Create_Curve_Panel import (
    MAGICCURVE_PT_create_curve_panel
)
from .Magic_Curve.Panels.Curve_Methods_Panel import (
    MAGICCURVE_PT_curve_methods_panel
)

classes = (
    CURVEARRAY_OT_create_array_by_offset,
    CURVEARRAY_OT_path_calc,

    CURVEARRAY_PT_general_panel,


    MAGICCURVE_OT_create_split_curve,
    MAGICCURVE_OT_create_smooth_curve,
    MAGICCURVE_OT_switch_twist_method,
    MAGICCURVE_OT_switch_direction,
    MAGICCURVE_OT_toggle_cyclic,

    MAGICCURVE_PT_general_panel,
    MAGICCURVE_PT_create_curve_panel,
    MAGICCURVE_PT_curve_methods_panel,
)

bl_info = {
    "name": "CurveArray + MagicCurve",
    "author": "JobWeek",
    "version": (4, 0, 0),
    "blender": (3, 2, 0),
    "location": "View3d > Tool",
    "warning": "",
    "wiki_url": "https://github.com/jobweek/CurveArray/tree/Curve_Array_4.0",
    "category": "3D View"
}


def register():

    for cls in registaration_order:
        bpy.utils.register_class(cls)

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.curve_array_properties = bpy.props.PointerProperty(
        type=CurveArrayProps,
        name='CurveArray Properties'
    )


def unregister():

    for cls in registaration_order:
        bpy.utils.unregister_class(cls)

    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.curve_array_properties


if __name__ == "__main__":
    register()
