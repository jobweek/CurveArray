import bpy # type: ignore
import bmesh # type: ignore
import mathutils # type: ignore
import copy
import numpy as np 
from .Errors import CancelError, ShowMessageBox
from .Classes import checker
       
class Curve_Data:
    
    __curve = None
    __cyclic = None
    
    def set_curve(self, curve):
        
        self.__curve = curve
        
    def get_curve(self):
        
        return self.__curve
            
    def set_cyclic(self, cyclic):
        
        self.__cyclic = cyclic
        
    def get_cyclic(self):
        
        return self.__cyclic
            
def active_vertex(bm):
    
    try:
        
        act_vert = bm.select_history.active
        
        return act_vert

    except:
        
        ShowMessageBox("Error","The active vertex must be selected", 'ERROR')
        
        raise CancelError

def selected_verts(bm):
    
    selected = np.frompyfunc(lambda a: a.select, 1, 1)
    
    sel_set = selected(bm.verts).astype(bool)
        
    verts_array = np.array(bm.verts)
    
    selected_verts_array = verts_array[sel_set]
                                    
    if len(selected_verts_array) < 1:
        
        ShowMessageBox("Error","Select two or more vertices", 'ERROR')
        
        raise CancelError
    
    else:
    
        return selected_verts_array
         
def verts_sequence(selected_verts_array, act_vert, curve_data):
                
    def selected_linked_edges(searched_vertex):        
        
        linked_edges = searched_vertex.link_edges
        
        selected_linked_edges_buffer = []
        
        for edge in linked_edges:
            
            if edge.select == True:
                
                selected_linked_edges_buffer.append(edge)
        
        return selected_linked_edges_buffer
                                                                          
    vert_sequence_array = np.empty(len(selected_verts_array), dtype=object)
    
    vert_sequence_array[0] = act_vert
        
    selected_linked_edges_buffer = selected_linked_edges(act_vert)
                    
    if len(selected_linked_edges_buffer) < 1 or len(selected_linked_edges_buffer) > 2:
                
        ShowMessageBox("Error","Select only one loop, or a line segment from connected edges, without intersection, and activate start point at one end", 'ERROR')
        
        raise CancelError
    
    linked_edge = selected_linked_edges_buffer[0]
    
    searched_vertex = linked_edge.other_vert(act_vert)
                                  
    i = 1
        
    while i < len(selected_verts_array) - 1:
                
        vert_sequence_array[i] = searched_vertex
                                
        selected_linked_edges_buffer = selected_linked_edges(searched_vertex)
        
        if len(selected_linked_edges_buffer) != 2:
            
            ShowMessageBox("Error","Select only one loop, or a line segment from connected edges, without intersection, and activate start point at one end", 'ERROR')
            
            raise CancelError
        
        if selected_linked_edges_buffer[0] != linked_edge:
            
            linked_edge = selected_linked_edges_buffer[0]
            
        else:
            
            linked_edge = selected_linked_edges_buffer[1]
    
        searched_vertex = linked_edge.other_vert(searched_vertex)
                
        i += 1
    
    vert_sequence_array[i] = searched_vertex
      
    selected_linked_edges_buffer = selected_linked_edges(searched_vertex)
                    
    if len(selected_linked_edges_buffer) == 2:
        
        curve_data.set_cyclic(True)
        
    else:
        
        curve_data.set_cyclic(False)
                        
    return vert_sequence_array

def create_extruded_curve(main_curve):
        
    extruded_curve = main_curve.copy()
    extruded_curve.data = main_curve.data.copy()
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

def active_mesh_vector(vert_sequence_array):
    
    active_mesh_vector_array = np.empty(len(vert_sequence_array), dtype=object)
    
    iterator = 0
    
    for i in vert_sequence_array:
        
        vertex = copy.deepcopy(i.normal)
        
        active_mesh_vector_array[iterator] = vertex
        
        iterator += 1
        
    return active_mesh_vector_array

def direction_vector(vert_sequence_array):
    
    direction_vetor_array = np.empty(len(vert_sequence_array), dtype=object)
    
    i = 0
    
    while i < len(vert_sequence_array) - 1:
        
        first_vertex = vert_sequence_array[i]
        second_vertex = vert_sequence_array[i + 1]
            
        direction_vetor = mathutils.Vector((second_vertex.co[0] -  first_vertex.co[0], second_vertex.co[1] -  first_vertex.co[1], second_vertex.co[2] -  first_vertex.co[2]))
            
        direction_vetor_array[i] = direction_vetor.normalized()
        
        i += 1
    
    direction_vetor_array[i] = direction_vetor.normalized()
    
    return direction_vetor_array 

def vert_co(vert_sequence_array):
    
    vert_co_array = np.frompyfunc(lambda a: copy.deepcopy(a.co), 1, 1)
    
    vert_co_array = vert_co_array(vert_sequence_array)
    
    return vert_co_array

def first_step():
    
    active_object = bpy.context.active_object
    active_mesh = active_object.data

    checker.start_checker()
    curve_data = Curve_Data()
        
    bm = bmesh.from_edit_mesh(active_mesh)
            
    act_vert = active_vertex(bm)
        
    selected_verts_array = selected_verts(bm)
                
    vert_sequence_array = verts_sequence(selected_verts_array, act_vert, curve_data)
    
    active_mesh_vector_array = active_mesh_vector(vert_sequence_array)
    
    direction_vetor_array = direction_vector(vert_sequence_array)
    
    vert_co_array = vert_co(vert_sequence_array)
        
    bpy.ops.object.editmode_toggle()
        
    return vert_co_array, active_mesh_vector_array, direction_vetor_array, active_object, curve_data

def second_step(curve_data):
    
    extruded_curve = create_extruded_curve(curve_data.get_curve())
    
    extruded_mesh = convert_extuded_curve_to_mesh(extruded_curve)
    
    return extruded_mesh

def final_step(extruded_mesh, curve_data):
    
    main_curve = curve_data.get_curve()
    
    bpy.data.objects.remove(extruded_mesh, do_unlink=True)
    
    bpy.ops.object.select_all(action='DESELECT') 
    main_curve.select_set(True)
    bpy.context.view_layer.objects.active = main_curve