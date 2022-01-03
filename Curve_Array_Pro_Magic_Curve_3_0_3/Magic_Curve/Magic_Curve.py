import bpy
import bmesh
import mathutils
import copy
import math
import collections

class CancelError(Exception):

    pass

def ShowMessageBox(title, message, icon):

    def draw(self, context):
        self.layout.label(text = message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

class Checker():

    def __object_checker(self):
        
        object = bpy.context.active_object
        
        if object == None:
            
            ShowMessageBox("Error","Select object", 'ERROR')
            
            raise CancelError

        if object.type != 'MESH':
            
            ShowMessageBox("Error","Object shoud be mesh", 'ERROR')
            
            raise CancelError  
    
    def __mode_checker(self):
            
        mode = bpy.context.active_object.mode
        
        if mode != 'EDIT':
            
            ShowMessageBox("Error","Go to Edit Mode", 'ERROR')
            
            raise CancelError
        
    def start_checker(self):
        
        self.__object_checker
        self.__mode_checker
            
ckecker = Checker()

class Cyclic_Curve():
    
    def __init__(self):
    
        self.cyclic = None
        
    def get(self):
                
        return self.cyclic
    
    def set(self, input):
        
        self.cyclic = input

cyclic_curve = Cyclic_Curve()

def active_vertex(bm):
    
    try:
        
        act_vert_index = bm.select_history.active.index
        
        return act_vert_index

    except:
        
        ShowMessageBox("Error","The active vertex must be selected", 'ERROR')
        
        raise CancelError
  
def selected_edges(active_mesh):
    
    selected_edges_list = []
    
    for i in active_mesh.edges:
        
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
            
            if i.vertices[0] == searched_vertex: 
                
                return i, i.vertices[1]
            
            elif i.vertices[1] == searched_vertex:
                
                return i, i.vertices[0]
                
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
    
def create_curve(vertices_line_list, active_object, active_mesh):
    
    def cyclic_check(vertices_line_list):
        
        if vertices_line_list[0] == vertices_line_list[-1]:
            
            vertices_line_list.pop(-1)
            
            cyclic_curve.set(True)
            
            return True
        
        else:
            
            return False
    
    crv_mesh = bpy.data.curves.new('MgCrv_curve', 'CURVE')
    crv_mesh.dimensions = '3D'
    crv_mesh.twist_mode = 'MINIMUM'        
    spline = crv_mesh.splines.new(type='POLY')
    
    if cyclic_check(vertices_line_list) == True:
        
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
            
            deque_list = collections.deque(extruded_mesh_vertices_list)         
            deque_list.extend([deque_list.popleft()])
            
            extruded_mesh_vertices_list = list(deque_list)

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
        
        print('VERTEX:', i)
        print('vec_extruded_mesh', vec_extruded_mesh)
        print('vec_active_mesh', vec_active_mesh)
        print('vec_direction', vec_direction)
        
        projection = vec_active_mesh.project(vec_direction)
        correct_vec_active_mesh = vec_active_mesh - projection
        
        projection = vec_extruded_mesh.project(vec_direction)
        correct_vec_extruded_mesh = vec_extruded_mesh - projection
                
        angle = correct_vec_extruded_mesh.angle(correct_vec_active_mesh)
        
        cross_vector = vec_direction.cross(correct_vec_extruded_mesh)
        
        print('correct_vec_active_mesh', correct_vec_active_mesh)
        print('correct_vec_extruded_mesh', correct_vec_extruded_mesh)
        print('cross_vector', cross_vector)
                
        angle = angle_correction(angle, cross_vector, vec_active_mesh)
                
        angle_list.append(angle)
        
        i += 1
    print('angle_list', angle_list)
    return angle_list
    
def tilt_correction(angle_list, main_curve):
    
    i = 0
    
    spline = main_curve.data.splines[0]
    
    while i < len(angle_list):
        
        spline.bezier_points[i].tilt = angle_list[i]
        
        i += 1
    
def manager_mgcrv():

    active_object = bpy.context.active_object
    active_mesh = active_object.data

    ckecker.start_checker
        
    bm = bmesh.from_edit_mesh(active_mesh)
    
    act_vert_index = active_vertex(bm)
    
    bpy.ops.object.editmode_toggle()

    selected_edges_list = selected_edges(active_mesh)
    
    vertices_line_list = vertices_line(selected_edges_list, act_vert_index)
            
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
            
def main():
    
    try:
        
        manager_mgcrv()
    
    except CancelError:
        
        return {'CANCELLED'}

    # except Exception as e:
        
    #     ShowMessageBox("Unkown Error", "Please send me this report:", e, 'ERROR')
        
    #     return {'CANCELLED'}

main()