import bpy  # type: ignore
from .Get_Property_Path import get_groups_props


class Queue(bpy.types.PropertyGroup):

    index: bpy.props.IntProperty(
        name="index",
        description="Queue Index",
        default=0,
        min=0,
        )

    type: bpy.props.BoolProperty(
        name="type",
        description="True=Object, False=Group",
        default=True,
        )

    count: bpy.props.IntProperty(
        name="count",
        description="Number of repetitions",
        default=1,
        min=0,
        max=1000,
        )

    ghost: bpy.props.BoolProperty(
        name="ghost",
        description="Is the object ghost",
        default=False,
        )

    ghost_percentage: bpy.props.IntProperty(
        name="ghost_percentage",
        description="The likelihood of the object being a ghost",
        default=0,
        min=0,
        max=100,
        )


class Objects(bpy.types.PropertyGroup):

    name: bpy.props.StringProperty(
        name="name",
        description="Object to be used to create the array",
        default="",
        )


class Collection(bpy.types.PropertyGroup):

    index: bpy.props.IntProperty(
        name="index",
        description="Item index",
        default=0,
        min=0,
        )

    type: bpy.props.BoolProperty(
        name="type",
        description="True=Object, False=Group",
        default=True,
        )

    count: bpy.props.IntProperty(
        name="count",
        description="Item count",
        default=1,
        min=0,
        max=100,
        )


class Groups(bpy.types.PropertyGroup):

    name: bpy.props.StringProperty(
        name="name",
        description="Group name",
        default="",
        )

    collection: bpy.props.CollectionProperty(
        type=Collection,
        name="collection",
        description="",
        )


class WMProperty(bpy.types.PropertyGroup):

    def _get_groups(self, _) -> list[[tuple[str, str, str]]]:

        items = [
            ('-1', "Create Group", ""),
            ('-2', "Queue", ""),
        ]

        groups_props = get_groups_props()
        for i, g in enumerate(groups_props):
            name: str = g.name

            items.append((str(i), name, ""))

        return items

    choose_group: bpy.props.EnumProperty(
        name="Choose Group",
        description="",
        items=_get_groups
    )


class ObjectEditorData(bpy.types.PropertyGroup):

    queue: bpy.props.CollectionProperty(
        type=Queue,
        name="queue",
        description="",
        )

    objects: bpy.props.CollectionProperty(
        type=Objects,
        name="objects",
        description="",
        )

    groups: bpy.props.CollectionProperty(
        type=Groups,
        name="groups",
        description="",
        )

    wm_property: bpy.props.PointerProperty(
        type=WMProperty,
        name="wm_property",
        description=""
        )
