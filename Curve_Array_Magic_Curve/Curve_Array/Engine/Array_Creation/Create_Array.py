import bpy  # type: ignore
from typing import Any
from math import radians
from mathutils import Vector, Matrix
from ...Property.Get_Property_Path import get_curve_props, get_queue_props
from ...Property.Get_Property_Path import get_instant_data_props
from ..Path_Calculation.Calc_Path_Data import calc_path_data_manager
from ..Queue_Calculation.Calc_Queue_Data import calc_queue_data_manager
from .Spacing_Types.Fill_By_Offset import fill_by_offset_manager
from .Spacing_Types.General_Data_Classes import ItemData
from ..Queue_Calculation.Calc_Queue_Data_Functions import ItemTransform
from ....Errors.Errors import show_message_box, CancelError


def start_check():

    if get_curve_props().name == '':
        show_message_box("Error", f"To create an array, select a curve!", 'ERROR')
        raise CancelError

    if len(get_queue_props()) == 0:
        show_message_box("Error", f"To create an array, store the objects!", 'ERROR')
        raise CancelError


def create_collection(parent=None):
    collection = bpy.data.collections.new("CurveArray")

    if parent is None:
        bpy.context.scene.collection.children.link(collection)
    else:
        parent.children.link(collection)

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


def align_obj(obj: Any, direction: Vector, normal: Vector, rail_axis: str, normal_axis: str):

    if rail_axis[0] == '-':
        direction = direction * -1
    if normal_axis[0] == '-':
        normal = normal * -1

    def _align(obj: Any, x_vec=None, y_vec=None, z_vec=None):

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
            _align(obj, x_vec=direction, y_vec=normal)
        else:
            _align(obj, x_vec=direction, z_vec=normal)
    elif rail_axis[1] == 'y':
        if normal_axis[1] == 'x':
            _align(obj, x_vec=normal, y_vec=direction)
        else:
            _align(obj, y_vec=direction, z_vec=normal)
    elif rail_axis[1] == 'z':
        if normal_axis[1] == 'x':
            _align(obj, x_vec=normal, z_vec=direction)
        else:
            _align(obj, y_vec=normal, z_vec=direction)
    else:
        raise AssertionError


def trasnform_obj(obj: Any, transform: ItemTransform, rail_axis: str, normal_axis: str):

    def _transform_x_y_z(obj, transform):
        obj.rotation_euler[0] += radians(transform.rotation_x)
        obj.rotation_euler[1] += radians(transform.rotation_y)
        obj.rotation_euler[2] += radians(transform.rotation_z)

    def _transform_x_z_y(obj, transform):
        obj.rotation_euler[0] += radians(transform.rotation_x)
        obj.rotation_euler[2] += radians(transform.rotation_z)
        obj.rotation_euler[1] += radians(transform.rotation_y)

    def _transform_y_x_z(obj, transform):
        obj.rotation_euler[1] += radians(transform.rotation_y)
        obj.rotation_euler[0] += radians(transform.rotation_x)
        obj.rotation_euler[2] += radians(transform.rotation_z)

    def _transform_y_z_x(obj, transform):
        obj.rotation_euler[1] += radians(transform.rotation_y)
        obj.rotation_euler[2] += radians(transform.rotation_z)
        obj.rotation_euler[0] += radians(transform.rotation_x)

    def _transform_z_x_y(obj, transform):
        obj.rotation_euler[2] += radians(transform.rotation_z)
        obj.rotation_euler[0] += radians(transform.rotation_x)
        obj.rotation_euler[1] += radians(transform.rotation_y)

    def _transform_z_y_x(obj, transform):
        obj.rotation_euler[2] += radians(transform.rotation_z)
        obj.rotation_euler[1] += radians(transform.rotation_y)
        obj.rotation_euler[0] += radians(transform.rotation_x)

    if rail_axis[1] == 'x':
        if normal_axis[1] == 'y':
            _transform_x_y_z(obj, transform)
        else:
            _transform_x_z_y(obj, transform)
    elif rail_axis[1] == 'y':
        if normal_axis[1] == 'x':
            _transform_y_x_z(obj, transform)
        else:
            _transform_y_z_x(obj, transform)
    elif rail_axis[1] == 'z':
        if normal_axis[1] == 'x':
            _transform_z_x_y(obj, transform)
        else:
            _transform_z_y_x(obj, transform)

    lov_vec = Vector((transform.location_x, transform.location_y, transform.location_z))
    rot_matrix = obj.rotation_euler.to_matrix().inverted()

    obj.location += lov_vec @ rot_matrix

    obj.scale[0] += transform.scale_x
    obj.scale[1] += transform.scale_y
    obj.scale[2] += transform.scale_z


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

    main_collection = create_collection()
    ghost_collection = None

    while True:
        try:
            item_data: ItemData = next(gen)

            if item_data.ghost:

                if ghost_collection is None:
                    ghost_collection = create_collection(main_collection)

                duplicate = clone_obj(item_data.obj, params['cloning_type'], ghost_collection)
            else:
                duplicate = clone_obj(item_data.obj, params['cloning_type'], main_collection)

            move_obj(duplicate, item_data.co)

            if params['align_rotation']:
                align_obj(duplicate, item_data.direction, item_data.normal, params['rail_axis'], params['normal_axis'])

            trasnform_obj(duplicate, item_data.transform, params['rail_axis'], params['normal_axis'])

        except StopIteration:
            break
