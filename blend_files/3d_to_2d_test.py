import bpy
import mathutils

vec_1 = mathutils.Vector((0.642855, 0.478683, 0.59798)).normalized()
vec_2 = mathutils.Vector((-0.076521, 0.7254, 0.684061)).normalized()

print(vec_1, vec_2)

vec_1_2d = vec_1.to_2d()
vec_2_2d = vec_2.to_2d()

print(vec_1_2d, vec_2_2d)