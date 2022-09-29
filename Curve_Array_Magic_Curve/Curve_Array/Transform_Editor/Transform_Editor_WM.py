import bpy  # type: ignore
from typing import Any
from ..Property.Get_Property_Path import (
    get_queue_props,
    get_objects_props,
    get_groups_props,
)


class CURVEARRAY_OT_open_transform_editor(bpy.types.Operator):
    """Editing Objects which will be used for array creation"""
    bl_label = "Transform Editor"
    bl_idname = 'curvearray.open_transform_editor'
    bl_options = {'UNDO'}

    index: bpy.props.IntProperty(
        name="index",
        description="",
        default=0,
        )

    def draw(self, _):

        queue_item = get_queue_props()[self.index]
        transform = queue_item.transform_data

        layout = self.layout

        split = layout.row().split(factor=0.04)
        split.row()
        split = split.box().split(factor=0.3333)
        split.row().label(text=f'Queue № {self.index+1}: {_get_name(queue_item)}')
        split.row().operator('curvearray.reset_transform', text='Reset Transform')


        split = layout.row().split(factor=0.04)

        axis_coll = split.column()
        axis_coll.row().label(text='')
        axis_coll.row().label(text='')
        axis_coll.row().label(text='')
        axis_coll.row().label(text='Axis X')
        axis_coll.row().label(text='Axis Y')
        axis_coll.row().label(text='Axis Z')

        split = split.split(factor=0.3333)
        rotation_side = split.column()
        split = split.split(factor=0.5)
        location_side = split.column()
        scale_side = split.column()

        rotation_side.row().box().label(text='Rotation')
        location_side.row().box().label(text='Location')
        scale_side.row().box().label(text='Scale')

        rotation_box = rotation_side.row().box()
        location_box = location_side.row().box()
        scale_box = scale_side.row().box()

        # Rotation
        BoxSplitLayout.layout_split(rotation_box)

        BoxSplitLayout.progressive_label.box().label(text='Progressive')
        BoxSplitLayout.rand_label.box().label(text='Random Min')
        BoxSplitLayout.rand_label.box().label(text='Random Max')

        BoxSplitLayout.progressive_x.prop(transform, 'rotation_progressive_x', text='')
        BoxSplitLayout.rand_x.prop(transform, 'rotation_random_min_x', text='')
        BoxSplitLayout.rand_x.prop(transform, 'rotation_random_max_x', text='')
        BoxSplitLayout.progressive_y.prop(transform, 'rotation_progressive_y', text='')
        BoxSplitLayout.rand_y.prop(transform, 'rotation_random_min_y', text='')
        BoxSplitLayout.rand_y.prop(transform, 'rotation_random_max_y', text='')
        BoxSplitLayout.progressive_z.prop(transform, 'rotation_progressive_z', text='')
        BoxSplitLayout.rand_z.prop(transform, 'rotation_random_min_z', text='')
        BoxSplitLayout.rand_z.prop(transform, 'rotation_random_max_z', text='')

        # Location
        BoxSplitLayout.layout_split(location_box)

        BoxSplitLayout.progressive_label.box().label(text='Progressive')
        BoxSplitLayout.rand_label.box().label(text='Random Min')
        BoxSplitLayout.rand_label.box().label(text='Random Max')

        BoxSplitLayout.progressive_x.prop(transform, 'location_progressive_x', text='')
        BoxSplitLayout.rand_x.prop(transform, 'location_random_min_x', text='')
        BoxSplitLayout.rand_x.prop(transform, 'location_random_max_x', text='')
        BoxSplitLayout.progressive_y.prop(transform, 'location_progressive_y', text='')
        BoxSplitLayout.rand_y.prop(transform, 'location_random_min_y', text='')
        BoxSplitLayout.rand_y.prop(transform, 'location_random_max_y', text='')
        BoxSplitLayout.progressive_z.prop(transform, 'location_progressive_z', text='')
        BoxSplitLayout.rand_z.prop(transform, 'location_random_min_z', text='')
        BoxSplitLayout.rand_z.prop(transform, 'location_random_max_z', text='')

        # Scale
        BoxSplitLayout.layout_split(scale_box)

        BoxSplitLayout.progressive_label.box().label(text='Progressive')
        BoxSplitLayout.rand_label.box().label(text='Random Min')
        BoxSplitLayout.rand_label.box().label(text='Random Max')

        BoxSplitLayout.progressive_x.prop(transform, 'scale_progressive_x', text='')
        BoxSplitLayout.rand_x.prop(transform, 'scale_random_min_x', text='')
        BoxSplitLayout.rand_x.prop(transform, 'scale_random_max_x', text='')
        BoxSplitLayout.progressive_y.prop(transform, 'scale_progressive_y', text='')
        BoxSplitLayout.rand_y.prop(transform, 'scale_random_min_y', text='')
        BoxSplitLayout.rand_y.prop(transform, 'scale_random_max_y', text='')
        BoxSplitLayout.progressive_z.prop(transform, 'scale_progressive_z', text='')
        BoxSplitLayout.rand_z.prop(transform, 'scale_random_min_z', text='')
        BoxSplitLayout.rand_z.prop(transform, 'scale_random_max_z', text='')

    def execute(self, _):

        return {'FINISHED'}

    def invoke(self, context, _):
        wm = context.window_manager

        return wm.invoke_props_dialog(self, width=810)


def _get_name(queue_item):

    if queue_item.type:
        return get_objects_props()[queue_item.index].name
    else:
        return get_groups_props()[queue_item.index].name


class BoxSplitLayout:

    progressive_label: Any
    progressive_x: Any
    progressive_y: Any
    progressive_z: Any
    rand_label: Any
    rand_x: Any
    rand_y: Any
    rand_z: Any

    @staticmethod
    def row_split(row):

        split = row.split(factor=0.3333)
        progressive_row = split.row()
        rand_row = split.row(align=True)

        return progressive_row, rand_row

    @classmethod
    def layout_split(cls, box):

        coll = box.column(align=True)

        label = coll.row()
        axis_x = coll.row()
        axis_y = coll.row()
        axis_z = coll.row()

        cls.progressive_label, cls.rand_label = cls.row_split(label)
        cls.progressive_x, cls.rand_x = cls.row_split(axis_x)
        cls.progressive_y, cls.rand_y = cls.row_split(axis_y)
        cls.progressive_z, cls.rand_z = cls.row_split(axis_z)
