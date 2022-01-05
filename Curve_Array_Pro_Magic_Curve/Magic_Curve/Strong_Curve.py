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

def extruded_mesh_vector(extruded_mesh, vetices_count, main_curve):
    
    def extruded_mesh_vertices(extruded_mesh, vetices_count):
    
        extruded_mesh_vertices_list = []
        
        i = 0

        while i < vetices_count:
            
            points_first = [extruded_mesh.data.vertices[0 + i*4], extruded_mesh.data.vertices[1 + i*4]]
            
            points_second = [extruded_mesh.data.vertices[2 + i*4], extruded_mesh.data.vertices[3 + i*4]]
            
            extruded_mesh_vertices_list.append([points_first, points_second])
            
            i += 1
                        
        return extruded_mesh_vertices_list
    
    extruded_mesh_vertices_list = extruded_mesh_vertices(extruded_mesh, vetices_count)
    extruded_mesh_vector_list = []

    for i in extruded_mesh_vertices_list:

        vector_group = []

        for m in i:

            firts = m[0]
            second = m[1]
            
            vector = mathutils.Vector((second.co[0] - firts.co[0], second.co[1] - firts.co[1], second.co[2] - firts.co[2]))
            
            vector_group.append(vector)
        
        extruded_mesh_vector_list.append(vector_group)
            
    return extruded_mesh_vector_list