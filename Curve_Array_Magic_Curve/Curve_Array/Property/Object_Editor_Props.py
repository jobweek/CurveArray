import bpy  # type: ignore
from .Get_Property_Path import get_groups_props


class TransformData(bpy.types.PropertyGroup):

    def _rot_rand_min_x_update(self, _):
        if self.rotation_random_min_x > self.rotation_random_max_x:
            self.rotation_random_min_x = self.rotation_random_max_x

    def _rot_rand_min_y_update(self, _):
        if self.rotation_random_min_y > self.rotation_random_max_y:
            self.rotation_random_min_y = self.rotation_random_max_y

    def _rot_rand_min_z_update(self, _):
        if self.rotation_random_min_z > self.rotation_random_max_z:
            self.rotation_random_min_z = self.rotation_random_max_z

    def _rot_rand_max_x_update(self, _):
        if self.rotation_random_max_x < self.rotation_random_min_x:
            self.rotation_random_max_x = self.rotation_random_min_x

    def _rot_rand_max_y_update(self, _):
        if self.rotation_random_max_y < self.rotation_random_min_y:
            self.rotation_random_max_y = self.rotation_random_min_y

    def _rot_rand_max_z_update(self, _):
        if self.rotation_random_max_z < self.rotation_random_min_z:
            self.rotation_random_max_z = self.rotation_random_min_z

    def _loc_rand_min_x_update(self, _):
        if self.location_random_min_x > self.location_random_max_x:
            self.location_random_min_x = self.location_random_max_x

    def _loc_rand_min_y_update(self, _):
        if self.location_random_min_y > self.location_random_max_y:
            self.location_random_min_y = self.location_random_max_y

    def _loc_rand_min_z_update(self, _):
        if self.location_random_min_z > self.location_random_max_z:
            self.location_random_min_z = self.location_random_max_z

    def _loc_rand_max_x_update(self, _):
        if self.location_random_max_x < self.location_random_min_x:
            self.location_random_max_x = self.location_random_min_x

    def _loc_rand_max_y_update(self, _):
        if self.location_random_max_y < self.location_random_min_y:
            self.location_random_max_y = self.location_random_min_y

    def _loc_rand_max_z_update(self, _):
        if self.location_random_max_z < self.location_random_min_z:
            self.location_random_max_z = self.location_random_min_z

    def _scale_rand_min_x_update(self, _):
        if self.scale_random_min_x > self.scale_random_max_x:
            self.scale_random_min_x = self.scale_random_max_x

    def _scale_rand_min_y_update(self, _):
        if self.scale_random_min_y > self.scale_random_max_y:
            self.scale_random_min_y = self.scale_random_max_y

    def _scale_rand_min_z_update(self, _):
        if self.scale_random_min_z > self.scale_random_max_z:
            self.scale_random_min_z = self.scale_random_max_z

    def _scale_rand_max_x_update(self, _):
        if self.scale_random_max_x < self.scale_random_min_x:
            self.scale_random_max_x = self.scale_random_min_x

    def _scale_rand_max_y_update(self, _):
        if self.scale_random_max_y < self.scale_random_min_y:
            self.scale_random_max_y = self.scale_random_min_y

    def _scale_rand_max_z_update(self, _):
        if self.scale_random_max_z < self.scale_random_min_z:
            self.scale_random_max_z = self.scale_random_min_z

    rotation_progressive_x: bpy.props.FloatProperty(
        name="rotation_progressive_x",
        description="Progressive Rotation X Axis",
        default=0,
        soft_min=-360,
        soft_max=360,
        )

    rotation_progressive_y: bpy.props.FloatProperty(
        name="rotation_progressive_y",
        description="Progressive Rotation Y Axis",
        default=0,
        soft_min=-360,
        soft_max=360,
        )

    rotation_progressive_z: bpy.props.FloatProperty(
        name="rotation_progressive_z",
        description="Progressive Rotation Z Axis",
        default=0,
        soft_min=-360,
        soft_max=360,
        )

    rotation_random_min_x: bpy.props.FloatProperty(
        name="rotation_random_soft_min_x",
        description="soft_minimum Random Rotation X Axis",
        default=0,
        soft_min=-360,
        soft_max=360,
        update=_rot_rand_min_x_update,
        )

    rotation_random_min_y: bpy.props.FloatProperty(
        name="rotation_random_soft_min_y",
        description="soft_minimum Random Rotation Y Axis",
        default=0,
        soft_min=-360,
        soft_max=360,
        update=_rot_rand_min_y_update,
        )

    rotation_random_min_z: bpy.props.FloatProperty(
        name="rotation_random_soft_min_z",
        description="soft_minimum Random Rotation Z Axis",
        default=0,
        soft_min=-360,
        soft_max=360,
        update=_rot_rand_min_z_update,
        )

    rotation_random_max_x: bpy.props.FloatProperty(
        name="rotation_random_soft_max_x",
        description="soft_maximum Random Rotation X Axis",
        default=0,
        soft_min=-360,
        soft_max=360,
        update=_rot_rand_max_x_update,
        )

    rotation_random_max_y: bpy.props.FloatProperty(
        name="rotation_random_soft_max_y",
        description="soft_maximum Random Rotation Y Axis",
        default=0,
        soft_min=-360,
        soft_max=360,
        update=_rot_rand_max_y_update,
        )

    rotation_random_max_z: bpy.props.FloatProperty(
        name="rotation_random_soft_max_z",
        description="soft_maximum Random Rotation Z Axis",
        default=0,
        soft_min=-360,
        soft_max=360,
        update=_rot_rand_max_z_update,
        )

    location_progressive_x: bpy.props.FloatProperty(
        name="location_progressive_x",
        description="Progressive Location X Axis",
        default=0,
        )

    location_progressive_y: bpy.props.FloatProperty(
        name="location_progressive_y",
        description="Progressive Location Y Axis",
        default=0,
        )

    location_progressive_z: bpy.props.FloatProperty(
        name="location_progressive_z",
        description="Progressive Location Z Axis",
        default=0,
        )

    location_random_min_x: bpy.props.FloatProperty(
        name="location_random_min_x",
        description="Minimum Random Location X Axis",
        default=0,
        update=_loc_rand_min_x_update,
        )

    location_random_min_y: bpy.props.FloatProperty(
        name="location_random_min_y",
        description="Minimum Random Location Y Axis",
        default=0,
        update=_loc_rand_min_y_update,
        )

    location_random_min_z: bpy.props.FloatProperty(
        name="location_random_min_z",
        description="Minimum Random Location Z Axis",
        default=0,
        update=_loc_rand_min_z_update,
        )

    location_random_max_x: bpy.props.FloatProperty(
        name="location_random_max_x",
        description="Maximum Random Location X Axis",
        default=0,
        update=_loc_rand_max_x_update,
        )

    location_random_max_y: bpy.props.FloatProperty(
        name="location_random_max_y",
        description="Maximum Random Location Y Axis",
        default=0,
        update=_loc_rand_max_y_update,
        )

    location_random_max_z: bpy.props.FloatProperty(
        name="location_random_max_z",
        description="Maximum Random Location Z Axis",
        default=0,
        update=_loc_rand_max_z_update,
        )

    scale_progressive_x: bpy.props.FloatProperty(
        name="scale_progressive_x",
        description="Progressive Scale X Axis",
        default=0,
        soft_min=-1,
        soft_max=1,
        )

    scale_progressive_y: bpy.props.FloatProperty(
        name="scale_progressive_y",
        description="Progressive Scale Y Axis",
        default=0,
        soft_min=-1,
        soft_max=1,
        )

    scale_progressive_z: bpy.props.FloatProperty(
        name="scale_progressive_z",
        description="Progressive Scale Z Axis",
        default=0,
        soft_min=-1,
        soft_max=1,
        )

    scale_random_min_x: bpy.props.FloatProperty(
        name="scale_random_min_x",
        description="Minimum Random Scale X Axis",
        default=0,
        soft_min=-1,
        soft_max=1,
        update=_scale_rand_min_x_update,
        )

    scale_random_min_y: bpy.props.FloatProperty(
        name="scale_random_min_y",
        description="Minimum Random Scale Y Axis",
        default=0,
        soft_min=-1,
        soft_max=1,
        update=_scale_rand_min_y_update,
        )

    scale_random_min_z: bpy.props.FloatProperty(
        name="scale_random_min_z",
        description="Minimum Random Scale Z Axis",
        default=0,
        soft_min=-1,
        soft_max=1,
        update=_scale_rand_min_z_update,
        )

    scale_random_max_x: bpy.props.FloatProperty(
        name="scale_random_max_x",
        description="Maximum Random Scale X Axis",
        default=0,
        soft_min=-1,
        soft_max=1,
        update=_scale_rand_max_x_update,
        )

    scale_random_max_y: bpy.props.FloatProperty(
        name="scale_random_max_y",
        description="Maximum Random Scale Y Axis",
        default=0,
        soft_min=-1,
        soft_max=1,
        update=_scale_rand_max_y_update,
        )

    scale_random_max_z: bpy.props.FloatProperty(
        name="scale_random_max_z",
        description="Maximum Random Scale Z Axis",
        default=0,
        soft_min=-1,
        soft_max=1,
        update=_scale_rand_max_z_update,
        )


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
        max=9999,
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

    transform_data: bpy.props.PointerProperty(
        type=TransformData,
        name="transform_data",
        description="Transform Data"
        )


class Objects(bpy.types.PropertyGroup):

    name: bpy.props.StringProperty(
        name="name",
        description="Object to be used to create the array",
        default="",
        )

    pivot: bpy.props.FloatProperty(
        name="pivot",
        description="Distance to pivot",
        default=0,
        min=0,
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

    pivot: bpy.props.FloatProperty(
        name="pivot",
        description="Distance to pivot",
        default=0,
        min=0,
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
        name="choose_group",
        description="",
        items=_get_groups
    )

    queue_repetitions: bpy.props.IntProperty(
        name="queue_repetitions",
        description="",
        default=1000,
        min=1,
        max=9999,
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
