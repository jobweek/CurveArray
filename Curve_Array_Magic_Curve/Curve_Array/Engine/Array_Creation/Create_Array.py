import bpy  # type: ignore
from typing import Any
from mathutils import Vector, Matrix
from ...Property.Get_Property_Path import get_curve_props, get_queue_props
from ...Property.Get_Property_Path import get_instant_data_props
from ..Path_Calculation.Calc_Path_Data import calc_path_data_manager
from ..Queue_Calculation.Calc_Queue_Data import calc_queue_data_manager
from .Spacing_Types.Fill_By_Offset import fill_by_offset_manager
from....Errors.Errors import show_message_box, CancelError


def start_check():

    if get_curve_props().name == '':
        show_message_box("Error", f"To create an array, select a curve!", 'ERROR')
        raise CancelError

    if len(get_queue_props()) == 0:
        show_message_box("Error", f"To create an array, store the objects!", 'ERROR')
        raise CancelError


def create_collection():
    collection = bpy.data.collections.new("CurveArray")
    bpy.context.scene.collection.children.link(collection)
    return collection


def clone_obj(obj: Any, cloning_type: str, collection) -> Any:

    if cloning_type == '0':
        duplicate = obj.copy()
        duplicate.data = obj.data.copy()

        if obj.animation_data:
            duplicate.animation_data.action = obj.animation_data.action.copy()

    elif cloning_type == '1':
        duplicate = obj.copy()
    else:
        duplicate = bpy.data.objects.new(obj.name, obj.data)

    collection.objects.link(duplicate)

    return duplicate


def move_obj(obj: Any, co: Vector):

    obj.location = co


def rotate_obj(obj: Any, direction: Vector, normal: Vector, rail_axis: str, normal_axis: str):

    if rail_axis[0] == '-':
        direction = direction * -1
    if normal_axis[0] == '-':
        normal = normal * -1

    def _align_object(obj: Any, x_vec=None, y_vec=None, z_vec=None):

        if x_vec is None:
            x_vec = y_vec.cross(z_vec)
        elif y_vec is None:
            y_vec = z_vec.cross(x_vec)
        else:
            z_vec = x_vec.cross(y_vec)

        rot_mat = Matrix.Rotation(0, 3, 'X')

        rot_mat[0] = x_vec
        rot_mat[1] = y_vec
        rot_mat[2] = z_vec

        rot_mat_inverted = rot_mat.inverted()
        rot_euler = rot_mat_inverted.to_euler('XYZ')  # type: ignore

        obj.rotation_euler = rot_euler

    if rail_axis[1] == 'x':
        if normal_axis[1] == 'y':
            _align_object(obj, x_vec=direction, y_vec=normal)
        else:
            _align_object(obj, x_vec=direction, z_vec=normal)
    elif rail_axis[1] == 'y':
        if normal_axis[1] == 'x':
            _align_object(obj, x_vec=normal, y_vec=direction)
        else:
            _align_object(obj, y_vec=direction, z_vec=normal)
    elif rail_axis[1] == 'z':
        if normal_axis[1] == 'x':
            _align_object(obj, x_vec=normal, z_vec=direction)
        else:
            _align_object(obj, y_vec=normal, z_vec=direction)
    else:
        raise AssertionError


def crete_array_manager(**params):

    start_check()

    if params['calculate_path_data']:
        calc_path_data_manager()
    path_data = get_instant_data_props().path_data.get()

    if params['calculate_queue_data']:
        calc_queue_data_manager(params['random_seed'])
    queue_data = get_instant_data_props().queue_data.get()

    if params['spacing_type'] == '0':
        gen = fill_by_offset_manager(params, path_data, queue_data)
    else:
        gen = fill_by_offset_manager(params, path_data, queue_data)

    collection = create_collection()

    while True:
        try:
            obj, co, direction, normal = next(gen)

            if obj is None:
                continue

            duplicate = clone_obj(obj, params['cloning_type'], collection)
            move_obj(duplicate, co)

            if params['align_rotation']:
                rotate_obj(duplicate, direction, normal, params['rail_axis'], params['normal_axis'])

        except StopIteration:
            break
