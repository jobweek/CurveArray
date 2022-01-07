import bpy # type: ignore
import bmesh # type: ignore
import mathutils # type: ignore
import copy
import time
from .Errors import CancelError, ShowMessageBox
from .Classes import checker, cyclic_curve

def active_vertex(bm):
    
    try:
        
        act_vert_index = bm.select_history.active.index
        
        return act_vert_index

    except:
        
        ShowMessageBox("Error","The active vertex must be selected", 'ERROR')
        
        raise CancelError

def selected_edges(bm):
    
    selected_edges_list = []
    
    for i in bm.edges:
        
        if i.select:
            
            selected_edges_list.append(i)   
            
    if len(selected_edges_list) < 1:
        
        ShowMessageBox("Error","Select two or more vertices", 'ERROR')
        
        raise CancelError
    
    else:
    
        return selected_edges_list

def vertices_line(selected_edges_list, act_vert_index):
    
    def vertex_search(edges_list, searched_vertex):
        
        for i in edges_list:
            
            if i.verts[0].index == searched_vertex: 
                
                return i, i.verts[1].index 
            
            elif i.verts[1].index == searched_vertex:
                
                return i, i.verts[0].index 
                
        ShowMessageBox("Error","Select only one loop, or a line segment from connected edges, without intersection, and activate start point at one end", 'ERROR')

        raise CancelError
        
    edges_list = copy.copy(selected_edges_list)
    vertices_line_list = [act_vert_index]
    searched_vertex = act_vert_index
    
    for _ in selected_edges_list:
        
        edge, searched_vertex = vertex_search(edges_list, searched_vertex)
        
        vertices_line_list.append(searched_vertex)
        edges_list.remove(edge)
            
    if len(edges_list) != 0:
        
        ShowMessageBox("Error","Select only one loop, or a line segment from connected edges, without intersection, and activate start point at one end", 'ERROR')

        raise CancelError
    
    return vertices_line_list

def create_extruded_curve(main_curve):
        
    extruded_curve = main_curve.get_curve().copy()
    extruded_curve.data = main_curve.get_curve().data.copy()
    extruded_curve.name = 'MgCrv_duplicate'
    extruded_curve.data.name = 'MgCrv_duplicate'
    extruded_curve.data.extrude = 0.5
    bpy.context.scene.collection.objects.link(extruded_curve)
    
    return extruded_curve

def convert_extuded_curve_to_mesh(extruded_curve):
    
    bpy.ops.object.select_all(action='DESELECT')
    extruded_curve.select_set(True)
    bpy.context.view_layer.objects.active =  extruded_curve
    
    bpy.ops.object.convert(target='MESH')
    
    extruded_mesh = bpy.context.active_object
    
    return extruded_mesh

def active_mesh_vector(bm, vertices_line_list):
    
    active_mesh_vector_list = []
    
    for i in vertices_line_list:
        
        vertex = bm.verts[i].normal
        
        active_mesh_vector_list.append(vertex)
        
    return active_mesh_vector_list

def direction_vector(bm, vertices_line_list):
    
    direction_vetor_list = []
    
    i = 0
    
    while i < len(vertices_line_list) - 1:
        
        first_vertex_index = vertices_line_list[i]
        second_vertex_index = vertices_line_list[i + 1]
            
        first_vertex = bm.verts[first_vertex_index]
        second_vertex = bm.verts[second_vertex_index]
            
        direction_vetor = mathutils.Vector((second_vertex.co[0] -  first_vertex.co[0], second_vertex.co[1] -  first_vertex.co[1], second_vertex.co[2] -  first_vertex.co[2]))
            
        direction_vetor_list.append(direction_vetor.normalized())
        
        i += 1
    
    direction_vetor_list.append(direction_vetor.normalized())
    
    return direction_vetor_list 

def first_step():
    
    active_object = bpy.context.active_object
    active_mesh = active_object.data

    checker.start_checker()
        
    bm = bmesh.from_edit_mesh(active_mesh)
        
    act_vert_index = active_vertex(bm)
    
    selected_edges_list = selected_edges(bm)

    vertices_line_list = vertices_line(selected_edges_list, act_vert_index)
    
    active_mesh_vector_list = active_mesh_vector(bm, vertices_line_list)
    active_mesh_vector_list = copy.deepcopy(active_mesh_vector_list)
    
    direction_vetor_list = direction_vector(bm, vertices_line_list)
    direction_vetor_list = copy.deepcopy(direction_vetor_list)
        
    bpy.ops.object.editmode_toggle()
        
    return vertices_line_list, active_mesh_vector_list, direction_vetor_list, active_object, active_mesh

def second_step(main_curve):
    
    extruded_curve = create_extruded_curve(main_curve)
    
    extruded_mesh = convert_extuded_curve_to_mesh(extruded_curve)
    
    return extruded_mesh

def final_step(extruded_mesh, main_curve):
    
    bpy.data.objects.remove(extruded_mesh, do_unlink=True)
    
    bpy.ops.object.select_all(action='DESELECT') 
    main_curve.get_curve().select_set(True)
    bpy.context.view_layer.objects.active = main_curve.get_curve()