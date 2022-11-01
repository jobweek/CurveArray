import bpy  # type: ignore
import mathutils  # type: ignore


def duplicate(active_curve: bpy.types.Curve):

    duplicate_curve = active_curve.copy()
    duplicate_curve.data = active_curve.data.copy()

    if active_curve.animation_data:
        duplicate_curve.animation_data.action = active_curve.animation_data.action.copy()

    for i in active_curve.users_collection:

        i.objects.link(duplicate_curve)

    return duplicate_curve


def convert_to_mesh(curve: bpy.types.Curve):

    curve.data.extrude = 0.5
    curve.data.offset = 0.0
    curve.data.taper_object = None
    curve.data.bevel_depth = 0.0
    curve.data.bevel_object = None
    bpy.ops.object.select_all(action='DESELECT')
    curve.select_set(True)
    bpy.context.view_layer.objects.active = curve
    bpy.ops.object.convert(target='MESH')
    mesh = bpy.context.active_object

    return mesh


def calc_vec(p_0_co: mathutils.Vector, p_1_co: mathutils.Vector, normalize: bool) -> mathutils.Vector:

    vec: mathutils.Vector = p_1_co - p_0_co

    assert vec.length > 0.00002

    if normalize:

        vec = vec.normalized()

    return vec


def midle_point_calc(p_0_co: mathutils.Vector, p_1_co: mathutils.Vector) -> mathutils.Vector:

    vec = calc_vec(p_0_co, p_1_co, False)

    midle_point_co = p_0_co + vec/2

    return midle_point_co


def delete_objects(*objects: bpy.types.Object):

    for obj in objects:

        bpy.data.objects.remove(obj, do_unlink=True)
