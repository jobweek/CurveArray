import bpy # type: ignore
import copy
from .Errors import CancelError, ShowMessageBox
from .General_Functions import first_step, second_step, final_step
from .Smooth_Curve import (
    create_curve as Smooth_create_curve, 
    extruded_mesh_vector as Smooth_extruded_mesh_vector,
    angle_between_vector as Smooth_angle_between_vector,
    tilt_correction as Smooth_tilt_correction
)
from .Strong_Curve import (
    create_curve as Strong_create_curve,
    extruded_mesh_vector as Strong_extruded_mesh_vector,
    angle_between_vector as Strong_angle_between_vector,
    cyclic_correction as Strong_cyclic_correction,
    tilt_correction as Strong_tilt_correction
)

def manager_smooth_curve():
        
    vert_co_array, active_mesh_vector_array, direction_vetor_array, active_object , curve_data = first_step()
            
    curve_data = Smooth_create_curve(vert_co_array, active_object, curve_data)
        
    extruded_mesh = second_step(curve_data)
        
    extruded_mesh_vector_array = Smooth_extruded_mesh_vector(extruded_mesh, len(vert_co_array)*2)
        
    angle_array = Smooth_angle_between_vector(extruded_mesh_vector_array, active_mesh_vector_array, direction_vetor_array)
    
    Smooth_tilt_correction(angle_array, curve_data)
    
    final_step(extruded_mesh, curve_data)

def manager_strong_curve():
    
    vert_co_array, active_mesh_vector_array, direction_vetor_array, active_object , curve_data = first_step()
    
    vert_co_array = Strong_cyclic_correction(vert_co_array, curve_data)
    
    curve_data = Strong_create_curve(vert_co_array, active_object, curve_data)
    
    extruded_mesh = second_step(curve_data)
    
    vector_count = (len(vert_co_array) - 1)
    extruded_mesh_vector_array = Strong_extruded_mesh_vector(extruded_mesh, vector_count)
    
    angle_array = Strong_angle_between_vector(extruded_mesh_vector_array, active_mesh_vector_array, direction_vetor_array)
    
    Strong_tilt_correction(angle_array, curve_data)
    
    final_step(extruded_mesh, curve_data)
                 
class MAGICCURVE_OT_mgcrv_ops(bpy.types.Operator):
    '''Clear selected curve'''
    bl_label = "Curve from loop"
    bl_idname = 'magiccurve.mgcrv_ops'
    bl_options = {'REGISTER', 'UNDO'}
        
    curve_type : bpy.props.BoolProperty(
        name = "Strong Curve",
        description="Type of algoritm",
        default = False
        )
        
    def execute(self, context):
 
        try:
            
            if self.curve_type == False:
                
                manager_smooth_curve()
                
            else:
                
                manager_strong_curve()
        
            return {'FINISHED'}
        
        except CancelError:
            
            return {'CANCELLED'}

        # except Exception as err:
            
        #     ShowMessageBox("Unkown Error, Please send me this report:", repr(err), 'ERROR')
            
        #     return {'CANCELLED'}       
 
        