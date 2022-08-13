# Magic Curve module

The magic curve module includes two methods for creating curves and a couple of methods for changing them.

## Curve Creation

In Blender, there is only one way to create a curve from the mesh edges. This is the "Convert" operator. Let's take a look at how it works. 

  1. Let's create a primitive plane and unfold it randomly in space.
  ![Plane](/documentation_resources/1.png)
  2. We then have to separate the selected edges and create a separate object from them.
  ![Edges](/documentation_resources/2.png) 
  3. Only now will we be able to call the 'Convert' operator. Let's have a look at the result:
  ![Curve](/documentation_resources/3.png) 
  ![Curve](/documentation_resources/4.png) 
  Yes, we got the curve geometry right. But note the tilt of its points. It clearly doesn't match the normals of the mesh vertices. Using built-in blender method 'Convert' we can't create a curve with each of its points directed to corresponding normals of mesh vertices. But you can  do it with curve creation functions of the Magic Curve module !
