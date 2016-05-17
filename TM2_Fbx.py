import FbxCommon
import math
import glob
import random
import os, sys

#Variables

sdk_manager, scene = FbxCommon.InitializeSdkObjects()
fbxlist = glob.glob("*.fbx")
path = os.getcwd();
rads = 3.1415/180
meshlist = []
polycount = []
polygons = []
maxX = 0
minX = 0
maxY = 0
minY = 0
cam = [[1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]]


##Functions


def clearSVG():
    #Clear SVG files
    for file in glob.glob("*.svg"):
        fullpath = path + "\\" + file
        print "clearSVG() - %s removed" % ( fullpath )
        os.remove(fullpath)

def createSVG(fbx): #Create SVG Files and translates fbx into it
    print "createSVG() - creating for %s" % (fbx)
    #initialize scene for fbxcommon
    sdk_manager, scene = FbxCommon.InitializeSdkObjects()
    if not FbxCommon.LoadScene(sdk_manager, scene, fbx):
            print("Error loading scene for %s" % (fbx))

    #

    #
    getMesh(scene.GetRootNode())
    genSVG(polygons, fbx)
    del polygons[:]

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
    print ("genSVG() - created svg file at %s" % (svg))


def getMesh(root):
    count = root.GetChildCount()
    meshlist = range(count)
    polycount = []
    num = 0
    global maxX 
    global minX 
    global maxY 
    global minY 
    maxX = 0
    minX = 0
    maxY = 0
    minY = 0
    for meshidx in range(count): #get polys from mesh
        #meshidx = 1
        counter = 0
        mesh = meshlist[meshidx] = root.GetChild(meshidx).GetMesh()
        #polycount.append(mesh.GetPolygonCount())
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
                #for use with scaling later
                if(polyverts[vert][0] > maxX):
                    maxX = polyverts[vert][0]
                if(polyverts[vert][0] < minX): 
                    minX = polyverts[vert][0]
                if(polyverts[vert][1] > maxY):
                    maxY = polyverts[vert][1]
                if(polyverts[vert][1] < minY):
                    minY = polyverts[vert][1]
            polygons.append(polyverts)
            #print ("(%s) Polyverts = %s \n" % (counter, polyverts))
            counter += 1
            #print ("    added %s vertices into ploygon array, polygons size = %s * %s \n" % (num, len(polygons), len(polygons[0])) )
        print (" mesh %s = %s with %s polygons" % (meshidx, root.GetChild(meshidx).GetMesh(), polycount[meshidx]))
    #translate to camera veiwport default is top down so using 45 degrees
    rotate(45, 0)
    rotate(45, 2)
    scale()
    #normals()

def scale():
    print (" minX = %s \n minY = %s \n maxX = %s \n maxY = %s" % (minX, minY, maxX, maxY))

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
    counter = 0
    for poly in polygons:
        numverts = len(poly)
        #print ("(%s) poly %s has %s \n" % (counter, poly, numverts))
        counter += 1
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
    counter = 0
    for poly in polygons:
        numverts = len(poly)
        #print ("(%s) poly %s has %s \n" % (counter, poly, numverts))
        counter += 1
        for vert in range(numverts):
              poly[vert]= Vec3Product(result,poly[vert])


def Vec3Product(transform, vector):
    result = [0,0,0]
    if(len(vector)==3):
        for i in range(3):
            result[i] = vector[0]*transform[0][i] + vector[1]*transform[1][i] + vector[2]*transform[2][i]
    return result

    
##Main

clearSVG()
for fbx in fbxlist:
    createSVG(fbx)
#result = [0]*3
#print result
#createSVG(fbxlist[0])
