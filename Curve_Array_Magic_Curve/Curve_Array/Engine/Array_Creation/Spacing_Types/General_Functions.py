import bpy  # type: ignore
import bmesh  # type: ignore
import numpy as np
from mathutils import Matrix, Vector, Euler  # type: ignore
from Curve_Array_Magic_Curve.Curve_Array.Engine.General_Data_Classes import ArrayTransform, ItemTransform
from Curve_Array_Magic_Curve.Errors.Errors import show_message_box, CancelError


def get_object_by_name(name: str) -> bpy.types.Object:

    try:
        obj = bpy.context.scene.objects[name]
    except KeyError:
        show_message_box("Error", f"Object '{name}' could not be found, "
                                  f"it has been removed from the scene or renamed.", 'ERROR')
        raise CancelError

    return obj


def get_collection_by_name(name: str) -> bpy.types.Collection:

    try:
        coll = bpy.data.collections[name]
    except KeyError:
        show_message_box("Error", f"Collection '{name}' could not be found, "
                                  f"it has been removed from the scene or renamed.", 'ERROR')
        raise CancelError

    return coll


def calc_total_transform(
    obj: bpy.types.Object, array_transform: ArrayTransform, item_transform: ItemTransform
        ) -> Matrix:

    array_transform_matrix = Matrix.LocRotScale(
        Vector((
            array_transform.location_x,
            array_transform.location_y,
            array_transform.location_z,
        )),
        Euler((
            array_transform.rotation_x,
            array_transform.rotation_y,
            array_transform.rotation_z,
        ), 'XYZ'),
        Vector((
            array_transform.scale_x + array_transform.scale_xyz + 1,
            array_transform.scale_y + array_transform.scale_xyz + 1,
            array_transform.scale_z + array_transform.scale_xyz + 1,
        )),
    )

    item_rotation = Matrix.LocRotScale(
        Vector((0, 0, 0)),
        Euler((
            item_transform.rotation_x,
            item_transform.rotation_y,
            item_transform.rotation_z,
        ), 'XYZ'),
        Vector((1, 1, 1)),
    )

    item_loc_scale = Matrix.LocRotScale(
        Vector((
            item_transform.location_x,
            item_transform.location_y,
            item_transform.location_z,
        )),
        Euler((0, 0, 0), 'XYZ'),
        Vector((
            item_transform.scale_x+1,
            item_transform.scale_y+1,
            item_transform.scale_z+1,
        )),
    )

    item_transform_matrix: Matrix = item_rotation @ item_loc_scale

    obj_loc, obj_rot, obj_scale = obj.matrix_world.decompose()

    obj_transform = Matrix.LocRotScale(
        Vector((0, 0, 0)),
        obj_rot,
        obj_scale,
    )
    total_transform: Matrix = obj_transform @ array_transform_matrix @ item_transform_matrix

    return total_transform


def _calc_bm_transform(obj: bpy.types.Object, total_transform: Matrix):

    bm = bmesh.new()
    bm.from_mesh(obj.data)

    bmesh.ops.transform(bm, matrix=total_transform, verts=bm.verts)

    # test_mesh = bpy.data.meshes.new('Test_Mesh')
    # bm.to_mesh(test_mesh)
    # test_obj = bpy.data.objects.new("Test_Obj", test_mesh)
    # bpy.context.collection.objects.link(test_obj)

    return bm


def get_bb_offset(
    obj: bpy.types.Object, array_transform: ArrayTransform, item_transform: ItemTransform,  axis: str, direction: bool
                  ) -> float:

    total_transform = calc_total_transform(obj, array_transform, item_transform)

    try:
        bm = _calc_bm_transform(obj, total_transform)
    except TypeError:
        return 0

    def __collect_points(axis: int) -> np.ndarray:
        def __func(v):
            return v.co[axis]
        arr = np.frompyfunc(__func, 1, 1)
        return arr(bm.verts)

    def _positive_x():
        points = __collect_points(0)
        offset = np.amax(points)
        bm.free()
        return offset

    def _negative_x():
        points = __collect_points(0)
        offset = np.amin(points)
        bm.free()
        return -offset

    def _positive_y():
        points = __collect_points(1)
        offset = np.amax(points)
        bm.free()
        return offset

    def _negative_y():
        points = __collect_points(1)
        offset = np.amin(points)
        bm.free()
        return -offset

    def _positive_z():
        points = __collect_points(2)
        offset = np.amax(points)
        bm.free()
        return offset

    def _negative_z():
        points = __collect_points(2)
        offset = np.amin(points)
        bm.free()
        return -offset

    if axis == '+x':
        if direction:
            return _positive_x()
        else:
            return _negative_x()
    elif axis == '-x':
        if direction:
            return _negative_x()
        else:
            return _positive_x()
    elif axis == '+y':
        if direction:
            return _positive_y()
        else:
            return _negative_y()
    elif axis == '-y':
        if direction:
            return _negative_y()
        else:
            return _positive_y()
    elif axis == '+z':
        if direction:
            return _positive_z()
        else:
            return _negative_z()
    elif axis == '-z':
        if direction:
            return _negative_z()
        else:
            return _positive_z()


def get_dimension_offset(obj: bpy.types.Object, total_transform: Matrix,  axis: str) -> tuple[float, float]:

    try:
        bm = _calc_bm_transform(obj, total_transform)
    except TypeError:
        return 0, 0

    def __collect_points(axis: int) -> np.ndarray:
        def __func(v):
            return v.co[axis]
        arr = np.frompyfunc(__func, 1, 1)
        return arr(bm.verts)

    def __get_dimension(axis: int) -> tuple[float, float]:
        points = __collect_points(axis)
        neg_offset = np.amin(points)
        pos_offset = np.amax(points)
        bm.free()
        return -neg_offset, pos_offset

    if axis[1] == 'x':
        return __get_dimension(0)
    elif axis[1] == 'y':
        return __get_dimension(1)
    elif axis[1] == 'z':
        return __get_dimension(2)
