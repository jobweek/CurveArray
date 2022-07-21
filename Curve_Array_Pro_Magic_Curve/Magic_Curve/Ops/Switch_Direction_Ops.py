import bpy # type: ignore
from ..Engine.Errors import CancelError
from ..Engine.General_Functions import first_step, second_step, final_step
from ..Engine.Smooth_Curve_Old import (
    create_curve as Smooth_create_curve, 
    extruded_mesh_vector as Smooth_extruded_mesh_vector,
    angle_between_vector as Smooth_angle_between_vector,
    tilt_correction as Smooth_tilt_correction
)
from ..Engine.Strong_Curve import (
    create_curve as Strong_create_curve,
    extruded_mesh_vector as Strong_extruded_mesh_vector,
    angle_between_vector as Strong_angle_between_vector,
    cyclic_correction as Strong_cyclic_correction,
    tilt_correction as Strong_tilt_correction,
    curve_correction as Strong_curve_correction
)

def manager_recalculate_curve():
    
    pass
 
class MAGICCURVE_OT_switch_direction(bpy.types.Operator):
    '''Switch curve direction and recalculate to right tilt'''
    bl_label = "Switch curve direction"
    bl_idname = 'magiccurve.switch_direction'
    bl_options = {'REGISTER', 'UNDO'}
        
    def execute(self, context):
 
        try:
            
            manager_recalculate_curve()
        
            return {'FINISHED'}
        
        except CancelError:
            
            return {'CANCELLED'}

        # except Exception as err:
            
        #     ShowMessageBox("Unkown Error, Please send me this report:", repr(err), 'ERROR')
            
        #     return {'CANCELLED'}   