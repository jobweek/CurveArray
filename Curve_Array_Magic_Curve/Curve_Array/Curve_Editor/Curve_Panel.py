import bpy  # type: ignore
from ..Property.Get_Property_Path import (
    get_curve_props
)


class CURVEARRAY_PT_curve_panel(bpy.types.Panel):

    bl_label = 'Curve Editor'
    bl_idname = 'CURVEARRAY_PT_curve_panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CrvArrMgcCrv'
    bl_parent_id = 'CURVEARRAY_PT_general_panel'

    def draw(self, _):

        curve = get_curve_props()
        layout = self.layout

        row = layout.row()
        row.operator('curvearray.set_curve', icon='CURVE_DATA')

        row = layout.row()

        if curve.name != '':

            row.label(text=curve.name, icon=curve.icon)

        else:

            row.label(text="None", icon=curve.icon)

        row = layout.row()
        row.operator('curvearray.clear_curve', icon='CANCEL')
