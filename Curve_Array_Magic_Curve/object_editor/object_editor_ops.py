import bpy

from Curve_Array_Magic_Curve.props.curve_array_props import (
Obj_Stor_Draw_Count,
Obj_Stor_NewObj,
Obj_Stor_Clear,
Obj_Stor_Draw_NewObj,
Obj_Stor_Draw_Clear,
Obj_Stor_Draw_ObjName,
Edit_Stor_NewObj,
Edit_Stor_Clear,
Edit_Stor_Draw_NewObj,
Edit_Stor_Draw_Clear,
Edit_Stor_Draw_Count,
Edit_Stor_Draw_ObjNameParentProp,
Ran_Gr_Count,
Ran_Gr_ObjNameParentProp,
Edit_Stor_Draw_RemoveObj,
Edit_Stor_RemoveObj,
Obj_Stor_RemoveObj,
Obj_Stor_Draw_RemoveObj,
Edit_Stor_Draw_Up,
Edit_Stor_Draw_Down,
Edit_Stor_Draw_LinkToObj,
Ran_Gr_LinkToObj,
Ran_Gr_AddObj,
Ran_Gr_RemoveObj,
Ran_Gr_Clear,
Ran_Gr_ObjCount,
Edit_Stor_New_Ran_Gr
)

def CheckRG(rg):

    count = Edit_Stor_Draw_Count()

    y = True

    rg_ind = ('-' + str(rg))

    for i in range(count):

        link = Edit_Stor_Draw_LinkToObj(i)

        if link == rg_ind:

            y = False

            break

    return y

def RemoveObj(i):

    link = Edit_Stor_Draw_RemoveObj(i)

    link = Edit_Stor_RemoveObj(link)

    if int(link) <0:

        return 

    Obj_Stor_RemoveObj(link)
    Obj_Stor_Draw_RemoveObj(link)

def Chance(rg, index):

    m = Ran_Gr_ObjCount(rg, index)

    n = 0

    count = Ran_Gr_Count(rg)

    for i in range(count):

        cou = Ran_Gr_ObjCount(rg, i)

        n += cou    

    try:

        chance = round((float((m/n)*100)),1)

    except:

        chance = float(0)

    return chance

def RemoveObjFromRG(rg, index):

    link = Ran_Gr_RemoveObj(rg, index)
    Obj_Stor_RemoveObj(link)
    Obj_Stor_Draw_RemoveObj(link)

class CRVARRPRO_OT_ObjectEditor(bpy.types.Operator):
    '''Editing Objects which will be used for array creation'''
    bl_label = "Object Editor"
    bl_idname = 'crvarrpro.object_editor'
    bl_options = {'UNDO'}
        
    def draw(self, context):    
        active_scene = bpy.context.scene 
        props = active_scene.curve_array_properties
        main_props = props.other_props.array_settings
        layout = self.layout

        count = Edit_Stor_Draw_Count()

        split = layout.split(factor = 0.726)

        row = split.box().row(align = True)
        row_right = split.row(align = True)

        row = row.split(factor = 0.06, align = True)
        row.label(text='№')
        row = row.split(factor = 0.4, align = True)
        row.label(text='Name')
        row = row.split(factor = 0.25, align = True)
        row.label(text='     Count')
        row = row.split(factor = 0.25, align = True)
        row.label(text='  Ghost?')
        row = row.split(factor = 0.4, align = False)            
        row.label(text='   Ghost %')
        row = row.split(factor = 0.333, align = True)
        row.label(text='')
        row = row.split(factor = 0.5, align = True)
        row.label(text='')
        row.label(text='')

        row_right.box().label(text = " Set Group")

        row = layout.row()
        row.label(text = "")


        for i in range(count):

            name, parent, editor_prop_i = Edit_Stor_Draw_ObjNameParentProp(i)
                
            split = layout.split(factor = 0.726)

            row = split.box().row(align = True)
            row_right = split.row(align = True)

            row = row.split(factor = 0.06, align = True)
            row.label(text= str(i+1))
            row = row.split(factor = 0.4, align = True)
            row.label(text= name)
            row = row.split(factor = 0.25, align = True)
            row.prop(editor_prop_i, "count", text="")
            row = row.split(factor = 0.05, align = True)
            row.label(text='')
            row = row.split(factor = 0.2, align = True)
            row.prop(editor_prop_i, "ghost", text = "")
            row = row.split(factor = 0.4, align = False)            
            row.prop(editor_prop_i, "ghost_p", text = "")
            row = row.split(factor = 0.333, align = True)
            oper = row.operator('crvarrpro.up_prop', icon='TRIA_UP')
            oper.draw_count_i = i
            row = row.split(factor = 0.5, align = True)
            oper = row.operator('crvarrpro.down_prop', icon='TRIA_DOWN')
            oper.draw_count_i = i
            oper = row.operator('crvarrpro.clear_prop', icon='PANEL_CLOSE')
            oper.draw_count_i = i
                
            if  parent == 0:

                row_right = row_right.box()
                row_right = row_right.split(factor = 0.75)
                row_right.prop(main_props, "set_group", text = "")
                oper = row_right.operator('crvarrpro.set_group', text = 'Set')
                oper.set_group = main_props.set_group
                oper.set_group_id = i
                oper.parent_id = 0


        row = layout.row()
        row.label(text = "")

        for n in range(1,6):

            split = layout.split(factor = 0.27)
            row_l = split.row().split(factor = 0.57)
            row_r = split.row()
            row_l.label(text = ("Random Group #" + str(n)))
            oper = row_l.operator('crvarrpro.new_random_group', text = 'Add to Main')
            oper.rg = n

            split = layout.box().split(factor = 0.737)
            l_col = split.column()
            r_col = split.column()

            rgcount =  Ran_Gr_Count(n)

            for i in range(rgcount):

                name, parent, editor_prop_i = Ran_Gr_ObjNameParentProp(n, i)
                chance = '             Chance: ' + str(Chance(n, i)) + '%'

                row = l_col.split(factor = 0.058)
                row.label(text= str(i+1))
                row = row.split(factor = 0.39)
                row.label(text= name)
                row = row.split(factor = 0.243)
                row.prop(editor_prop_i, "count", text="")
                row = row.split(factor = 0.83)
                row.label(text= chance)
                row = row.split(factor = 0.95)
                oper = row.operator('crvarrpro.remove_obj_from_r_g', icon='PANEL_CLOSE')
                oper.index = i
                oper.rg = n
                row.label(text= '')

                row = r_col.split(factor = 0.75)
                row.prop(main_props, "set_group", text = "")
                oper = row.operator('crvarrpro.set_group', text = 'Set')
                oper.set_group = main_props.set_group
                oper.set_group_id = i
                oper.parent_id = n
        
    def execute(self,context):
        
        active_scene = bpy.context.scene   
        selected_objects = bpy.context.selected_objects

        bpy.ops.object.select_all(action = 'SELECT')
        bpy.ops.object.select_all(action = 'DESELECT')
        
        for i in selected_objects:

            i.select_set(True)

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        
        return wm.invoke_props_dialog(self, width=688)
                
        return {'FINISHED'}

class CRVARRPRO_OT_UpProp(bpy.types.Operator):
    '''Up object in editor'''
    bl_label = ""
    bl_idname = 'crvarrpro.up_prop'
    bl_options = {'UNDO'}

    draw_count_i : bpy.props.IntProperty(
        name = "draw_count_i",
        description="",
        default = 0,
        min = 0
        )

    def execute(self,context):

        active_scene = bpy.context.scene   
        selected_objects = bpy.context.selected_objects
        active_object = bpy.context.active_object
        index = self.draw_count_i

        try:

            Edit_Stor_Draw_Up(index)

            return {'FINISHED'}

        except:

            return {'FINISHED'}

class CRVARRPRO_OT_DownProp(bpy.types.Operator):
    '''Up object in editor'''
    bl_label = ""
    bl_idname = 'crvarrpro.down_prop'
    bl_options = {'UNDO'}

    draw_count_i : bpy.props.IntProperty(
        name = "draw_count_i",
        description="",
        default = 0,
        min = 0
        )

    def execute(self,context):

        active_scene = bpy.context.scene   
        selected_objects = bpy.context.selected_objects
        active_object = bpy.context.active_object
        index = self.draw_count_i

        try:

            Edit_Stor_Draw_Down(index)

            return {'FINISHED'}

        except:

            return {'FINISHED'}

class CRVARRPRO_OT_ClearProp(bpy.types.Operator):
    '''Clear object from editor'''
    bl_label = ""
    bl_idname = 'crvarrpro.clear_prop'
    bl_options = {'UNDO'}

    draw_count_i : bpy.props.IntProperty(
        name = "draw_count_i",
        description="",
        default = 0,
        min = 0
        )

    def execute(self,context):

        i = self.draw_count_i

        RemoveObj(i)

        return {'FINISHED'}

class CRVARRPRO_OT_NewRandomGroup(bpy.types.Operator):
    '''Up object in editor'''
    bl_label = ""
    bl_idname = 'crvarrpro.new_random_group'
    bl_options = {'UNDO'}

    rg : bpy.props.IntProperty(
        name = "rg",
        description="",
        default = 0,
        min = 0
        )

    def execute(self,context):

        rg = str(self.rg)

        Edit_Stor_New_Ran_Gr(rg)

        return {'FINISHED'}

class CRVARRPRO_OT_SetGroup(bpy.types.Operator):
    ''' '''
    bl_label = "Set Group"
    bl_idname = 'crvarrpro.set_group'
    bl_options = {'UNDO'}

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

    set_group_id : bpy.props.IntProperty(
        name = "set_group_id",
        description="",
        default = 0,
        min = 0
        )

    parent_id : bpy.props.IntProperty(
        name = "parent_id",
        description="",
        default = 0,
        min = 0
        )

    def execute(self,context):

        active_scene = bpy.context.scene   
        my_props = active_scene.curve_array_properties

        selected_objects = bpy.context.selected_objects
        active_object = bpy.context.active_object
        set_group = self.set_group
        id = self.set_group_id
        parent_id = self.parent_id

        if str(parent_id) == set_group:

            return {'FINISHED'}

        if set_group != '0':

            if Ran_Gr_Count(int(set_group)) == 5:

                return {'FINISHED'}

        if parent_id == 0:

            link = Edit_Stor_Draw_LinkToObj(id)

            lin = Edit_Stor_Draw_RemoveObj(id)
            Edit_Stor_RemoveObj(lin)

        else:

            link = Ran_Gr_LinkToObj(parent_id, id)
            Ran_Gr_RemoveObj(parent_id, id)

        if set_group == '0':

            link = Edit_Stor_NewObj(link)

            Edit_Stor_Draw_NewObj(link)

        else:
    
            if Ran_Gr_Count(set_group) == 0 and CheckRG(set_group) == True:

                Edit_Stor_New_Ran_Gr(set_group)

            Ran_Gr_AddObj(set_group, link)

        return {'FINISHED'}
        
class CRVARRPRO_OT_RemoveObjFromRG(bpy.types.Operator):
    ''' '''
    bl_label = ""
    bl_idname = 'crvarrpro.remove_obj_from_r_g'
    bl_options = {'UNDO'}

    index : bpy.props.IntProperty(
        name = "index",
        description="",
        default = 0,
        min = 0
        )

    rg : bpy.props.IntProperty(
        name = "rg",
        description="",
        default = 0,
        min = 0
        )

    def execute(self,context):

        index = self.index
        rg = self.rg

        RemoveObjFromRG(rg, index)

        return {'FINISHED'}

class CRVARRPRO_OT_Empty(bpy.types.Operator):
    ''' '''
    bl_label = "Empty"
    bl_idname = 'crvarrpro.empty'

    def execute(self,context):

        return {'FINISHED'}