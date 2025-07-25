import bpy  # type: ignore
from ...Property.Get_Property_Path import get_instant_data_props
from ..Queue_Calculation.Calc_Queue_Data_Functions import QueueData
from ..General_Data_Classes import QueueItem
from ..Array_Creation.Spacing_Types.General_Functions import get_object_by_name, get_collection_by_name


def create_collection(parent=None) -> str:

    if parent is None:
        collection = bpy.data.collections.new("CurveArray")
        bpy.context.scene.collection.children.link(collection)
    else:
        collection = bpy.data.collections.new("GhostObjects")
        collection.hide_viewport = True
        collection.hide_render = True
        parent.children.link(collection)

    return collection.name


def clone_obj(obj: bpy.types.Object, cloning_type: str, collection: str) -> bpy.types.Object:

    if cloning_type == '0':
        duplicate = obj.copy()
        try:
            duplicate.data = obj.data.copy()
        except AttributeError:
            pass

        if obj.animation_data:
            duplicate.animation_data.action = obj.animation_data.action.copy()

    elif cloning_type == '1':
        duplicate = obj.copy()
    else:
        duplicate = bpy.data.objects.new(obj.name, obj.data)

    get_collection_by_name(collection).objects.link(duplicate)

    return duplicate


class ObjectsList:

    def __init__(self, count: int, cloning_type: str):

        self.object_list = []
        self.main_collection: str = create_collection()
        self.ghost_collection: str = create_collection(get_collection_by_name(self.main_collection))
        self.count = count
        self.cloning_type = cloning_type

        self._calc_object_list()

    def __duplcate_obj_by_index(self, index: int) -> list[str, bool]:

        queue_data: QueueData = get_instant_data_props().queue_data.get()
        queue_item: QueueItem = queue_data.get_by_index(index)

        obj = get_object_by_name(queue_item.object_name)

        if queue_item.ghost:
            duplicate = clone_obj(obj, self.cloning_type, self.ghost_collection)
        else:
            duplicate = clone_obj(obj, self.cloning_type, self.main_collection)

        return [duplicate.name, queue_item.ghost]

    def _calc_object_list(self):

        for i in range(self.count):

            duplicate = self.__duplcate_obj_by_index(i)

            self.object_list.append(duplicate)

    def check_count(self, count):

        if count != self.count:
            correction = count - self.count

            if correction > 0:
                self._add_objects(correction)
                self.count += correction
            else:
                self._remove_objects(correction)
                self.count += correction

    def _add_objects(self, correction: int):

        for i in range(correction):

            duplicate = self.__duplcate_obj_by_index(self.count + i)

            self.object_list.append(duplicate)

    def _remove_objects(self, correction: int):

        for i in range(-correction):

            obj_name: str = self.object_list.pop()[0]
            obj = get_object_by_name(obj_name)
            bpy.data.objects.remove(obj, do_unlink=True)

    def update_object_list(self, cloning_type, count):

        self._remove_objects(-self.count)
        self.count = 0
        self.cloning_type = cloning_type
        self._add_objects(count)
        self.count = count

    def get_obj_by_index(self, index: int) -> bpy.types.Object:

        obj_name: str = self.object_list[index][0]
        obj = get_object_by_name(obj_name)

        return obj

    def move_obj_to_coll(self, index, ghost: bool):

        item = self.object_list[index]
        obj = get_object_by_name(item[0])
        main_coll = get_collection_by_name(self.main_collection)
        ghost_coll = get_collection_by_name(self.ghost_collection)

        if ghost and not item[1]:

            main_coll.objects.unlink(obj)
            ghost_coll.objects.link(obj)
            item[1] = True
        elif not ghost and item[1]:

            ghost_coll.objects.unlink(obj)
            main_coll.objects.link(obj)
            item[1] = False
