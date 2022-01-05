import bpy
import random
import math
import mathutils

from Curve_Array_Pro_Magic_Curve.props.curve_array_props import (
Edit_Stor_Draw_Count,
Ran_Gr_LinkToObj,
Ran_Gr_Count,
Ran_Gr_ObjCount
)

def ShowMessageBox(title, message, icon):

    def draw(self, context):
        self.layout.label(text = message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

random_num = []
for _ in range(5):

    random_num_str = []

    for _ in range(100):

        rand = random.randint(0, 10000)

        random_num_str.append(rand)
    
    random_num.append(random_num_str)

def Size_Ofset(obj, axis, znak, start):

    location = obj.location
    bb = obj.bound_box
    axis_vertex = 0.0

    if start == False:

        znak = znak * (-1)

    if znak == 1:

        for i in range(8):

            if bb[i][axis] > axis_vertex:

                axis_vertex = bb[i][axis]
    
    else:

        for i in range(8):

            if bb[i][axis] < axis_vertex:

                axis_vertex = bb[i][axis]


    ofset = abs(axis_vertex) * obj.scale[axis]

    return ofset

def Chance(rg, index):

    m = Ran_Gr_ObjCount(rg, index)

    n = 0

    count = Ran_Gr_Count(rg)

    for i in range(count):

        cou = Ran_Gr_ObjCount(rg, i)

        n += cou    

    chance = m/n

    return chance

def RG_list(rg):

    rg_list = []
    rg_list_objects = []
    rg_list_chance = []
    count = Ran_Gr_Count(rg)

    for i in range(count):

        index = Ran_Gr_LinkToObj(rg, i)

        strind = 'obj_stor_' + str(index)
        name = getattr(getattr(bpy.context.scene.curve_array_properties.object_props.object_storage, strind), 'obj_name')
        obj = bpy.context.scene.objects.get(name)
        chance = Chance(rg , i)

        rg_list_objects.append(obj)
        rg_list_chance.append(chance)

    rg_list.append(rg_list_objects)
    rg_list.append(rg_list_chance)

    return rg_list

def Random_List(rg_list, gr):

    counter = bpy.context.scene.curve_array_properties.other_props.array_settings.counter  
    length = len(rg_list)
    rand = random_num[gr][counter-1]

    ost = int(math.fmod(rand, length)) 

    return rg_list[ost]

def Last_Obj(count, obj_list):

    length = len(obj_list)
    last = int(math.fmod(count, length))
    obj = obj_list[last][0]

    return obj

def Object_List():

    props = bpy.context.scene.curve_array_properties
    counter = getattr(bpy.context.scene.curve_array_properties.other_props.array_settings, 'counter')
    count_draw = Edit_Stor_Draw_Count()
    obj_list = []

    for i in range(count_draw):

        strind = 'edit_stor_draw_' + str(i)
        id = getattr(props.object_props.editor_storage_draw, strind)
        strind = 'edit_stor_' + str(id)
        prop = getattr(props.object_props.editor_storage, strind) 
        link = getattr(prop, 'link')
        count = getattr(prop, 'count')
        ghost = getattr(prop, 'ghost')
        ghost_p = getattr(prop, 'ghost_p')

        if int(link) >= 0:

            strind = 'obj_stor_' + str(link)
            name = getattr(getattr(props.object_props.object_storage, strind), 'obj_name')
            obj = bpy.context.scene.objects.get(name)

        else:

            gr_id = abs(int(link))
            rg_count = Ran_Gr_Count(gr_id)

            if rg_count == 0:

                continue

            else:

                obj = RG_list(gr_id)

        for _ in range(count):

            str_list = []

            if obj == None :
            
                ShowMessageBox("Error","Object does not exist", 'ERROR')
            
                return {'CANCELLED'}

            str_list.append(obj)
            str_list.append(ghost)
            str_list.append(ghost_p/100)
            obj_list.append(str_list)

    return obj_list

class Obj_List:

    def __init__(self):
        self.obj_list = [] 
        self.obj_list_scene = None
        self.ghost = False

    def update(self):
        self.obj_list = Object_List()
        self.obj_list_scene = bpy.context.scene

        ysl = False
        for i in self.obj_list:

            if i[1] == True:
                
                ysl = True
                break

        self.ghost = ysl

        return self.obj_list

    def get_scene(self):
        sc = self.obj_list_scene

        return sc

    def get_list(self):
        sc = self.obj_list

        return sc

    def get_ghost(self):
        sc = self.ghost

        return sc

object_list = Obj_List()

class Transform_Editor:

    def __init__(self):
        self.editor = False 
        self.editor_scene = None

    def update(self):
        self.editor_scene = bpy.context.scene
        self.editor = False 

        active_scene = bpy.context.scene 
        props = active_scene.curve_array_properties
        rot_props = props.transform_props.rotation_trform
        loc_props = props.transform_props.location_trform
        scale_props = props.transform_props.scale_trform

        if rot_props.rotation_min_x > rot_props.rotation_max_x:

            rot_props.rotation_min_x = rot_props.rotation_max_x

        if rot_props.rotation_min_y > rot_props.rotation_max_y:

            rot_props.rotation_min_y = rot_props.rotation_max_y

        if rot_props.rotation_min_z > rot_props.rotation_max_z:

            rot_props.rotation_min_z = rot_props.rotation_max_z

        if loc_props.location_min_x > loc_props.location_max_x:

            loc_props.location_min_x = loc_props.location_max_x

        if loc_props.location_min_y > loc_props.location_max_y:

            loc_props.location_min_y = loc_props.location_max_y

        if loc_props.location_min_z > loc_props.location_max_z:

            loc_props.location_min_z = loc_props.location_max_z

        if scale_props.scale_min_x > scale_props.scale_max_x:

            scale_props.scale_min_x = scale_props.scale_max_x

        if scale_props.scale_min_y > scale_props.scale_max_y:

            scale_props.scale_min_y = scale_props.scale_max_y

        if scale_props.scale_min_z > scale_props.scale_max_z:

            scale_props.scale_min_z = scale_props.scale_max_z

        if rot_props.rotation_progressive_x != 0:

            self.editor = True

            return
        if rot_props.rotation_progressive_y != 0:

            self.editor = True

            return
        if rot_props.rotation_progressive_z != 0:

            self.editor = True

            return
        if rot_props.rotation_min_x != 0:

            self.editor = True

            return
        if rot_props.rotation_min_y != 0:

            self.editor = True

            return
        if rot_props.rotation_min_z != 0:

            self.editor = True

            return
        if rot_props.rotation_max_x != 0:

            self.editor = True

            return
        if rot_props.rotation_max_y != 0:

            self.editor = True

            return
        if rot_props.rotation_max_z != 0:

            self.editor = True

            return
        if loc_props.location_progressive_x != 0:

            self.editor = True

            return
        if loc_props.location_progressive_y != 0:

            self.editor = True

            return
        if loc_props.location_progressive_z != 0:

            self.editor = True

            return
        if loc_props.location_min_x != 0:

            self.editor = True

            return
        if loc_props.location_min_y != 0:

            self.editor = True

            return
        if loc_props.location_min_z != 0:

            self.editor = True

            return
        if loc_props.location_max_x != 0:

            self.editor = True

            return
        if loc_props.location_max_y != 0:

            self.editor = True

            return
        if loc_props.location_max_z != 0:

            self.editor = True

            return
        if scale_props.scale_progressive_x != 0:

            self.editor = True

            return
        if scale_props.scale_progressive_y != 0:

            self.editor = True

            return
        if scale_props.scale_progressive_z != 0:

            self.editor = True

            return
        if scale_props.scale_min_x != 0:

            self.editor = True

            return
        if scale_props.scale_min_y != 0:

            self.editor = True

            return
        if scale_props.scale_min_z != 0:

            self.editor = True

            return
        if scale_props.scale_max_x != 0:

            self.editor = True

            return
        if scale_props.scale_max_y != 0:

            self.editor = True

            return
        if scale_props.scale_max_z != 0:

            self.editor = True

            return

    def get_scene(self):
        sc = self.editor_scene

        return sc

    def get(self):
        sc = self.editor

        return sc

transform_editor = Transform_Editor()