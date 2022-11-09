import bpy  # type: ignore
from ..Property.Get_Property_Path import get_instant_data_props
from ..Engine.Object_Creation.Create_Objects_Functions import ObjectsList
from ..Engine.Array_Creation.Spacing_Types.General_Functions import get_collection_by_name


def remove_last_array_manager():

    object_list: ObjectsList = get_instant_data_props().object_list.get()

    if object_list is not None:

        ghost_coll = get_collection_by_name(object_list.ghost_collection)

        for obj in ghost_coll.objects:
            bpy.data.objects.remove(obj, do_unlink=True)

        bpy.data.collections.remove(ghost_coll)

        main_coll = get_collection_by_name(object_list.main_collection)

        for obj in main_coll.objects:
            bpy.data.objects.remove(obj, do_unlink=True)

        bpy.data.collections.remove(main_coll)

    get_instant_data_props().object_list.clear()
    get_instant_data_props().path_data.clear()
    get_instant_data_props().queue_data.clear()
