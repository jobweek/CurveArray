import bpy
import mathutils

z_vec = mathutils.Vector((1, 1, 1)).normalized()
y_vec = mathutils.Vector((0.3, -0.3, 1)).normalized()

print(z_vec, y_vec)

projection = y_vec.project(z_vec)
reflection = y_vec.reflect(z_vec)

print(projection)