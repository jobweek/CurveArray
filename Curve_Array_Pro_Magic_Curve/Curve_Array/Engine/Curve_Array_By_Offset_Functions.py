import bpy  # type: ignore
import bmesh  # type: ignore
import mathutils  # type: ignore


def create_profile_direction():

    crv_mesh = bpy.data.curves.new('Curve_Profile', 'CURVE')
    crv_mesh.dimensions = '3D'
    crv_mesh.twist_mode = 'MINIMUM'

    spline = crv_mesh.splines.new(type='POLY')

    spline.points.add(2)

    spline = crv_mesh.splines[0]

    spline.points[0].co[0] = 0
    spline.points[0].co[1] = -0.5
    spline.points[0].co[2] = 0
    spline.points[0].co[3] = 0

    spline.points[1].co[0] = 0
    spline.points[1].co[1] = 0
    spline.points[1].co[2] = 0
    spline.points[1].co[3] = 0

    spline.points[2].co[0] = 0
    spline.points[2].co[1] = 0.5
    spline.points[2].co[2] = 0
    spline.points[2].co[3] = 0

    crv_obj = bpy.data.objects.new('Curve_Profile', crv_mesh)

    bpy.context.scene.collection.objects.link(crv_obj)

    return crv_obj


def get_point_on_spline(distance, spline_segment):

    interpolated_segment = mathutils.geometry.interpolate_bezier(*spline_segment)

    print(interpolated_segment)
