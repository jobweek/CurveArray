import bpy

def ShowMessageBox(title, message, icon):

    def draw(self, context):
        self.layout.label(text = message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

def Search_Parent(obj, ss):

    for i in obj.children:

        ss.append(i)

        Search_Parent(i, ss)

class CRVARRPRO_OT_Delete_Last_Array(bpy.types.Operator):
    '''Delete all objects in the collection of the last created array'''
    bl_label = "Delete last Array"
    bl_idname = 'crvarrpro.delete_last_array'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self,context):
        
        active_scene = bpy.context.scene
        my_props = active_scene.curve_array_properties.other_props.array_settings   
        ss = []

        if my_props.last_array == '':

            ShowMessageBox("Error", "Last Array collection was not found", 'ERROR')
        
            return {'CANCELLED'}
        print(my_props.last_array)
        col = bpy.data.collections.get(my_props.last_array)
        print(col)
        if col is None:

            ShowMessageBox("Error", "Last Array collection was not found", 'ERROR')

        ss.append(col)
        Search_Parent(col, ss)

        for i in ss:

            try:
            
                bpy.data.objects.remove(i, do_unlink=True)

            except:

                bpy.data.collections.remove(i)

        return {'FINISHED'}
                