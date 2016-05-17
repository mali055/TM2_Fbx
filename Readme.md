# Rendering FBX files to SVG format using Python
#### This script reads the current directory for fbx files and generates corresponding svg files for each fbx files found.

This is the report for the second Tools and Middleware's assignment. This project was a Solo project by Mohammad Ali. Originally supposed to be a team project this turned out to have some short comings due to the limitations.

![Example](https://github.com/mali055/TM2_Fbx/blob/master/assignment%20raven%20weapon.FBX.svg)

### The script
I use the Fbx Python bindings to extract a data structure of the fbx file and translate that into a structure usable for the SVG file format. It was a little bit of a challenge as it was the first project using python and the documentation for the Fbx pythong binding seemed to be for the C++ version.

I had the script divided in three parts Variables, Functions, and Main in that specific order.

I extract the code each mesh > polygon > vertice at a time and store them array as shown below:

```python  
    for meshidx in range(count): #get polys from mesh
        mesh = meshlist[meshidx] = root.GetChild(meshidx).GetMesh()
        polycount.append(mesh.GetPolygonCount())
        for poly in range(polycount[meshidx]): #get vertices from poly
            num = mesh.GetPolygonSize(poly)
            polyverts = []
            fbxverts = []
            for vert in range(num):#translating from fbxVector4 to array
                fbxverts.append(mesh.GetControlPointAt(mesh.GetPolygonVertex(poly, vert)))
                newVertex = [0, 0, 0]
                polyverts.append(newVertex)
                for h in range(3):
                    polyverts[vert][h] = fbxverts[vert][h]
            polygons.append(polyverts)
```  

By doing this we no longer need to depend on the fbx file or the python bindings data structure.
After extracting all the vertices we try to translate them to be more visible to the cmera's perspective (which by defualt would be top down) so we rotate it 45 degree on two axis, and try to scale it up or down (which needs more work specifically for the large model) as you can see in the code below it was time restrictions at this point that made me skip some polishing. 

```python  

def scale():
    factor = float( min(float(1/ float((maxY - minY)/(670))),float(1/float((maxX - minX)/(670)))) - 1)
    cam = [[1, 0, 0],
          [0, 1, 0],
          [0, 0, 1]]
    scale = [[factor, 0, 0],
        [0, factor, 0],
        [0, 0, factor]]
    final = [[0,0,0],[0,0,0],[0,0,0]]

    for i in range(3):
        for j in range(3):
            final[i][j] = cam[i][0]*scale[0][j] + cam[i][1]*scale[1][j] + cam[i][2]*scale[2][j]
    for poly in polygons:
        numverts = len(poly)
        for vert in range(numverts):
             poly[vert]= Vec3Product(final,poly[vert])

def rotate(degree, axis):
    cam = [[1, 0, 0],
          [0, 1, 0],
          [0, 0, 1]]
    if (axis == 0):
        rot = [[1, 0, 0],
               [0, math.cos(degree*rads), -math.sin(degree*rads)],
               [0, math.sin(degree*rads), math.cos(degree*rads)]]
    elif (axis == 1):
        rot = [[ math.cos(degree*rads), 0, math.sin(degree*rads)],
               [0, 1, 0],
               [-math.sin(degree*rads), 0, math.cos(degree*rads)]]
    elif (axis == 2):
        rot = [[math.cos(degree*rads), -math.sin(degree*rads),0],
               [ math.sin(degree*rads), math.cos(degree*rads),0],
               [0,0,1]]
    result = [[0,0,0],[0,0,0],[0,0,0]]
    
    for x in range(3):
        for y in range(3):
            result[x][y] = cam[x][0]*rot[0][y] + cam[x][1]*rot[1][y] + cam[x][2]*rot[2][y]
    for poly in polygons:
        numverts = len(poly)
        for vert in range(numverts):
              poly[vert]= Vec3Product(result,poly[vert])

```  
After all the quick and dirty translation scaling and rotation. The script starts building the SVG xml data into a file with the following piece of code. Here I also apply some quick and ditry shading to the models as it slowly changes shade every polygon it draws.

```python  

def genSVG(polys, file):
    svg = "%s\%s.svg" % (path,file)
    f = open(svg, 'w')
    if  f.errors:
            print ("Error in opening file %s" % (svg))

    #SVG header
    f.write('<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="720" height="720" style="background: #AAAAAA">')
    color = 30 
    if len(polys) == 0:
        print "Error polygon array is empty!"
    else:
        shading = 69.0/len(polys)
    center = 360
    for poly in polys:
        f.write('<polygon points="')
        for vertex in poly:
            f.write( '%d,%d ' % (vertex[0]+center, center-vertex[1]) )
        f.write('" style="fill:#%d%d00;stroke:none"/>' % (color,color) )
        color = color + shading
    #SVG footer
    f.write('</svg>')
    f.close()   

```  
### Conclusion

This being a solo project intended for a team of two presented challenging time difficulties, and cause me to reduce my expectation on the outcome, there is alot of room for polishing as the camera position and scaling could be less messy, it does not even capture the full model of the large character. The rendered even crashes on a more complicated model that i tried which is in the DOESNTWORK folder. Other things I would have liked to polish out was texturing and shading as well as other ways to render like wireframe. One downfall of the current implementation looks like normals need correcting which is something i was working on before i ran out of time. Overall a good experience in my first python project.

Note: I had a video recorded but it went corrupted before i uploaded it due to laptop trouble.

##References  
* [List of Python fbx classes. Autodesk FBX help for SDK](http://download.autodesk.com/us/fbx/20112/FBX_SDK_HELP/index.html?url=WS1a9193826455f5ff453265c9125faa23bbb5fe8.htm,topicNumber=d0e8312)
* Game Programming with Python, Lua, and Ruby  By Tom Gutschmidt

##Repositories
* [Mohammad Ali Githud Project Link](https://github.com/mali055/TM2_Fbx/)


