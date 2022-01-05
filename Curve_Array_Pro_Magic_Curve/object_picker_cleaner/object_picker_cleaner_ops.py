import bpy

from Curve_Array_Pro_Magic_Curve.props.curve_array_props import (
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
Ran_Gr_Clear,
Edit_Stor_Draw_RemoveObj,
Edit_Stor_RemoveObj,
Obj_Stor_RemoveObj,
Obj_Stor_Draw_RemoveObj,
)

def  AddObject(obj):

    name = obj.name

    link = Obj_Stor_NewObj(name)

    Obj_Stor_Draw_NewObj(link)

    link = Edit_Stor_NewObj(link)

    Edit_Stor_Draw_NewObj(link)

def ClearObject():

    Edit_Stor_Draw_Clear()
    Edit_Stor_Clear()
    Obj_Stor_Draw_Clear()
    Ran_Gr_Clear()
    Obj_Stor_Clear()

def RemoveObj(i):

    link = Edit_Stor_Draw_RemoveObj(i)

    link = Edit_Stor_RemoveObj(link)

    if int(link) <0:

        Ran_Gr_RemoveObj(abs(int(link)), index)

    Obj_Stor_RemoveObj(link)
    Obj_Stor_Draw_RemoveObj(link)

class CRVARRPRO_OT_ObjectPicker(bpy.types.Operator):
    '''Select Object, witch be used for array, and press "Store"'''
    bl_label = "Store selected object(s)"
    bl_idname = 'crvarrpro.pick_object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self,context):
        
        active_scene = bpy.context.scene   
        selected_objects = bpy.context.selected_objects
        active_object = bpy.context.active_object

        for i in selected_objects:

            AddObject(i)
             
        #bpy.ops.object.select_all(action='DESELECT')

        return {'FINISHED'}
                

class CRVARRPRO_OT_ObjectCleaner(bpy.types.Operator):
    '''Clear selected object'''
    bl_label = "Clear all"
    bl_idname = 'crvarrpro.clear_object'
        
    def execute(self,context):
                           
        active_scene = bpy.context.scene
        coun = Edit_Stor_Draw_Count() - 1

        ClearObject()

        #for i in range(coun,-1,-1):

            #RemoveObj(i)
                    
        return {'FINISHED'}