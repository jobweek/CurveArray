import bpy
import mathutils

z_vec = mathutils.Vector((0.10333, -0.571133, 0.814328)).normalized()
y_vec = mathutils.Vector((-0.805194, 0.432619, 0.405591)).normalized()
x_vec = mathutils.Vector((0.58394, 0.697601, 0.41517)).normalized()

axis_vec = mathutils.Vector((0, 0, 1))

rotation = z_vec.rotation_difference(axis_vec)
print(rotation)

z_vec.rotate(rotation)
y_vec.rotate(rotation)
x_vec.rotate(rotation)

print(z_vec, y_vec, x_vec)