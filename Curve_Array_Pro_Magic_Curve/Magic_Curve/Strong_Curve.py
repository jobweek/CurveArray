import bpy # type: ignore
import bmesh # type: ignore
import mathutils # type: ignore
import math

def create_curve(vertices_line_list, active_object, active_mesh):
    
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
                    
    def create_spline(crv_mesh, vertices_line_list):
                
        for _ in range(len(vertices_line_list)-1):
            
            spline = crv_mesh.splines.new(type='POLY')
            
            spline.points.add(1) 
    
    crv_mesh = bpy.data.curves.new('MgCrv_curve_strong', 'CURVE')
    crv_mesh.dimensions = '3D'
    crv_mesh.twist_mode = 'MINIMUM'        
    create_spline(crv_mesh, vertices_line_list)
        
    i = 0
               
    while i < len(vertices_line_list) - 1:
        
        mesh_vertex_index_first = vertices_line_list[i]
        mesh_vertex_index_second = vertices_line_list[i + 1]
        
        spline = crv_mesh.splines[i]
        
        spline.points[0].co[0] =  active_mesh.vertices[mesh_vertex_index_first].co[0]
        spline.points[0].co[1] =  active_mesh.vertices[mesh_vertex_index_first].co[1]
        spline.points[0].co[2] =  active_mesh.vertices[mesh_vertex_index_first].co[2]
        spline.points[0].co[3] =  0
        
        spline.points[1].co[0] =  active_mesh.vertices[mesh_vertex_index_second].co[0]
        spline.points[1].co[1] =  active_mesh.vertices[mesh_vertex_index_second].co[1]
        spline.points[1].co[2] =  active_mesh.vertices[mesh_vertex_index_second].co[2]
        spline.points[1].co[3] =  0
        
        i += 1
        
    crv_obj = bpy.data.objects.new('MgCrv_curve_strong', crv_mesh)
        
    crv_obj.location = active_object.location
        
    crv_obj.rotation_euler = active_object.rotation_euler
        
    crv_obj.scale = active_object.scale
  
    bpy.context.scene.collection.objects.link(crv_obj)
    
    for spline in crv_mesh.splines:
    
        spline.type = 'BEZIER'
    
    main_curve.set_curve(crv_obj)
    
    return main_curve

def extruded_mesh_vector(extruded_mesh, vetices_count):
    
    def extruded_mesh_vertices(extruded_mesh, vetices_count):
    
        extruded_mesh_vertices_list = []
        
        i = 0

        while i < vetices_count:
            
            points = [extruded_mesh.data.vertices[0 + i*4], extruded_mesh.data.vertices[1 + i*4]]
            
            extruded_mesh_vertices_list.append(points)
            
            i += 1
                        
        return extruded_mesh_vertices_list
    
    extruded_mesh_vertices_list = extruded_mesh_vertices(extruded_mesh, vetices_count)
    extruded_mesh_vector_list = []

    for i in extruded_mesh_vertices_list:

        firts_point = i[0]
        second_point = i[1]
        
        vector = mathutils.Vector((second_point.co[0] - firts_point.co[0], second_point.co[1] - firts_point.co[1], second_point.co[2] - firts_point.co[2]))
            
        extruded_mesh_vector_list.append(vector)
            
    return extruded_mesh_vector_list

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
    
    while i < len(extruded_mesh_vector_list) - 1:
        
        vec_extruded_mesh = extruded_mesh_vector_list[i]
        vec_active_mesh = active_mesh_vector_list[i]
        vec_direction = direction_vetor_list[i]
               
        print('vec_extruded_mesh', vec_extruded_mesh)
        print('vec_active_mesh', vec_active_mesh)
        print('vec_direction', vec_direction)
                                
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