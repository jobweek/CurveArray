import bpy # type: ignore
import bmesh # type: ignore
import mathutils # type: ignore
import math
import numpy as np 

def cyclic_correction(vert_co_array, curve_data):
    
    if curve_data.get_cyclic() == True:
                
        arr = np.empty(1, dtype=object)
        
        arr[0] = vert_co_array[0]
                
        vert_co_array = np.append(vert_co_array, arr, axis = 0)
    
    return vert_co_array

def create_curve(vert_co_array, active_object, curve_data):
                        
    def create_spline(crv_mesh, vert_co_array):
                
        for _ in range(len(vert_co_array)-1):
            
            spline = crv_mesh.splines.new(type='POLY')
            
            spline.points.add(1)        
    
    crv_mesh = bpy.data.curves.new('MgCrv_curve_strong', 'CURVE')
    crv_mesh.dimensions = '3D'
    crv_mesh.twist_mode = 'MINIMUM'        
    create_spline(crv_mesh, vert_co_array)
        
    i = 0
               
    while i < len(vert_co_array) - 1:
 
        mesh_vertex_first_co = vert_co_array[i]
        mesh_vertex_second_co = vert_co_array[i + 1]
        
        spline = crv_mesh.splines[i]
        
        spline.points[0].co[0] =  mesh_vertex_first_co[0]
        spline.points[0].co[1] =  mesh_vertex_first_co[1]
        spline.points[0].co[2] =  mesh_vertex_first_co[2]
        spline.points[0].co[3] =  0
                
        spline.points[1].co[0] =  mesh_vertex_second_co[0]
        spline.points[1].co[1] =  mesh_vertex_second_co[1]
        spline.points[1].co[2] =  mesh_vertex_second_co[2]
        spline.points[1].co[3] =  0
                
        i += 1
        
    crv_obj = bpy.data.objects.new('MgCrv_curve_strong', crv_mesh)
        
    crv_obj.location = active_object.location
        
    crv_obj.rotation_euler = active_object.rotation_euler
        
    crv_obj.scale = active_object.scale
  
    bpy.context.scene.collection.objects.link(crv_obj)
    
    for spline in crv_mesh.splines:
    
        spline.type = 'BEZIER'
    
        spline.bezier_points[0].handle_left_type = 'FREE'
        spline.bezier_points[0].handle_right_type = 'FREE'
        
        spline.bezier_points[1].handle_left_type = 'FREE'
        spline.bezier_points[1].handle_right_type = 'FREE'
            
    curve_data.set_curve(crv_obj)
    
    return curve_data

def extruded_mesh_vector(extruded_mesh, vector_count):
    
    extruded_mesh_vector_array = np.empty(vector_count, dtype=object)
    
    i = 0

    while i < vector_count:
        
        firts_point = extruded_mesh.data.vertices[0 + i*4]
        second_point = extruded_mesh.data.vertices[1 + i*4]

        vector = mathutils.Vector((second_point.co[0] - firts_point.co[0], second_point.co[1] - firts_point.co[1], second_point.co[2] - firts_point.co[2]))
        
        extruded_mesh_vector_array[i] = vector

        i += 1
                        
    return extruded_mesh_vector_array

def angle_between_vector(extruded_mesh_vector_array, active_mesh_vector_array, direction_vetor_array):
    print('extruded_mesh_vector_array', extruded_mesh_vector_array)
    print('active_mesh_vector_array', active_mesh_vector_array)
    print('direction_vetor_array', direction_vetor_array)
    def angle_correction(angle, cross_vector, vec_active_mesh):
        
        direction_angle = cross_vector.angle(vec_active_mesh)
                
        if direction_angle < math.pi/2:
            
            return angle
        
        elif direction_angle > math.pi/2:
            
            return angle * (-1)
        
        else:
            
            return angle
                                      
    def corrcet_vec(vec, vec_direction):
            
        projection = vec.project(vec_direction)
        correct_vec = vec - projection    
        
        return correct_vec
        
    angle_array = np.empty(len(extruded_mesh_vector_array), dtype=object)
    
    i = 0
    
    while i < len(extruded_mesh_vector_array):
        
        vec_extruded_mesh = extruded_mesh_vector_array[i]
        vec_active_mesh_first = active_mesh_vector_array[i]
        vec_active_mesh_second = active_mesh_vector_array[i + 1]
        vec_direction = direction_vetor_array[i]
               
        correct_vec_active_mesh_first = corrcet_vec(vec_active_mesh_first, vec_direction)
        correct_vec_active_mesh_second = corrcet_vec(vec_active_mesh_second, vec_direction)
        
        correct_vec_extruded_mesh = corrcet_vec(vec_extruded_mesh, vec_direction)
                
        angle_first = correct_vec_extruded_mesh.angle(correct_vec_active_mesh_first)
        angle_second = correct_vec_extruded_mesh.angle(correct_vec_active_mesh_second)
                
        cross_vector = vec_direction.cross(correct_vec_extruded_mesh)
        print('cross_vector', cross_vector)            
        angle_first = angle_correction(angle_first, cross_vector, vec_active_mesh_first)
        angle_second = angle_correction(angle_second, cross_vector, vec_active_mesh_second)
        
        if math.fabs(angle_first - angle_second) > math.pi:
            
            if angle_second < 0:
            
                angle_second = (math.pi*2 - math.fabs(angle_second))
                
            else: 

                angle_second = (math.pi*2 - math.fabs(angle_second)) * (-1)

        angle_array[i] = [angle_first, angle_second]
        
        i += 1

    return angle_array

def tilt_correction(angle_array, curve_data):
    
    i = 0
    
    while i < len(curve_data.get_curve().data.splines):
    
        spline = curve_data.get_curve().data.splines[i]
        
        angle_spine_list = angle_array[i]
        
        spline.bezier_points[0].tilt = angle_spine_list[0]
        
        spline.bezier_points[1].tilt = angle_spine_list[1]
                
        i += 1