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
    tilt_correction as Strong_tilt_correction
)

def manager_smooth_curve():
        
    vertices_line_list, active_mesh_vector_list, direction_vetor_list, active_object, active_mesh = first_step()
            
    main_curve = Smooth_create_curve(vertices_line_list, active_object, active_mesh)
        
    extruded_mesh = second_step(main_curve)
    
    extruded_mesh_vector_list = Smooth_extruded_mesh_vector(extruded_mesh, len(vertices_line_list)*2, main_curve)
    extruded_mesh_vector_list = copy.deepcopy(extruded_mesh_vector_list)
        
    angle_list = Smooth_angle_between_vector(extruded_mesh_vector_list, active_mesh_vector_list, direction_vetor_list)
    
    Smooth_tilt_correction(angle_list, main_curve)
    
    final_step(extruded_mesh, main_curve)

def manager_strong_curve():
    
    vertices_line_list, active_mesh_vector_list, direction_vetor_list, active_object, active_mesh  = first_step()
    
    main_curve = Strong_create_curve(vertices_line_list, active_object, active_mesh)
    
    extruded_mesh = second_step(main_curve)
    
    extruded_mesh_vector_list = Strong_extruded_mesh_vector(extruded_mesh, len(vertices_line_list) - 1)
    extruded_mesh_vector_list = copy.deepcopy(extruded_mesh_vector_list)
    
    angle_list = Strong_angle_between_vector(extruded_mesh_vector_list, active_mesh_vector_list, direction_vetor_list)
    
    Strong_tilt_correction(angle_list, main_curve)
    
    final_step(extruded_mesh, main_curve)
                 
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

        except Exception as e:
            
            ShowMessageBox("Unkown Error, Please send me this report:", e, 'ERROR')
            
            return {'CANCELLED'}       
 
        