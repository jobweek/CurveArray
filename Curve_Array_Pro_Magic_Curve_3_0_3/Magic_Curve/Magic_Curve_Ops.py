import bpy
import bmesh
import mathutils
import math
from .Errors import CancelError, ShowMessageBox
from .Classes import checker, cyclic_curve
from .First_Step import first_step

def create_curve(vertices_line_list, active_object, active_mesh):
    
    def cyclic_check(vertices_line_list):
        
        if vertices_line_list[0] == vertices_line_list[-1]:
            
            vertices_line_list.pop(-1)
             
            vertices_line_list.extend([vertices_line_list.pop(0)])
            
            cyclic_curve.set(True)
                    
        else:
            
            cyclic_curve.set(False)
    
    cyclic_check(vertices_line_list)
    crv_mesh = bpy.data.curves.new('MgCrv_curve', 'CURVE')
    crv_mesh.dimensions = '3D'
    crv_mesh.twist_mode = 'MINIMUM'        
    spline = crv_mesh.splines.new(type='POLY')
    
    if cyclic_curve.get() == True:
        
        spline.use_cyclic_u = True
    
    spline.points.add(len(vertices_line_list) - 1) 
    
    i = 0
               
    while i < len(vertices_line_list):
        
        mesh_vertex_index = vertices_line_list[i]
        
        spline.points[i].co[0] =  active_mesh.vertices[mesh_vertex_index].co[0]
        spline.points[i].co[1] =  active_mesh.vertices[mesh_vertex_index].co[1]
        spline.points[i].co[2] =  active_mesh.vertices[mesh_vertex_index].co[2]
        spline.points[i].co[3] =  0
        
        i += 1
        
    crv_obj = bpy.data.objects.new('MgCrv_curve', crv_mesh)
        
    crv_obj.location = active_object.location
        
    crv_obj.rotation_euler = active_object.rotation_euler
        
    crv_obj.scale = active_object.scale
  
    bpy.context.scene.collection.objects.link(crv_obj)
    
    spline.type = 'BEZIER'
    
    return crv_obj
    
def create_extruded_curve(main_curve):
    
    extruded_curve = main_curve.copy()
    extruded_curve.data = main_curve.data.copy()
    extruded_curve.name = 'MgCrv_duplicate'
    extruded_curve.data.name = 'MgCrv_duplicate'
    extruded_curve.data.extrude = 0.5
    bpy.context.scene.collection.objects.link(extruded_curve)
    
    return extruded_curve

def convert_curve_to_mesh(extruded_curve):
    
    bpy.ops.object.select_all(action='DESELECT')
    extruded_curve.select_set(True)
    bpy.context.view_layer.objects.active =  extruded_curve
    
    bpy.ops.object.convert(target='MESH')
    
    extruded_mesh = bpy.context.active_object
    
    return extruded_mesh
    
def extruded_mesh_vector(extruded_mesh, vetices_count):
    
    def extruded_mesh_vertices(extruded_mesh, vetices_count):
    
        extruded_mesh_vertices_list = []
        
        i = 0

        while i < vetices_count:
            
            points = [extruded_mesh.data.vertices[0 + i], extruded_mesh.data.vertices[1 + i]]
            
            extruded_mesh_vertices_list.append(points)
            
            i += 2
            
        if cyclic_curve.get() == True:
               
            extruded_mesh_vertices_list.extend([extruded_mesh_vertices_list.pop(0)])
            
        return extruded_mesh_vertices_list
    
    extruded_mesh_vertices_list = extruded_mesh_vertices(extruded_mesh, vetices_count)
    extruded_mesh_vector_list = []

    for i in extruded_mesh_vertices_list:

        firts = i[0]
        second = i[1]
        
        vector = mathutils.Vector((second.co[0] - firts.co[0], second.co[1] - firts.co[1], second.co[2] - firts.co[2]))
        
        extruded_mesh_vector_list.append(vector)
            
    return extruded_mesh_vector_list
    
def active_mesh_vector(active_mesh, vertices_line_list):
    
    active_mesh_vector_list = []
    
    for i in vertices_line_list:
        
        vector = active_mesh.vertices[i].normal
        
        active_mesh_vector_list.append(vector)
    
    return active_mesh_vector_list

def direction_vector(vertices_line_list, active_mesh):
    
    direction_vetor_list = []
    
    i = 0
    
    while i < len(vertices_line_list) - 1:
        
        first_vertex_index = vertices_line_list[i]
        second_vertex_index = vertices_line_list[i + 1]
            
        first_vertex = active_mesh.vertices[first_vertex_index]
        second_vertex = active_mesh.vertices[second_vertex_index]
            
        direction_vetor = mathutils.Vector((second_vertex.co[0] -  first_vertex.co[0], second_vertex.co[1] -  first_vertex.co[1], second_vertex.co[2] -  first_vertex.co[2]))
            
        direction_vetor_list.append(direction_vetor.normalized())
        
        i += 1
    
    direction_vetor_list.append(direction_vetor.normalized())
    
    return direction_vetor_list 
    
def angle_between_vector(extruded_mesh_vector_list, active_mesh_vector_list, direction_vetor_list):
    
    def angle_correction(angle, cross_vector, vec_active_mesh):
        
        direction_angle = cross_vector.angle(vec_active_mesh)
                
        if direction_angle < math.pi/2:
            
            return angle
        
        elif direction_angle > math.pi/2:
            
            return angle * (-1)
        
        else:
            
            return angle
            
    angle_list = []
    
    i = 0
    
    while i < len(extruded_mesh_vector_list):
        
        vec_extruded_mesh = extruded_mesh_vector_list[i]
        
        vec_active_mesh = active_mesh_vector_list[i]
        
        vec_direction = direction_vetor_list[i]
                                
        projection = vec_active_mesh.project(vec_direction)
        correct_vec_active_mesh = vec_active_mesh - projection
        
        projection = vec_extruded_mesh.project(vec_direction)
        correct_vec_extruded_mesh = vec_extruded_mesh - projection
                
        angle = correct_vec_extruded_mesh.angle(correct_vec_active_mesh)
                
        cross_vector = vec_direction.cross(correct_vec_extruded_mesh)
                        
        angle = angle_correction(angle, cross_vector, vec_active_mesh)

        angle_list.append(angle)
        
        i += 1

    return angle_list
    
def tilt_correction(angle_list, main_curve):
    
    i = 0
    
    spline = main_curve.data.splines[0]
    
    while i < len(angle_list):
        
        spline.bezier_points[i].tilt = angle_list[i]
        
        i += 1
    
def manager_smooth_curve():
        
    active_object, active_mesh, vertices_line_list = first_step()
            
    main_curve = create_curve(vertices_line_list, active_object, active_mesh)
        
    extruded_curve = create_extruded_curve(main_curve)
    
    extruded_mesh = convert_curve_to_mesh(extruded_curve)
    
    extruded_mesh_vector_list = extruded_mesh_vector(extruded_mesh, len(vertices_line_list)*2)

    active_mesh_vector_list = active_mesh_vector(active_mesh, vertices_line_list)
    
    direction_vetor_list = direction_vector(vertices_line_list, active_mesh)
    
    angle_list = angle_between_vector(extruded_mesh_vector_list, active_mesh_vector_list, direction_vetor_list)
    
    tilt_correction(angle_list, main_curve)
    
    bpy.data.objects.remove(extruded_mesh, do_unlink=True)
    
    bpy.ops.object.select_all(action='DESELECT') 
    main_curve.select_set(True)
    bpy.context.view_layer.objects.active = main_curve
        
def manager_strong_curve():
    
    active_object, active_mesh, vertices_line_list = first_step()
             
class MAGICCURVE_OT_mgcrv_ops(bpy.types.Operator):
    '''Clear selected curve'''
    bl_label = "Curve from loop"
    bl_idname = 'magiccurve.mgcrv_ops'
    bl_options = {'REGISTER', 'UNDO'}
        
    curve_type : bpy.props.BoolProperty(
        name = "Strong Curve",
        description="Type of algoritm",
        default = False
        )
        
    def execute(self,context):
 
        try:
            
            if self.curve_type == False:
            
                manager_smooth_curve()
            
            else:
                
                manager_strong_curve()
        
        except CancelError:
            
            return {'CANCELLED'}

        # except Exception as e:
            
        #     ShowMessageBox("Unkown Error", "Please send me this report:", e, 'ERROR')
            
        #     return {'CANCELLED'}       
 
        return {'FINISHED'}