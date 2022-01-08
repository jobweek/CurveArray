import bpy # type: ignore
import bmesh # type: ignore
import mathutils # type: ignore
import math

def dict_index_correction(dict):
    
    correct_dict = {}
    
    iterator = 0
    
    for i in dict:
        
       correct_dict[iterator] = dict[i]
       
       iterator += 1
       
    return correct_dict

def create_curve(vertices_line_dict, active_object, active_mesh):
    
    class Main_Curve:
        
        def set_curve(self, curve):
            
            self.curve = curve
        
        def get_curve(self):
            
            return self.curve
        
        def set_cyclic(self, cyclic):
            
            self.cyclic = cyclic
            
        def get_cyclic(self):
            
            return self.cyclic
                
    main_curve = Main_Curve()
                               
    def cyclic_check(vertices_line_dict):
        
        last_element = len(vertices_line_dict) - 1
        
        if vertices_line_dict[0] == vertices_line_dict[last_element]:
            
            last_index = vertices_line_dict.popitem()[0]
             
            vertices_line_dict[last_index] = vertices_line_dict.pop(0)
                        
            main_curve.set_cyclic(True)
            
            return dict_index_correction(vertices_line_dict)
                    
        else:
            
            main_curve.set_cyclic(False)
    
            return vertices_line_dict

    vertices_line_dict = cyclic_check(vertices_line_dict)
    crv_mesh = bpy.data.curves.new('MgCrv_curve_smooth', 'CURVE')
    crv_mesh.dimensions = '3D'
    crv_mesh.twist_mode = 'MINIMUM'        
    spline = crv_mesh.splines.new(type='POLY')
    
    if main_curve.get_cyclic() == True:
        
        spline.use_cyclic_u = True
    
    spline.points.add(len(vertices_line_dict) - 1) 
    
    i = 0
               
    while i < len(vertices_line_dict):
        
        mesh_vertex_index = vertices_line_dict[i]
        
        spline.points[i].co[0] =  active_mesh.vertices[mesh_vertex_index].co[0]
        spline.points[i].co[1] =  active_mesh.vertices[mesh_vertex_index].co[1]
        spline.points[i].co[2] =  active_mesh.vertices[mesh_vertex_index].co[2]
        spline.points[i].co[3] =  0
        
        i += 1
        
    crv_obj = bpy.data.objects.new('MgCrv_curve_smooth', crv_mesh)
        
    crv_obj.location = active_object.location
        
    crv_obj.rotation_euler = active_object.rotation_euler
        
    crv_obj.scale = active_object.scale
  
    bpy.context.scene.collection.objects.link(crv_obj)
    
    spline.type = 'BEZIER'
    
    main_curve.set_curve(crv_obj)
    
    return main_curve
        
def extruded_mesh_vector(extruded_mesh, vetices_count, main_curve):
    
    def extruded_mesh_vertices(extruded_mesh, vetices_count):
    
        extruded_mesh_vertices_dict = {}
        
        i = 0
        iterator = 0

        while i < vetices_count:
            
            points = [extruded_mesh.data.vertices[0 + i], extruded_mesh.data.vertices[1 + i]]
            
            extruded_mesh_vertices_dict[iterator] = points
            
            last_index = i
            
            iterator += 1
            i += 2
            
        if main_curve.get_cyclic() == True:
               
            extruded_mesh_vertices_dict[last_index] = extruded_mesh_vertices_dict.pop(0)
            
            extruded_mesh_vertices_dict = dict_index_correction(extruded_mesh_vertices_dict)
            
        return extruded_mesh_vertices_dict
    
    extruded_mesh_vertices_dict = extruded_mesh_vertices(extruded_mesh, vetices_count)
    extruded_mesh_vector_dict = {}

    for i in extruded_mesh_vertices_dict:

        firts_point = extruded_mesh_vertices_dict[i][0]
        second_point = extruded_mesh_vertices_dict[i][1]
        
        vector = mathutils.Vector((second_point.co[0] - firts_point.co[0], second_point.co[1] - firts_point.co[1], second_point.co[2] - firts_point.co[2]))
        
        extruded_mesh_vector_dict[i] = vector
            
    return extruded_mesh_vector_dict
        
def angle_between_vector(extruded_mesh_vector_dict, active_mesh_vector_dict, direction_vetor_dict):
    
    def angle_correction(angle, cross_vector, vec_active_mesh):
        
        direction_angle = cross_vector.angle(vec_active_mesh)
                
        if direction_angle < math.pi/2:
            
            return angle
        
        elif direction_angle > math.pi/2:
            
            return angle * (-1)
        
        else:
            
            return angle
            
    angle_dict = {}
    
    i = 0
    
    while i < len(extruded_mesh_vector_dict):
        
        vec_extruded_mesh = extruded_mesh_vector_dict[i]
        
        vec_active_mesh = active_mesh_vector_dict[i]
        
        vec_direction = direction_vetor_dict[i]
                                
        projection = vec_active_mesh.project(vec_direction)
        correct_vec_active_mesh = vec_active_mesh - projection
        
        projection = vec_extruded_mesh.project(vec_direction)
        correct_vec_extruded_mesh = vec_extruded_mesh - projection
                
        angle = correct_vec_extruded_mesh.angle(correct_vec_active_mesh)
                
        cross_vector = vec_direction.cross(correct_vec_extruded_mesh)
                        
        angle = angle_correction(angle, cross_vector, vec_active_mesh)

        angle_dict[i] = angle
        
        i += 1

    return angle_dict
    
def tilt_correction(angle_dict, main_curve):
    
    i = 0
    
    spline = main_curve.get_curve().data.splines[0]
    
    while i < len(angle_dict):
        
        spline.bezier_points[i].tilt = angle_dict[i]
        
        i += 1
   