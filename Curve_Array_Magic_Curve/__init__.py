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
from .curve_array_pro_3_0 import (
    CRVARRPRO_PT_CurveArrayPro,
    CRVARRPRO_PT_CurvePanel,
    CRVARRPRO_OT_CurvePicker,
    CRVARRPRO_OT_CurveCleaner,
    CRVARRPRO_PT_ObjectPanel,
    CRVARRPRO_OT_ObjectPicker,
    CRVARRPRO_OT_ObjectCleaner,
    CRVARRPRO_OT_ObjectEditor,
    CRVARRPRO_OT_TransformEditor,
    CRVARRPRO_OT_ClearProp,
    CRVARRPRO_OT_UpProp,
    CRVARRPRO_OT_DownProp,
    CRVARRPRO_OT_NewRandomGroup,
    CRVARRPRO_OT_SetGroup,
    CRVARRPRO_OT_RemoveObjFromRG,
    CRVARRPRO_OT_Empty,
    CRVARRPRO_PT_MainPanel,
    CRVARRPRO_OT_MakeIt,
    CRVARRPRO_PT_ButtonPanel,
    CRVARRPRO_OT_Delete_Last_Array,
    CRVARRPRO_OT_Reset_Settings,
    CRVARRPRO_OT_Flip_Curve
)
from .props.curve_array_props import (
    reg_0,
    reg_1,
    reg_2,
    Main_Props
)
from .Curve_Array.Ops.Curve_Array_By_Offset_Ops import (
    CURVEARRAY_OT_create_array_by_offset
)
from .Curve_Array.Ops.Test_Core_ops import (
    CURVEARRAY_OT_path_calc
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
from .Magic_Curve.Panels.Main_Panel import (
    MAGICCURVE_PT_main_panel
)
from .Magic_Curve.Panels.Create_Curve_Panel import (
    MAGICCURVE_PT_create_curve_panel
)
from .Magic_Curve.Panels.Curve_Methods_Panel import (
    MAGICCURVE_PT_curve_methods_panel
)

classes = (
    Main_Props,
    CURVEARRAY_OT_create_array_by_offset,
    CURVEARRAY_OT_path_calc,
    CRVARRPRO_PT_CurveArrayPro,
    CRVARRPRO_PT_CurvePanel,
    CRVARRPRO_OT_CurvePicker,
    CRVARRPRO_OT_CurveCleaner,
    CRVARRPRO_PT_ObjectPanel,
    CRVARRPRO_OT_ObjectPicker,
    CRVARRPRO_OT_ObjectCleaner,
    CRVARRPRO_OT_ObjectEditor,
    CRVARRPRO_OT_TransformEditor,
    CRVARRPRO_OT_ClearProp,
    CRVARRPRO_OT_UpProp,
    CRVARRPRO_OT_DownProp,
    CRVARRPRO_OT_NewRandomGroup,
    CRVARRPRO_OT_SetGroup,
    CRVARRPRO_OT_RemoveObjFromRG,
    CRVARRPRO_OT_Empty,
    CRVARRPRO_PT_MainPanel,
    CRVARRPRO_OT_MakeIt,
    CRVARRPRO_PT_ButtonPanel,
    CRVARRPRO_OT_Delete_Last_Array,
    CRVARRPRO_OT_Reset_Settings,
    CRVARRPRO_OT_Flip_Curve,
    MAGICCURVE_OT_create_split_curve,
    MAGICCURVE_OT_create_smooth_curve,
    MAGICCURVE_OT_switch_twist_method,
    MAGICCURVE_OT_switch_direction,
    MAGICCURVE_OT_toggle_cyclic,
    MAGICCURVE_PT_main_panel,
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

    for cls in reg_0:
        bpy.utils.register_class(cls)

    for cls in reg_1:
        bpy.utils.register_class(cls)

    for cls in reg_2:
        bpy.utils.register_class(cls)

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.curve_array_properties = bpy.props.PointerProperty(
        type=Main_Props,
        name='Curve Array Properties'
    )


def unregister():

    for cls in reg_0:
        bpy.utils.unregister_class(cls)

    for cls in reg_1:
        bpy.utils.unregister_class(cls)

    for cls in reg_2:
        bpy.utils.unregister_class(cls)

    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.curve_array_properties


if __name__ == "__main__":
    register()
