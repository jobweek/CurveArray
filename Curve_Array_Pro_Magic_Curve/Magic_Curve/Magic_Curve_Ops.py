import bpy
import bmesh
import mathutils
import math
from .Errors import CancelError, ShowMessageBox
from .First_Step import first_step
from .Smooth_Curve import (
    create_curve as Smooth_create_curve, 
    create_extruded_curve as Smooth_create_extruded_curve,
    convert_extuded_curve_to_mesh as Smooth_convert_extuded_curve_to_mesh,
    extruded_mesh_vector as Smooth_extruded_mesh_vector,
    active_mesh_vector as Smooth_active_mesh_vector,
    direction_vector as Smooth_direction_vector,
    angle_between_vector as Smooth_angle_between_vector,
    tilt_correction as Smooth_tilt_correction
)
from .Strong_Curve import (
    create_curve as Strong_create_curve, 
)
 
def manager_smooth_curve():
        
    vertices_line_list, active_object, active_mesh = first_step()
            
    main_curve = Smooth_create_curve(vertices_line_list, active_object, active_mesh)
        
    extruded_curve = Smooth_create_extruded_curve(main_curve)
    
    extruded_mesh = Smooth_convert_extuded_curve_to_mesh(extruded_curve)
    
    extruded_mesh_vector_list = Smooth_extruded_mesh_vector(extruded_mesh, len(vertices_line_list)*2, main_curve)

    active_mesh_vector_list = Smooth_active_mesh_vector(active_mesh, vertices_line_list)
    
    direction_vetor_list = Smooth_direction_vector(vertices_line_list, active_mesh)
    
    angle_list = Smooth_angle_between_vector(extruded_mesh_vector_list, active_mesh_vector_list, direction_vetor_list)
    
    Smooth_tilt_correction(angle_list, main_curve)
    
    bpy.data.objects.remove(extruded_mesh, do_unlink=True)
    
    bpy.ops.object.select_all(action='DESELECT') 
    main_curve.get_curve().select_set(True)
    bpy.context.view_layer.objects.active = main_curve.get_curve()
        
def manager_strong_curve():
    
    vertices_line_list, active_object, active_mesh  = first_step()
    
    main_curve = Strong_create_curve(vertices_line_list, active_object, active_mesh)
    
             
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

        # except Exception as e:
            
        #     ShowMessageBox("Unkown Error", "Please send me this report:", e, 'ERROR')
            
        #     return {'CANCELLED'}       
 
        