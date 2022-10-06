import bpy

rng = 20

def update_func(self, context):

    from Curve_Array_Magic_Curve.engine.functions import (
    object_list
    )

    object_list.update()

def update_transform(self, context):

    from Curve_Array_Magic_Curve.engine.functions import (
    transform_editor
    )

    transform_editor.update()

def Obj_Stor_Draw_Count():

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties

    count = 0

    for i in range(rng):

        index = 'obj_stor_draw_' + str(i)

        if getattr(props.object_props.object_storage_draw, index) != '':

            count += 1

    return count

def Obj_Stor_NewObj(obj_name):

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties

    for i in range(rng):

        strind = 'obj_stor_' + str(i)

        direct = getattr(props.object_props.object_storage, strind)

        if getattr(direct, 'obj_name') == '':

            setattr(direct, 'obj_name', obj_name)

            setattr(direct, 'obj_parent', 0)

            break

    return i

def Obj_Stor_Clear():

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties

    for i in range(rng):

        strind = 'obj_stor_' + str(i)

        direct = getattr(props.object_props.object_storage, strind)

        setattr(direct, 'obj_name', '')

def Obj_Stor_RemoveObj(link):

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties    

    strind = 'obj_stor_' + str(link)
    direct = getattr(props.object_props.object_storage, strind)
    setattr(direct, 'obj_name', '')
    setattr(direct, 'obj_parent', 0)

def Obj_Stor_Draw_NewObj(link):

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties

    count = Obj_Stor_Draw_Count()

    strind = 'obj_stor_draw_' + str(count)

    setattr(props.object_props.object_storage_draw, strind, str(link))

def Obj_Stor_Draw_ObjName(index):

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties

    strind = 'obj_stor_draw_' + str(index)

    id = getattr(props.object_props.object_storage_draw, strind)

    strind = 'obj_stor_' + str(id)

    name = getattr(getattr(props.object_props.object_storage, strind), 'obj_name')

    return name

def Obj_Stor_Draw_Clear():

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties

    for i in range(rng):

        strind = 'obj_stor_draw_' + str(i)

        setattr(props.object_props.object_storage_draw, strind, '')

def Obj_Stor_Draw_RemoveObj(link):

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties    
    count = Obj_Stor_Draw_Count()

    def Search(link):

        for i in range(count):

            strind = 'obj_stor_draw_' + str(i)

            if getattr(props.object_props.object_storage_draw, strind) == link:

                newlink = i

                break

        return newlink

    newlink = Search(link)

    delrng = count - 1

    index = newlink

    for i in range(index, delrng):

        strind = 'obj_stor_draw_' + str(i + 1)
        next = getattr(props.object_props.object_storage_draw, strind)

        strind = 'obj_stor_draw_' + str(i)
        setattr(props.object_props.object_storage_draw, strind, next)

    strind = 'obj_stor_draw_' + str(delrng)
    setattr(props.object_props.object_storage_draw, strind, '')

def Edit_Stor_NewObj(link):

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties

    for i in range(rng):

        strind = 'edit_stor_' + str(i)

        direct = getattr(props.object_props.editor_storage, strind)

        if getattr(direct, 'link') == '':

            setattr(direct, 'link', str(link))

            break

    return i

def Edit_Stor_Clear():

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties

    for i in range(rng):

        strind = 'edit_stor_' + str(i)

        direct = getattr(props.object_props.editor_storage, strind)

        setattr(direct, 'link', '')

def Edit_Stor_RemoveObj(link):

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties    

    strind = 'edit_stor_' + str(link)
    direct = getattr(props.object_props.editor_storage, strind)
    link = getattr(direct, 'link')
    setattr(direct, 'link', '')
    setattr(direct, 'count', 1)
    setattr(direct, 'ghost', False)
    setattr(direct, 'ghost_p', 50)

    return link

def Edit_Stor_Draw_NewObj(link):

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties

    count = Edit_Stor_Draw_Count()

    strind = 'edit_stor_draw_' + str(count)

    setattr(props.object_props.editor_storage_draw, strind, link)

def Edit_Stor_Draw_Clear():

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties

    for i in range(rng):

        strind = 'edit_stor_draw_' + str(i)

        setattr(props.object_props.editor_storage_draw, strind, -1)

def Edit_Stor_Draw_Count():

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties

    count = 0

    for i in range(rng):

        index = 'edit_stor_draw_' + str(i)

        if getattr(props.object_props.editor_storage_draw, index) != -1:

            count += 1

    return count

def Edit_Stor_Draw_ObjNameParentProp(index):

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties

    strind = 'edit_stor_draw_' + str(index)

    id = getattr(props.object_props.editor_storage_draw, strind)

    strind = 'edit_stor_' + str(id)

    prop = getattr(props.object_props.editor_storage, strind) 

    id = getattr(prop, 'link')

    if int(id) >= 0:

        strind = 'obj_stor_' + str(id)

        name = getattr(getattr(props.object_props.object_storage, strind), 'obj_name')

        parent = getattr(getattr(props.object_props.object_storage, strind), 'obj_parent')

    else:

        gr_id = abs(int(id))

        strind = 'Random Group #' + str(gr_id)
        name = strind
        parent = gr_id

    return name, parent, prop

def Edit_Stor_Draw_RemoveObj(index):

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties    

    count = Edit_Stor_Draw_Count()

    delrng = count - 1

    strind = 'edit_stor_draw_' + str(index)
    link = getattr(props.object_props.editor_storage_draw, strind)

    for i in range(index, delrng):

        strind = 'edit_stor_draw_' + str(i + 1)
        next = getattr(props.object_props.editor_storage_draw, strind)

        strind = 'edit_stor_draw_' + str(i)
        setattr(props.object_props.editor_storage_draw, strind, next)

    strind = 'edit_stor_draw_' + str(delrng)
    setattr(props.object_props.editor_storage_draw, strind, -1)

    return link

def Edit_Stor_Draw_Up(i):

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties  

    nex_strind = 'edit_stor_draw_' + str(i - 1)
    next = getattr(props.object_props.editor_storage_draw, nex_strind)

    cur_strind = 'edit_stor_draw_' + str(i)
    current = getattr(props.object_props.editor_storage_draw, cur_strind)

    setattr(props.object_props.editor_storage_draw, cur_strind, next)
    setattr(props.object_props.editor_storage_draw, nex_strind, current)

def Edit_Stor_Draw_Down(i):

    count  = Edit_Stor_Draw_Count()

    if i == (count-1):

        return

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties  

    nex_strind = 'edit_stor_draw_' + str(i + 1)
    next = getattr(props.object_props.editor_storage_draw, nex_strind)

    cur_strind = 'edit_stor_draw_' + str(i)
    current = getattr(props.object_props.editor_storage_draw, cur_strind)

    setattr(props.object_props.editor_storage_draw, cur_strind, next)
    setattr(props.object_props.editor_storage_draw, nex_strind, current)

def Edit_Stor_Draw_LinkToObj(index):

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties

    strind = 'edit_stor_draw_' + str(index)

    id = getattr(props.object_props.editor_storage_draw, strind)

    strind = 'edit_stor_' + str(id)

    prop = getattr(props.object_props.editor_storage, strind) 

    link = getattr(prop, 'link')

    return link

def Edit_Stor_New_Ran_Gr(gr):

    gr = '-'+gr

    link = Edit_Stor_NewObj(gr)

    Edit_Stor_Draw_NewObj(link)

def Ran_Gr_Count(id):

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties

    count = 0

    strind = 'random_group_' + str(id)

    direct = getattr(props.object_props, strind)

    strind = 'ran_gr_' + str(id) + '_'    

    for i in range(5):

        index = strind + str(i)

        direct_group = getattr(direct, index)

        if getattr(direct_group, 'link') != '':

            count += 1

    return count

def Ran_Gr_ObjNameParentProp(id, index):

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties

    strind = 'random_group_' + str(id)

    direct = getattr(props.object_props, strind)

    strind = 'ran_gr_' + str(id) + '_' + str(index)

    prop = getattr(direct, strind)

    link = getattr(prop, 'link')

    strind = 'obj_stor_' + str(link)

    name = getattr(getattr(props.object_props.object_storage, strind), 'obj_name')
    parent = getattr(getattr(props.object_props.object_storage, strind), 'obj_parent')

    return name, parent, prop

def Ran_Gr_LinkToObj(gr, index):

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties

    strind = 'random_group_' + str(gr)

    direct = getattr(props.object_props, strind)

    strind = 'ran_gr_' + str(gr) + '_' + str(index)

    prop = getattr(direct, strind)

    link = getattr(prop, 'link')

    return link

def Ran_Gr_AddObj(gr, link):

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties

    count = Ran_Gr_Count(gr)

    if count == 5:

        return

    strind = 'random_group_' + str(gr)

    direct = getattr(props.object_props, strind)

    strind = 'ran_gr_' + str(gr) + '_' + str(count)

    prop = getattr(direct, strind)

    setattr(prop, 'link', link)

def Ran_Gr_RemoveObj(gr, index):

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties

    count = Ran_Gr_Count(gr) - 1

    strind = 'random_group_' + str(gr)
    direct = getattr(props.object_props, strind)
    grstr = 'ran_gr_' + str(gr) + '_'

    strind =  grstr + str(index)
    prop = getattr(direct, strind)
    link = getattr(prop, 'link')

    if count <0:

        strind =  grstr + str(0)
        prop = getattr(direct, strind)
        setattr(prop, 'link', '')
        setattr(prop, 'count', 1)

        return

    for i in range(index, count):

        strind =  grstr + str(i+1)
        prop = getattr(direct, strind)
        next_link = getattr(prop, 'link')
        next_count = getattr(prop, 'count')

        strind =  grstr + str(i)
        prop = getattr(direct, strind)
        setattr(prop, 'link', next_link)
        setattr(prop, 'count', next_count)

    strind =  grstr + str(count)
    prop = getattr(direct, strind)
    setattr(prop, 'link', '')
    setattr(prop, 'count', 1)

    return link

def Ran_Gr_Clear():

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties

    for gr in range(1, 6):

        strind = 'random_group_' + str(gr)
        direct = getattr(props.object_props, strind)
        grstr = 'ran_gr_' + str(gr) + '_'

        count = Ran_Gr_Count(gr)

        for i in range(count):
        
            strind =  grstr + str(i)
            prop = getattr(direct, strind)
            setattr(prop, 'link', '')
            setattr(prop, 'count', 1)

def Ran_Gr_ObjCount(gr, index):

    active_scene = bpy.context.scene 
    props = active_scene.curve_array_properties

    strind = 'random_group_' + str(gr)

    direct = getattr(props.object_props, strind)

    strind = 'ran_gr_' + str(gr) + '_' + str(index)

    prop = getattr(direct, strind)

    count = getattr(prop, 'count')

    return count

class Obj_Stor_0(bpy.types.PropertyGroup):
    obj_name : bpy.props.StringProperty(
        name = "obj_name",
        description= "",
        default = "",
        #update=update_func
        )

    obj_parent : bpy.props.IntProperty(
        name = "obj_parent",
        description= "",
        default = 0,
        #update=update_func
        )

class Obj_Stor_1(bpy.types.PropertyGroup):
    obj_name : bpy.props.StringProperty(
        name = "obj_name",
        description= "",
        default = "",
        #update=update_func
        )

    obj_parent : bpy.props.IntProperty(
        name = "obj_parent",
        description= "",
        default = 0,
        #update=update_func
        )

class Obj_Stor_2(bpy.types.PropertyGroup):
    obj_name : bpy.props.StringProperty(
        name = "obj_name",
        description= "",
        default = "",
        #update=update_func
        )

    obj_parent : bpy.props.IntProperty(
        name = "obj_parent",
        description= "",
        default = 0,
        #update=update_func
        )

class Obj_Stor_3(bpy.types.PropertyGroup):
    obj_name : bpy.props.StringProperty(
        name = "obj_name",
        description= "",
        default = "",
        #update=update_func
        )

    obj_parent : bpy.props.IntProperty(
        name = "obj_parent",
        description= "",
        default = 0,
        #update=update_func
        )

class Obj_Stor_4(bpy.types.PropertyGroup):
    obj_name : bpy.props.StringProperty(
        name = "obj_name",
        description= "",
        default = "",
        #update=update_func
        )

    obj_parent : bpy.props.IntProperty(
        name = "obj_parent",
        description= "",
        default = 0,
        #update=update_func
        )

class Obj_Stor_5(bpy.types.PropertyGroup):
    obj_name : bpy.props.StringProperty(
        name = "obj_name",
        description= "",
        default = "",
        #update=update_func
        )

    obj_parent : bpy.props.IntProperty(
        name = "obj_parent",
        description= "",
        default = 0,
        #update=update_func
        )

class Obj_Stor_6(bpy.types.PropertyGroup):
    obj_name : bpy.props.StringProperty(
        name = "obj_name",
        description= "",
        default = "",
        #update=update_func
        )

    obj_parent : bpy.props.IntProperty(
        name = "obj_parent",
        description= "",
        default = 0,
        #update=update_func
        )

class Obj_Stor_7(bpy.types.PropertyGroup):
    obj_name : bpy.props.StringProperty(
        name = "obj_name",
        description= "",
        default = "",
        #update=update_func
        )

    obj_parent : bpy.props.IntProperty(
        name = "obj_parent",
        description= "",
        default = 0,
        #update=update_func
        )

class Obj_Stor_8(bpy.types.PropertyGroup):
    obj_name : bpy.props.StringProperty(
        name = "obj_name",
        description= "",
        default = "",
        #update=update_func
        )

    obj_parent : bpy.props.IntProperty(
        name = "obj_parent",
        description= "",
        default = 0,
        #update=update_func
        )

class Obj_Stor_9(bpy.types.PropertyGroup):
    obj_name : bpy.props.StringProperty(
        name = "obj_name",
        description= "",
        default = "",
        #update=update_func
        )

    obj_parent : bpy.props.IntProperty(
        name = "obj_parent",
        description= "",
        default = 0,
        #update=update_func
        )

class Obj_Stor_10(bpy.types.PropertyGroup):
    obj_name : bpy.props.StringProperty(
        name = "obj_name",
        description= "",
        default = "",
        #update=update_func
        )

    obj_parent : bpy.props.IntProperty(
        name = "obj_parent",
        description= "",
        default = 0,
        #update=update_func
        )

class Obj_Stor_11(bpy.types.PropertyGroup):
    obj_name : bpy.props.StringProperty(
        name = "obj_name",
        description= "",
        default = "",
        #update=update_func
        )

    obj_parent : bpy.props.IntProperty(
        name = "obj_parent",
        description= "",
        default = 0,
        #update=update_func
        )

class Obj_Stor_12(bpy.types.PropertyGroup):
    obj_name : bpy.props.StringProperty(
        name = "obj_name",
        description= "",
        default = "",
        #update=update_func
        )

    obj_parent : bpy.props.IntProperty(
        name = "obj_parent",
        description= "",
        default = 0,
        #update=update_func
        )

class Obj_Stor_13(bpy.types.PropertyGroup):
    obj_name : bpy.props.StringProperty(
        name = "obj_name",
        description= "",
        default = "",
        #update=update_func
        )

    obj_parent : bpy.props.IntProperty(
        name = "obj_parent",
        description= "",
        default = 0,
        #update=update_func
        )

class Obj_Stor_14(bpy.types.PropertyGroup):
    obj_name : bpy.props.StringProperty(
        name = "obj_name",
        description= "",
        default = "",
        #update=update_func
        )

    obj_parent : bpy.props.IntProperty(
        name = "obj_parent",
        description= "",
        default = 0,
        #update=update_func
        )

class Obj_Stor_15(bpy.types.PropertyGroup):
    obj_name : bpy.props.StringProperty(
        name = "obj_name",
        description= "",
        default = "",
        #update=update_func
        )

    obj_parent : bpy.props.IntProperty(
        name = "obj_parent",
        description= "",
        default = 0,
        #update=update_func
        )

class Obj_Stor_16(bpy.types.PropertyGroup):
    obj_name : bpy.props.StringProperty(
        name = "obj_name",
        description= "",
        default = "",
        #update=update_func
        )

    obj_parent : bpy.props.IntProperty(
        name = "obj_parent",
        description= "",
        default = 0,
        #update=update_func
        )

class Obj_Stor_17(bpy.types.PropertyGroup):
    obj_name : bpy.props.StringProperty(
        name = "obj_name",
        description= "",
        default = "",
        #update=update_func
        )

    obj_parent : bpy.props.IntProperty(
        name = "obj_parent",
        description= "",
        default = 0,
        #update=update_func
        )

class Obj_Stor_18(bpy.types.PropertyGroup):
    obj_name : bpy.props.StringProperty(
        name = "obj_name",
        description= "",
        default = "",
        #update=update_func
        )

    obj_parent : bpy.props.IntProperty(
        name = "obj_parent",
        description= "",
        default = 0,
        #update=update_func
        )

class Obj_Stor_19(bpy.types.PropertyGroup):
    obj_name : bpy.props.StringProperty(
        name = "obj_name",
        description= "",
        default = "",
        #update=update_func
        )

    obj_parent : bpy.props.IntProperty(
        name = "obj_parent",
        description= "",
        default = 0,
        #update=update_func
        )

class Edit_Stor_0(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = "",
        #update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

    ghost : bpy.props.BoolProperty(
        name = "ghost",
        description= "",
        default = False,
        update=update_func
        )

    ghost_p : bpy.props.IntProperty(
        name = "ghost_p",
        description= "",
        default = 50,
        min = 0,
        max = 100,
        update=update_func
        )

class Edit_Stor_1(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = "",
        #update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

    ghost : bpy.props.BoolProperty(
        name = "ghost",
        description= "",
        default = False,
        update=update_func
        )

    ghost_p : bpy.props.IntProperty(
        name = "ghost_p",
        description= "",
        default = 50,
        min = 0,
        max = 100,
        update=update_func
        )

class Edit_Stor_2(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = "",
        #update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

    ghost : bpy.props.BoolProperty(
        name = "ghost",
        description= "",
        default = False,
        update=update_func
        )

    ghost_p : bpy.props.IntProperty(
        name = "ghost_p",
        description= "",
        default = 50,
        min = 0,
        max = 100,
        update=update_func
        )

class Edit_Stor_3(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = "",
        #update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

    ghost : bpy.props.BoolProperty(
        name = "ghost",
        description= "",
        default = False,
        update=update_func
        )

    ghost_p : bpy.props.IntProperty(
        name = "ghost_p",
        description= "",
        default = 50,
        min = 0,
        max = 100,
        update=update_func
        )

class Edit_Stor_4(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = "",
        #update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

    ghost : bpy.props.BoolProperty(
        name = "ghost",
        description= "",
        default = False,
        update=update_func
        )

    ghost_p : bpy.props.IntProperty(
        name = "ghost_p",
        description= "",
        default = 50,
        min = 0,
        max = 100,
        update=update_func
        )

class Edit_Stor_5(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = "",
        #update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

    ghost : bpy.props.BoolProperty(
        name = "ghost",
        description= "",
        default = False,
        update=update_func
        )

    ghost_p : bpy.props.IntProperty(
        name = "ghost_p",
        description= "",
        default = 50,
        min = 0,
        max = 100,
        update=update_func
        )

class Edit_Stor_6(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = "",
        #update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

    ghost : bpy.props.BoolProperty(
        name = "ghost",
        description= "",
        default = False,
        update=update_func
        )

    ghost_p : bpy.props.IntProperty(
        name = "ghost_p",
        description= "",
        default = 50,
        min = 0,
        max = 100,
        update=update_func
        )

class Edit_Stor_7(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = "",
        #update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

    ghost : bpy.props.BoolProperty(
        name = "ghost",
        description= "",
        default = False,
        update=update_func
        )

    ghost_p : bpy.props.IntProperty(
        name = "ghost_p",
        description= "",
        default = 50,
        min = 0,
        max = 100,
        update=update_func
        )

class Edit_Stor_8(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = "",
        #update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

    ghost : bpy.props.BoolProperty(
        name = "ghost",
        description= "",
        default = False,
        update=update_func
        )

    ghost_p : bpy.props.IntProperty(
        name = "ghost_p",
        description= "",
        default = 50,
        min = 0,
        max = 100,
        update=update_func
        )

class Edit_Stor_9(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = "",
        #update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

    ghost : bpy.props.BoolProperty(
        name = "ghost",
        description= "",
        default = False,
        update=update_func
        )

    ghost_p : bpy.props.IntProperty(
        name = "ghost_p",
        description= "",
        default = 50,
        min = 0,
        max = 100,
        update=update_func
        )

class Edit_Stor_10(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = "",
        #update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

    ghost : bpy.props.BoolProperty(
        name = "ghost",
        description= "",
        default = False,
        update=update_func
        )

    ghost_p : bpy.props.IntProperty(
        name = "ghost_p",
        description= "",
        default = 50,
        min = 0,
        max = 100,
        update=update_func
        )

class Edit_Stor_11(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = "",
        #update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

    ghost : bpy.props.BoolProperty(
        name = "ghost",
        description= "",
        default = False,
        update=update_func
        )

    ghost_p : bpy.props.IntProperty(
        name = "ghost_p",
        description= "",
        default = 50,
        min = 0,
        max = 100,
        update=update_func
        )

class Edit_Stor_12(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = "",
        #update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

    ghost : bpy.props.BoolProperty(
        name = "ghost",
        description= "",
        default = False,
        update=update_func
        )

    ghost_p : bpy.props.IntProperty(
        name = "ghost_p",
        description= "",
        default = 50,
        min = 0,
        max = 100,
        update=update_func
        )

class Edit_Stor_13(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = "",
        #update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

    ghost : bpy.props.BoolProperty(
        name = "ghost",
        description= "",
        default = False,
        update=update_func
        )

    ghost_p : bpy.props.IntProperty(
        name = "ghost_p",
        description= "",
        default = 50,
        min = 0,
        max = 100,
        update=update_func
        )

class Edit_Stor_14(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = "",
        #update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

    ghost : bpy.props.BoolProperty(
        name = "ghost",
        description= "",
        default = False,
        update=update_func
        )

    ghost_p : bpy.props.IntProperty(
        name = "ghost_p",
        description= "",
        default = 50,
        min = 0,
        max = 100,
        update=update_func
        )

class Edit_Stor_15(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = "",
        #update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

    ghost : bpy.props.BoolProperty(
        name = "ghost",
        description= "",
        default = False,
        update=update_func
        )

    ghost_p : bpy.props.IntProperty(
        name = "ghost_p",
        description= "",
        default = 50,
        min = 0,
        max = 100,
        update=update_func
        )

class Edit_Stor_16(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = "",
        #update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

    ghost : bpy.props.BoolProperty(
        name = "ghost",
        description= "",
        default = False,
        update=update_func
        )

    ghost_p : bpy.props.IntProperty(
        name = "ghost_p",
        description= "",
        default = 50,
        min = 0,
        max = 100,
        update=update_func
        )

class Edit_Stor_17(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = "",
        #update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

    ghost : bpy.props.BoolProperty(
        name = "ghost",
        description= "",
        default = False,
        update=update_func
        )

    ghost_p : bpy.props.IntProperty(
        name = "ghost_p",
        description= "",
        default = 50,
        min = 0,
        max = 100,
        update=update_func
        )

class Edit_Stor_18(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = "",
        #update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

    ghost : bpy.props.BoolProperty(
        name = "ghost",
        description= "",
        default = False,
        update=update_func
        )

    ghost_p : bpy.props.IntProperty(
        name = "ghost_p",
        description= "",
        default = 50,
        min = 0,
        max = 100,
        update=update_func
        )

class Edit_Stor_19(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = "",
        #update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

    ghost : bpy.props.BoolProperty(
        name = "ghost",
        description= "",
        default = False,
        update=update_func
        )

    ghost_p : bpy.props.IntProperty(
        name = "ghost_p",
        description= "",
        default = 50,
        min = 0,
        max = 100,
        update=update_func
        )

class Editor_Storage_Draw(bpy.types.PropertyGroup):

    edit_stor_draw_0 : bpy.props.IntProperty(
        name = "edit_stor_draw_0",
        description= "",
        default = -1,
        update=update_func
        )

    edit_stor_draw_1 : bpy.props.IntProperty(
        name = "edit_stor_draw_1",
        description= "",
        default = -1,
        update=update_func
        )

    edit_stor_draw_2 : bpy.props.IntProperty(
        name = "edit_stor_draw_2",
        description= "",
        default = -1,
        update=update_func
        )

    edit_stor_draw_3 : bpy.props.IntProperty(
        name = "edit_stor_draw_3",
        description= "",
        default = -1,
        update=update_func
        )

    edit_stor_draw_4 : bpy.props.IntProperty(
        name = "edit_stor_draw_4",
        description= "",
        default = -1,
        update=update_func
        )

    edit_stor_draw_5 : bpy.props.IntProperty(
        name = "edit_stor_draw_5",
        description= "",
        default = -1,
        update=update_func
        )

    edit_stor_draw_6 : bpy.props.IntProperty(
        name = "edit_stor_draw_6",
        description= "",
        default = -1,
        update=update_func
        )

    edit_stor_draw_7 : bpy.props.IntProperty(
        name = "edit_stor_draw_7",
        description= "",
        default = -1,
        update=update_func
        )

    edit_stor_draw_8 : bpy.props.IntProperty(
        name = "edit_stor_draw_8",
        description= "",
        default = -1,
        update=update_func
        )

    edit_stor_draw_9 : bpy.props.IntProperty(
        name = "edit_stor_draw_9",
        description= "",
        default = -1,
        update=update_func
        )

    edit_stor_draw_10 : bpy.props.IntProperty(
        name = "edit_stor_draw_10",
        description= "",
        default = -1,
        update=update_func
        )

    edit_stor_draw_11 : bpy.props.IntProperty(
        name = "edit_stor_draw_11",
        description= "",
        default = -1,
        update=update_func
        )

    edit_stor_draw_12 : bpy.props.IntProperty(
        name = "edit_stor_draw_12",
        description= "",
        default = -1,
        update=update_func
        )

    edit_stor_draw_13 : bpy.props.IntProperty(
        name = "edit_stor_draw_13",
        description= "",
        default = -1,
        update=update_func
        )

    edit_stor_draw_14 : bpy.props.IntProperty(
        name = "edit_stor_draw_14",
        description= "",
        default = -1,
        update=update_func
        )

    edit_stor_draw_15 : bpy.props.IntProperty(
        name = "edit_stor_draw_15",
        description= "",
        default = -1,
        update=update_func
        )

    edit_stor_draw_16 : bpy.props.IntProperty(
        name = "edit_stor_draw_16",
        description= "",
        default = -1,
        update=update_func
        )

    edit_stor_draw_17 : bpy.props.IntProperty(
        name = "edit_stor_draw_17",
        description= "",
        default = -1,
        update=update_func
        )

    edit_stor_draw_18 : bpy.props.IntProperty(
        name = "edit_stor_draw_18",
        description= "",
        default = -1,
        update=update_func
        )

    edit_stor_draw_19 : bpy.props.IntProperty(
        name = "edit_stor_draw_19",
        description= "",
        default = -1,
        update=update_func
        )

class Ran_Gr_1_0(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_1_1(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_1_2(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_1_3(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_1_4(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_2_0(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_2_1(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_2_2(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_2_3(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_2_4(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_3_0(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_3_1(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_3_2(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_3_3(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_3_4(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_4_0(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_4_1(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_4_2(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_4_3(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_4_4(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_5_0(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_5_1(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_5_2(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_5_3(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Ran_Gr_5_4(bpy.types.PropertyGroup):
    link : bpy.props.StringProperty(
        name = "link",
        description= "",
        default = '',
        update=update_func
        )

    count : bpy.props.IntProperty(
        name = "count",
        description= "",
        default = 1,
        min = 0,
        update=update_func
        )

class Random_Group_5(bpy.types.PropertyGroup):

    ran_gr_5_0 : bpy.props.PointerProperty(
        type = Ran_Gr_5_0,
        name = "ran_gr_5_0",
        description=""
        )

    ran_gr_5_1 : bpy.props.PointerProperty(
        type = Ran_Gr_5_1,
        name = "ran_gr_5_1",
        description=""
        )

    ran_gr_5_2 : bpy.props.PointerProperty(
        type = Ran_Gr_5_2,
        name = "ran_gr_5_2",
        description=""
        )

    ran_gr_5_3 : bpy.props.PointerProperty(
        type = Ran_Gr_5_3,
        name = "ran_gr_5_3",
        description=""
        )

    ran_gr_5_4 : bpy.props.PointerProperty(
        type = Ran_Gr_5_4,
        name = "ran_gr_5_4",
        description=""
        )

class Random_Group_4(bpy.types.PropertyGroup):

    ran_gr_4_0 : bpy.props.PointerProperty(
        type = Ran_Gr_4_0,
        name = "ran_gr_4_0",
        description=""
        )

    ran_gr_4_1 : bpy.props.PointerProperty(
        type = Ran_Gr_4_1,
        name = "ran_gr_4_1",
        description=""
        )

    ran_gr_4_2 : bpy.props.PointerProperty(
        type = Ran_Gr_4_2,
        name = "ran_gr_4_2",
        description=""
        )

    ran_gr_4_3 : bpy.props.PointerProperty(
        type = Ran_Gr_4_3,
        name = "ran_gr_4_3",
        description=""
        )

    ran_gr_4_4 : bpy.props.PointerProperty(
        type = Ran_Gr_4_4,
        name = "ran_gr_4_4",
        description=""
        )

class Random_Group_3(bpy.types.PropertyGroup):

    ran_gr_3_0 : bpy.props.PointerProperty(
        type = Ran_Gr_3_0,
        name = "ran_gr_3_0",
        description=""
        )

    ran_gr_3_1 : bpy.props.PointerProperty(
        type = Ran_Gr_3_1,
        name = "ran_gr_3_1",
        description=""
        )

    ran_gr_3_2 : bpy.props.PointerProperty(
        type = Ran_Gr_3_2,
        name = "ran_gr_3_2",
        description=""
        )

    ran_gr_3_3 : bpy.props.PointerProperty(
        type = Ran_Gr_3_3,
        name = "ran_gr_3_3",
        description=""
        )

    ran_gr_3_4 : bpy.props.PointerProperty(
        type = Ran_Gr_3_4,
        name = "ran_gr_3_4",
        description=""
        )

class Random_Group_2(bpy.types.PropertyGroup):

    ran_gr_2_0 : bpy.props.PointerProperty(
        type = Ran_Gr_2_0,
        name = "ran_gr_2_0",
        description=""
        )

    ran_gr_2_1 : bpy.props.PointerProperty(
        type = Ran_Gr_2_1,
        name = "ran_gr_2_1",
        description=""
        )

    ran_gr_2_2 : bpy.props.PointerProperty(
        type = Ran_Gr_2_2,
        name = "ran_gr_2_2",
        description=""
        )

    ran_gr_2_3 : bpy.props.PointerProperty(
        type = Ran_Gr_2_3,
        name = "ran_gr_2_3",
        description=""
        )

    ran_gr_2_4 : bpy.props.PointerProperty(
        type = Ran_Gr_2_4,
        name = "ran_gr_2_4",
        description=""
        )

class Random_Group_1(bpy.types.PropertyGroup):

    ran_gr_1_0 : bpy.props.PointerProperty(
        type = Ran_Gr_1_0,
        name = "ran_gr_1_0",
        description=""
        )

    ran_gr_1_1 : bpy.props.PointerProperty(
        type = Ran_Gr_1_1,
        name = "ran_gr_1_1",
        description=""
        )

    ran_gr_1_2 : bpy.props.PointerProperty(
        type = Ran_Gr_1_2,
        name = "ran_gr_1_2",
        description=""
        )

    ran_gr_1_3 : bpy.props.PointerProperty(
        type = Ran_Gr_1_3,
        name = "ran_gr_1_3",
        description=""
        )

    ran_gr_1_4 : bpy.props.PointerProperty(
        type = Ran_Gr_1_4,
        name = "ran_gr_1_4",
        description=""
        )

class Object_Storage_Draw(bpy.types.PropertyGroup):

    obj_stor_draw_0 : bpy.props.StringProperty(
        name = "obj_stor_draw_0",
        description= "",
        default = '',
        update=update_func
        )

    obj_stor_draw_1 : bpy.props.StringProperty(
        name = "obj_stor_draw_1",
        description= "",
        default = '',
        update=update_func
        )

    obj_stor_draw_2 : bpy.props.StringProperty(
        name = "obj_stor_draw_2",
        description= "",
        default = '',
        update=update_func
        )

    obj_stor_draw_3 : bpy.props.StringProperty(
        name = "obj_stor_draw_3",
        description= "",
        default = '',
        update=update_func
        )

    obj_stor_draw_4 : bpy.props.StringProperty(
        name = "obj_stor_draw_4",
        description= "",
        default = '',
        update=update_func
        )

    obj_stor_draw_5 : bpy.props.StringProperty(
        name = "obj_stor_draw_5",
        description= "",
        default = '',
        update=update_func
        )

    obj_stor_draw_6 : bpy.props.StringProperty(
        name = "obj_stor_draw_6",
        description= "",
        default = '',
        update=update_func
        )

    obj_stor_draw_7 : bpy.props.StringProperty(
        name = "obj_stor_draw_7",
        description= "",
        default = '',
        update=update_func
        )

    obj_stor_draw_8 : bpy.props.StringProperty(
        name = "obj_stor_draw_8",
        description= "",
        default = '',
        update=update_func
        )

    obj_stor_draw_9 : bpy.props.StringProperty(
        name = "obj_stor_draw_9",
        description= "",
        default = '',
        update=update_func
        )

    obj_stor_draw_10 : bpy.props.StringProperty(
        name = "obj_stor_draw_10",
        description= "",
        default = '',
        update=update_func
        )

    obj_stor_draw_11 : bpy.props.StringProperty(
        name = "obj_stor_draw_11",
        description= "",
        default = '',
        update=update_func
        )

    obj_stor_draw_12 : bpy.props.StringProperty(
        name = "obj_stor_draw_12",
        description= "",
        default = '',
        update=update_func
        )

    obj_stor_draw_13 : bpy.props.StringProperty(
        name = "obj_stor_draw_13",
        description= "",
        default = '',
        update=update_func
        )

    obj_stor_draw_14 : bpy.props.StringProperty(
        name = "obj_stor_draw_14",
        description= "",
        default = '',
        update=update_func
        )

    obj_stor_draw_15 : bpy.props.StringProperty(
        name = "obj_stor_draw_15",
        description= "",
        default = '',
        update=update_func
        )

    obj_stor_draw_16 : bpy.props.StringProperty(
        name = "obj_stor_draw_16",
        description= "",
        default = '',
        update=update_func
        )

    obj_stor_draw_17 : bpy.props.StringProperty(
        name = "obj_stor_draw_17",
        description= "",
        default = '',
        update=update_func
        )

    obj_stor_draw_18 : bpy.props.StringProperty(
        name = "obj_stor_draw_18",
        description= "",
        default = '',
        update=update_func
        )

    obj_stor_draw_19 : bpy.props.StringProperty(
        name = "obj_stor_draw_19",
        description= "",
        default = '',
        update=update_func
        )

class Editor_Storage(bpy.types.PropertyGroup):

    edit_stor_0 : bpy.props.PointerProperty(
        type = Edit_Stor_0,
        name = "edit_stor_0",
        description=""
        )

    edit_stor_1 : bpy.props.PointerProperty(
        type = Edit_Stor_1,
        name = "edit_stor_1",
        description=""
        )

    edit_stor_2 : bpy.props.PointerProperty(
        type = Edit_Stor_2,
        name = "edit_stor_2",
        description=""
        )

    edit_stor_3 : bpy.props.PointerProperty(
        type = Edit_Stor_3,
        name = "edit_stor_3",
        description=""
        )

    edit_stor_4 : bpy.props.PointerProperty(
        type = Edit_Stor_4,
        name = "edit_stor_4",
        description=""
        )

    edit_stor_5 : bpy.props.PointerProperty(
        type = Edit_Stor_5,
        name = "edit_stor_5",
        description=""
        )

    edit_stor_6 : bpy.props.PointerProperty(
        type = Edit_Stor_6,
        name = "edit_stor_6",
        description=""
        )

    edit_stor_7 : bpy.props.PointerProperty(
        type = Edit_Stor_7,
        name = "edit_stor_7",
        description=""
        )

    edit_stor_8 : bpy.props.PointerProperty(
        type = Edit_Stor_8,
        name = "edit_stor_8",
        description=""
        )

    edit_stor_9 : bpy.props.PointerProperty(
        type = Edit_Stor_9,
        name = "edit_stor_9",
        description=""
        )

    edit_stor_10 : bpy.props.PointerProperty(
        type = Edit_Stor_10,
        name = "edit_stor_10",
        description=""
        )

    edit_stor_11 : bpy.props.PointerProperty(
        type = Edit_Stor_11,
        name = "edit_stor_11",
        description=""
        )

    edit_stor_12 : bpy.props.PointerProperty(
        type = Edit_Stor_12,
        name = "edit_stor_12",
        description=""
        )

    edit_stor_13 : bpy.props.PointerProperty(
        type = Edit_Stor_13,
        name = "edit_stor_13",
        description=""
        )

    edit_stor_14 : bpy.props.PointerProperty(
        type = Edit_Stor_14,
        name = "edit_stor_14",
        description=""
        )

    edit_stor_15 : bpy.props.PointerProperty(
        type = Edit_Stor_15,
        name = "edit_stor_15",
        description=""
        )

    edit_stor_16 : bpy.props.PointerProperty(
        type = Edit_Stor_16,
        name = "edit_stor_16",
        description=""
        )

    edit_stor_17 : bpy.props.PointerProperty(
        type = Edit_Stor_17,
        name = "edit_stor_17",
        description=""
        )

    edit_stor_18 : bpy.props.PointerProperty(
        type = Edit_Stor_18,
        name = "edit_stor_18",
        description=""
        )

    edit_stor_19 : bpy.props.PointerProperty(
        type = Edit_Stor_19,
        name = "edit_stor_19",
        description=""
        )

class Object_Storage(bpy.types.PropertyGroup):

    obj_stor_0 : bpy.props.PointerProperty(
        type = Obj_Stor_0,
        name = "obj_stor_0",
        description="",
        )

    obj_stor_1 : bpy.props.PointerProperty(
        type = Obj_Stor_1,
        name = "obj_stor_1",
        description=""
        )

    obj_stor_2 : bpy.props.PointerProperty(
        type = Obj_Stor_2,
        name = "obj_stor_2",
        description=""
        )

    obj_stor_3 : bpy.props.PointerProperty(
        type = Obj_Stor_3,
        name = "obj_stor_3",
        description=""
        )

    obj_stor_4 : bpy.props.PointerProperty(
        type = Obj_Stor_4,
        name = "obj_stor_4",
        description=""
        )

    obj_stor_5 : bpy.props.PointerProperty(
        type = Obj_Stor_5,
        name = "obj_stor_5",
        description=""
        )

    obj_stor_6 : bpy.props.PointerProperty(
        type = Obj_Stor_6,
        name = "obj_stor_6",
        description=""
        )

    obj_stor_7 : bpy.props.PointerProperty(
        type = Obj_Stor_7,
        name = "obj_stor_7",
        description=""
        )

    obj_stor_8 : bpy.props.PointerProperty(
        type = Obj_Stor_8,
        name = "obj_stor_8",
        description=""
        )

    obj_stor_9 : bpy.props.PointerProperty(
        type = Obj_Stor_9,
        name = "obj_stor_9",
        description=""
        )

    obj_stor_10 : bpy.props.PointerProperty(
        type = Obj_Stor_10,
        name = "obj_stor_10",
        description=""
        )

    obj_stor_11 : bpy.props.PointerProperty(
        type = Obj_Stor_11,
        name = "obj_stor_11",
        description=""
        )

    obj_stor_12 : bpy.props.PointerProperty(
        type = Obj_Stor_12,
        name = "obj_stor_12",
        description=""
        )

    obj_stor_13 : bpy.props.PointerProperty(
        type = Obj_Stor_13,
        name = "obj_stor_13",
        description=""
        )

    obj_stor_14 : bpy.props.PointerProperty(
        type = Obj_Stor_14,
        name = "obj_stor_14",
        description=""
        )

    obj_stor_15 : bpy.props.PointerProperty(
        type = Obj_Stor_15,
        name = "obj_stor_15",
        description=""
        )

    obj_stor_16 : bpy.props.PointerProperty(
        type = Obj_Stor_16,
        name = "obj_stor_16",
        description=""
        )

    obj_stor_17 : bpy.props.PointerProperty(
        type = Obj_Stor_17,
        name = "obj_stor_17",
        description=""
        )

    obj_stor_18 : bpy.props.PointerProperty(
        type = Obj_Stor_18,
        name = "obj_stor_18",
        description=""
        )

    obj_stor_19 : bpy.props.PointerProperty(
        type = Obj_Stor_19,
        name = "obj_stor_19",
        description=""
        )

class Path_Props(bpy.types.PropertyGroup):

    path_name : bpy.props.StringProperty(
        name = "path_name",
        description="",
        default = ""
        )

    path_icon : bpy.props.StringProperty(
        name = "path_icon",
        description="",
        default = 'UNLOCKED'
        )

class Array_Settings(bpy.types.PropertyGroup):

    last_array : bpy.props.StringProperty(
        name = "last_array",
        description= "",
        default = ''
        )

    set_group : bpy.props.EnumProperty(
        name = "",
        description="Select group",
        items = (
            ('0',"Main Group",""),
            ('1',"Random Group #1",""),
            ('2',"Random Group #2",""),
            ('3',"Random Group #3",""),
            ('4',"Random Group #4",""),
            ('5',"Random Group #5","")
        )
        )
        
    slide : bpy.props.FloatProperty(
        name = "slide ",
        description="slide along path",
        default = 0,
        )
                        
    count : bpy.props.IntProperty(
        name = "count",
        description="Count of objects in array",
        default = 1,
        min = 1,
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
        items = [
            ('OP1',"Constant","Add a constant offset"),
            ('OP2',"Relative","Add an offset relative to the object's bounding box")
        ]
        )
        
    cloning_type : bpy.props.EnumProperty(
        name = "",
        description="Select type of cloning",
        items = [
            ('OP3',"Real instance (Light)","All objects use main object data, and copy queue_transform"),
            ('OP2',"Real instance","All objects use main object data, but have a custom queue_transform"),
            ('OP1',"Usual Copy","Every object is unique")
        ]
        )

    enable_parenting : bpy.props.BoolProperty(
        name = "enable_parenting",
        description="Enable parenting",
        default = False
        )

    spacing_type : bpy.props.EnumProperty(
        name = "",
        description="Select type of spacing",
        items = [
            ('OP1',"Fill by count","Uniform filling of the entire length"),
            ('OP2',"Fill by offset","Uniform filling of the entire length"),
            ('OP3',"Free","Free mode")
        ]
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

    x_axis : bpy.props.BoolProperty(
        name = "x_axis",
        description="Align x axis rotation",
        default = True       
        )

    y_axis : bpy.props.BoolProperty(
        name = "y_axis",
        description="Align y axis rotation",
        default = True
        )

    z_axis : bpy.props.BoolProperty(
        name = "z_axis",
        description="Align y axis rotation",
        default = True
        )
                
    size_ofset : bpy.props.BoolProperty(
        name = "size_ofset",
        description="Take into account the size of the object",
        default = False
        )
        
    rail_axis : bpy.props.EnumProperty(
        name = "",
        description="Select type of spacing",
        items = [
            ('+x',"X","Rail +x"),
            ('+y',"Y","Rail +y"),
            ('+z',"Z","Rail +z"),
            ('-y',"-Y","Rail -y"),
            ('-x',"-X","Rail -x"),
            ('-z',"-Z","Rail -z")
        ]
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
        update = update_func
        )

class Rotation_Trform(bpy.types.PropertyGroup):

    rotation_progressive_x : bpy.props.FloatProperty(
        name = "rotation_progressive_x",
        description= "",
        default = 0,
        min = -360,
        max = 360,
        update = update_transform
        )

    rotation_min_x : bpy.props.FloatProperty(
        name = "rotation_min_x",
        description= "",
        default = 0,
        min = -360,
        max = 360,
        update = update_transform
        )

    rotation_max_x : bpy.props.FloatProperty(
        name = "rotation_max_x",
        description= "",
        default = 0,
        min = -360,
        max = 360,
        update = update_transform
        )

    rotation_progressive_y : bpy.props.FloatProperty(
        name = "rotation_progressive_y",
        description= "",
        default = 0,
        min = -360,
        max = 360,
        update = update_transform
        )

    rotation_min_y : bpy.props.FloatProperty(
        name = "rotation_min_y",
        description= "",
        default = 0,
        min = -360,
        max = 360,
        update = update_transform
        )

    rotation_max_y : bpy.props.FloatProperty(
        name = "rotation_max_y",
        description= "",
        default = 0,
        min = -360,
        max = 360,
        update = update_transform
        )

    rotation_progressive_z : bpy.props.FloatProperty(
        name = "rotation_progressive_z",
        description= "",
        default = 0,
        min = -360,
        max = 360,
        update = update_transform
        )

    rotation_min_z : bpy.props.FloatProperty(
        name = "rotation_min_z",
        description= "",
        default = 0,
        min = -360,
        max = 360,
        update = update_transform
        )

    rotation_max_z : bpy.props.FloatProperty(
        name = "rotation_max_z",
        description= "",
        default = 0,
        min = -360,
        max = 360,
        update = update_transform
        )

class Location_Trform(bpy.types.PropertyGroup):

    location_progressive_x : bpy.props.FloatProperty(
        name = "location_progressive_x",
        description= "",
        default = 0,
        update = update_transform
        )

    location_min_x : bpy.props.FloatProperty(
        name = "location_min_x",
        description= "",
        default = 0,
        update = update_transform
        )

    location_max_x : bpy.props.FloatProperty(
        name = "location_max_x",
        description= "",
        default = 0,
        update = update_transform
        )

    location_progressive_y : bpy.props.FloatProperty(
        name = "location_progressive_y",
        description= "",
        default = 0,
        update = update_transform
        )

    location_min_y : bpy.props.FloatProperty(
        name = "location_min_y",
        description= "",
        default = 0,
        update = update_transform
        )

    location_max_y : bpy.props.FloatProperty(
        name = "location_max_y",
        description= "",
        default = 0,
        update = update_transform
        )

    location_progressive_z : bpy.props.FloatProperty(
        name = "location_progressive_z",
        description= "",
        default = 0,
        update = update_transform
        )

    location_min_z : bpy.props.FloatProperty(
        name = "location_min_z",
        description= "",
        default = 0,
        update = update_transform
        )

    location_max_z : bpy.props.FloatProperty(
        name = "location_max_z",
        description= "",
        default = 0,
        update = update_transform
        )

class Scale_Trform(bpy.types.PropertyGroup):

    scale_progressive_x : bpy.props.FloatProperty(
        name = "scale_progressive_x",
        description= "",
        default = 0,
        update = update_transform
        )

    scale_min_x : bpy.props.FloatProperty(
        name = "scale_min_x",
        description= "",
        default = 0,
        update = update_transform
        )

    scale_max_x : bpy.props.FloatProperty(
        name = "scale_max_x",
        description= "",
        default = 0,
        update = update_transform
        )

    scale_progressive_y : bpy.props.FloatProperty(
        name = "scale_progressive_y",
        description= "",
        default = 0,
        update = update_transform
        )

    scale_min_y : bpy.props.FloatProperty(
        name = "scale_min_y",
        description= "",
        default = 0,
        update = update_transform
        )

    scale_max_y : bpy.props.FloatProperty(
        name = "scale_max_y",
        description= "",
        default = 0,
        update = update_transform
        )

    scale_progressive_z : bpy.props.FloatProperty(
        name = "scale_progressive_z",
        description= "",
        default = 0,
        update = update_transform
        )

    scale_min_z : bpy.props.FloatProperty(
        name = "scale_min_z",
        description= "",
        default = 0,
        update = update_transform
        )

    scale_max_z : bpy.props.FloatProperty(
        name = "scale_max_z",
        description= "",
        default = 0,
        update = update_transform
        )

class Settings_Pointer(bpy.types.PropertyGroup):

    array_settings : bpy.props.PointerProperty(
        type = Array_Settings,
        name = "array_settings",
        description=""
        )

class Object_Pointer(bpy.types.PropertyGroup):

    object_storage : bpy.props.PointerProperty(
        type = Object_Storage,
        name = "object_storage",
        description=""
        )

    object_storage_draw : bpy.props.PointerProperty(
        type = Object_Storage_Draw,
        name = "object_storage_draw",
        description=""
        )
    
    editor_storage : bpy.props.PointerProperty(
        type = Editor_Storage,
        name = "editor_storage",
        description=""
        )

    editor_storage_draw : bpy.props.PointerProperty(
        type = Editor_Storage_Draw,
        name = "editor_storage_draw",
        description=""
        )

    random_group_1 : bpy.props.PointerProperty(
        type = Random_Group_1,
        name = "random_group_1",
        description=""
        )

    random_group_2 : bpy.props.PointerProperty(
        type = Random_Group_2,
        name = "random_group_2",
        description=""
        )

    random_group_3 : bpy.props.PointerProperty(
        type = Random_Group_3,
        name = "random_group_3",
        description=""
        )

    random_group_4 : bpy.props.PointerProperty(
        type = Random_Group_4,
        name = "random_group_4",
        description=""
        )

    random_group_5 : bpy.props.PointerProperty(
        type = Random_Group_5,
        name = "random_group_5",
        description=""
        )

class Path_Pointer(bpy.types.PropertyGroup):

    path_main : bpy.props.PointerProperty(
        type = Path_Props,
        name = "path_main",
        description=""
        )

class Transform_Pointer(bpy.types.PropertyGroup):

    rotation_trform : bpy.props.PointerProperty(
        type = Rotation_Trform,
        name = "rotation_trform",
        description=""
        )

    location_trform : bpy.props.PointerProperty(
        type = Location_Trform,
        name = "location_trform",
        description=""
        )

    scale_trform : bpy.props.PointerProperty(
        type = Scale_Trform,
        name = "scale_trform",
        description=""
        )

class Main_Props(bpy.types.PropertyGroup):

    path_props : bpy.props.PointerProperty(
        type = Path_Pointer,
        name = "path_props",
        description=""
        )

    object_props : bpy.props.PointerProperty(
        type = Object_Pointer,
        name = "object_props",
        description=""
        )

    transform_props : bpy.props.PointerProperty(
        type = Transform_Pointer,
        name = "transform_props",
        description=""
        )

    other_props : bpy.props.PointerProperty(
        type = Settings_Pointer,
        name = "other_props",
        description=""
        )

reg_0 = [
Obj_Stor_0,
Obj_Stor_1,
Obj_Stor_2,
Obj_Stor_3,
Obj_Stor_4,
Obj_Stor_5,
Obj_Stor_6,
Obj_Stor_7,
Obj_Stor_8,
Obj_Stor_9,
Obj_Stor_10,
Obj_Stor_11,
Obj_Stor_12,
Obj_Stor_13,
Obj_Stor_14,
Obj_Stor_15,
Obj_Stor_16,
Obj_Stor_17,
Obj_Stor_18,
Obj_Stor_19,
Edit_Stor_0,
Edit_Stor_1,
Edit_Stor_2,
Edit_Stor_3,
Edit_Stor_4,
Edit_Stor_5,
Edit_Stor_6,
Edit_Stor_7,
Edit_Stor_8,
Edit_Stor_9,
Edit_Stor_10,
Edit_Stor_11,
Edit_Stor_12,
Edit_Stor_13,
Edit_Stor_14,
Edit_Stor_15,
Edit_Stor_16,
Edit_Stor_17,
Edit_Stor_18,
Edit_Stor_19,
Ran_Gr_1_0,
Ran_Gr_1_1,
Ran_Gr_1_2,
Ran_Gr_1_3,
Ran_Gr_1_4,
Ran_Gr_2_0,
Ran_Gr_2_1,
Ran_Gr_2_2,
Ran_Gr_2_3,
Ran_Gr_2_4,
Ran_Gr_3_0,
Ran_Gr_3_1,
Ran_Gr_3_2,
Ran_Gr_3_3,
Ran_Gr_3_4,
Ran_Gr_4_0,
Ran_Gr_4_1,
Ran_Gr_4_2,
Ran_Gr_4_3,
Ran_Gr_4_4,
Ran_Gr_5_0,
Ran_Gr_5_1,
Ran_Gr_5_2,
Ran_Gr_5_3,
Ran_Gr_5_4
]

reg_1 = [
Array_Settings,
Path_Props,
Object_Storage,
Object_Storage_Draw,
Editor_Storage,
Editor_Storage_Draw,
Random_Group_1,
Random_Group_2,
Random_Group_3,
Random_Group_4,
Random_Group_5,
Rotation_Trform,
Location_Trform,
Scale_Trform
]

reg_2 = [
Path_Pointer,
Object_Pointer,
Settings_Pointer,
Transform_Pointer,
]