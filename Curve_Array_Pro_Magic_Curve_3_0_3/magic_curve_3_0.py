bl_info = {
    "name":"Magic Curve",
    "author":"JobWeek",
    "version":(1, 2),
    "blender":(3, 0, 0),
    "location":"View3d > Tool",
    "warning":"",
    "wiki_url":"",
    "category":"3D View"
}

import bpy
import bmesh
import mathutils
import math

def Direction(vec_spline, vec_mesh):
    
    scalar  = vec_spline[0]*vec_mesh[0] + vec_spline[1]*vec_mesh[1] + vec_spline[2]*vec_mesh[2]
    
    if scalar > 0:
        
        direction = True
        
    elif scalar < 0:
        
        direction = False
        
    elif scalar == 0:
    
        direction = None
        
    return direction

def CreateShape():
    
    active_scene = bpy.context.scene
    active_object = bpy.context.active_object
    active_mesh = active_object.data
        
    crv_mesh = bpy.data.curves.new('MgCrv_shape', 'CURVE')
    crv_mesh.dimensions = '3D'      
    shape = crv_mesh.splines.new(type='POLY')
    shape.points.add(2)  

    shape.points[0].co[0] = -0.5
    shape.points[0].co[1] = 0
    shape.points[0].co[2] = 0  
    
    shape.points[1].co[0] = 0
    shape.points[1].co[1] = 0
    shape.points[1].co[2] = 0  
    
    shape.points[2].co[0] = 0.5
    shape.points[2].co[1] = 0
    shape.points[2].co[2] = 0  
    
    crv_obj = bpy.data.objects.new('MgCrv_shape', crv_mesh)
    
    bpy.context.scene.collection.objects.link(crv_obj)
    
    return crv_obj

def Tilt(spline, mesh_vertex_index, curve_duplicate):
    
    active_scene = bpy.context.scene
    active_object = bpy.context.active_object
    active_mesh = active_object.data
    
    i = 0
    
    while i < len(spline.bezier_points):
        
        vec_spline = curve_duplicate.data.vertices[1 + i * 3].normal
        
        vec_tilt = mathutils.Vector((curve_duplicate.data.vertices[2 + i * 3].co[0] - curve_duplicate.data.vertices[1 + i * 3].co[0], curve_duplicate.data.vertices[2 + i * 3].co[1] - curve_duplicate.data.vertices[1 + i * 3].co[1],curve_duplicate.data.vertices[2 + i * 3].co[2] - curve_duplicate.data.vertices[1 + i * 3].co[2]))
        
        vec_mesh = active_mesh.vertices[mesh_vertex_index[i]].normal
        
        angle = vec_spline.angle(vec_mesh)
        
        direction = Direction(vec_tilt, vec_mesh)
        
        if direction == True:
                    
            spline.bezier_points[i].tilt = angle
            
            #print("True")
            
        elif direction == False:
            
            spline.bezier_points[i].tilt = angle * (-1)
            
            #print("False")
            
        elif direction == None:
            
            spline.bezier_points[i].tilt = 0           
        
        #print("Mesh_vertex:", mesh_vertex_index[i])
        
        #print("Vec_spline:", vec_spline)
        
        #print("Vec_mesh:", vec_mesh)
        
        #print("Angle:", angle)

        i += 1
    
    return 

def VecSpline(spline_point):
    
    vec_spline = mathutils.Vector((spline_point.handle_right[0]-spline_point.handle_left[0],spline_point.handle_right[1]-spline_point.handle_left[1],spline_point.handle_right[2]-spline_point.handle_left[2]))
    
    return vec_spline

def CreateCyclicCruve(sel_ed, act_vert_index, w):
          
    active_scene = bpy.context.scene
    active_object = bpy.context.active_object
    active_mesh = active_object.data
    count_edge = len(sel_ed)
    mesh_vertex_index = []
        
    crv_mesh = bpy.data.curves.new('MgCrv_curve', 'CURVE')
    crv_mesh.dimensions = '3D'
    crv_mesh.twist_mode = 'MINIMUM'        
    spline = crv_mesh.splines.new(type='POLY')
    spline.points.add(count_edge - 1) 
     
    spline.use_cyclic_u = True
        
    spline.points[-1].co[0] = active_mesh.vertices[act_vert_index].co[0]
    spline.points[-1].co[1] = active_mesh.vertices[act_vert_index].co[1]
    spline.points[-1].co[2] = active_mesh.vertices[act_vert_index].co[2]
    spline.points[-1].co[3] = w 
    mesh_vertex_index.append(act_vert_index)
  
        
    i = 0
        
    ser_vertex = act_vert_index
        
    while i <= count_edge - 2:
            
        next_vert, index_edge = SearchVertex(ser_vertex, sel_ed)
            
        del sel_ed[index_edge]
            
        spline.points[i].co[0] = active_mesh.vertices[next_vert].co[0]
        spline.points[i].co[1] = active_mesh.vertices[next_vert].co[1]
        spline.points[i].co[2] = active_mesh.vertices[next_vert].co[2]
        spline.points[i].co[3] = w
        mesh_vertex_index.append(next_vert)    
        
        ser_vertex = next_vert       
            
        i += 1

    crv_obj = bpy.data.objects.new('MgCrv_curve', crv_mesh)
        
    crv_obj.location = active_object.location
        
    crv_obj.rotation_euler = active_object.rotation_euler
        
    crv_obj.scale = active_object.scale
  
    bpy.context.scene.collection.objects.link(crv_obj)
    
    spline.type = 'BEZIER'
    
    return spline, mesh_vertex_index, crv_obj

def CreateCruve(sel_ed, act_vert_index, w):
          
    active_scene = bpy.context.scene
    active_object = bpy.context.active_object
    active_mesh = active_object.data
    count_edge = len(sel_ed)
    mesh_vertex_index = []
        
    crv_mesh = bpy.data.curves.new('MgCrv_curve', 'CURVE')
    crv_mesh.dimensions = '3D'
    crv_mesh.twist_mode = 'MINIMUM'        
    spline = crv_mesh.splines.new(type='POLY')
    spline.points.add(count_edge) 
                        
    spline.points[0].co[0] = active_mesh.vertices[act_vert_index].co[0]
    spline.points[0].co[1] = active_mesh.vertices[act_vert_index].co[1]
    spline.points[0].co[2] = active_mesh.vertices[act_vert_index].co[2]
    spline.points[0].co[3] = w 
    mesh_vertex_index.append(act_vert_index)
  
        
    i = 1
        
    ser_vertex = act_vert_index
        
    while i <= count_edge:
            
        next_vert, index_edge = SearchVertex(ser_vertex, sel_ed)
            
        del sel_ed[index_edge]
            
        spline.points[i].co[0] = active_mesh.vertices[next_vert].co[0]
        spline.points[i].co[1] = active_mesh.vertices[next_vert].co[1]
        spline.points[i].co[2] = active_mesh.vertices[next_vert].co[2]
        spline.points[i].co[3] = w
        mesh_vertex_index.append(next_vert)    
        
        ser_vertex = next_vert       
            
        i += 1

    crv_obj = bpy.data.objects.new('MgCrv_curve', crv_mesh)
        
    crv_obj.location = active_object.location
        
    crv_obj.rotation_euler = active_object.rotation_euler
        
    crv_obj.scale = active_object.scale
  
    bpy.context.scene.collection.objects.link(crv_obj)
    
    spline.type = 'BEZIER'
    
    return spline, mesh_vertex_index, crv_obj

def DuplicateCurve(sel_ed, spline, shape):
          
    active_scene = bpy.context.scene
    active_object = bpy.context.active_object
    active_mesh = active_object.data
    count_vert = len(spline.bezier_points)
        
    crv_mesh = bpy.data.curves.new('MgCrv_duplicate', 'CURVE')
    crv_mesh.dimensions = '3D'
    crv_mesh.twist_mode = 'MINIMUM'        
    duplicate = crv_mesh.splines.new(type='POLY')
    duplicate.points.add(count_vert - 1) 
    crv_mesh.bevel_mode = 'OBJECT'
    crv_mesh.bevel_object = shape
           
    duplicate.use_cyclic_u = spline.use_cyclic_u
        
    i = 0
    
    while i < count_vert:
        
        duplicate.points[i].co = (spline.bezier_points[i].co[0], spline.bezier_points[i].co[1], spline.bezier_points[i].co[2], spline.bezier_points[i].weight_softbody)
                
        i +=1

    crv_obj = bpy.data.objects.new('MgCrv_duplicate', crv_mesh)
        
    crv_obj.location = active_object.location
        
    crv_obj.rotation_euler = active_object.rotation_euler
        
    crv_obj.scale = active_object.scale
  
    bpy.context.scene.collection.objects.link(crv_obj)
    
    duplicate.type = 'BEZIER'
    
    crv_mesh_name = crv_mesh.name
    
    bpy.ops.object.select_all(action='DESELECT')
    crv_obj.select_set(True)
    bpy.context.view_layer.objects.active =  crv_obj
    
    bpy.ops.object.convert(target='MESH')
    
    bpy.ops.object.select_all(action='DESELECT')
    active_object.select_set(True)
    bpy.context.view_layer.objects.active = active_object
    
    bpy.data.curves.remove(bpy.data.curves[crv_mesh_name])
    
    return crv_obj

def LoopCheck(sel_ed, act_vert_index):
    
    count_edge = len(sel_ed)
    
    i = 0
        
    m = 0
        
    while i < count_edge:
            
        if sel_ed[i].vertices[0] == act_vert_index or sel_ed[i].vertices[1] == act_vert_index:
            
            m += 1
            
        i += 1
            
    if m == 2:
            
        o = 1
            
    else:
            
        o = 0    
    
    return o

def CreateVector(ser_vertex, next_vert):
    
    mesh_vert = bpy.context.active_object.data.vertices
    
    x_cord = mesh_vert[next_vert].co[0]-mesh_vert[ser_vertex].co[0]
    
    y_cord = mesh_vert[next_vert].co[1]-mesh_vert[ser_vertex].co[1]
    
    z_cord = mesh_vert[next_vert].co[2]-mesh_vert[ser_vertex].co[2]
    
    vec = mathutils.Vector((x_cord, y_cord, z_cord))
    
    return vec

def SearchVertex(ser_vertex, sel_ed):
    
    #print("PRISHLO:", "ser_vertex", ser_vertex)
    #print("PRISHLO:", "sel_ed", sel_ed)
    
    i = 0
    
    yslovie = False
    
    next_vert = None
    
    index_edge = None
    
    while i < len(sel_ed) and yslovie == False:
        
        if sel_ed[i].vertices[0] == ser_vertex or sel_ed[i].vertices[1] == ser_vertex:
            
            yslovie = True
            #print("SRABOTALO:", "sel_ed.index", sel_ed[i].index)
            #print("SRABOTALO:", "sel_ed.i", i)
            #print("SRABOTALO:", "vertex 0", sel_ed[i].vertices[0])
            #print("SRABOTALO:", "vertex 1", sel_ed[i].vertices[1])
            index_edge = i
            
            if sel_ed[i].vertices[0] == ser_vertex:
                
                next_vert = sel_ed[i].vertices[1]
                
            else:
                
                next_vert = sel_ed[i].vertices[0]
        
        i += 1    
        
    #print("VISHLO:", "next_vert", next_vert)
    #print("VISHLO:", "index_edge", index_edge)
    
    return next_vert, index_edge

def ShowMessageBox(title, message, icon):

    def draw(self, context):
        self.layout.label(text = message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

class MAGICCURVE_OT_mgcrv_main(bpy.types.Operator):
    '''Clear selected curve'''
    bl_label = "Curve from loop"
    bl_idname = 'magiccurve.mgcrv_main'
    bl_options = {'REGISTER', 'UNDO'}
        
    def execute(self,context):
        
        active_scene = bpy.context.scene
        active_object = bpy.context.active_object
        active_mesh = active_object.data

        try:

            bm = bmesh.from_edit_mesh(active_mesh)
        
        except:
            
            ShowMessageBox("Error","Go to edit mode", 'ERROR')
            
            return {'CANCELLED'}

        try:
                
            act_vert_index = bm.select_history.active.index

        except:
            
            ShowMessageBox("Error","Select at least one edge, and pick active point", 'ERROR')
            
            return {'CANCELLED'}
        
        bpy.ops.object.editmode_toggle()
        
        #get edges
        sel_ed = list(filter(lambda i: i.select, active_mesh.edges))    
        mesh_edges = sel_ed 
        count_edge = len(sel_ed)
                       
        #create curve
        w = 1
        
        o = LoopCheck(sel_ed, act_vert_index)
        
        try:

            if o == 0:

                spline, mesh_vertex_index, crv_obj = CreateCruve(sel_ed, act_vert_index, w)

            else:

                spline, mesh_vertex_index, crv_obj = CreateCyclicCruve(sel_ed, act_vert_index, w)

        except:
            
            ShowMessageBox("Error","Select only one loop, or a line segment from connected edges, without intersection, and activate start point at one end", 'ERROR')
            
            return {'CANCELLED'}        
                
        shape = CreateShape()
        
        curve_duplicate = DuplicateCurve(sel_ed, spline, shape)
        
        #Tilt correction        
        
        try:
            
            Tilt(spline, mesh_vertex_index, curve_duplicate)

        except:
            
            ShowMessageBox("Error","Select minimum 2 vertex", 'ERROR')
            
            return {'CANCELLED'}      
        
        bpy.data.meshes.remove(curve_duplicate.data)
        bpy.data.curves.remove(shape.data)       
        bpy.ops.object.select_all(action='DESELECT') 
        crv_obj.select_set(True)
        bpy.context.view_layer.objects.active = crv_obj
        return {'FINISHED'}

class MAGICCURVE_PT_mgcrv_panel(bpy.types.Panel):
    bl_label = "Magic Curve"
    bl_idname = "MAGICCURVE_PT_mgcrv_panel"
    bl_space_type = 'VIEW_3D' 
    bl_region_type = 'UI'
    bl_category = 'CrvArrPro' 
    
    def draw(self, context):
               
        active_scene = bpy.context.scene
                
        layout = self.layout
                    
        row = layout.row()
        row.operator('magiccurve.mgcrv_main', icon = 'TRACKING')

def register():
    bpy.utils.register_class(MAGICCURVE_PT_mgcrv_panel)
    bpy.utils.register_class(MAGICCURVE_OT_mgcrv_main)
    
    #bpy.types.Scene.curve_array_propeties = bpy.props.PointerProperty(type=Properties)

def unregister():
    bpy.utils.unregister_class(MAGICCURVE_PT_mgcrv_panel)
    bpy.utils.unregister_class(MAGICCURVE_OT_mgcrv_main)
    
    #del bpy.types.Scene.my_props
    
if __name__== "__main__" :
    register()