import bpy # type: ignore
import bmesh # type: ignore
import mathutils # type: ignore
import math
import numpy as np 

def dict_index_correction(dict):
    
    correct_dict = {}
    
    iterator = 0
    
    for i in dict:
        
       correct_dict[iterator] = dict[i]
       
       iterator += 1
       
    return correct_dict

def create_curve(vert_co_array, active_object):
    
    crv_mesh = bpy.data.curves.new('MgCrv_curve_smooth', 'CURVE')
    crv_mesh.dimensions = '3D'
    crv_mesh.twist_mode = 'MINIMUM'        
    spline = crv_mesh.splines.new(type='POLY')
        
    spline.points.add(len(vert_co_array) - 1) 
    
    iterator = 0
    
    for i in vert_co_array:
 
        spline.points[iterator].co[0] =  i[0]
        spline.points[iterator].co[1] =  i[1]
        spline.points[iterator].co[2] =  i[2]
        spline.points[iterator].co[3] =  0
        
        iterator += 1
                
    main_curve = bpy.data.objects.new('MgCrv_curve_smooth', crv_mesh)
        
    main_curve.location = active_object.location
        
    main_curve.rotation_euler = active_object.rotation_euler
        
    main_curve.scale = active_object.scale
  
    bpy.context.scene.collection.objects.link(main_curve)
    
    spline.type = 'BEZIER'
        
    return main_curve
        
def extruded_mesh_vector(extruded_mesh, verts_count):
        
    def extruded_mesh_verts(extruded_mesh, verts_count):
    
        extruded_mesh_verts_array = np.empty(int(verts_count/2), dtype=object)
        
        i = 0
        iterator = 0

        while i < verts_count:
            
            points = [extruded_mesh.data.vertices[0 + i], extruded_mesh.data.vertices[1 + i]]
            
            extruded_mesh_verts_array[iterator] = points
            
            iterator += 1
            i += 2
            
        return extruded_mesh_verts_array
    
    extruded_mesh_verts_array = extruded_mesh_verts(extruded_mesh, verts_count)
    extruded_mesh_vector_array = np.empty(len(extruded_mesh_verts_array), dtype=object)

    iterator = 0

    for i in extruded_mesh_verts_array:

        firts_point = i[0]
        second_point = i[1]
        
        vector = mathutils.Vector((second_point.co[0] - firts_point.co[0], second_point.co[1] - firts_point.co[1], second_point.co[2] - firts_point.co[2]))
        
        extruded_mesh_vector_array[iterator] = vector
        
        iterator += 1
            
    return extruded_mesh_vector_array
        
def angle_between_vector(extruded_mesh_vector_array, active_mesh_vector_array, direction_vetor_array):
    
    def angle_correction(angle, cross_vector, vec_active_mesh):
        
        direction_angle = cross_vector.angle(vec_active_mesh)
                
        if direction_angle < math.pi/2:
            
            return angle
        
        elif direction_angle > math.pi/2:
            
            return angle * (-1)
        
        else:
            
            return angle
            
    angle_array = np.empty(len(extruded_mesh_vector_array), dtype=object)
    
    i = 0
    
    while i < len(extruded_mesh_vector_array):
        
        vec_extruded_mesh = extruded_mesh_vector_array[i]
        
        vec_active_mesh = active_mesh_vector_array[i]
        
        vec_direction = direction_vetor_array[i]
                                
        projection = vec_active_mesh.project(vec_direction)
        correct_vec_active_mesh = vec_active_mesh - projection
        
        projection = vec_extruded_mesh.project(vec_direction)
        correct_vec_extruded_mesh = vec_extruded_mesh - projection
                
        angle = correct_vec_extruded_mesh.angle(correct_vec_active_mesh)
                
        cross_vector = vec_direction.cross(correct_vec_extruded_mesh)
                        
        angle = angle_correction(angle, cross_vector, vec_active_mesh)

        angle_array[i] = angle
        
        i += 1

    return angle_array
    
def tilt_correction(angle_array, main_curve):

    spline = main_curve.data.splines[0]
    
    iterator = 0
    
    for i in angle_array:
            
        spline.bezier_points[iterator].tilt = i
        
        iterator += 1
        

   