import bpy
from .Errors import CancelError, ShowMessageBox

class Checker():

    def __object_checker(self):
        
        objects = bpy.context.selected_objects
        
        if len(objects) == 0:
            
            ShowMessageBox("Error","Select object", 'ERROR')
            
            raise CancelError
        
        elif len(objects) > 1:

            ShowMessageBox("Error","Select only one object", 'ERROR')
            
            raise CancelError

        if objects[0].type != 'MESH':
            
            ShowMessageBox("Error","Object shoud be mesh", 'ERROR')
            
            raise CancelError  
    
    def __mode_checker(self):
            
        mode = bpy.context.active_object.mode
        
        if mode != 'EDIT':
            
            ShowMessageBox("Error","Go to Edit Mode", 'ERROR')
            
            raise CancelError
        
    def start_checker(self):
        
        self.__object_checker()
        self.__mode_checker()
        
checker = Checker()
            
class Cyclic_Curve():
    
    def __init__(self):
    
        self.cyclic = None
        
    def get(self):
                
        return self.cyclic
    
    def set(self, input):
        
        self.cyclic = input

cyclic_curve = Cyclic_Curve()