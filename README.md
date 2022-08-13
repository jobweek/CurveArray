# Magic Curve module

The magic curve module includes two methods for creating curves and a couple of methods for changing them.

## Curve Creation

In Blender, there is only one way to create a curve from the mesh edges. This is the "Convert" operator. Let's take a look at how it works. 

  1. Let's create a primitive plane and unfold it randomly in space.
  ![Plane](/documentation_resources/1.png)
  2. We then have to detach the selected edges and create a separate object from them.
  ![Edges](/documentation_resources/2.png) 
  3. Only now will we be able to call the 'Convert' operator. Let's have a look at the result:
  ![Curve](/documentation_resources/3.png) 
  ![Curve](/documentation_resources/4.png) 
  4. Yes, we got the curve geometry right. But note the tilt of its points. It clearly doesn't match the normals of the mesh vertices. Using built-in blender method 'Convert' we can't create a curve with each of its points directed to corresponding normals of mesh vertices. But you can  do it with curve creation functions of the Magic Curve module !
  ![Smooth Curve](/documentation_resources/5.png) 
  ![Smooth Curve vs Convert](/documentation_resources/6.png) 

To create a curve with the Smooth Curve or Split Curve operators, you need to do two things:

  1. Select a sequence of vertices.
  2. Сlick the operator call button with the corresponding name.

**Select a sequence of vertices.**

There are a number of conditions which, if not met, will result in known error:

1. The number of vertices selected must be greater than 1.

    ![Smooth Curve vs Convert](/documentation_resources/7.png)
    
    Error text:

        > No existing edges at selected sequence.

2. There must be an active vertex among the selected vertices. 

    _For non-cyclic curves, either at the very beginning or at the end of the sequence._
  
    _For cyclic - anywhere in the sequence._

    ![Smooth Curve vs Convert](/documentation_resources/8.png)
    
    Error text:

        > The active vertex must be selected.

3. The selected sequence of vertices must not have any branches or intersections. Also, it must not be interrupted and then continue again.

     _For non-cyclic curves, the first and the last vertex have a connection with only one other vertex, while the others have two connections with the previous and the next one._
     
     _For cyclic curves, all vertices have two connections with the previous and the next one._
  
    ![Smooth Curve vs Convert](/documentation_resources/9.png)
    
    Error text:

        > Make sure that the sequence of vertices does not intersect or branch, 
        > and that the vertex at the beginning of the sequence is selected.

### Smooth Curve operator
