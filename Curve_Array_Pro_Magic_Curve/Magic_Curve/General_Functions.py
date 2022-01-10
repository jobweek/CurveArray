import bpy # type: ignore
import bmesh # type: ignore
import mathutils # type: ignore
import copy
import numpy as np 
from .Errors import CancelError, ShowMessageBox
from .Classes import checker, cyclic_curve
from ..Python_Modules.Memory_Profiler.memory_profiler import profile

def active_vertex(bm):
    
    try:
        
        act_vert_index = bm.select_history.active.index
        
        return act_vert_index

    except:
        
        ShowMessageBox("Error","The active vertex must be selected", 'ERROR')
        
        raise CancelError

@profile
def selected_edges(bm):
    
    selected = np.frompyfunc(lambda a: a.select, 1, 1)
    
    sel_set = selected(bm.edges).astype(bool)
        
    selected_edges_array = np.array(bm.edges)
    
    selected_edges_array = selected_edges_array[sel_set]
    
    print(selected_edges_array)
    print(selected_edges_array[0])
                                
    if len(selected_edges_array) < 1:
        
        ShowMessageBox("Error","Select two or more vertices", 'ERROR')
        
        raise CancelError
    
    else:
    
        return selected_edges_array

def vertices_line(selected_edges_dict, act_vert_index):
    
    def vertex_search(edges_dict, searched_vertex):
        
        for i in edges_dict:
            
            if edges_dict[i].verts[0].index == searched_vertex: 
                
                return i, edges_dict[i].verts[1].index 
            
            elif edges_dict[i].verts[1].index == searched_vertex:
                
                return i, edges_dict[i].verts[0].index 
                
        ShowMessageBox("Error","Select only one loop, or a line segment from connected edges, without intersection, and activate start point at one end", 'ERROR')

        raise CancelError
        
    edges_dict = copy.copy(selected_edges_dict)
    vertices_line_dict = {0:act_vert_index}
    searched_vertex = act_vert_index

    iterator = 1

    for _ in selected_edges_dict:
        
        edge_index, searched_vertex = vertex_search(edges_dict, searched_vertex)
        
        vertices_line_dict[iterator] = searched_vertex
        edges_dict.pop(edge_index)
        
        iterator += 1
            
    if len(edges_dict) != 0:
        
        ShowMessageBox("Error","Select only one loop, or a line segment from connected edges, without intersection, and activate start point at one end", 'ERROR')

        raise CancelError
    
    return vertices_line_dict

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

def active_mesh_vector(bm, vertices_line_dict):
    
    active_mesh_vector_dict = {}
    
    iterator = 0
    
    for i in vertices_line_dict:
        
        vertex = copy.deepcopy(bm.verts[vertices_line_dict[i]].normal)
        
        active_mesh_vector_dict[iterator] = vertex
        
        iterator += 1
        
    return active_mesh_vector_dict

def direction_vector(bm, vertices_line_dict):
    
    direction_vetor_dict = {}
    
    i = 0
    
    while i < len(vertices_line_dict) - 1:
        
        first_vertex_index = vertices_line_dict[i]
        second_vertex_index = vertices_line_dict[i + 1]
            
        first_vertex = bm.verts[first_vertex_index]
        second_vertex = bm.verts[second_vertex_index]
            
        direction_vetor = mathutils.Vector((second_vertex.co[0] -  first_vertex.co[0], second_vertex.co[1] -  first_vertex.co[1], second_vertex.co[2] -  first_vertex.co[2]))
            
        direction_vetor_dict[i] = direction_vetor.normalized()
        
        i += 1
    
    direction_vetor_dict[i] = direction_vetor.normalized()
    
    return direction_vetor_dict 

def first_step():
    
    active_object = bpy.context.active_object
    active_mesh = active_object.data

    checker.start_checker()
        
    bm = bmesh.from_edit_mesh(active_mesh)
        
    act_vert_index = active_vertex(bm)
        
    selected_edges_dict = selected_edges(bm)
    vertices_line_dict = vertices_line(selected_edges_dict, act_vert_index)
    
    active_mesh_vector_dict = active_mesh_vector(bm, vertices_line_dict)
    
    direction_vetor_dict = direction_vector(bm, vertices_line_dict)
        
    bpy.ops.object.editmode_toggle()
        
    return vertices_line_dict, active_mesh_vector_dict, direction_vetor_dict, active_object, active_mesh

def second_step(main_curve):
    
    extruded_curve = create_extruded_curve(main_curve)
    
    extruded_mesh = convert_extuded_curve_to_mesh(extruded_curve)
    
    return extruded_mesh

def final_step(extruded_mesh, main_curve):
    
    bpy.data.objects.remove(extruded_mesh, do_unlink=True)
    
    bpy.ops.object.select_all(action='DESELECT') 
    main_curve.get_curve().select_set(True)
    bpy.context.view_layer.objects.active = main_curve.get_curve()