import bpy
from .Errors import CancelError, ShowMessageBox

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