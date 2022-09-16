import bpy  # type: ignore
from typing import Iterator
from ..Property.Get_Property_Path import (
    get_queue_props,
    get_groups_props,
    get_objects_props,
)


class CURVEARRAY_PT_object_panel(bpy.types.Panel):

    bl_label = 'Object Editor'
    bl_idname = 'CURVEARRAY_PT_object_panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CrvArrMgcCrv'
    bl_parent_id = 'CURVEARRAY_PT_general_panel'

    def draw(self, _):

        layout = self.layout
        object_count = len(bpy.context.scene.curve_array_properties.engine_props.object_editor_data.objects)

        row = layout.row()
        row.operator('curvearray.add_objects', icon='MESH_DATA')

        row = layout.row().split(factor=0.8)
        row.label(text='Objects stored:')
        row.label(text=str(object_count))

        row = layout.box().split(factor=0.5)
        col_left = row.column()
        col_right = row.column()

        col_generator = _col_generator(col_left, col_right)
        object_names_generator = _object_names_generator()

        i = 1

        for name in object_names_generator:

            if i == 6:
                col = next(col_generator)

                if object_count > 6:
                    col.label(text='And more...')

                else:
                    col.label(text=f'{i}. {name}')

                break

            col = next(col_generator)
            col.label(text=f'{i}. {name}')

            i += 1

        if i == 1:
            col_left.label(text="None")

        row = layout.row()
        row.operator('curvearray.open_editor', icon='OPTIONS')

        row = layout.row()
        row.operator('curvearray.clear_all', icon='CANCEL')


def _object_names_generator() -> Iterator[str]:

    queue = get_queue_props()
    objects = get_objects_props()
    groups = get_groups_props()

    for q in queue:

        if q.type:

            yield objects[q.index].name

        else:

            def __func(index):

                for coll in groups[index].collection:

                    if coll.type:

                        yield objects[coll.index].name

                    else:

                        for y in __func(coll.index):
                            yield y

            for y in __func(q.index):
                yield y


def _col_generator(left, right) -> Iterator[any]:

    while True:
        yield left
        yield right
