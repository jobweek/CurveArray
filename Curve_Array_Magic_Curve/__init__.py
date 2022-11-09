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
from .Curve_Array.Engine.Array_Creation.Create_Array_Ops import CURVEARRAY_OT_create_array
from .Curve_Array.Engine.Array_Creation.Update_Array_Ops import CURVEARRAY_OT_update_array

from .Curve_Array.Curve_Editor.Ops.Set_Curve_Ops import CURVEARRAY_OT_set_curve
from .Curve_Array.Curve_Editor.Ops.Clear_Curve_Ops import CURVEARRAY_OT_clear_curve

from .Curve_Array.Object_Editor.Ops.Add_Objects_Ops import CURVEARRAY_OT_add_objects
from .Curve_Array.Object_Editor.Ops.Clear_All_Ops import CURVEARRAY_OT_clear_all
from .Curve_Array.Object_Editor.Ops.Queue_Move_Ops import CURVEARRAY_OT_queue_move
from .Curve_Array.Object_Editor.Ops.Create_Empty_Group_Ops import CURVEARRAY_OT_create_empty_group
from .Curve_Array.Object_Editor.Ops.Create_Set_Group_Ops import CURVEARRAY_OT_create_set_group
from .Curve_Array.Object_Editor.Ops.Remove_Item_Ops import CURVEARRAY_OT_remove_item
from .Curve_Array.Object_Editor.Ops.Duplicate_Item_Ops import CURVEARRAY_OT_duplicate_item
from .Curve_Array.Object_Editor.Ops.Catch_Pivot_Ops import CURVEARRAY_OT_catch_pivot
from .Curve_Array.Object_Editor.Object_Editor_WM import CURVEARRAY_OT_open_object_editor

from .Curve_Array.Transform_Editor.Ops.Reset_Transform_Ops import CURVEARRAY_OT_reset_transform
from .Curve_Array.Transform_Editor.Transform_Editor_WM import CURVEARRAY_OT_open_transform_editor

from .Curve_Array.Ops.Remove_Last_Array_Ops import CURVEARRAY_OT_remove_last_array
from .Curve_Array.Ops.Reset_Array_Settings_Ops import CURVEARRAY_OT_reset_array_settings

from .Curve_Array.Panels.General_Panel import CURVEARRAY_PT_general_panel
from .Curve_Array.Curve_Editor.Curve_Panel import CURVEARRAY_PT_curve_panel
from .Curve_Array.Object_Editor.Object_Panel import CURVEARRAY_PT_object_panel
from .Curve_Array.Panels.Array_Settings_Panel import CURVEARRAY_PT_array_settings_panel


from .Magic_Curve.Ops.Smooth_Curve_Ops import MAGICCURVE_OT_create_smooth_curve
from .Magic_Curve.Ops.Split_Curve_Ops import MAGICCURVE_OT_create_split_curve
from .Magic_Curve.Ops.Change_Twist_Method_Ops import MAGICCURVE_OT_switch_twist_method
from .Magic_Curve.Ops.Switch_Direction_Ops import MAGICCURVE_OT_switch_direction
from .Magic_Curve.Ops.Toggle_Cyclic_Ops import MAGICCURVE_OT_toggle_cyclic

from .Magic_Curve.Panels.General_Panel import MAGICCURVE_PT_general_panel
from .Magic_Curve.Panels.Create_Curve_Panel import MAGICCURVE_PT_create_curve_panel
from .Magic_Curve.Panels.Curve_Methods_Panel import MAGICCURVE_PT_curve_methods_panel

classes = (
    CURVEARRAY_OT_create_array,
    CURVEARRAY_OT_update_array,

    CURVEARRAY_OT_set_curve,
    CURVEARRAY_OT_clear_curve,

    CURVEARRAY_OT_add_objects,
    CURVEARRAY_OT_clear_all,

    CURVEARRAY_OT_queue_move,
    CURVEARRAY_OT_create_empty_group,
    CURVEARRAY_OT_create_set_group,
    CURVEARRAY_OT_remove_item,
    CURVEARRAY_OT_duplicate_item,
    CURVEARRAY_OT_catch_pivot,
    CURVEARRAY_OT_open_object_editor,

    CURVEARRAY_OT_reset_transform,
    CURVEARRAY_OT_open_transform_editor,

    CURVEARRAY_OT_remove_last_array,
    CURVEARRAY_OT_reset_array_settings,

    CURVEARRAY_PT_general_panel,
    CURVEARRAY_PT_curve_panel,
    CURVEARRAY_PT_object_panel,
    CURVEARRAY_PT_array_settings_panel,


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

    bpy.types.Scene.curve_array_properties = bpy.props.PointerProperty(
        type=CurveArrayProps,
        name='CurveArray Properties'
    )

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in registaration_order:
        bpy.utils.unregister_class(cls)

    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.curve_array_properties


if __name__ == "__main__":
    register()
