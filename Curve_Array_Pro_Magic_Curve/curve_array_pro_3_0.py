import bpy
import bmesh
import mathutils
import math
import numpy
import inspect
import time

from .array_panels.header_panel import (
CRVARRPRO_PT_CurveArrayPro
)

from .array_panels.curve_panel import (
CRVARRPRO_PT_CurvePanel
)

from .array_panels.object_panel import (
CRVARRPRO_PT_ObjectPanel
)

from .array_panels.main_panel import (
CRVARRPRO_PT_MainPanel
)

from .array_panels.button_panel import (
CRVARRPRO_PT_ButtonPanel
)

from .object_editor.object_editor_ops import (
CRVARRPRO_OT_ClearProp,
CRVARRPRO_OT_DownProp,
CRVARRPRO_OT_ObjectEditor,
CRVARRPRO_OT_UpProp,
CRVARRPRO_OT_NewRandomGroup,
CRVARRPRO_OT_SetGroup,
CRVARRPRO_OT_RemoveObjFromRG,
CRVARRPRO_OT_Empty
)

from .trasform_editor.transform_editor_ops import (
CRVARRPRO_OT_TransformEditor
)

from .object_picker_cleaner.object_picker_cleaner_ops import (
CRVARRPRO_OT_ObjectPicker,
CRVARRPRO_OT_ObjectCleaner
)

from .curve_picker_cleaner.curve_picker_cleaner_ops import (
CRVARRPRO_OT_CurvePicker,
CRVARRPRO_OT_CurveCleaner
)

from .engine.functions import (
object_list,
Size_Ofset,
Last_Obj,
transform_editor
)

from .button_ops.last_array import (
CRVARRPRO_OT_Delete_Last_Array
)

from .button_ops.reset_settings import (
CRVARRPRO_OT_Reset_Settings
)

from .button_ops.flip_curve import (
CRVARRPRO_OT_Flip_Curve
)

obj_list_scene = None

def Align_Rotation(face, i_obj, obj, plane_nrml, rail_axis):

    vx_0_x = face.verts[0].co[0]
    vx_0_y = face.verts[0].co[1]
    vx_0_z = face.verts[0].co[2]                        
    vx_1_x = face.verts[1].co[0]
    vx_1_y = face.verts[1].co[1]
    vx_1_z = face.verts[1].co[2]                        
    vx_2_x = face.verts[3].co[0] 
    vx_2_y = face.verts[3].co[1] 
    vx_2_z = face.verts[3].co[2]

    i_plane_vec_x =  mathutils.Vector(((vx_1_x - vx_0_x), (vx_1_y - vx_0_y), (vx_1_z - vx_0_z)))
    i_plane_vec_x.normalize()
    i_plane_vec_y = mathutils.Vector(((vx_2_x - vx_0_x), (vx_2_y - vx_0_y), (vx_2_z - vx_0_z)))
    i_plane_vec_y.normalize()
    i_plane_vec_z = plane_nrml

    rot_mat = mathutils.Matrix.Rotation(0, 3, 'X')

    #print('VERT 1:', face.verts[0].co, 'VERT 2:', face.verts[1].co, 'VERT 3:', face.verts[2].co, 'NRML:', i_plane_vec_z)

    if rail_axis == "+z":

        rot_mat[0] = i_plane_vec_x   
        rot_mat[1] = i_plane_vec_y 
        rot_mat[2] = i_plane_vec_z 
    
    elif rail_axis == "-z":
    
        rot_mat[0] = i_plane_vec_x  
        rot_mat[1] = i_plane_vec_y * (-1) 
        rot_mat[2] = i_plane_vec_z * (-1) 
    
    elif rail_axis == "+x":
        
        rot_mat[0] = i_plane_vec_z   
        rot_mat[1] = i_plane_vec_x 
        rot_mat[2] = i_plane_vec_y
    
    elif rail_axis == "-x":
        
        rot_mat[0] = i_plane_vec_z * (-1)  
        rot_mat[1] = i_plane_vec_x * (-1)
        rot_mat[2] = i_plane_vec_y
    
    elif rail_axis == "+y":
        
        rot_mat[0] = i_plane_vec_x * (-1) 
        rot_mat[1] = i_plane_vec_z 
        rot_mat[2] = i_plane_vec_y
    
    elif rail_axis == "-y":
        
        rot_mat[0] = i_plane_vec_x
        rot_mat[1] = i_plane_vec_z * (-1) 
        rot_mat[2] = i_plane_vec_y 

    rot_mat_inverted = rot_mat.inverted() 
    rot_euler = rot_mat_inverted.to_euler('XYZ')

    i_obj.rotation_euler = rot_euler
    i_obj.rotation_euler.rotate_axis('Z', obj.rotation_euler[2])
    i_obj.rotation_euler.rotate_axis('Y', obj.rotation_euler[1]) 
    i_obj.rotation_euler.rotate_axis('X', obj.rotation_euler[0])

def Align_Rotation_2(i_obj, obj, plane_nrml, rail_axis , vx_0, vx_1, vx_2):

    #print('GET', vx_0, vx_1, vx_2)

    vx_0_x = vx_0[0]
    vx_0_y = vx_0[1]
    vx_0_z = vx_0[2]                        
    vx_1_x = vx_1[0]
    vx_1_y = vx_1[1]
    vx_1_z = vx_1[2]                        
    vx_2_x = vx_2[0] 
    vx_2_y = vx_2[1] 
    vx_2_z = vx_2[2]

    i_plane_vec_x =  mathutils.Vector(((vx_1_x - vx_0_x), (vx_1_y - vx_0_y), (vx_1_z - vx_0_z)))
    i_plane_vec_x.normalize()
    i_plane_vec_y = mathutils.Vector(((vx_2_x - vx_0_x), (vx_2_y - vx_0_y), (vx_2_z - vx_0_z)))
    i_plane_vec_y.normalize()
    i_plane_vec_z = mathutils.Vector(plane_nrml)
    #i_plane_vec_z.normalize()

    rot_mat = mathutils.Matrix.Rotation(0, 3, 'X')

    #print('VEC X:', i_plane_vec_x, 'VEC Y:', i_plane_vec_y, 'VEC Z:', i_plane_vec_z)

    if rail_axis == "+z":

        rot_mat[0] = i_plane_vec_x   
        rot_mat[1] = i_plane_vec_y 
        rot_mat[2] = i_plane_vec_z 
    
    elif rail_axis == "-z":
    
        rot_mat[0] = i_plane_vec_x  
        rot_mat[1] = i_plane_vec_y * (-1) 
        rot_mat[2] = i_plane_vec_z * (-1) 
    
    elif rail_axis == "+x":
        
        rot_mat[0] = i_plane_vec_z   
        rot_mat[1] = i_plane_vec_x 
        rot_mat[2] = i_plane_vec_y
    
    elif rail_axis == "-x":
        print('VEC Z',i_plane_vec_z)
        rot_mat[0] = i_plane_vec_z * (-1)  
        rot_mat[1] = i_plane_vec_x * (-1)
        rot_mat[2] = i_plane_vec_y
    
    elif rail_axis == "+y":
        
        rot_mat[0] = i_plane_vec_x * (-1) 
        rot_mat[1] = i_plane_vec_z 
        rot_mat[2] = i_plane_vec_y
    
    elif rail_axis == "-y":
        
        rot_mat[0] = i_plane_vec_x
        print('VEC Z',i_plane_vec_z)
        rot_mat[1] = i_plane_vec_z * (-1) 
        rot_mat[2] = i_plane_vec_y 
    #print(rot_mat)
    rot_mat_inverted = rot_mat.inverted() 
    rot_euler = rot_mat_inverted.to_euler('XYZ')
    #print('ROT EULER', rot_euler)

    i_obj.rotation_euler = rot_euler
    i_obj.rotation_euler.rotate_axis('Z', obj.rotation_euler[2])
    i_obj.rotation_euler.rotate_axis('Y', obj.rotation_euler[1]) 
    i_obj.rotation_euler.rotate_axis('X', obj.rotation_euler[0])

def Get_Obj(obj_list, obj_list_len, i):

    try:
        
        obj = obj_list[i][0]
        ghost = obj_list[i][1]
        ghost_p = obj_list[i][2]

    except:

        new_i = int(math.fmod(i, obj_list_len))
        obj = obj_list[new_i][0]
        ghost = obj_list[new_i][1]
        ghost_p = obj_list[new_i][2]

    if type(obj) is list:

        obj = Random_Obj(obj, i)

    return obj, ghost, ghost_p

def Random_Obj(obj_list,i):

    seed = bpy.context.scene.curve_array_properties.other_props.array_settings.counter
    numpy.random.seed(seed + i*seed)

    objects = obj_list[0]
    chances = obj_list[1]

    obj = numpy.random.choice(objects, p = chances)

    return obj

def Search_Parent_Instance(obj, i_obj, main_col):

    for i in obj.children:

        i_child = i.copy()
        i_child.animation_data_clear()
        i_child.name = (i.name + "_instance.001") 

        main_col.objects.link(i_child)
        i_child.scale = i.scale

        i_child.parent = i_obj
        i_child.matrix_parent_inverse = i.matrix_parent_inverse

        Search_Parent_Copy(i, i_child, main_col)

def Search_Parent_Copy(obj, i_obj, main_col):

    for i in obj.children:

        i_child = i.copy()
        i_child.data = i.data.copy()
        i_child.animation_data_clear()
        i_child.name = (i.name + "_copy.001") 

        main_col.objects.link(i_child)
        i_child.parent = i_obj
        i_child.matrix_parent_inverse = i.matrix_parent_inverse

        Search_Parent_Copy(i, i_child, main_col)

def Cloning_Type(obj, cl_type, main_col, i, parent, ysl_ghost, ghost_col, ghost, ghost_p):

    if parent == True:

        if cl_type == 'OP1':

            i_obj = obj.copy()
            i_obj.data = obj.data.copy()
            i_obj.animation_data_clear()
            i_obj.name = (obj.name + "_copy.001") 

            if ghost == True:

                objects = [main_col, ghost_col]
                chances = [1-ghost_p, ghost_p]

                main_col = numpy.random.choice(objects, p = chances)

            Search_Parent_Copy(obj, i_obj, main_col)

            main_col.objects.link(i_obj)
            i_obj.scale = obj.scale

        else:

            i_obj = obj.copy()
            i_obj.animation_data_clear()
            i_obj.name = (obj.name + "_instance.001") 

            if ghost == True:

                objects = [main_col, ghost_col]
                chances = [1-ghost_p, ghost_p]

                main_col = numpy.random.choice(objects, p = chances)

            Search_Parent_Instance(obj, i_obj, main_col)

            main_col.objects.link(i_obj)
            i_obj.scale = obj.scale

    else:

        if cl_type == 'OP1':

            i_obj = obj.copy()
            i_obj.data = obj.data.copy()
            i_obj.animation_data_clear()
            i_obj.name = (obj.name + "_copy.001") 

            if ghost == True:

                objects = [main_col, ghost_col]
                chances = [1-ghost_p, ghost_p]

                main_col = numpy.random.choice(objects, p = chances)

            main_col.objects.link(i_obj)
            i_obj.scale = obj.scale

        elif cl_type == 'OP2':

            i_obj = obj.copy()
            i_obj.animation_data_clear()
            i_obj.name = (obj.name + "_instance.001")     

            if ghost == True:

                objects = [main_col, ghost_col]
                chances = [1-ghost_p, ghost_p]

                main_col = numpy.random.choice(objects, p = chances)

            main_col.objects.link(i_obj)
            i_obj.scale = obj.scale

        else:

            i_obj = bpy.data.objects.new((obj.name + "_instance.001"), obj.data)

            if ghost == True:

                objects = [main_col, ghost_col]
                chances = [1-ghost_p, ghost_p]

                main_col = numpy.random.choice(objects, p = chances)

            main_col.objects.link(i_obj)
            i_obj.scale = obj.scale

    return i_obj

def main_collection(obj_list, obj_list_len, obj, ysl_ghost):

    ins_col = bpy.data.collections.new("CurveArray Objects")

    if obj_list_len == 1 and type(obj) is not list:

        obj_old_col = obj.users_collection
        obj_col = obj_old_col[0].name

        if obj_col == 'Scene Collection':
                    
            bpy.context.scene.collection.children.link(ins_col)
                        
        else:
                                                
            bpy.data.collections.get(obj_col).children.link(ins_col) 

    else:

        bpy.context.scene.collection.children.link(ins_col)

    if ysl_ghost == True:

        ghost_col = bpy.data.collections.new("Ghost Objects")
        ins_col.children.link(ghost_col)

    else:

        ghost_col = None

    return ins_col, ghost_col

def loc_translate(obj, vec_tr):

    if vec_tr == (0,0,0):

        return

    vec = mathutils.Vector(vec_tr)

    if obj.parent is None:

        inv = obj.matrix_basis.copy()

    else:
        
        inv = obj.parent.matrix_world.copy() @ (obj.matrix_parent_inverse.copy() @ obj.matrix_basis.copy())
    obj.matrix_world = inv
    inv.invert()
    vec_rot = vec @ inv
    obj.location = obj.location + vec_rot

def i_plane_loc_normal(i_plane):

    depsgraph = bpy.context.evaluated_depsgraph_get()
    bm = bmesh.new()
    bm.from_object(i_plane, depsgraph)

    mat_rot = i_plane.rotation_euler.to_matrix()
    bmesh.ops.rotate(bm, cent = (0,0,0), matrix = mat_rot, verts=bm.verts)
    bm.verts.ensure_lookup_table()
    bmesh.ops.translate(bm, vec = i_plane.location, verts=bm.verts)

    bm.faces.ensure_lookup_table()
    f = bm.faces[0]
    loc = f.calc_center_median()
    nrml = f.normal

    bm.free()
    return loc, nrml, f

def i_plane_loc_normal_2(i_plane):

    depsgraph = bpy.context.evaluated_depsgraph_get()

    bm = bmesh.new()
    bm.from_object(i_plane, depsgraph)

    mat_rot = i_plane.rotation_euler.to_matrix()
    bmesh.ops.rotate(bm, cent = (0,0,0), matrix = mat_rot, verts=bm.verts)
    bm.verts.ensure_lookup_table()
    bmesh.ops.translate(bm, vec = i_plane.location, verts=bm.verts)

    bm.faces.ensure_lookup_table()

    f = bm.faces[0]
    loc = f.calc_center_median()

    vx_0 = [f.verts[0].co[0], f.verts[0].co[1], f.verts[0].co[2]]
    vx_1 = [f.verts[1].co[0], f.verts[1].co[1], f.verts[1].co[2]]
    vx_2 = [f.verts[3].co[0], f.verts[3].co[1], f.verts[3].co[2]]

    nrml = [f.normal[0], f.normal[1], f.normal[2]]

    bm.free()

    return loc, nrml, vx_0, vx_1, vx_2

def I_plane(path):

    new_vertices = [
    (-0.1, -0.1, 0), 
    (0.1, -0.1, 0),
    (-0.1, 0.1, 0),
    (0.1, 0.1, 0)
    ]
    new_edges = [(0,1),(0,2),(2,3),(1,3)]
    new_faces = [(0,1,3,2)]
    new_mesh = bpy.data.meshes.new('i_plane')
    new_mesh.from_pydata(new_vertices, new_edges, new_faces)
    new_mesh.update()
    i_plane = bpy.data.objects.new('i_plane', new_mesh)
    bpy.context.scene.collection.objects.link(i_plane)

    i_plane.location = path.location
    i_plane.rotation_euler = path.rotation_euler

    mod_curve = i_plane.modifiers.new(name="Curve", type='CURVE')
    mod_curve.object = path
    mod_curve.deform_axis = "POS_Z" 

    return i_plane

def I_plane_Count(path, count, ofset_z):

    new_vertices = [
    (-0.1, -0.1, 0), 
    (0.1, -0.1, 0),
    (-0.1, 0.1, 0),
    (0.1, 0.1, 0)
    ]
    new_edges = [(0,1),(0,2),(2,3),(1,3)]
    new_faces = [(0,1,3,2)]
    new_mesh = bpy.data.meshes.new('i_plane')
    new_mesh.from_pydata(new_vertices, new_edges, new_faces)
    new_mesh.update()
    i_plane = bpy.data.objects.new('i_plane', new_mesh)
    bpy.context.scene.collection.objects.link(i_plane)

    i_plane.location = path.location
    i_plane.rotation_euler = path.rotation_euler

    mod_array = i_plane.modifiers.new(name="Array", type='ARRAY')
    mod_array.use_relative_offset = False
    mod_array.use_constant_offset = True
    mod_array.constant_offset_displace[0] = 0
    mod_array.constant_offset_displace[1] = 0
    mod_array.constant_offset_displace[2] = ofset_z

    mod_curve = i_plane.modifiers.new(name="Curve", type='CURVE')
    mod_curve.object = path
    mod_curve.deform_axis = "POS_Z" 
    mod_array.count = count
    
    return i_plane

def update_func(self, context):

    object_list.update()

def update_transform(self, context):

    transform_editor.update()

def PrintAll():

    active_scene = bpy.context.scene
    my_props = active_scene.curve_array_properties.object_props

    for i in range(20):

        strind = 'obj_stor_' + str(i)
        direct = getattr(my_props.object_storage, strind)
        print('OBJECT STORAGE ' + str(i), getattr(direct, 'obj_name'))

    for i in range(20):

        strind = 'obj_stor_draw_' + str(i)
        print('OBJECT STORAGE DRAW ' + str(i), getattr(my_props.object_storage_draw, strind))

    for i in range(20):

        strind = 'edit_stor_' + str(i)
        direct = getattr(my_props.editor_storage, strind)
        print('EDITOR STORAGE ' + str(i), getattr(direct, 'link'))

    for i in range(20):

        strind = 'edit_stor_draw_' + str(i)
        print('EDITOR STORAGE DRAW ' + str(i), getattr(my_props.editor_storage_draw, strind))

def CheckPar(obj):

    for i in bpy.data.objects:

        if i.parent == obj:

            return True

    return False

def LengthOfCurve(spline, crv):

    if crv.scale[0] != 1 or crv.scale[1] != 1 or crv.scale[2] != 1:

        dupl_crv = crv.copy()
        dupl_crv.data = crv.data.copy()
        dupl_crv.animation_data_clear()
        dupl_crv.data.transform(dupl_crv.matrix_world)
        dupl_crv.matrix_world = mathutils.Matrix()
        length = dupl_crv.data.splines[0].calc_length()
        bpy.data.curves.remove(dupl_crv.data)

    else:

        length = spline.calc_length()

    return length

def ShowMessageBox(title, message, icon):

    def draw(self, context):
        self.layout.label(text = message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

def Transform_Editor(
i_obj,     
i,
rotation_x,
rotation_y,
rotation_z,
location_x,
location_y,
location_z,
scale_x,
scale_y,
scale_z,
rotation_progressive_x,
rotation_progressive_y,
rotation_progressive_z,
rotation_min_x,
rotation_min_y,
rotation_min_z,
rotation_max_x,
rotation_max_y,
rotation_max_z,
location_progressive_x,
location_progressive_y,
location_progressive_z,
location_min_x,
location_min_y,
location_min_z,
location_max_x,
location_max_y,
location_max_z,
scale_progressive_x,
scale_progressive_y,
scale_progressive_z,
scale_min_x,
scale_min_y,
scale_min_z,
scale_max_x,
scale_max_y,
scale_max_z,
pr_loc_x,
pr_loc_y,
pr_loc_z,
pr_rot_x,
pr_rot_y,
pr_rot_z,
pr_scale_x,
pr_scale_y,
pr_scale_z,
):

    seed = bpy.context.scene.curve_array_properties.other_props.array_settings.counter
    numpy.random.seed(seed + i*seed)

    if location_x == True:

        pr_loc_x += location_progressive_x

        loc = numpy.random.uniform(location_min_x,location_max_x) + pr_loc_x

        loc_translate(i_obj, (loc, 0, 0))

    if location_y == True:

        pr_loc_y += location_progressive_y

        loc = numpy.random.uniform(location_min_y,location_max_y) + pr_loc_y

        loc_translate(i_obj, (0, loc, 0))

    if location_z == True:

        pr_loc_z += location_progressive_z

        loc = numpy.random.uniform(location_min_z,location_max_z) + pr_loc_z

        loc_translate(i_obj, (0, 0, loc))

    if scale_x == True:
        
        pr_scale_x += scale_progressive_x

        sc = numpy.random.uniform(scale_min_x,scale_max_x) + pr_scale_x + 1

        i_obj.scale[0] = i_obj.scale[0] * sc

    if scale_y == True:

        pr_scale_y += scale_progressive_y

        sc = numpy.random.uniform(scale_min_y,scale_max_y) + pr_scale_y + 1

        i_obj.scale[1] = i_obj.scale[1] * sc

    if scale_z == True:

        pr_scale_z += scale_progressive_z

        sc = numpy.random.uniform(scale_min_z,scale_max_z) + pr_scale_z + 1

        i_obj.scale[2] = i_obj.scale[2] * sc

    if rotation_z == True:

        pr_rot_z += rotation_progressive_z

        rot = numpy.random.uniform(rotation_min_z,rotation_max_z) + pr_rot_z

        i_obj.rotation_euler.rotate_axis('Z', math.radians(rot))

    if rotation_y == True:

        pr_rot_y += rotation_progressive_y

        rot = numpy.random.uniform(rotation_min_y,rotation_max_y) + pr_rot_y

        i_obj.rotation_euler.rotate_axis('Y', math.radians(rot))

    if rotation_x == True:

        pr_rot_x += rotation_progressive_x

        rot = numpy.random.uniform(rotation_min_x,rotation_max_x) + pr_rot_x

        i_obj.rotation_euler.rotate_axis('X', math.radians(rot))

    return pr_loc_x, pr_loc_y, pr_loc_z, pr_rot_x, pr_rot_y, pr_rot_z, pr_scale_x, pr_scale_y, pr_scale_z

def Count_Fill(
count,
crv_len,
cyclic,
znak,
size_ofset,
start_ofset, 
end_ofset, 
obj_list, 
obj_list_len, 
dimension_axis, 
path, 
cloning_type, 
slide, 
enable_parenting, 
align_rot, 
rail_axis,
rotation_x,
rotation_y,
rotation_z,
location_x,
location_y,
location_z,
scale_x,
scale_y,
scale_z,
rotation_progressive_x,
rotation_progressive_y,
rotation_progressive_z,
rotation_min_x,
rotation_min_y,
rotation_min_z,
rotation_max_x,
rotation_max_y,
rotation_max_z,
location_progressive_x,
location_progressive_y,
location_progressive_z,
location_min_x,
location_min_y,
location_min_z,
location_max_x,
location_max_y,
location_max_z,
scale_progressive_x,
scale_progressive_y,
scale_progressive_z,
scale_min_x,
scale_min_y,
scale_min_z,
scale_max_x,
scale_max_y,
scale_max_z,
global_transform,
ysl_ghost
):

    if cyclic == True:

        if size_ofset == True:

            first, _, _ = Get_Obj(obj_list, obj_list_len, 0)
            last, _, _ = Get_Obj(obj_list, obj_list_len, count - 1)
            first_of = Size_Ofset(first, dimension_axis, znak, True)
            last_of = Size_Ofset(last, dimension_axis, znak, False)
            sz_of = first_of + last_of
            length = crv_len - (start_ofset + end_ofset + sz_of) 
            main_col, ghost_col = main_collection(obj_list, obj_list_len, first, ysl_ghost)

        else:

            length = crv_len - (start_ofset + end_ofset) 
            first_of = start_ofset
            obj = obj_list[0][0]
            main_col, ghost_col = main_collection(obj_list, obj_list_len, obj, ysl_ghost)

        try:

            ofset = length/(count-1)

        except:

            ofset = 0            

    else:

        length = crv_len - (start_ofset + end_ofset) 
        first_of = start_ofset
        obj = obj_list[0][0]
        main_col, ghost_col = main_collection(obj_list, obj_list_len, obj, ysl_ghost)
        ofset = length/count

    i_plane = I_plane_Count(path, count, ofset)
    loc_translate(i_plane, (0,0,first_of+slide))
    depsgraph = bpy.context.evaluated_depsgraph_get()
    bm = bmesh.new()
    bm.from_object(i_plane, depsgraph)

    mat_rot = i_plane.rotation_euler.to_matrix()
    bmesh.ops.rotate(bm, cent = (0,0,0), matrix = mat_rot, verts=bm.verts)
    bm.verts.ensure_lookup_table()
    bmesh.ops.translate(bm, vec = i_plane.location, verts=bm.verts)
    bm.faces.ensure_lookup_table()

    pr_loc_x = 0.0
    pr_loc_y = 0.0
    pr_loc_z = 0.0
    pr_rot_x = 0.0
    pr_rot_y = 0.0
    pr_rot_z = 0.0
    pr_scale_x = 0.0
    pr_scale_y = 0.0
    pr_scale_z = 0.0

    for i in range(count):

        obj, ghost, ghost_p = Get_Obj(obj_list, obj_list_len, i)
        f = bm.faces[i]
        plane_loc = f.calc_center_median()
        plane_nrml = f.normal
        i_obj = Cloning_Type(obj, cloning_type, main_col, i, enable_parenting, ysl_ghost, ghost_col, ghost, ghost_p)
        i_obj.location = plane_loc        

        if align_rot == True:

            Align_Rotation(f, i_obj, obj, plane_nrml, rail_axis)

        if global_transform == True:

            pr_loc_x, pr_loc_y, pr_loc_z, pr_rot_x, pr_rot_y, pr_rot_z, pr_scale_x, pr_scale_y, pr_scale_z = Transform_Editor(
            i_obj,     
            i,
            rotation_x,
            rotation_y,
            rotation_z,
            location_x,
            location_y,
            location_z,
            scale_x,
            scale_y,
            scale_z,
            rotation_progressive_x,
            rotation_progressive_y,
            rotation_progressive_z,
            rotation_min_x,
            rotation_min_y,
            rotation_min_z,
            rotation_max_x,
            rotation_max_y,
            rotation_max_z,
            location_progressive_x,
            location_progressive_y,
            location_progressive_z,
            location_min_x,
            location_min_y,
            location_min_z,
            location_max_x,
            location_max_y,
            location_max_z,
            scale_progressive_x,
            scale_progressive_y,
            scale_progressive_z,
            scale_min_x,
            scale_min_y,
            scale_min_z,
            scale_max_x,
            scale_max_y,
            scale_max_z,
            pr_loc_x,
            pr_loc_y,
            pr_loc_z,
            pr_rot_x,
            pr_rot_y,
            pr_rot_z,
            pr_scale_x,
            pr_scale_y,
            pr_scale_z,
            )

    bm.free()
    bpy.data.meshes.remove(i_plane.data)
    bpy.context.scene.curve_array_properties.other_props.array_settings.last_array = main_col.name

def Constant_Fill(
obj_list, 
obj_list_len, 
dimension_axis, 
znak, 
start_ofset, 
end_ofset, 
crv_len, 
size_ofset, 
constant_ofset, 
path, 
slide, 
cloning_type, 
enable_parenting, 
align_rot, 
rail_axis,
rotation_x,
rotation_y,
rotation_z,
location_x,
location_y,
location_z,
scale_x,
scale_y,
scale_z,
rotation_progressive_x,
rotation_progressive_y,
rotation_progressive_z,
rotation_min_x,
rotation_min_y,
rotation_min_z,
rotation_max_x,
rotation_max_y,
rotation_max_z,
location_progressive_x,
location_progressive_y,
location_progressive_z,
location_min_x,
location_min_y,
location_min_z,
location_max_x,
location_max_y,
location_max_z,
scale_progressive_x,
scale_progressive_y,
scale_progressive_z,
scale_min_x,
scale_min_y,
scale_min_z,
scale_max_x,
scale_max_y,
scale_max_z,
global_transform,
ysl_ghost             
):

    i = 0
    i_plane =  I_plane(path)
    pr_loc_x = 0.0
    pr_loc_y = 0.0
    pr_loc_z = 0.0
    pr_rot_x = 0.0
    pr_rot_y = 0.0
    pr_rot_z = 0.0
    pr_scale_x = 0.0
    pr_scale_y = 0.0
    pr_scale_z = 0.0
    i_plane_list = []

    if size_ofset == True:

        first_obj, _, _ = Get_Obj(obj_list, obj_list_len, 0)
        first_ofset = Size_Ofset(first_obj, dimension_axis, znak, True)
        main_of = first_ofset
        main_len = crv_len - (start_ofset + end_ofset)
        loc_translate(i_plane, (0,0,first_ofset + slide + start_ofset))
        main_col, ghost_col = main_collection(obj_list, obj_list_len, first_obj, ysl_ghost)

    else:

        main_of = 0
        main_len = crv_len - (start_ofset + end_ofset)
        loc_translate(i_plane, (0,0,slide + start_ofset))
        obj, _, _ = Get_Obj(obj_list, obj_list_len, 0)
        main_col, ghost_col = main_collection(obj_list, obj_list_len, obj, ysl_ghost)

    if size_ofset == True:

        while True:

            obj, _, _ = Get_Obj(obj_list, obj_list_len, i)
            last_of = Size_Ofset(obj, dimension_axis, znak, False)
            plane_loc, plane_nrml, vx_0, vx_1, vx_2 = i_plane_loc_normal_2(i_plane)
            i_plane_list.append([plane_loc, plane_nrml, vx_0, vx_1, vx_2])

            main_of += constant_ofset
            if main_of >= (main_len - last_of):
                break

            i += 1
            loc_translate(i_plane, (0,0,constant_ofset))

    else:

        while True:

            plane_loc, plane_nrml, vx_0, vx_1, vx_2 = i_plane_loc_normal_2(i_plane)
            i_plane_list.append([plane_loc, plane_nrml, vx_0, vx_1, vx_2])

            main_of += constant_ofset
            if main_of >= main_len:
                break

            loc_translate(i_plane, (0,0,constant_ofset))

    bpy.data.meshes.remove(i_plane.data)
    bpy.context.scene.curve_array_properties.other_props.array_settings.last_array = main_col.name
    len_i_plane_list = len(i_plane_list)
    bpy.context.view_layer.update()

    for i in range(len_i_plane_list):

        obj, ghost, ghost_p = Get_Obj(obj_list, obj_list_len, i)
        i_obj = Cloning_Type(obj, cloning_type, main_col, i, enable_parenting, ysl_ghost, ghost_col, ghost, ghost_p)
        i_obj.location = i_plane_list[i][0]

        if align_rot == True:
            
            Align_Rotation_2(i_obj, obj, i_plane_list[i][1], rail_axis, i_plane_list[i][2], i_plane_list[i][3], i_plane_list[i][4])               

        if global_transform == True:

            pr_loc_x, pr_loc_y, pr_loc_z, pr_rot_x, pr_rot_y, pr_rot_z, pr_scale_x, pr_scale_y, pr_scale_z = Transform_Editor(
            i_obj,     
            i,
            rotation_x,
            rotation_y,
            rotation_z,
            location_x,
            location_y,
            location_z,
            scale_x,
            scale_y,
            scale_z,
            rotation_progressive_x,
            rotation_progressive_y,
            rotation_progressive_z,
            rotation_min_x,
            rotation_min_y,
            rotation_min_z,
            rotation_max_x,
            rotation_max_y,
            rotation_max_z,
            location_progressive_x,
            location_progressive_y,
            location_progressive_z,
            location_min_x,
            location_min_y,
            location_min_z,
            location_max_x,
            location_max_y,
            location_max_z,
            scale_progressive_x,
            scale_progressive_y,
            scale_progressive_z,
            scale_min_x,
            scale_min_y,
            scale_min_z,
            scale_max_x,
            scale_max_y,
            scale_max_z,
            pr_loc_x,
            pr_loc_y,
            pr_loc_z,
            pr_rot_x,
            pr_rot_y,
            pr_rot_z,
            pr_scale_x,
            pr_scale_y,
            pr_scale_z,
            )

        bpy.context.scene.curve_array_properties.other_props.array_settings.last_array = main_col.name

def Relative_Fill(
obj_list, 
obj_list_len, 
dimension_axis, 
znak,
start_ofset, 
end_ofset, 
crv_len, 
size_ofset, 
relative_ofset, 
path, 
slide, 
cloning_type, 
enable_parenting, 
align_rot, 
rail_axis,
rotation_x,
rotation_y,
rotation_z,
location_x,
location_y,
location_z,
scale_x,
scale_y,
scale_z,
rotation_progressive_x,
rotation_progressive_y,
rotation_progressive_z,
rotation_min_x,
rotation_min_y,
rotation_min_z,
rotation_max_x,
rotation_max_y,
rotation_max_z,
location_progressive_x,
location_progressive_y,
location_progressive_z,
location_min_x,
location_min_y,
location_min_z,
location_max_x,
location_max_y,
location_max_z,
scale_progressive_x,
scale_progressive_y,
scale_progressive_z,
scale_min_x,
scale_min_y,
scale_min_z,
scale_max_x,
scale_max_y,
scale_max_z,
global_transform,
ysl_ghost
):

    i = 0
    i_plane =  I_plane(path)
    pr_loc_x = 0.0
    pr_loc_y = 0.0
    pr_loc_z = 0.0
    pr_rot_x = 0.0
    pr_rot_y = 0.0
    pr_rot_z = 0.0
    pr_scale_x = 0.0
    pr_scale_y = 0.0
    pr_scale_z = 0.0
    i_plane_list = []
    real_obj_list = []

    if size_ofset == True:

        first_obj, _, _ = Get_Obj(obj_list, obj_list_len, 0)
        first_ofset = Size_Ofset(first_obj, dimension_axis, znak, True)
        main_of = first_ofset
        main_len = crv_len - (start_ofset + end_ofset)
        loc_translate(i_plane, (0,0,first_ofset + slide + start_ofset))
        main_col, ghost_col = main_collection(obj_list, obj_list_len, first_obj, ysl_ghost)

    else:

        main_of = 0
        main_len = crv_len - (start_ofset + end_ofset)
        loc_translate(i_plane, (0,0,slide + start_ofset))
        obj = obj_list[0][0]
        main_col, ghost_col = main_collection(obj_list, obj_list_len, obj, ysl_ghost)

    if size_ofset == True:

        while True:

            try:

                obj = nextobj
                ghost = nextghost
                ghost_p = nextghost_p

            except:
                
                obj, ghost, ghost_p = Get_Obj(obj_list, obj_list_len, i)

            nextobj, nextghost, nextghost_p = Get_Obj(obj_list, obj_list_len, i+1)
            first_ofset = Size_Ofset(nextobj, dimension_axis, znak, True)
            last_of = Size_Ofset(obj, dimension_axis, znak, False)
            rel_of = (last_of + first_ofset)*relative_ofset
            plane_loc, plane_nrml, vx_0, vx_1, vx_2 = i_plane_loc_normal_2(i_plane)
            i_plane_list.append([plane_loc, plane_nrml, vx_0, vx_1, vx_2])
            real_obj_list.append(obj)
            
            main_of += rel_of
            if main_of >= (main_len - last_of):
                break

            loc_translate(i_plane, (0,0,rel_of))
            i += 1

    else:

        while True:

            try:

                obj = nextobj
                ghost = nextghost
                ghost_p = nextghost_p

            except:
                
                obj, ghost, ghost_p = Get_Obj(obj_list, obj_list_len, i)

            nextobj, nextghost, nextghost_p = Get_Obj(obj_list, obj_list_len, i+1)
            first_ofset = Size_Ofset(nextobj, dimension_axis, znak, True)
            last_of = Size_Ofset(obj, dimension_axis, znak, False)
            rel_of = (last_of + first_ofset)*relative_ofset
            plane_loc, plane_nrml, vx_0, vx_1, vx_2 = i_plane_loc_normal_2(i_plane)
            i_plane_list.append([plane_loc, plane_nrml, vx_0, vx_1, vx_2])
            real_obj_list.append(obj)

            main_of += rel_of
            if main_of >= main_len:
                break

            i += 1
            loc_translate(i_plane, (0,0,rel_of))
    
    bpy.data.meshes.remove(i_plane.data)
    bpy.context.scene.curve_array_properties.other_props.array_settings.last_array = main_col.name
    len_i_plane_list = len(i_plane_list)
    bpy.context.view_layer.update()

    for i in range(len_i_plane_list):

        i_obj = Cloning_Type(real_obj_list[i], cloning_type, main_col, i, enable_parenting, ysl_ghost, ghost_col, ghost, ghost_p)
        i_obj.location = i_plane_list[i][0]

        if align_rot == True:
            
            Align_Rotation_2(i_obj, obj, i_plane_list[i][1], rail_axis, i_plane_list[i][2], i_plane_list[i][3], i_plane_list[i][4])               

        if global_transform == True:

            pr_loc_x, pr_loc_y, pr_loc_z, pr_rot_x, pr_rot_y, pr_rot_z, pr_scale_x, pr_scale_y, pr_scale_z = Transform_Editor(
            i_obj,     
            i,
            rotation_x,
            rotation_y,
            rotation_z,
            location_x,
            location_y,
            location_z,
            scale_x,
            scale_y,
            scale_z,
            rotation_progressive_x,
            rotation_progressive_y,
            rotation_progressive_z,
            rotation_min_x,
            rotation_min_y,
            rotation_min_z,
            rotation_max_x,
            rotation_max_y,
            rotation_max_z,
            location_progressive_x,
            location_progressive_y,
            location_progressive_z,
            location_min_x,
            location_min_y,
            location_min_z,
            location_max_x,
            location_max_y,
            location_max_z,
            scale_progressive_x,
            scale_progressive_y,
            scale_progressive_z,
            scale_min_x,
            scale_min_y,
            scale_min_z,
            scale_max_x,
            scale_max_y,
            scale_max_z,
            pr_loc_x,
            pr_loc_y,
            pr_loc_z,
            pr_rot_x,
            pr_rot_y,
            pr_rot_z,
            pr_scale_x,
            pr_scale_y,
            pr_scale_z,
            )

def Constant_Free(
obj_list, 
obj_list_len, 
dimension_axis, 
znak, 
start_ofset, 
end_ofset, 
crv_len, 
size_ofset, 
constant_ofset, 
path, 
slide, 
cloning_type, 
count, 
enable_parenting, 
align_rot, 
rail_axis,
rotation_x,
rotation_y,
rotation_z,
location_x,
location_y,
location_z,
scale_x,
scale_y,
scale_z,
rotation_progressive_x,
rotation_progressive_y,
rotation_progressive_z,
rotation_min_x,
rotation_min_y,
rotation_min_z,
rotation_max_x,
rotation_max_y,
rotation_max_z,
location_progressive_x,
location_progressive_y,
location_progressive_z,
location_min_x,
location_min_y,
location_min_z,
location_max_x,
location_max_y,
location_max_z,
scale_progressive_x,
scale_progressive_y,
scale_progressive_z,
scale_min_x,
scale_min_y,
scale_min_z,
scale_max_x,
scale_max_y,
scale_max_z,
global_transform,
ysl_ghost
):

    i = 0
    i_plane =  I_plane(path)
    count -=1
    pr_loc_x = 0.0
    pr_loc_y = 0.0
    pr_loc_z = 0.0
    pr_rot_x = 0.0
    pr_rot_y = 0.0
    pr_rot_z = 0.0
    pr_scale_x = 0.0
    pr_scale_y = 0.0
    pr_scale_z = 0.0
    i_plane_list = []

    if size_ofset == True:

        first_obj, _, _ = Get_Obj(obj_list, obj_list_len, 0)
        first_ofset = Size_Ofset(first_obj, dimension_axis, znak, True)

        main_of = first_ofset
        main_len = crv_len - (start_ofset + end_ofset)
        loc_translate(i_plane, (0,0,first_ofset + slide + start_ofset))
        main_col, ghost_col = main_collection(obj_list, obj_list_len, first_obj, ysl_ghost)

    else:

        main_len = crv_len - (start_ofset + end_ofset)
        loc_translate(i_plane, (0,0,slide + start_ofset))
        obj, _, _ = Get_Obj(obj_list, obj_list_len, 0)
        main_col, ghost_col = main_collection(obj_list, obj_list_len, obj, ysl_ghost)

    while True:

        plane_loc, plane_nrml, vx_0, vx_1, vx_2 = i_plane_loc_normal_2(i_plane)
        i_plane_list.append([plane_loc, plane_nrml, vx_0, vx_1, vx_2])

        if i >= count:
            break

        i += 1
        loc_translate(i_plane, (0,0,constant_ofset))

    bpy.data.meshes.remove(i_plane.data)
    bpy.context.scene.curve_array_properties.other_props.array_settings.last_array = main_col.name
    len_i_plane_list = len(i_plane_list)
    bpy.context.view_layer.update()

    for i in range(len_i_plane_list):

        obj, ghost, ghost_p = Get_Obj(obj_list, obj_list_len, i)
        i_obj = Cloning_Type(obj, cloning_type, main_col, i, enable_parenting, ysl_ghost, ghost_col, ghost, ghost_p)
        i_obj.location = i_plane_list[i][0]

        if align_rot == True:
            print(i_plane_list[i][1])
            Align_Rotation_2(i_obj, obj, i_plane_list[i][1], rail_axis, i_plane_list[i][2], i_plane_list[i][3], i_plane_list[i][4])               

        if global_transform == True:

            pr_loc_x, pr_loc_y, pr_loc_z, pr_rot_x, pr_rot_y, pr_rot_z, pr_scale_x, pr_scale_y, pr_scale_z = Transform_Editor(
            i_obj,     
            i,
            rotation_x,
            rotation_y,
            rotation_z,
            location_x,
            location_y,
            location_z,
            scale_x,
            scale_y,
            scale_z,
            rotation_progressive_x,
            rotation_progressive_y,
            rotation_progressive_z,
            rotation_min_x,
            rotation_min_y,
            rotation_min_z,
            rotation_max_x,
            rotation_max_y,
            rotation_max_z,
            location_progressive_x,
            location_progressive_y,
            location_progressive_z,
            location_min_x,
            location_min_y,
            location_min_z,
            location_max_x,
            location_max_y,
            location_max_z,
            scale_progressive_x,
            scale_progressive_y,
            scale_progressive_z,
            scale_min_x,
            scale_min_y,
            scale_min_z,
            scale_max_x,
            scale_max_y,
            scale_max_z,
            pr_loc_x,
            pr_loc_y,
            pr_loc_z,
            pr_rot_x,
            pr_rot_y,
            pr_rot_z,
            pr_scale_x,
            pr_scale_y,
            pr_scale_z,
            )

def Relative_Free(
obj_list, 
obj_list_len, 
dimension_axis, 
znak, 
start_ofset, 
end_ofset, 
crv_len, 
size_ofset, 
relative_ofset, 
path, 
slide, 
cloning_type, 
count, 
enable_parenting, 
align_rot, 
rail_axis,
rotation_x,
rotation_y,
rotation_z,
location_x,
location_y,
location_z,
scale_x,
scale_y,
scale_z,
rotation_progressive_x,
rotation_progressive_y,
rotation_progressive_z,
rotation_min_x,
rotation_min_y,
rotation_min_z,
rotation_max_x,
rotation_max_y,
rotation_max_z,
location_progressive_x,
location_progressive_y,
location_progressive_z,
location_min_x,
location_min_y,
location_min_z,
location_max_x,
location_max_y,
location_max_z,
scale_progressive_x,
scale_progressive_y,
scale_progressive_z,
scale_min_x,
scale_min_y,
scale_min_z,
scale_max_x,
scale_max_y,
scale_max_z,
global_transform,
ysl_ghost               
):

    i = 0
    i_plane =  I_plane(path)
    count -=1
    pr_loc_x = 0.0
    pr_loc_y = 0.0
    pr_loc_z = 0.0
    pr_rot_x = 0.0
    pr_rot_y = 0.0
    pr_rot_z = 0.0
    pr_scale_x = 0.0
    pr_scale_y = 0.0
    pr_scale_z = 0.0
    i_plane_list = []
    real_obj_list = []

    if size_ofset == True:

        first_obj, _, _ = Get_Obj(obj_list, obj_list_len, 0)
        first_ofset = Size_Ofset(first_obj, dimension_axis, znak, True)
        main_of = first_ofset
        main_len = crv_len - (start_ofset + end_ofset)
        loc_translate(i_plane, (0,0,first_ofset + slide + start_ofset))
        main_col, ghost_col = main_collection(obj_list, obj_list_len, first_obj, ysl_ghost)

    else:

        main_of = 0
        main_len = crv_len - (start_ofset + end_ofset)
        loc_translate(i_plane, (0,0,slide + start_ofset))
        obj, _, _ = Get_Obj(obj_list, obj_list_len, 0)
        main_col, ghost_col = main_collection(obj_list, obj_list_len, obj, ysl_ghost)

    if size_ofset == True:

        while True:

            try:

                obj = nextobj
                ghost = nextghost
                ghost_p = nextghost_p

            except:
                
                obj, ghost, ghost_p = Get_Obj(obj_list, obj_list_len, i)

            nextobj, nextghost, nextghost_p = Get_Obj(obj_list, obj_list_len, i+1)
            first_ofset = Size_Ofset(nextobj, dimension_axis, znak, True)
            last_of = Size_Ofset(obj, dimension_axis, znak, False)
            rel_of = (last_of + first_ofset)*relative_ofset
            plane_loc, plane_nrml, vx_0, vx_1, vx_2 = i_plane_loc_normal_2(i_plane)
            i_plane_list.append([plane_loc, plane_nrml, vx_0, vx_1, vx_2])
            real_obj_list.append(obj)

            if i >= count:
                break

            loc_translate(i_plane, (0,0,rel_of))
            i += 1

    else:

        while True:

            try:

                obj = nextobj
                ghost = nextghost
                ghost_p = nextghost_p

            except:
                
                obj, ghost, ghost_p = Get_Obj(obj_list, obj_list_len, i)

            nextobj, nextghost, nextghost_p = Get_Obj(obj_list, obj_list_len, i+1)
            first_ofset = Size_Ofset(nextobj, dimension_axis, znak, True)
            last_of = Size_Ofset(obj, dimension_axis, znak, False)
            rel_of = (last_of + first_ofset)*relative_ofset
            plane_loc, plane_nrml, vx_0, vx_1, vx_2 = i_plane_loc_normal_2(i_plane)
            i_plane_list.append([plane_loc, plane_nrml, vx_0, vx_1, vx_2])
            real_obj_list.append(obj)

            if i >= count:
                break

            i += 1
            loc_translate(i_plane, (0,0,rel_of))
    
    bpy.data.meshes.remove(i_plane.data)
    bpy.context.scene.curve_array_properties.other_props.array_settings.last_array = main_col.name
    len_i_plane_list = len(i_plane_list)
    bpy.context.view_layer.update()

    for i in range(len_i_plane_list):

        i_obj = Cloning_Type(real_obj_list[i], cloning_type, main_col, i, enable_parenting, ysl_ghost, ghost_col, ghost, ghost_p)
        i_obj.location = i_plane_list[i][0]

        if align_rot == True:
            
            Align_Rotation_2(i_obj, obj, i_plane_list[i][1], rail_axis, i_plane_list[i][2], i_plane_list[i][3], i_plane_list[i][4])               

        if global_transform == True:

            pr_loc_x, pr_loc_y, pr_loc_z, pr_rot_x, pr_rot_y, pr_rot_z, pr_scale_x, pr_scale_y, pr_scale_z = Transform_Editor(
            i_obj,     
            i,
            rotation_x,
            rotation_y,
            rotation_z,
            location_x,
            location_y,
            location_z,
            scale_x,
            scale_y,
            scale_z,
            rotation_progressive_x,
            rotation_progressive_y,
            rotation_progressive_z,
            rotation_min_x,
            rotation_min_y,
            rotation_min_z,
            rotation_max_x,
            rotation_max_y,
            rotation_max_z,
            location_progressive_x,
            location_progressive_y,
            location_progressive_z,
            location_min_x,
            location_min_y,
            location_min_z,
            location_max_x,
            location_max_y,
            location_max_z,
            scale_progressive_x,
            scale_progressive_y,
            scale_progressive_z,
            scale_min_x,
            scale_min_y,
            scale_min_z,
            scale_max_x,
            scale_max_y,
            scale_max_z,
            pr_loc_x,
            pr_loc_y,
            pr_loc_z,
            pr_rot_x,
            pr_rot_y,
            pr_rot_z,
            pr_scale_x,
            pr_scale_y,
            pr_scale_z,
            )

class CRVARRPRO_OT_MakeIt(bpy.types.Operator):
    '''Make array along path'''
    bl_label = "Make it!"
    bl_idname = 'crvarrpro.make_it'
    bl_options = {'REGISTER', 'UNDO'}
    
    slide : bpy.props.FloatProperty(
        name = "slide ",
        description="slide along path",
        default = 0,
        )

    count : bpy.props.IntProperty(
        name = "count",
        description="Count of objects in array",
        default = 1,
        min = 1
        )
        
    main_ofset : bpy.props.FloatProperty(
        name = "main_ofset",
        description="distance between objects in array",
        default = 0.1,
        min = 0
        )
        
    relative_ofset : bpy.props.FloatProperty(
        name = "relative_ofset",
        description="offset relative to the object's bounding box",
        default = 1,
        min = 0
        )    
        
    constant_ofset : bpy.props.FloatProperty(
        name = "constant_ofset",
        description="Constant offset",
        default = 1,
        min = 0
        )            
        
    ofset_type : bpy.props.EnumProperty(
        name = "",
        description="Select type of offset",
        items = (
            ('OP1',"Constant","Add a constant offset"),
            ('OP2',"Relative","Add an offset relative to the object's bounding box")
        )
        )

    cloning_type : bpy.props.EnumProperty(
        name = "",
        description="Select type of cloning",
        items = (
            ('OP3',"Real instance (Light)","All objects use main object data, and copy transform"),
            ('OP2',"Real instance","All objects use main object data, but have a custom transform"),
            ('OP1',"Usual Copy","Every object is unique")
        )
        )

    enable_parenting : bpy.props.BoolProperty(
        name = "enable_parenting",
        description="Enable parenting",
        default = False
        )

    spacing_type : bpy.props.EnumProperty(
        name = "",
        description="Select type of spacing",
        items = (
            ('OP1',"Fill by count","Uniform filling of the entire length"),
            ('OP2',"Fill by offset","Uniform filling of the entire length"),
            ('OP3',"Free","Free mode")
        )
        )
                        
    start_ofset : bpy.props.FloatProperty(
        name = "start_ofset",
        description="Start offset",
        default = 0,
        min = 0
        )
        
    end_ofset : bpy.props.FloatProperty(
        name = "end_ofset",
        description="End offset",
        default = 0,
        min = 0
        )
                        
    size_ofset : bpy.props.BoolProperty(
        name = "size_ofset",
        description="Take into account the size of the object",
        default = False
        )
        
    rail_axis : bpy.props.EnumProperty(
        name = "",
        description="Select type of spacing",
        items = (
            ('+x',"X","Rail +x"),
            ('+y',"Y","Rail +y"),
            ('+z',"Z","Rail +z"),
            ('-y',"-Y","Rail -y"),
            ('-x',"-X","Rail -x"),
            ('-z',"-Z","Rail -z")
        )
        )
        
    align_rot : bpy.props.BoolProperty(
        name = "align_rot",
        description="Align rotation",
        default = True
        )
    
    counter : bpy.props.IntProperty(
        name = "counter",
        description="Random counter",
        default = 1,
        min = 1,
        max = 100,
        update=update_func
        )

    rotation_progressive_x : bpy.props.FloatProperty(
        name = "rotation_progressive_x",
        description= "",
        default = 0,
        min = -360,
        max = 360
        )

    rotation_min_x : bpy.props.FloatProperty(
        name = "rotation_min_x",
        description= "",
        default = 0,
        min = -360,
        max = 360
        )

    rotation_max_x : bpy.props.FloatProperty(
        name = "rotation_max_x",
        description= "",
        default = 0,
        min = -360,
        max = 360
        )

    rotation_progressive_y : bpy.props.FloatProperty(
        name = "rotation_progressive_y",
        description= "",
        default = 0,
        min = -360,
        max = 360
        )

    rotation_min_y : bpy.props.FloatProperty(
        name = "rotation_min_y",
        description= "",
        default = 0,
        min = -360,
        max = 360
        )

    rotation_max_y : bpy.props.FloatProperty(
        name = "rotation_max_y",
        description= "",
        default = 0,
        min = -360,
        max = 360
        )

    rotation_progressive_z : bpy.props.FloatProperty(
        name = "rotation_progressive_z",
        description= "",
        default = 0,
        min = -360,
        max = 360
        )

    rotation_min_z : bpy.props.FloatProperty(
        name = "rotation_min_z",
        description= "",
        default = 0,
        min = -360,
        max = 360
        )

    rotation_max_z : bpy.props.FloatProperty(
        name = "rotation_max_z",
        description= "",
        default = 0,
        min = -360,
        max = 360
        )

    location_progressive_x : bpy.props.FloatProperty(
        name = "location_progressive_x",
        description= "",
        default = 0
        )

    location_min_x : bpy.props.FloatProperty(
        name = "location_min_x",
        description= "",
        default = 0
        )

    location_max_x : bpy.props.FloatProperty(
        name = "location_max_x",
        description= "",
        default = 0
        )

    location_progressive_y : bpy.props.FloatProperty(
        name = "location_progressive_y",
        description= "",
        default = 0
        )

    location_min_y : bpy.props.FloatProperty(
        name = "location_min_y",
        description= "",
        default = 0
        )

    location_max_y : bpy.props.FloatProperty(
        name = "location_max_y",
        description= "",
        default = 0
        )

    location_progressive_z : bpy.props.FloatProperty(
        name = "location_progressive_z",
        description= "",
        default = 0
        )

    location_min_z : bpy.props.FloatProperty(
        name = "location_min_z",
        description= "",
        default = 0
        )

    location_max_z : bpy.props.FloatProperty(
        name = "location_max_z",
        description= "",
        default = 0
        )

    scale_progressive_x : bpy.props.FloatProperty(
        name = "scale_progressive_x",
        description= "",
        default = 0
        )

    scale_min_x : bpy.props.FloatProperty(
        name = "scale_min_x",
        description= "",
        default = 0
        )

    scale_max_x : bpy.props.FloatProperty(
        name = "scale_max_x",
        description= "",
        default = 0
        )

    scale_progressive_y : bpy.props.FloatProperty(
        name = "scale_progressive_y",
        description= "",
        default = 0
        )

    scale_min_y : bpy.props.FloatProperty(
        name = "scale_min_y",
        description= "",
        default = 0
        )

    scale_max_y : bpy.props.FloatProperty(
        name = "scale_max_y",
        description= "",
        default = 0
        )

    scale_progressive_z : bpy.props.FloatProperty(
        name = "scale_progressive_z",
        description= "",
        default = 0
        )

    scale_min_z : bpy.props.FloatProperty(
        name = "scale_min_z",
        description= "",
        default = 0
        )

    scale_max_z : bpy.props.FloatProperty(
        name = "scale_max_z",
        description= "",
        default = 0
        )

    def draw(self, context):
        
        layout = self.layout
        active_scene = bpy.context.scene

        row = layout.row()
        row.label(text = "Object cloning type:", icon = 'PARTICLE_POINT')
        
        row = layout.row()
        row.prop(self, "cloning_type")

        if self.cloning_type != 'OP3':

            row = layout.row()
            row.label(text = "Enable parenting:", icon = 'LINKED')
            row.prop(self, "enable_parenting", text = "")
        
        row = layout.row()
        row.label(text = "Type of spacing:", icon = 'TOOL_SETTINGS')
        
        row = layout.row()
        row.prop(self, "spacing_type")
        
        if self.spacing_type == 'OP1':
                
            row = layout.row()
            row.label(text = "Count:", icon = 'MOD_ARRAY')
            row.prop(self, "count", text = "")
        
        elif self.spacing_type == 'OP2':            
            
            row = layout.row()
            row.label(text = "Type of ofset:", icon = 'TOOL_SETTINGS')
            row.prop(self, "ofset_type")

            if self.ofset_type == 'OP1':            
            
                row = layout.row()
                row.label(text = "Constant offset:", icon = 'DRIVER_DISTANCE')
                row.prop(self, "constant_ofset", text = "")

            elif self.ofset_type == 'OP2':

                row = layout.row()
                row.label(text = "Relative offset:", icon = 'DRIVER_DISTANCE')
                row.prop(self, "relative_ofset", text = "")
                                               
        elif self.spacing_type == 'OP3':
            
            row = layout.row()
            row.label(text = "Count:", icon = 'MOD_ARRAY')
            row.prop(self, "count", text = "")            
            
            row = layout.row()
            row.label(text = "Type of ofset:", icon = 'TOOL_SETTINGS')
            row.prop(self, "ofset_type")

            if self.ofset_type == 'OP1':            
            
                row = layout.row()
                row.label(text = "Constant offset:", icon = 'DRIVER_DISTANCE')
                row.prop(self, "constant_ofset", text = "")

            elif self.ofset_type == 'OP2':

                row = layout.row()
                row.label(text = "Relative offset:", icon = 'DRIVER_DISTANCE')
                row.prop(self, "relative_ofset", text = "")               

        if self.spacing_type == 'OP1' or self.spacing_type == 'OP2':

            row = layout.row()
            row.label(text = "Start ofset:", icon = 'DRIVER_DISTANCE')
            row.prop(self, "start_ofset", text = "")
        
            row = layout.row()
            row.label(text = "End ofset:", icon = 'DRIVER_DISTANCE')
            row.prop(self, "end_ofset", text = "")                 
            
        row = layout.row()
        row.label(text = "Slide:", icon = 'FORCE_CURVE')
        row.prop(self, "slide", text = "")

        row = layout.row()
        row.label(text = "Track axis:", icon = 'EMPTY_AXIS')
        row.prop(self, "rail_axis") 
            
        row = layout.row()
        row.label(text = "Align rotation:", icon = 'CON_ROTLIKE')
        row.prop(self, "align_rot", text = "")
                        
        row = layout.row()
        row.label(text = "Consider size of object:", icon = 'PIVOT_BOUNDBOX')
        row.prop(self, "size_ofset", text = "")

        props = active_scene.curve_array_properties
        rot_props = props.transform_props.rotation_trform
        loc_props = props.transform_props.location_trform
        scale_props = props.transform_props.scale_trform
        layout = self.layout

        col = layout.box().column()
        row_1 = col.row()
        split = row_1.split(factor = 0.2)
        split_1 = split.row()
        split = split.split(factor = 0.333)
        split_2 = split.row()
        split_3 = split.row(align = True)

        split_1.label(text= '')
        split_2.label(text= 'Progressive')
        split_3.label(text= '   Rand Min ')
        split_3.label(text= '   Rand Max ')

        col = layout.box().column()
        row_1 = col.row()
        row_2 = col.row()
        row_3 = col.row()

        split = row_1.split(factor = 0.2)
        split_1 = split.row()
        split = split.split(factor = 0.333)
        split_2 = split.row()
        split_3 = split.row(align = True)

        split_1.label(text= 'Rot X')
        split_2.prop(self, "rotation_progressive_x", text = "")
        split_3.prop(self, "rotation_min_x", text = "")
        split_3.prop(self, "rotation_max_x", text = "")

        split = row_2.split(factor = 0.2)
        split_1 = split.row()
        split = split.split(factor = 0.333)
        split_2 = split.row()
        split_3 = split.row(align = True)

        split_1.label(text= 'Rot Y')
        split_2.prop(self, "rotation_progressive_y", text = "")
        split_3.prop(self, "rotation_min_y", text = "")
        split_3.prop(self, "rotation_max_y", text = "")

        split = row_3.split(factor = 0.2)
        split_1 = split.row()
        split = split.split(factor = 0.333)
        split_2 = split.row()
        split_3 = split.row(align = True)

        split_1.label(text= 'Rot Z')
        split_2.prop(self, "rotation_progressive_z", text = "")
        split_3.prop(self, "rotation_min_z", text = "")
        split_3.prop(self, "rotation_max_z", text = "")

        col = layout.box().column()
        row_1 = col.row()
        row_2 = col.row()
        row_3 = col.row()

        split = row_1.split(factor = 0.2)
        split_1 = split.row()
        split = split.split(factor = 0.333)
        split_2 = split.row()
        split_3 = split.row(align = True)

        split_1.label(text= 'Loc X')
        split_2.prop(self, "location_progressive_x", text = "")
        split_3.prop(self, "location_min_x", text = "")
        split_3.prop(self, "location_max_x", text = "")

        split = row_2.split(factor = 0.2)
        split_1 = split.row()
        split = split.split(factor = 0.333)
        split_2 = split.row()
        split_3 = split.row(align = True)

        split_1.label(text= 'Loc Y')
        split_2.prop(self, "location_progressive_y", text = "")
        split_3.prop(self, "location_min_y", text = "")
        split_3.prop(self, "location_max_y", text = "")

        split = row_3.split(factor = 0.2)
        split_1 = split.row()
        split = split.split(factor = 0.333)
        split_2 = split.row()
        split_3 = split.row(align = True)

        split_1.label(text= 'Loc Z')
        split_2.prop(self, "location_progressive_z", text = "")
        split_3.prop(self, "location_min_z", text = "")
        split_3.prop(self, "location_max_z", text = "")

        col = layout.box().column()
        row_1 = col.row()
        row_2 = col.row()
        row_3 = col.row()

        split = row_1.split(factor = 0.2)
        split_1 = split.row()
        split = split.split(factor = 0.333)
        split_2 = split.row()
        split_3 = split.row(align = True)

        split_1.label(text= 'Scale X')
        split_2.prop(self, "scale_progressive_x", text = "")
        split_3.prop(self, "scale_min_x", text = "")
        split_3.prop(self, "scale_max_x", text = "")

        split = row_2.split(factor = 0.2)
        split_1 = split.row()
        split = split.split(factor = 0.333)
        split_2 = split.row()
        split_3 = split.row(align = True)

        split_1.label(text= 'Scale Y')
        split_2.prop(self, "scale_progressive_y", text = "")
        split_3.prop(self, "scale_min_y", text = "")
        split_3.prop(self, "scale_max_y", text = "")

        split = row_3.split(factor = 0.2)
        split_1 = split.row()
        split = split.split(factor = 0.333)
        split_2 = split.row()
        split_3 = split.row(align = True)

        split_1.label(text= 'Scale Z')
        split_2.prop(self, "scale_progressive_z", text = "")
        split_3.prop(self, "scale_min_z", text = "")
        split_3.prop(self, "scale_max_z", text = "")

        row = layout.box().row()
        row.label(text = "Seed:")
        row.prop(self, "counter", text = "")

    def execute(self,context):

        active_scene = bpy.context.scene
        my_props = active_scene.curve_array_properties.other_props.array_settings       
        rot_props = active_scene.curve_array_properties.transform_props.rotation_trform
        scale_props = active_scene.curve_array_properties.transform_props.scale_trform
        loc_props = active_scene.curve_array_properties.transform_props.location_trform

        cloning_type = self.cloning_type    
        setattr(my_props, 'cloning_type', cloning_type)
        enable_parenting = self.enable_parenting    
        setattr(my_props, 'enable_parenting', enable_parenting)  
        spacing_type = self.spacing_type     
        setattr(my_props, 'spacing_type', spacing_type)   
        ofset_type = self.ofset_type
        setattr(my_props, 'ofset_type', ofset_type)  
        constant_ofset = self.constant_ofset
        setattr(my_props, 'constant_ofset', constant_ofset)  
        relative_ofset = self.relative_ofset
        setattr(my_props, 'relative_ofset', relative_ofset)  
        count = self.count
        setattr(my_props, 'count', count)  
        start_ofset = self.start_ofset
        setattr(my_props, 'start_ofset', start_ofset)  
        end_ofset = self.end_ofset
        setattr(my_props, 'end_ofset', end_ofset)  
        slide = self.slide
        setattr(my_props, 'slide', slide)  
        align_rot = self.align_rot
        setattr(my_props, 'align_rot', align_rot)  
        rail_axis = self.rail_axis
        setattr(my_props, 'rail_axis', rail_axis)  
        size_ofset = self.size_ofset
        setattr(my_props, 'size_ofset', size_ofset)  
        counter = self.counter
        setattr(my_props, 'counter', counter)  

        rotation_progressive_x = self.rotation_progressive_x
        rotation_progressive_y = self.rotation_progressive_y
        rotation_progressive_z = self.rotation_progressive_z
        rotation_min_x = self.rotation_min_x
        rotation_min_y = self.rotation_min_y
        rotation_min_z = self.rotation_min_z
        rotation_max_x = self.rotation_max_x
        rotation_max_y = self.rotation_max_y
        rotation_max_z = self.rotation_max_z
        location_progressive_x = self.location_progressive_x
        location_progressive_y = self.location_progressive_y
        location_progressive_z = self.location_progressive_z
        location_min_x = self.location_min_x
        location_min_y = self.location_min_y
        location_min_z = self.location_min_z
        location_max_x = self.location_max_x
        location_max_y = self.location_max_y
        location_max_z = self.location_max_z
        scale_progressive_x = self.scale_progressive_x
        scale_progressive_y = self.scale_progressive_y
        scale_progressive_z = self.scale_progressive_z
        scale_min_x = self.scale_min_x
        scale_min_y = self.scale_min_y
        scale_min_z = self.scale_min_z
        scale_max_x = self.scale_max_x
        scale_max_y = self.scale_max_y
        scale_max_z = self.scale_max_z

        setattr(rot_props, 'rotation_progressive_x', rotation_progressive_x)  
        setattr(rot_props, 'rotation_progressive_y', rotation_progressive_y) 
        setattr(rot_props, 'rotation_progressive_z', rotation_progressive_z) 
        setattr(rot_props, 'rotation_min_x', rotation_min_x) 
        setattr(rot_props, 'rotation_min_y', rotation_min_y) 
        setattr(rot_props, 'rotation_min_z', rotation_min_z) 
        setattr(rot_props, 'rotation_max_x', rotation_max_x) 
        setattr(rot_props, 'rotation_max_y', rotation_max_y) 
        setattr(rot_props, 'rotation_max_z', rotation_max_z) 

        setattr(loc_props, 'location_progressive_x', location_progressive_x) 
        setattr(loc_props, 'location_progressive_y', location_progressive_y) 
        setattr(loc_props, 'location_progressive_z', location_progressive_z) 
        setattr(loc_props, 'location_min_x', location_min_x) 
        setattr(loc_props, 'location_min_y', location_min_y) 
        setattr(loc_props, 'location_min_z', location_min_z) 
        setattr(loc_props, 'location_max_x', location_max_x) 
        setattr(loc_props, 'location_max_y', location_max_y) 
        setattr(loc_props, 'location_max_z', location_max_z) 

        setattr(scale_props, 'scale_progressive_x', scale_progressive_x)
        setattr(scale_props, 'scale_progressive_y', scale_progressive_y)
        setattr(scale_props, 'scale_progressive_z', scale_progressive_z)
        setattr(scale_props, 'scale_min_x', scale_min_x)
        setattr(scale_props, 'scale_min_y', scale_min_y)
        setattr(scale_props, 'scale_min_z', scale_min_z)
        setattr(scale_props, 'scale_max_x', scale_max_x)
        setattr(scale_props, 'scale_max_y', scale_max_y)
        setattr(scale_props, 'scale_max_z', scale_max_z)

        path_name = active_scene.curve_array_properties.path_props.path_main.path_name
        path = active_scene.objects.get(path_name)

        if transform_editor.get_scene() == None or transform_editor.get_scene() != active_scene:

            transform_editor.update()

        global_transform = transform_editor.get()
        rotation_x = True
        rotation_y = True
        rotation_z = True
        location_x = True
        location_y = True
        location_z = True
        scale_x = True
        scale_y = True
        scale_z = True

        if path_name == "":
            
            ShowMessageBox("Error","Select any curve", 'ERROR')
        
            return {'CANCELLED'}
                        
        if path == None:
            
            ShowMessageBox("Error","Path does not exist", 'ERROR')
        
            return {'CANCELLED'}

        if path.type != 'CURVE':
            
            ShowMessageBox("Error","Select Curve", 'ERROR')
            
            return {'CANCELLED'}
        
        if bpy.context.mode != 'OBJECT':
            
            ShowMessageBox("Error","Exit Edit Mode", 'ERROR')
            
            return {'CANCELLED'}                                       
                           
        if len(path.data.splines) != 1:           
            
            ShowMessageBox("Error","Сurve should have only one spline", 'ERROR')
            
            return {'CANCELLED'}

        crv_len = LengthOfCurve(path.data.splines[0], path)

        if object_list.get_scene() != active_scene:

            obj_list = object_list.update()

        else:

            obj_list = object_list.get_list()
            ysl_ghost = object_list.get_ghost()

        obj_list_len = len(obj_list)

        if obj_list_len == 0:

            ShowMessageBox("Error","Store any object", 'ERROR')
        
            return {'CANCELLED'}

        if path.data.splines[0].use_cyclic_u == True:
            
            cyclic = 0   
        
        else:

            cyclic = 1

        if rail_axis == "+z":
 
            track_x = 1
            track_y = 1
            track_z = 1          
            dimension_axis = 2
            znak = 1

        elif rail_axis == "-z":
             
            track_x = -1
            track_y = 1
            track_z = -1 
            dimension_axis = 2
            znak = -1

        elif rail_axis == "+x":
             
            track_x = 1
            track_y = 1
            track_z = 1    
            dimension_axis = 0
            znak = 1

        elif rail_axis == "-x":
             
            track_x = -1
            track_y = 1
            track_z = -1    
            dimension_axis = 0
            znak = -1

        elif rail_axis == "+y":
             
            track_x = 1
            track_y = 1
            track_z = 1    
            dimension_axis = 1
            znak = 1

        else:
             
            track_x = -1
            track_y = 1
            track_z = -1
            dimension_axis = 1
            znak = -1

        if rotation_min_x > rotation_max_x:

            self.rotation_min_x = rotation_max_x
            rotation_min_x = rotation_max_x

        if rotation_min_y > rotation_max_y:

            self.rotation_min_y = rotation_max_y
            rotation_min_y = rotation_max_y

        if rotation_min_z > rotation_max_z:

            self.rotation_min_z = rotation_max_z
            rotation_min_z = rotation_max_z

        if location_min_x > location_max_x:

            self.location_min_x = location_max_x
            location_min_x = location_max_x

        if location_min_y > location_max_y:

            self.location_min_y = location_max_y
            location_min_y = location_max_y

        if location_min_z > location_max_z:

            self.location_min_z = location_max_z
            location_min_z = location_max_z

        if scale_min_x > scale_max_x:

            self.scale_min_x = scale_max_x
            scale_min_x = scale_max_x

        if scale_min_y > scale_max_y:

            self.scale_min_y = scale_max_y
            scale_min_y = scale_max_y

        if scale_min_z > scale_max_z:

            self.scale_min_z = scale_max_z
            scale_min_z = scale_max_z

        if global_transform == True:

            if (rotation_progressive_x == 0 and rotation_min_x == 0 and rotation_max_x == 0):

                rotation_x = False
                
            if (rotation_progressive_y == 0 and rotation_min_y == 0 and rotation_max_y == 0):

                rotation_y = False

            if (rotation_progressive_z == 0 and rotation_min_z == 0 and rotation_max_z == 0):

                rotation_z = False

            if (location_progressive_x == 0 and location_min_x == 0 and location_max_x == 0):

                location_x = False

            if (location_progressive_y == 0 and location_min_y == 0 and location_max_y == 0):

                location_y = False

            if (location_progressive_z == 0 and location_min_z == 0 and location_max_z == 0):

                location_z = False

            if (scale_progressive_x == 1 and scale_min_x == 1 and scale_max_x == 1):

                scale_x = False

            if (scale_progressive_y == 1 and scale_min_y == 1 and scale_max_y == 1):

                scale_y = False

            if (scale_progressive_z == 1 and scale_min_z == 1 and scale_max_z == 1):

                scale_z = False

        if spacing_type == 'OP1':

            Count_Fill(
            count,
            crv_len,
            cyclic,
            znak,
            size_ofset,
            start_ofset, 
            end_ofset, 
            obj_list, 
            obj_list_len, 
            dimension_axis, 
            path, 
            cloning_type, 
            slide, 
            enable_parenting, 
            align_rot, 
            rail_axis,
            rotation_x,
            rotation_y,
            rotation_z,
            location_x,
            location_y,
            location_z,
            scale_x,
            scale_y,
            scale_z,
            rotation_progressive_x,
            rotation_progressive_y,
            rotation_progressive_z,
            rotation_min_x,
            rotation_min_y,
            rotation_min_z,
            rotation_max_x,
            rotation_max_y,
            rotation_max_z,
            location_progressive_x,
            location_progressive_y,
            location_progressive_z,
            location_min_x,
            location_min_y,
            location_min_z,
            location_max_x,
            location_max_y,
            location_max_z,
            scale_progressive_x,
            scale_progressive_y,
            scale_progressive_z,
            scale_min_x,
            scale_min_y,
            scale_min_z,
            scale_max_x,
            scale_max_y,
            scale_max_z,
            global_transform,
            ysl_ghost
            )

        elif spacing_type == 'OP2':

            if ofset_type == 'OP1':
                            
                Constant_Fill(
                obj_list, 
                obj_list_len, 
                dimension_axis, 
                znak, 
                start_ofset, 
                end_ofset, 
                crv_len, 
                size_ofset, 
                constant_ofset, 
                path, 
                slide, 
                cloning_type, 
                enable_parenting, 
                align_rot, 
                rail_axis,
                rotation_x,
                rotation_y,
                rotation_z,
                location_x,
                location_y,
                location_z,
                scale_x,
                scale_y,
                scale_z,
                rotation_progressive_x,
                rotation_progressive_y,
                rotation_progressive_z,
                rotation_min_x,
                rotation_min_y,
                rotation_min_z,
                rotation_max_x,
                rotation_max_y,
                rotation_max_z,
                location_progressive_x,
                location_progressive_y,
                location_progressive_z,
                location_min_x,
                location_min_y,
                location_min_z,
                location_max_x,
                location_max_y,
                location_max_z,
                scale_progressive_x,
                scale_progressive_y,
                scale_progressive_z,
                scale_min_x,
                scale_min_y,
                scale_min_z,
                scale_max_x,
                scale_max_y,
                scale_max_z,
                global_transform,
                ysl_ghost              
                )

            else:
                            
                Relative_Fill(
                obj_list, 
                obj_list_len, 
                dimension_axis, 
                znak, 
                start_ofset, 
                end_ofset, 
                crv_len, 
                size_ofset, 
                relative_ofset, 
                path, 
                slide, 
                cloning_type, 
                enable_parenting, 
                align_rot, 
                rail_axis,
                rotation_x,
                rotation_y,
                rotation_z,
                location_x,
                location_y,
                location_z,
                scale_x,
                scale_y,
                scale_z,
                rotation_progressive_x,
                rotation_progressive_y,
                rotation_progressive_z,
                rotation_min_x,
                rotation_min_y,
                rotation_min_z,
                rotation_max_x,
                rotation_max_y,
                rotation_max_z,
                location_progressive_x,
                location_progressive_y,
                location_progressive_z,
                location_min_x,
                location_min_y,
                location_min_z,
                location_max_x,
                location_max_y,
                location_max_z,
                scale_progressive_x,
                scale_progressive_y,
                scale_progressive_z,
                scale_min_x,
                scale_min_y,
                scale_min_z,
                scale_max_x,
                scale_max_y,
                scale_max_z,
                global_transform,
                ysl_ghost
                )
        
        else:

            if ofset_type == 'OP1':
                            
                Constant_Free(
                obj_list, 
                obj_list_len, 
                dimension_axis, 
                znak, 
                start_ofset, 
                end_ofset, 
                crv_len, 
                size_ofset, 
                constant_ofset, 
                path, 
                slide, 
                cloning_type, 
                count, 
                enable_parenting, 
                align_rot, 
                rail_axis,
                rotation_x,
                rotation_y,
                rotation_z,
                location_x,
                location_y,
                location_z,
                scale_x,
                scale_y,
                scale_z,
                rotation_progressive_x,
                rotation_progressive_y,
                rotation_progressive_z,
                rotation_min_x,
                rotation_min_y,
                rotation_min_z,
                rotation_max_x,
                rotation_max_y,
                rotation_max_z,
                location_progressive_x,
                location_progressive_y,
                location_progressive_z,
                location_min_x,
                location_min_y,
                location_min_z,
                location_max_x,
                location_max_y,
                location_max_z,
                scale_progressive_x,
                scale_progressive_y,
                scale_progressive_z,
                scale_min_x,
                scale_min_y,
                scale_min_z,
                scale_max_x,
                scale_max_y,
                scale_max_z,
                global_transform,
                ysl_ghost
                )

            else:
                            
                Relative_Free(
                obj_list, 
                obj_list_len, 
                dimension_axis, 
                znak, 
                start_ofset, 
                end_ofset, 
                crv_len, 
                size_ofset, 
                relative_ofset, 
                path, 
                slide, 
                cloning_type, 
                count, 
                enable_parenting, 
                align_rot, 
                rail_axis,
                rotation_x,
                rotation_y,
                rotation_z,
                location_x,
                location_y,
                location_z,
                scale_x,
                scale_y,
                scale_z,
                rotation_progressive_x,
                rotation_progressive_y,
                rotation_progressive_z,
                rotation_min_x,
                rotation_min_y,
                rotation_min_z,
                rotation_max_x,
                rotation_max_y,
                rotation_max_z,
                location_progressive_x,
                location_progressive_y,
                location_progressive_z,
                location_min_x,
                location_min_y,
                location_min_z,
                location_max_x,
                location_max_y,
                location_max_z,
                scale_progressive_x,
                scale_progressive_y,
                scale_progressive_z,
                scale_min_x,
                scale_min_y,
                scale_min_z,
                scale_max_x,
                scale_max_y,
                scale_max_z,
                global_transform,
                ysl_ghost              
                )
        
        return {'FINISHED'}