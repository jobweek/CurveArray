import bpy  # type: ignore
from ..Property.Get_Property_Path import (
    get_array_settings_props
)


class CURVEARRAY_PT_array_settings_panel(bpy.types.Panel):

    bl_label = 'Array Settings'
    bl_idname = 'CURVEARRAY_PT_array_settings_panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CrvArrMgcCrv'
    bl_parent_id = 'CURVEARRAY_PT_general_panel'

    def draw(self, _):

        layout = self.layout
        sett = get_array_settings_props()

        split = layout.box().split(factor=0.5)
        left_side = split.column()
        right_side = split.column()

        left_side.row().label(text='Random Seed:')
        right_side.row().prop(sett, 'random_seed', text='')

        left_side.row().label(text='Cloning Type:')
        right_side.row().prop(sett, 'cloning_type', text='')

        left_side.row().label(text='Count:')
        right_side.row().prop(sett, 'count', text='')

        left_side.row().label(text='Spacing Type:')
        right_side.row().prop(sett, 'spacing_type', text='')

        left_side.row().label(text='Cyclic:')
        right_side.row().prop(sett, 'cyclic', text='')

        if sett.spacing_type != '3':

            left_side.row().label(text='Smooth Normals:')
            right_side.row().prop(sett, 'smooth_normal', text='')

        if sett.spacing_type == '1':
            left_side.row().label(text='Step Offset:')
            right_side.row().prop(sett, 'step_offset', text='')
        elif sett.spacing_type == '2':
            left_side.row().label(text='Size Offset:')
            right_side.row().prop(sett, 'size_offset', text='')
        elif sett.spacing_type == '3':
            left_side.row().label(text='Step:')
            right_side.row().prop(sett, 'step', text='')

        if sett.spacing_type != '3':

            left_side.row().label(text='Start Offset:')
            right_side.row().prop(sett, 'start_offset', text='')

            left_side.row().label(text='End Offset:')
            right_side.row().prop(sett, 'end_offset', text='')

            left_side.row().label(text='Consider Size:')
            right_side.row().prop(sett, 'consider_size', text='')

        left_side.row().label(text='Slide:')
        right_side.row().prop(sett, 'slide', text='')

        left_side.row().label(text='Align Rotation:')
        right_side.row().prop(sett, 'align_rotation', text='')

        left_side.row().label(text='Rail Axis:')
        right_side.row().prop(sett, 'rail_axis', text='')

        left_side.row().label(text='Normal Axis:')
        right_side.row().prop(sett, 'normal_axis', text='')

        left_coll = left_side.row().column(align=True)
        right_coll = right_side.row().column(align=True)

        left_coll.row().label(text='Rotation X')
        left_coll.row().label(text='Rotation Y')
        left_coll.row().label(text='Rotation Z')

        right_coll.row().prop(sett, 'rotation_x', text='')
        right_coll.row().prop(sett, 'rotation_y', text='')
        right_coll.row().prop(sett, 'rotation_z', text='')

        left_coll = left_side.row().column(align=True)
        right_coll = right_side.row().column(align=True)

        left_coll.row().label(text='Location X')
        left_coll.row().label(text='Location Y')
        left_coll.row().label(text='Location Z')

        right_coll.row().prop(sett, 'location_x', text='')
        right_coll.row().prop(sett, 'location_y', text='')
        right_coll.row().prop(sett, 'location_z', text='')

        left_coll = left_side.row().column(align=True)
        right_coll = right_side.row().column(align=True)

        left_coll.row().label(text='Scale X')
        left_coll.row().label(text='Scale Y')
        left_coll.row().label(text='Scale Z')
        left_coll.row().label(text='Scale XYZ')

        right_coll.row().prop(sett, 'scale_x', text='')
        right_coll.row().prop(sett, 'scale_y', text='')
        right_coll.row().prop(sett, 'scale_z', text='')
        right_coll.row().prop(sett, 'scale_xyz', text='')

        row = layout.row()
        row.label(text='Auto Update:')
        row.prop(sett, 'auto_update', text='')

        row = layout.row()
        row.operator('curvearray.create_array')

        oper = row.operator('curvearray.update_array', text='Update Array')
        oper.update_path_data = True
        oper.update_queue_data = True
