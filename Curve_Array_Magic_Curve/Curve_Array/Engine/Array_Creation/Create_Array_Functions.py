from typing import Any

import bpy  # type: ignore
from mathutils import Vector, Matrix

from Curve_Array_Magic_Curve.Curve_Array.Engine.General_Data_Classes import ItemTransform, ArrayTransform
from Curve_Array_Magic_Curve.Curve_Array.Property.Get_Property_Path import get_curve_props, get_queue_props
from Curve_Array_Magic_Curve.Errors.Errors import show_message_box, CancelError


def trasnform_obj(obj: Any, item_transform: ItemTransform, array_transform: ArrayTransform,
                  rail_axis: str, normal_axis: str):

    def __rotate_x():
        obj.rotation_euler.rotate_axis("X", item_transform.rotation_x + array_transform.rotation_x)

    def __rotate_y():
        obj.rotation_euler.rotate_axis("Y", item_transform.rotation_y + array_transform.rotation_y)

    def __rotate_z():
        obj.rotation_euler.rotate_axis("Z", item_transform.rotation_z + array_transform.rotation_z)

    if rail_axis[1] == 'x':
        if normal_axis[1] == 'y':
            __rotate_x()
            __rotate_y()
            __rotate_z()
        else:
            __rotate_x()
            __rotate_z()
            __rotate_y()
    elif rail_axis[1] == 'y':
        if normal_axis[1] == 'x':
            __rotate_y()
            __rotate_x()
            __rotate_z()

        else:
            __rotate_y()
            __rotate_z()
            __rotate_x()
    elif rail_axis[1] == 'z':
        if normal_axis[1] == 'x':
            __rotate_z()
            __rotate_y()
            __rotate_x()
        else:
            __rotate_z()
            __rotate_x()
            __rotate_y()

    lov_vec = Vector((
        item_transform.location_x + array_transform.location_x,
        item_transform.location_y + array_transform.location_y,
        item_transform.location_z + array_transform.location_z,
    ))

    rot_matrix = obj.rotation_euler.to_matrix().inverted()

    obj.location += lov_vec @ rot_matrix

    obj.scale[0] += item_transform.scale_x + array_transform.scale_x
    obj.scale[1] += item_transform.scale_y + array_transform.scale_y
    obj.scale[2] += item_transform.scale_z + array_transform.scale_z


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


def move_obj(obj: Any, co: Vector):

    obj.location = co


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


def create_collection(parent=None):
    collection = bpy.data.collections.new("CurveArray")

    if parent is None:
        bpy.context.scene.collection.children.link(collection)
    else:
        parent.children.link(collection)

    return collection


def start_check():

    if get_curve_props().name == '':
        show_message_box("Error", f"To create an array, select a curve!", 'ERROR')
        raise CancelError

    if len(get_queue_props()) == 0:
        show_message_box("Error", f"To create an array, store the objects!", 'ERROR')
        raise CancelError
