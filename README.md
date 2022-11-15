**A little preface**

I spent over 7 months of daily work on the 4.0 update, essentially redesigning Curve Array and Magic Curve modules from scratch. 
I have decided that I will make the Curve Array free, for all the support of the community.
However, if you'd like to say thank you, you can either buy it for price you think is fair at:

Gumroad(https://jobweek.gumroad.com/l/curve-array-pro)  
Blender Market(https://blendermarket.com/products/curvearraypro--magiccurve)  
Or donate to my crypto wallet: ETH(0x4d6E06EEb748A806f87734bcCbb26c0DF4c0f793)

Thanks for all, and have a great time using it!


# Curve Array

![Image](/documentation_resources/preview.png)

Curve Array is designed as a flexible tool for creating arrays along a curve.
Curve Array does not merge array objects, because it is not a modifier, and it does not distort the object mesh.

## What's the difference to existing methods in bender?

In version 4.0, Curve Array received a complete overhaul of its basic working algorithms. 
Previously based on a bundle of two Blender modifiers (Array + Curve), Curve Array now has its own core curve representation, allowing it to add unique features.

### Curve Array VS Geometry Nodes and Array+Curve modifiers:

**Perception of the path**

Curve Array works with all curve splines.

[![Video](/documentation_resources/50.png)](https://youtu.be/FofvjdWdlms)

Blender Array + Curve modifiers ignore other curve splines after the first one.

[![Video](/documentation_resources/51.png)](https://youtu.be/FofvjdWdlms)

Geometry Nodes, conversely treats all curve splines as independent curves, creating an array with specified parameters for each spline, rather than the entire curve as a whole.

[![Video](/documentation_resources/53.png)](https://youtu.be/UUdM9y9l0J0)

Also, Curve Array allows you to control the smoothness of curve normals, curve cyclicity, and many other small improvements, for example, if you create a circle, Blender will not consider the first point as the start, but the last one. 
And if you toggle cyclic, Blender will suddenly start taking the first point as the beginning, as it should be. 
The curve array is free of these oddities. All this is made possible by the new Path Data Core created in version 4.0. 
 

**Usability**

As a fact, to create a simple array, you need to make three mouse clicks. 
Also, unlike Blender modifiers or Geometry Nodes, you don't need to align the curve and reference object before creating the array, Curve Array will take them correctly wherever they are!


**Preservation of objects**

Unlike Geometry Nodex and Blender Array+Curve modifiers, Curve Array keeps each object individual. 

[![Video](/documentation_resources/79.png)](https://youtu.be/kpVv2Dw3XZg)

### Results:

Curve Array is not trying to compete with Geometry Nodes or Array + Curve modifiers. 
On the contrary, it takes its place as a tool for spacing objects, while Geometry Nodes has no equal in creating scenarios where objects behave like particles, and Curve + Array modifiers are perfect when you need to create a deformed array.

## Curve Editor

The Curve Editor exists to capture the current path. 
You can add only one object, and it must be a curve, otherwise you will get an error.

[![Video](/documentation_resources/58.png)](https://youtu.be/lrIAUW_hodo)

## Object Editor

### Adding objects

You can add any number of objects to the Object Editor. They can be of any type: Mesh, Curve, empty, etc. 
Each added object will take its place in the Queue. 

[![Video](/documentation_resources/59.png)](https://youtu.be/HwD-ZgMqeeM)

By opening the Object Editor, we can edit the Queue. All objects in the Queue can be deleted, duplicated or moved.

[![Video](/documentation_resources/60.png)](https://youtu.be/nQR35bvyjAs)

Also, all objects in the queue have their own settings:

### Count

Count - the number of times the object is repeated in the queue. 
In case the object has random parameters (Ghost, or Transformation), they will be unique for each repetition.

[![Video](/documentation_resources/61.png)](https://youtu.be/_MRKoGwemr8)

### Ghost

Ghost - the probability that the object will fall into a special collection, which is created inside the main collection, where objects fall when a new array is created. 
This collection is hidden, and so are its objects, but you can easily retrieve them from it 
(Only if this is the final result, deleting and renaming objects from Curve Array collections will cause an error when you try to update the array). 
This allows you to select any number of objects from a particular place in the queue.

[![Video](/documentation_resources/62.png)](https://youtu.be/Jshr6_0ijqw)

### Pivot

Pivot - the distance between Origin and Pivot, calculated automatically when you add an object.
It is used in the Fill by Pivot algorithm. See Fill by Pivot for details.

### Transform Editor

The Transform Editor allows you to set the parameters of random or progressive rotation, location, and scale for each Item of the Queue.

[![Video](/documentation_resources/63.png)](https://youtu.be/3OCyJwKSltY)

### Len

Len(Length) - the number of unique repetitions for the Queue.

[![Video](/documentation_resources/64.png)](https://youtu.be/RqcijVaKEzc)

### Random Group

Random Group - a group from which one random object will be selected at each iteration. 
You can create an empty group and then add objects to it. Or create a group immediately from a queue object. 

The Count parameter is responsible for the chance of selecting an object. 

[![Video](/documentation_resources/65.png)](https://youtu.be/e4K9AntJDRE)

## Array Settings

### Random Seed

Random Seed - when you change this parameter you get different random generations (Random Groups or Random Transformation) you set in the Object Editor settings. 
Changing Random Seed can be quite a heavy operation (in case of objects with a lot of geometry), because Curve Array will delete all copies of objects and recreate them when you change this parameter.  

### Cloning Type

Clone type - has three options for creating duplicate objects.

Copy - simple duplication, each object of the array is independent of its reference. It can be slow in case of copying many objects with heavy geometry.

Semi Instance - the mesh of the duplicate will be an instance of the reference, but it will also copy the modifiers of the reference, which can slow down the scene, in cases of heavy-weight modifiers.

Full Instance - the lightest way. Just an instance of the reference mesh.

[![Video](/documentation_resources/66.png)](https://youtu.be/GP69otjdsk0)

### Spacing Types

Spacing Types - the basic algorithms for spacing objects. At the moment there are 4 of them.

Fill by Count - evenly fills the path with the given number of objects.

[![Video](/documentation_resources/67.png)](https://youtu.be/lVDG62JhEwQ)

Fill by Offset - fills the path with the specified number of objects in a specified step (Step Offset).

[![Video](/documentation_resources/68.png)](https://youtu.be/02Z9Y6FYUkA)

Fill by Size - fills the path with the specified number of objects based on their size along the selected axis. 
You can also adjust this ratio with the Size Offset parameter. 
This is a very heavy algorithm, it takes into account the rotation, scaling and position of each object, so use it carefully with objects that have a heavy mesh.

[![Video](/documentation_resources/69.png)](https://youtu.be/R8PB7OnfIpM)

Fill by Pivot - a completely new algorithm. 
It emulates the sliding of objects along a curve not just by origins, like other algorithms, but also by a second hinge called Pivot. 
All you have to do is give the distance from the first hinge (Orgigin), to the second hinge (Pivot). 
When you add a new object in the Object Editor, it automatically calculates the distance between the 3D Cursor and Origin, so you can simply place the cursor at the intended hinge and add the object.

[![Video](/documentation_resources/70.png)](https://youtu.be/NuOw9TwSki4)

You also have the Step parameter available, this is the step between objects and here's how you can use it:

[![Video](/documentation_resources/71.png)](https://youtu.be/F8yew6Up_XI)

### Cyclic

Cyclic - a parameter that lets you decide if the curve is cyclic.

[![Video](/documentation_resources/54.png)](https://youtu.be/E_feGK0gyaM)

### Smooth Normals 

Smooth Normals - the parameter that lets you decide if the normals will be smoothed or sharp.

[![Video](/documentation_resources/56.png)](https://youtu.be/vbtv2WbQ-zI)

### Start & End Offset

These parameters are available in all algorithms except Fill By Pivot.
They actually shorten or lengthen the path by a given length.

[![Video](/documentation_resources/72.png)](https://youtu.be/faeWQatUUfs)

### Consider Size

Consider Size - a parameter that allows you to automatically take an offset equal to the size of the object, so that the array does not exceed the limits of the path.

In the Fill By Count algorithm, it works from both ends, and in the Fill By Offset and Fill by Size algorithms, only from the beginning.

[![Video](/documentation_resources/73.png)](https://youtu.be/dp7SAQcezkY)

### Slide

Slide - a parameter that allows all objects in the array to slide along the curve. 
In all algorithms except Fill By Pivot, it does not affect the operation of the algorithm (number of objects, their visibility, etc.). 
It is as if it fixes the current state and only allows it to slide.

[![Video](/documentation_resources/74.png)](https://youtu.be/abQ6CAPJE4A)

### Align Rotation

Align Rotation - a parameter that allows you to enable or disable the rotation of objects when aligning along the path.

[![Video](/documentation_resources/75.png)](https://youtu.be/CfQpTb6TN4c)

### Rail Axis

Rail Axis - the axis along which the object will be tracked along the path. 

This axis is not the local axis of the object, it is the axis of the world space. 
It allows you to rotate the reference object and get updates of the array objects.

[![Video](/documentation_resources/76.png)](https://youtu.be/r4GgAVVbcuU)

### Normal Axis

Normal Axis - the axis of direction of the curve normal. 
The working concept is the same as the Rail Axis.

### Rotation, Scale, Location

Rotation, location, and scale are execute along the local axes of the object.

In contrast to Object Editor, the rotation, scaling, and moving operations are performed here first, then the scaling, and then the rotation (as is standard). 
In the Object Editor, the rotation operation is performed first, followed by scaling and moving, to give you more freedom in creating fancy shapes.

[![Video](/documentation_resources/77.png)](https://youtu.be/HcJ7z5HuE-E)

### Auto Update

By setting the Auto Update flag, any change in parameters will cause the array to change. 
Be careful, if you manually delete/rename an object/collection that Curve Array was using, remove the Auto Update flag, otherwise every change to the array settings will result in an error.

### Create Array

Doesn't need a comment unless you're a potato, ahah))

### Update Array

Update Array - this function is not as simple as it sounds. 
It is not just a manual update array, instead of Auto Update, Update Array has more power, updating as well the Path and Queue data. 

[![Video](/documentation_resources/78.png)](https://youtu.be/5vJufEZKEuo)

### Remove Last Array

Remove Last Array - removes the current array, as well as clearing internal data, which will allow you to edit settings for a new array without unchecking the Auto Update.  

### Reset Array Settings

Resets current array settings to defaults.

## Errors and Rules.

Curve Array reuses objects created by it. 
So when you change the parameters of an array, it doesn't recreate them, it searches for them by name in the scene, in a particular collection, so don't rename, move, or delete objects or collections while you want to edit the created array.

All errors with the title 'Error' have an explanation of the cause, and the user can fix it himself. 

If you see the 'Unkown Error' header, or the wrong behavior of the add-on, please save the scene where the error occurred (so that I can reproduce it) and open an Issue on my GitHub, attaching the scene there. 
This will help not only you, but all the other users who might have encountered the same error as you!




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