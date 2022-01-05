import bpy
import bmesh
import mathutils
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
        
        spline_count = len(vertices_line_list)/2
        
        for _ in range(spline_count):
            
            spline = crv_mesh.splines.new(type='POLY')
            
            spline.points.add(2) 
    
    crv_mesh = bpy.data.curves.new('MgCrv_curve', 'CURVE')
    crv_mesh.dimensions = '3D'
    crv_mesh.twist_mode = 'MINIMUM'        
    create_spline(crv_mesh, vertices_line_list)
        
    i = 0
               
    while i < len(vertices_line_list) - 1:
        
        mesh_vertex_index_first = vertices_line_list[i]
        mesh_vertex_index_second = vertices_line_list[i + 1]
        
        spline = crv_mesh.splines[i // 2]
        
        spline.points[0].co[0] =  active_mesh.vertices[mesh_vertex_index_first].co[0]
        spline.points[0].co[1] =  active_mesh.vertices[mesh_vertex_index_first].co[1]
        spline.points[0].co[2] =  active_mesh.vertices[mesh_vertex_index_first].co[2]
        spline.points[0].co[3] =  0
        
        spline.points[1].co[0] =  active_mesh.vertices[mesh_vertex_index_second].co[0]
        spline.points[1].co[1] =  active_mesh.vertices[mesh_vertex_index_second].co[1]
        spline.points[1].co[2] =  active_mesh.vertices[mesh_vertex_index_second].co[2]
        spline.points[1].co[3] =  0
        
        i += 1
        
    crv_obj = bpy.data.objects.new('MgCrv_curve', crv_mesh)
        
    crv_obj.location = active_object.location
        
    crv_obj.rotation_euler = active_object.rotation_euler
        
    crv_obj.scale = active_object.scale
  
    bpy.context.scene.collection.objects.link(crv_obj)
    
    spline.type = 'BEZIER'
    
    main_curve.set_curve(crv_obj)
    
    return main_curve