# Curve Array

Curve Array is designed as a flexible tool for creating arrays along a curve.
Curve Array does not merge array objects, because it is not a modifier, and it does not distort the object mesh.

## What's the difference to existing methods in bender?

In version 4.0, Curve Array received a complete overhaul of its basic working algorithms. 
Previously based on a bundle of two Blender modifiers (Array + Curve), Curve Array now has its own core curve representation, allowing it to add unique features.

### Curve Array VS Geometry Nodes and Array+Curve modifiers:

**Perception of the path**

Curve Array works with all curve splines.

50

Blender Array + Curve modifiers ignore other curve splines after the first one.

51

Geometry Nodes, conversely treats all curve splines as independent curves, creating an array with specified parameters for each spline, rather than the entire curve as a whole.

53

Also, Curve Array allows you to control the smoothness of curve normals, curve cyclicity, and many other small improvements, for example, if you create a circle, Blender will not consider the first point as the start, but the last one. 
And if you switch the cycle, Blender will suddenly start taking the first point as the beginning, as it should be. 
The curve array is free of these oddities. All this is made possible by the new Path Data Core created in version 4.0. 
 

**Usability**

As a fact, to create a simple array, you need to make three mouse clicks. 
Also, unlike Blender modifiers or Geometry Nodes, you don't need to align the curve and reference object before creating the array, Curve Array will take them correctly wherever they are!


**Preservation of objects**

Unlike Geometry Nodex and Blender Array+Curve modifiers, Curve Array keeps each object individual. 

79

### Results:

Curve Array is not trying to compete with Geometry Nodes or Array + Curve modifiers. 
On the contrary, it takes its place as a tool for spacing objects, while Geometry Nodes has no equal in creating scenarios where objects behave like particles, and Curve + Array modifiers are perfect when you need to create a deformed array.

## Curve Editor

The Curve Editor exists to capture the current path. 
You can add only one object, and it must be a curve, otherwise you will get an error.

58

## Object Editor

### Adding objects

You can add any number of objects to the Object Editor. They can be of any type: Mesh, Curve, empty, etc. 
Each added object will take its place in the Queue. 

59

By opening the Object Editor, we can edit the Queue. All objects in the Queue can be deleted, duplicated or moved.

60

Also, all objects in the queue have their own settings:

### Count

Count - the number of times the object is repeated in the queue. 
In case the object has random parameters (Ghost, or Transformation), they will be unique for each repetition.

61

### Ghost

Ghost - the probability that the object will fall into a special collection, which is created inside the main collection, where objects fall when a new array is created. 
This collection is hidden, and so are its objects, but you can easily retrieve them from it 
(Only if this is the final result, deleting and renaming objects from Curve Array collections will cause an error when you try to update the array). 
This allows you to select any number of objects from a particular place in the queue.

62

### Pivot

Pivot - the distance between Origin and Pivot, calculated automatically when you add an object.
It is used in the Fill by Pivot algorithm. See Fill by Pivot for details.

### Transform Editor

The Transform Editor allows you to set the parameters of random or progressive rotation, location, and scale for each Item of the Queue.

63

### Len

Len(Length ) - the number of unique repetitions for the Queue.

64

### Random Group

Random Group - a group from which one random object will be selected at each iteration. 
You can create an empty group and then add objects to it. Or create a group immediately from a queue object. 

The Count parameter is responsible for the chance of selecting an object. 

65

## Array Settings

### Random Seed

Random Seed - when you change this parameter you get different random generations (Random Groups or Random Transformation) you set in the Object Editor settings. 
Changing Random Seed can be quite a heavy operation (in case of objects with a lot of geometry), because Curve Array will delete all copies of objects and recreate them when you change this parameter.  

### Cloning Type

Clone type - has three options for creating duplicate objects.

Copy - simple duplication, each object of the array is independent of its reference. It can be slow in case of copying many objects with heavy geometry.

Semi Instance - the mesh of the duplicate will be an instance of the reference, but it will also copy the modifiers of the reference, which can slow down the scene, in cases of heavy-weight modifiers.

Full Instance - the lightest way. Just an instance of the reference mesh.

66

### Spacing Types

Spacing Types - the basic algorithms for spacing objects. At the moment there are 4 of them.

Fill by Count - evenly fills the path with the given number of objects.

67

Fill by Offset - fills the path with the specified number of objects in a specified step (Step Offset).

68

Fill by Size - fills the path with the specified number of objects based on their size along the selected axis. 
You can also adjust this ratio with the Size Offset parameter. 
This is a very heavy algorithm, it takes into account the rotation, scaling and position of each object, so use it carefully with objects that have a heavy mesh.

69

Fill by Pivot - a completely new algorithm. 
It emulates the sliding of objects along a curve not just by origins, like other algorithms, but also by a second hinge called Pivot. 
All you have to do is give the distance from the first hinge (Orgigin), to the second hinge (Pivot). 
When you add a new object in the Object Editor, it automatically calculates the distance between the 3D Cursor and Origin, so you can simply place the cursor at the intended hinge and add the object.

70

You also have the Step parameter available, this is the step between objects and here's how you can use it:

71

### Cyclic

Cyclic - a parameter that lets you decide if the curve is cyclic.

54

### Smooth Normals 

Smooth Normals - the parameter that lets you decide if the normals will be smoothed or sharp.

56

### Start & End Offset

These parameters are available in all algorithms except Fill By Pivot.
They actually shorten or lengthen the path by a given length.

72

### Consider Size

Consider Size - a parameter that allows you to automatically take an offset equal to the size of the object, so that the array does not exceed the limits of the path.

In the Fill By Count algorithm, it works from both ends, and in the Fill By Offset and Fill by Size algorithms, only from the beginning.

73

### Slide

Slide - a parameter that allows all objects in the array to slide along the curve. 
In all algorithms except Fill By Pivot, it does not affect the operation of the algorithm (number of objects, their visibility, etc.). 
It is as if it fixes the current state and only allows it to slide.

74

### Align Rotation

Align Rotation - a parameter that allows you to enable or disable the rotation of objects when aligning along the path.

75

### Rail Axis

Rail Axis - the axis along which the object will be tracked along the path. 

This axis is not the local axis of the object, it is the axis of the world space. 
It allows you to rotate the reference object and get updates of the array objects.

76

### Normal Axis

Normal Axis - the axis of direction of the curve normal. 
The working concept is the same as the Rail Axis.

### Rotation, Scale, Location

Rotation, location, and scale are execute along the local axes of the object.

In contrast to Object Editor, the rotation, scaling, and moving operations are performed here first, then the scaling, and then the rotation (as is standard). 
In the Object Editor, the rotation operation is performed first, followed by scaling and moving, to give you more freedom in creating fancy shapes.

77

### Auto Update

By setting the Auto Update flag, any change in parameters will cause the array to change. 
Be careful, if you manually delete/rename an object/collection that Curve Array was using, remove the Auto Update flag, otherwise every change to the array settings will result in an error.

### Create Array

Doesn't need a comment unless you're a zucchini, ahah))

### Update Array

Update Array - this function is not as simple as it sounds. 
It is not just a manual update array, instead of Auto Update, Update Array has more power, updating as well the Path and Queue data. 

78

## Errors and Rules.

Curve Array reuses objects created by it. 
So when you change the parameters of an array, it doesn't recreate them, it searches for them by name in the scene, in a particular collection, so don't rename, move, or delete objects or collections while you want to edit the created array.

All errors with the title 'Error' have an explanation of the cause, and the user can fix it himself. 

If you see the 'Unkown Error' header, or the wrong behavior of the add-on, please save the scene where the error occurred (so that I can reproduce it) and open an Issue on my GitHub, attaching the scene there. 
This will help not only you, but all the other users who might have encountered the same error as you!