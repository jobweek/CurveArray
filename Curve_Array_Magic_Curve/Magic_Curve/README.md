# Magic Curve module

The magic curve module includes two methods for creating curves and a couple of methods for changing them.

## Curve Creation

In Blender, there is only one way to create a curve from the mesh edges. This is the "Convert" operator. Let's take a look at how it works. 

1. Let's create a primitive plane and unfold it randomly in space and detach the selected edges and create a separate object from them.
  
![Plane](/documentation_resources/1.png)
![Edges](/documentation_resources/2.png) 

2. Now will we be able to call the 'Convert' operator. Take a look at the result. Yes, we got the curve geometry right. But note the tilt of its points. It clearly doesn't match the normals of the mesh vertices. Using built-in blender method 'Convert' we can't create a curve with each of its points directed to corresponding normals of mesh vertices. But you can  do it with curve creation functions of the Magic Curve module !
  
![Curve](/documentation_resources/3.png)
![Curve](/documentation_resources/4.png) 


**Example of the difference between Magic Curve 'Smooth Curve' and Blender 'Convert'**


![Smooth Curve vs Convert](/documentation_resources/6.png) 

To create a curve with the Smooth Curve or Split Curve operators, you need to do two things:

  1. Select a sequence of vertices.
  2. Сlick the operator call button with the corresponding name.

### Rules and Errors

There are a number of conditions which, if not met, will result in known error:

1. In a scene, only one object must be selected from whose mesh you want to obtain the curve.

    Error text:

        > Select object.
    or

        > Select only one object.

2. The object type must be a mesh.
    
    Error text:

        > Object should be mesh.


3. The operator's start-up must be in edit mode.        

    Error text:

        > Go to Edit Mode.    

4. The sequence must contain more than one vertex, thereby creating at least one selected edge.

    ![Smooth Curve vs Convert](/documentation_resources/7.png)
    
    Error text:

        > No existing edges at selected sequence.

5. There must be an active vertex among the selected vertices. 

    _For non-cyclic curves, either at the very beginning or at the end of the sequence._
  
    _For cyclic - anywhere in the sequence._

    ![Smooth Curve vs Convert](/documentation_resources/8.png)
    
    Error text:

        > The active vertex must be selected.

6. The selected sequence of vertices must not have any branches or intersections. Also, it must not be interrupted and then continue again.

     _For non-cyclic curves, the first and the last vertex have a connection with only one other vertex, while the others have two connections with the previous and the next one._
     
     _For cyclic curves, all vertices have two connections with the previous and the next one._
  
    ![Smooth Curve vs Convert](/documentation_resources/9.png)
    
    Error text:

        > Make sure that the sequence of vertices does not intersect or branch, 
        > and that the vertex at the beginning of the sequence is selected.

7. The selected sequence of vertices must not have any vertices with same coordinates.
  
   _The error output will tell you the indices of such vertices. You can enable the display of mesh verts indices in Blender._

   ![Smooth Curve vs Convert](/documentation_resources/10.png)
    
   Error text:

       > In the sequence you have chosen, there are vertices in the same coordinates.
       > You can merge it.
       > Their indices: (8, 25)

8. In the event of an unknown error, caused by a bug in the program code, blender or for other reasons, you will see the following message:
   
    Error text:

       > Unknown Error. Please, open console and send me report.

   _I would also be very grateful if you could send me the scene where the unknown error occurred and the text from the console or open "Issues" on my GitHub. This will help me improve the addon._

It is also worth noting that in the case of an unknown error, the script stops, and everything that has happened since the beginning of the script will be applied to the scene. 
You may see an unexpected result. As recommended by the blender developers, for add-on developers, I have not built in a forced undo operation in case of failure, so you can do it yourself by simply pressing 'сtrl+z'

**Example of a correct vertex selection**

   _Cyclic curve_

   ![Smooth Curve vs Convert](/documentation_resources/11.png)
   ![Smooth Curve vs Convert](/documentation_resources/12.png)

   _Non-cyclic curve_

   ![Smooth Curve vs Convert](/documentation_resources/13.png)
   ![Smooth Curve vs Convert](/documentation_resources/14.png)

**Performance test**

   _Cpu: Ryzen5 5600x_

   _Ram: ddr4 16 gb_

   _Gpu: gtx 1050 ti_

   Simple changing object mode to edit mode: 3.118032500031404 seconds. (XD Lmao)

   Calling the Smooth Curve operator: 1.987318843654276 seconds.

   ![Smooth Curve vs Convert](/documentation_resources/26.png)
   ![Smooth Curve vs Convert](/documentation_resources/25.png)

### Smooth Curve operator

The Smooth Curve operator creates a curve with a single spline, each point of which has the same coordinates as the corresponding vertex of the mesh. 
The tilt of each spline point corresponds to the normal vector of the mesh vertex.

   _Spline type: Bezier_

   _Point handle type: Vector_
   
   _Curve twist method: Z-UP_

**Example of usage**

   ![Smooth Curve vs Convert](/documentation_resources/15.png)
   ![Smooth Curve vs Convert](/documentation_resources/16.png)
   
### An unexpected result

This happens when Smooth Curve works with geometry that has obvious bends in all three axes, as well as strong changing the direction of the curve.

   _Example_
   
   ![Smooth Curve vs Convert](/documentation_resources/17.png)
   ![Smooth Curve vs Convert](/documentation_resources/18.png)
   ![Smooth Curve vs Convert](/documentation_resources/19.png)
   ![Smooth Curve vs Convert](/documentation_resources/20.png)

If you extruded the resulting curve and turned on the meshes' vertex normals display (blue bars), you will see that at the point of the strongest bend, the curve is not extruded along the normal. 
It's not a bug, it's the way curves work in Blender. In fact, in this case, there is no curve that matches the vertex norals completely, and the result we have is the closest one. 
Nevertheless, if you need good precision in terms of normals, I suggest you look at the Split Curve operator.

### Split Curve operator

The Split Curve operator creates a curve in which each spline consists of two points and corresponds to one highlighted mesh edge.
The coordinates and normals of the points forming the spline correspond to the coordinates and normals of the points forming the corresponding edge on the mesh.  
  
   _Spline type: Bezier_

   _Point handle type: Vector_
   
   _Curve twist method: Z-UP_

**Example of usage**

   ![Smooth Curve vs Convert](/documentation_resources/21.png)
   ![Smooth Curve vs Convert](/documentation_resources/22.png)
   
**Difference to Smooth Curve**
   
   ![Smooth Curve vs Convert](/documentation_resources/23.png)
   ![Smooth Curve vs Convert](/documentation_resources/24.png)
   

## Curve Methods

There are three modes of calculating curve twist in Blender: Z-UP, Minimum and Tangent. 

The Z-UP and Minimum curves are most usefull.  Tangent curves have almost no application and the Magic Curve module does not support working with them.The main application is for curves of type Minimum, but there are useful application cases for Z-Up curves as well. 

   _For convenience, I have extruded the curve so that we can visually see the changes in the tilt of the curve normals._

![Plane](/documentation_resources/27.png)
![Edges](/documentation_resources/28.png) 

Let's see what happens to a curve of type Mimimum if we call the default Blender operator - Switch Direction:

![Plane](/documentation_resources/29.png)
![Edges](/documentation_resources/30.png) 

Let's also look at the result of another standard Blender operator - Toggle Cyclic:

![Plane](/documentation_resources/31.png)
![Edges](/documentation_resources/32.png) 

Now let's try changing the curve type from Minimum to Z-UP:

![Plane](/documentation_resources/33.png)
![Edges](/documentation_resources/34.png) 

Each of these operators changes the slope of the curve normals, which forces you to re-do everything manually. Magic Curve Methods is designed to fix this. 

### Rules and Errors

There are a number of conditions which, if not met, will result in known error:

1. In a scene, only one object must be selected from whose mesh you want to obtain the curve.

    Error text:

        > Select object.
    or

        > Select only one object.

2. The object type must be a curve.
    
    Error text:

        > Object should be curve.


3. The operator's start-up must be in object mode.        

   _The operator works on all curve splines, so an exit to object mode is required._

    Error text:

        > Go to Object Mode.    

**Performance test**

   _Cpu: Ryzen5 5600x_

   _Ram: ddr4 16 gb_

   _Gpu: gtx 1050 ti_

   Calling the Switch Twist Method (heaviest) operator: 0.2555739999515936 seconds.

   ![Smooth Curve vs Convert](/documentation_resources/35.png)

   It is worth noting that the Smooth parameter has a huge impact on performance. I will talk about this later, in the 'Unexpected Result' section. 
   But even now, it is important to understand that high values of this parameter will have a huge impact on the speed of both Blender itself and the magic curve methods. 
   Therefore, in case of long wait or program crash, I recommend lowering the Smooth value and repeating the operation.
   
### Switch Curve Direction Operator

   This operator allows you to switch the direction of all the splines of the curve, keeping the correct tilt of each point of the splines.
   
   _Working with Curves of type: Poly, Bezier._

   _Working with Twist Method of type: Minimum, Z-UP._

**Example of usage**

   _Before:_

![Plane](/documentation_resources/36.png)
![Edges](/documentation_resources/37.png) 

   _After:_

![Plane](/documentation_resources/38.png)
![Edges](/documentation_resources/39.png) 

### Toggle Cyclic Operator

   This operator allows you to toggle cyclic of all the splines of the curve, keeping the correct tilt of each point of the splines.
   
   _Working with Curves of type: Poly, Bezier._

   _Working with Twist Method of type: Minimum, Z-UP._

**Example of usage**

   _Before:_

![Plane](/documentation_resources/36.png)
![Edges](/documentation_resources/37.png) 

   _After:_

![Plane](/documentation_resources/40.png)
![Edges](/documentation_resources/41.png) 

### Change Twist Method Operator

   This operator allows you to change the curve calculation type from Minimum to Z-UP or vice versa.
   
   _Working with Curves of type: Poly, Bezier._

   _Working with Twist Method of type: Minimum, Z-UP._

**Example of usage**

   _Before:_

![Plane](/documentation_resources/42.png)
![Edges](/documentation_resources/43.png) 

   _After:_

![Plane](/documentation_resources/44.png)
![Edges](/documentation_resources/45.png) 

### An unexpected result

After applying Magic Curve operators to some curves (These are usually curves with unnatural, highly twisted and curved geometry), you may think something has gone wrong. Take a look at the example below. 

![Plane](/documentation_resources/46.png)
![Edges](/documentation_resources/47.png) 

_As you can see, with Smooth = 100, you will always get perfect results when using Magic Curve operators._

![Plane](/documentation_resources/48.png)
![Edges](/documentation_resources/49.png) 

But this feeling is wrong. In fact, the operator worked as it should, and the normal of each curve point before and after the call is identical. 
But then why is there this visual difference? The point is that Blender calculates the "geometry" between the control points, and the accuracy of this calculation depends on the Smooth parameter. 
You can change it at any time. The higher the parameter, the more accurately the segments between the control points will be drawn, and vice versa. 
Be warned, however, that high values have an extremely strong effect on the performance of both your scene and your operators. 
I therefore recommend not using high Smooth parameter values on curves with a high number of points and high Resolution_U.