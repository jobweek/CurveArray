import bpy  # type: ignore
from typing import Any
from ..Property.Get_Property_Path import (
    get_queue_props,
    get_objects_props,
    get_groups_props,
    get_wm_props,
    get_wm_choose_group_props,
)


class CURVEARRAY_OT_open_object_editor(bpy.types.Operator):
    """Editing Objects which will be used for array creation"""
    bl_label = "Object Editor"
    bl_idname = 'curvearray.open_object_editor'
    bl_options = {'UNDO'}

    def draw(self, _):

        groups = get_groups_props()
        objects = get_objects_props()
        queue = get_queue_props()
        wm_props = get_wm_props()
        wm_choose_group = get_wm_choose_group_props()

        layout = self.layout

        LabelSplitLayout.layout_split(layout)

        LabelSplitLayout.number_row.label(text='№')
        LabelSplitLayout.name_row.label(text='Object Name')
        LabelSplitLayout.count_row.label(text='     Count')
        LabelSplitLayout.ghost_percent_row.label(text='   Ghost %')
        LabelSplitLayout.pivot_row.label(text='      Pivot')
        LabelSplitLayout.transform_row.label(text='  Transform')
        LabelSplitLayout.repition_label_row.label(text='Len:')
        LabelSplitLayout.repition_prop_row.prop(wm_props, 'queue_repetitions', text='')
        LabelSplitLayout.choose_group_row.operator('curvearray.create_empty_group', text='Create Empty Group')
        LabelSplitLayout.set_group_row.label(text='Set')

        if len(queue) > 0:
            layout.row().label(text='Queue:')

        for item_index, q in enumerate(queue):

            QueueSplitLayout.layout_split(layout)

            item_prop = _get_item_prop(q.type, q.index, objects, groups)

            QueueSplitLayout.number_row.label(text=str(item_index + 1))
            QueueSplitLayout.name_row.label(text=item_prop.name)
            QueueSplitLayout.count_row.prop(q, 'count', text='')
            QueueSplitLayout.ghost_percent_row.prop(q, 'ghost_percentage', text='')
            QueueSplitLayout.pivot_row.prop(item_prop, 'pivot', text='')

            oper = QueueSplitLayout.transform_row.operator('curvearray.open_transform_editor', text='Open Editor')
            oper.index = item_index

            oper = QueueSplitLayout.butt_up_down.operator('curvearray.queue_move', text='', icon='TRIA_UP')
            oper.index = item_index
            oper.direction = True

            oper = QueueSplitLayout.butt_up_down.operator('curvearray.queue_move', text='', icon='TRIA_DOWN')
            oper.index = item_index
            oper.direction = False

            oper = QueueSplitLayout.butt_copy_remove.operator('curvearray.duplicate_item', text='', icon='DUPLICATE')
            oper.call_owner = True
            oper.owner_id = 0
            oper.item_id = item_index

            oper = QueueSplitLayout.butt_copy_remove.operator('curvearray.remove_item', text='', icon='PANEL_CLOSE')
            oper.call_owner = True
            oper.owner_id = 0
            oper.item_id = item_index

            QueueSplitLayout.choose_group_row.prop(wm_props, 'choose_group', text='')
            oper = QueueSplitLayout.set_group_row.operator('curvearray.create_set_group', text='Set')
            oper.call_owner = True
            oper.owner_id = 0
            oper.item_id = item_index
            oper.target_id = wm_choose_group

        if len(groups) > 0:
            layout.row().label(text='Groups:')

        for group_index, g in enumerate(groups):

            layout.row().prop(g, 'name', text='')
            box = layout.row().box()

            sum_count = _get_sum_element_count(g)

            if len(g.collection) == 0:
                box.row().label(text='Empty Group')

            for item_index, coll in enumerate(g.collection):

                item_prop = _get_item_prop(coll.type, coll.index, objects, groups)

                chance = _calc_chance(coll.count, sum_count)

                GroupsSplitLayout.layout_split(box.row())

                GroupsSplitLayout.number_row.label(text=str(item_index + 1))
                GroupsSplitLayout.name_row.label(text=item_prop.name)
                GroupsSplitLayout.count_row.prop(coll, 'count', text='')
                GroupsSplitLayout.chance_row.label(text=f"Chance: {chance}%")
                GroupsSplitLayout.pivot_label_row.label(text='Personal Pivot: ')
                GroupsSplitLayout.pivot_prop_row.prop(item_prop, 'pivot', text='')

                oper = GroupsSplitLayout.butt_row.operator('curvearray.duplicate_item', text='', icon='DUPLICATE')
                oper.call_owner = False
                oper.owner_id = group_index
                oper.item_id = item_index

                oper = GroupsSplitLayout.butt_row.operator('curvearray.remove_item', text='', icon='PANEL_CLOSE')
                oper.call_owner = False
                oper.owner_id = group_index
                oper.item_id = item_index

                GroupsSplitLayout.choose_group_row.prop(wm_props, 'choose_group', text='')
                oper = GroupsSplitLayout.set_group_row.operator('curvearray.create_set_group', text='Set')
                oper.call_owner = False
                oper.owner_id = group_index
                oper.item_id = item_index
                oper.target_id = wm_choose_group

    def execute(self, _):

        for area in bpy.context.window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()

        return {'FINISHED'}

    def invoke(self, context, _):
        wm = context.window_manager

        return wm.invoke_props_dialog(self, width=810)


def _calc_chance(part: int, whole: int) -> str:

    if whole == 0 or part == 0:
        chance = 0
    else:
        chance = 100 * float(part) / float(whole)

    return "{0:.1f}".format(chance)


def _get_sum_element_count(group: Any) -> int:

    sum_count = 0

    for coll in group.collection:
        sum_count += coll.count

    return sum_count


def _get_name(item_type: bool, item_index: int, objects: Any, groups: Any) -> str:

    if item_type:
        name: str = objects[item_index].name
    else:
        name: str = groups[item_index].name

    return name


def _get_item_prop(item_type: bool, item_index: int, objects: Any, groups: Any) -> Any:

    if item_type:
        prop = objects[item_index]
    else:
        prop = groups[item_index]

    return prop


class LabelSplitLayout:

    number_row: Any
    name_row: Any
    count_row: Any
    ghost_percent_row: Any
    pivot_row: Any
    transform_row: Any
    repition_label_row: Any
    repition_prop_row: Any
    choose_group_row: Any
    set_group_row: Any

    @classmethod
    def layout_split(cls, layout):

        split = layout.split(factor=0.8)

        left_side = split.row()  # 648 pix
        right_side = split.box()  # 162 pix

        split = left_side.split(factor=0.849)
        left_box = split.box()  # 551 pix
        right_box = split.box()  # 97 pix

        split = left_box.split(factor=0.027)  # 536 pix
        cls.number_row = split.row()  # 15 pix

        split = split.split(factor=0.422)  # 491 pix
        cls.name_row = split.row()  # 190 pix

        split = split.split(factor=0.76)
        left_block = split.row()
        right_block = split.row()

        cls.count_row = left_block.row()
        cls.ghost_percent_row = left_block.row()
        cls.pivot_row = left_block.row()

        cls.transform_row = right_block.row()

        split = right_box.split(factor=0.32)
        cls.repition_label_row = split.row()
        cls.repition_prop_row = split.row()

        split = right_side.split(factor=0.82)
        cls.choose_group_row = split.row()
        cls.set_group_row = split.row()


class QueueSplitLayout:

    number_row: Any
    name_row: Any
    count_row: Any
    ghost_percent_row: Any
    pivot_row: Any
    transform_row: Any
    butt_up_down: Any
    butt_copy_remove: Any
    choose_group_row: Any
    set_group_row: Any

    @classmethod
    def layout_split(cls, layout):

        split = layout.split(factor=0.8)

        left_side = split.box()  # 648 pix
        right_side = split.box()  # 162 pix

        split = left_side.split(factor=0.0231)  # 633 pix
        cls.number_row = split.row()  # 15 pix

        split = split.split(factor=0.35)  # 491 pix
        cls.name_row = split.row()  # 190 pix

        split = split.split(factor=0.55)
        left_block = split.row()
        right_block = split.row()

        cls.count_row = left_block.row()
        cls.ghost_percent_row = left_block.row()
        cls.pivot_row = left_block.row()

        split = right_block.split(factor=0.45)

        cls.transform_row = split.row()

        split = split.split(factor=0.5)
        cls.butt_up_down = split.row(align=True)
        cls.butt_copy_remove = split.row(align=True)

        split = right_side.split(factor=0.82)
        cls.choose_group_row = split.row()
        cls.set_group_row = split.row()


class GroupsSplitLayout:

    number_row: Any
    name_row: Any
    count_row: Any
    chance_row: Any
    pivot_label_row: Any
    pivot_prop_row: Any
    butt_row: Any
    choose_group_row: Any
    set_group_row: Any

    @classmethod
    def layout_split(cls, layout):

        split = layout.split(factor=0.8)

        left_side = split.row()  # 648 pix
        right_side = split.row()  # 162 pix

        split = left_side.split(factor=0.0231)  # 633 pix
        cls.number_row = split.row()  # 15 pix

        split = split.split(factor=0.3487)  # 491 pix
        cls.name_row = split.row()  # 190 pix

        split = split.split(factor=0.168)
        cls.count_row = split.row()

        split = split.split(factor=0.86)
        chance_pivot_row = split.row()

        cls.butt_row = split.row(align=True)

        split = chance_pivot_row.split(factor=0.35)
        cls.chance_row = split.row()

        split = split.split(factor=0.5)
        cls.pivot_label_row = split.row()
        cls.pivot_prop_row = split.row()

        split = right_side.split(factor=0.006)
        split.row()
        right_side = split.row()
        split = right_side.split(factor=0.82)
        cls.choose_group_row = split.row()
        cls.set_group_row = split.row()
