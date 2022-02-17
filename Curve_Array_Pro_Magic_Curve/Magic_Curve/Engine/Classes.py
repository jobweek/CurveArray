import bpy  # type: ignore
from .Errors import CancelError, ShowMessageBox


class Checker:

    @staticmethod
    def __object_checker():

        objects = bpy.context.selected_objects

        if len(objects) == 0:

            ShowMessageBox("Error", "Select object", 'ERROR')

            raise CancelError

        elif len(objects) > 1:

            ShowMessageBox("Error", "Select only one object", 'ERROR')

            raise CancelError

        if objects[0].type != 'MESH':

            ShowMessageBox("Error", "Object should be mesh", 'ERROR')

            raise CancelError

    @staticmethod
    def __mode_checker():
            
        mode = bpy.context.active_object.mode
        
        if mode != 'EDIT':
            
            ShowMessageBox("Error", "Go to Edit Mode", 'ERROR')
            
            raise CancelError
        
    def start_checker(self):
        
        self.__object_checker()
        self.__mode_checker()


class CurveData:

    __curve = None
    __cyclic = None

    def set_curve(self, curve):
        self.__curve = curve

    def get_curve(self):
        return self.__curve

    def set_cyclic(self, cyclic):
        self.__cyclic = cyclic

    def get_cyclic(self):
        return self.__cyclic
