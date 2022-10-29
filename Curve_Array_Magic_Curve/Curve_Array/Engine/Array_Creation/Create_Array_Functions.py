import bpy  # type: ignore
from typing import Any
from mathutils import Vector, Matrix  # type: ignore
from Curve_Array_Magic_Curve.Curve_Array.Property.Get_Property_Path import get_curve_props, get_queue_props
from Curve_Array_Magic_Curve.Errors.Errors import show_message_box, CancelError


def trasnform_obj(obj: Any, total_transform: Matrix):

    loc, rot, scale = total_transform.decompose()
    obj.location += loc
    obj.rotation_euler = rot.to_euler('XYZ')  # type: ignore
    obj.scale = scale


def align_obj(direction: Vector, normal: Vector, rail_axis: str, normal_axis: str) -> Matrix:

    if rail_axis[0] == '-':
        direction = direction * -1
    if normal_axis[0] == '-':
        normal = normal * -1

    def _align(x_vec=None, y_vec=None, z_vec=None) -> Matrix:

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

        align_matrix = Matrix.LocRotScale(
            Vector((0, 0, 0)),
            rot_mat.inverted(),
            Vector((1, 1, 1)),
        )

        return align_matrix

    if rail_axis[1] == 'x':
        if normal_axis[1] == 'y':
            return _align(x_vec=direction, y_vec=normal)
        else:
            return _align(x_vec=direction, z_vec=normal)
    elif rail_axis[1] == 'y':
        if normal_axis[1] == 'x':
            return _align(x_vec=normal, y_vec=direction)
        else:
            return _align(y_vec=direction, z_vec=normal)
    else:
        if normal_axis[1] == 'x':
            return _align(x_vec=normal, z_vec=direction)
        else:
            return _align(y_vec=normal, z_vec=direction)


def move_obj(obj: Any, co: Vector):

    obj.location = co


def start_check():

    if get_curve_props().name == '':
        show_message_box("Error", f"To create an array, select a curve!", 'ERROR')
        raise CancelError

    if len(get_queue_props()) == 0:
        show_message_box("Error", f"To create an array, store the objects!", 'ERROR')
        raise CancelError
