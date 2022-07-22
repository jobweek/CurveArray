import bpy  # type: ignore


class CurveData:

    def __init__(self):
        self.__curve = None
        self.__cyclic = None

    def set_curve(self, curve):
        self.__curve = curve

    def get_curve(self):
        return self.__curve

    def set_cyclic(self, cyclic):
        self.__cyclic = cyclic

    def get_cyclic(self):
        return self.__cyclic
