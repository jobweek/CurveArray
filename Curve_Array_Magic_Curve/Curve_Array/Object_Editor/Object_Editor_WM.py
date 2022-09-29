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

        QueueSplitLayout.layout_split(layout)

        QueueSplitLayout.number_row.label(text='№')
        QueueSplitLayout.name_row.label(text='Object Name')
        QueueSplitLayout.count_row.label(text='Count')
        QueueSplitLayout.ghost_percent_row.label(text='Ghost %')
        QueueSplitLayout.butt_up_down.label(text='')
        QueueSplitLayout.butt_copy_remove.label(text='')
        QueueSplitLayout.choose_group_row.operator('curvearray.create_empty_group', text='Create Empty Group')
        QueueSplitLayout.set_group_row.label(text='Set')

        if len(queue) > 0:
            layout.row().label(text='Queue:')

        for item_index, q in enumerate(queue):

            QueueSplitLayout.layout_split(layout)

            name = _get_name(q.type, q.index, objects, groups)

            QueueSplitLayout.number_row.label(text=str(item_index + 1))
            QueueSplitLayout.name_row.label(text=name)
            QueueSplitLayout.count_row.prop(q, 'count', text='')
            QueueSplitLayout.ghost_percent_row.prop(q, 'ghost_percentage', text='')

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

                name = _get_name(coll.type, coll.index, objects, groups)

                chance = _calc_chance(coll.count, sum_count)

                GroupsSplitLayout.layout_split(box.row())

                GroupsSplitLayout.number_row.label(text=str(group_index + 1))
                GroupsSplitLayout.name_row.label(text=name)
                GroupsSplitLayout.count_row.prop(coll, 'count', text='')
                GroupsSplitLayout.chance_row.label(text=f"Chance: {chance}%")

                oper = GroupsSplitLayout.butt_up_down.operator('curvearray.duplicate_item', text='', icon='DUPLICATE')
                oper.call_owner = False
                oper.owner_id = group_index
                oper.item_id = item_index

                oper = GroupsSplitLayout.butt_up_down.operator('curvearray.remove_item', text='', icon='PANEL_CLOSE')
                oper.call_owner = False
                oper.owner_id = group_index
                oper.item_id = item_index

                GroupsSplitLayout.choose_group_row.prop(wm_props, 'choose_group', text='')
                oper = GroupsSplitLayout.set_group_row.operator('curvearray.create_set_group', text='Set')
                oper.call_owner = False
                oper.owner_id = group_index
                oper.item_id = item_index
                oper.target_id = wm_choose_group

        layout.row().operator('curvearray.open_editor', icon='OPTIONS')

    def execute(self, _):

        for area in bpy.context.window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()

        return {'FINISHED'}

    def invoke(self, context, _):
        wm = context.window_manager

        return wm.invoke_props_dialog(self, width=540)


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


class QueueSplitLayout:

    number_row: Any
    name_row: Any
    count_row: Any
    ghost_percent_row: Any
    butt_up_down: Any
    butt_copy_remove: Any
    choose_group_row: Any
    set_group_row: Any

    @classmethod
    def layout_split(cls, layout):

        split = layout.split(factor=0.7)

        left_side = split.box()  # 378 pix
        right_side = split.box()  # 162 pix

        split = left_side.split(factor=0.04)  # 363 pix
        cls.number_row = split.row()  # 15 pix

        split = split.split(factor=0.4)  # 214 pix
        cls.name_row = split.row()  # 142 pix

        split = split.split(factor=0.6)
        left_block = split.row()
        right_block = split.row()

        split = left_block.split(factor=0.5)
        cls.count_row = split.row()
        cls.ghost_percent_row = split.row()

        split = right_block.split(factor=0.5)
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
    butt_up_down: Any
    choose_group_row: Any
    set_group_row: Any

    @classmethod
    def layout_split(cls, layout):

        split = layout.split(factor=0.695)

        left_side = split.row()  # 378 pix
        right_side = split.row()  # 162 pix

        split = left_side.split(factor=0.04)  # 363 pix
        cls.number_row = split.row()  # 15 pix

        split = split.split(factor=0.4)  # 214 pix
        cls.name_row = split.row()  # 142 pix

        split = split.split(factor=0.28)
        cls.count_row = split.row()

        split = split.split(factor=0.74)
        cls.chance_row = split.row()
        cls.butt_up_down = split.row(align=True)

        split = right_side.split(factor=0.014)
        split.row()
        right_side = split.row()
        split = right_side.split(factor=0.82)
        cls.choose_group_row = split.row()
        cls.set_group_row = split.row()