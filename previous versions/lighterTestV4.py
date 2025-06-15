#!/usr/bin/env rmanpy

# import the python renderman library
import prman
import math

ri = prman.Ri()  # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "Primitives.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render")

ri.Hider("raytrace", {"int incremental": [1]})
ri.Integrator("PxrPathTracer", "intigrator",{})

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("Primitives.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(3840, 2160, 1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 50})


# now we start our world
ri.WorldBegin()



#######################################################################
# Lighting 
#######################################################################
ri.TransformBegin()
ri.AttributeBegin()
ri.Declare("domeLight", "string")
ri.Rotate(-90, 1, 0, 0)
ri.Rotate(100, 0, 0, 1)
ri.Attribute("visibility", {"int camera": [0]})
ri.Light("PxrDomeLight", "domeLight", {"string lightColorMap": "txmaketest.tx", })
ri.AttributeEnd()
ri.TransformEnd()
#######################################################################
# end lighting
#######################################################################

ri.Translate(0, 0, 10)

ri.AttributeBegin()

ri.Bxdf(
    "PxrSurface",
    "plastic",
    {
        "color diffuseColor": [0, 0, 0],

        "float diffuseGain": [0],
        "int specularFresnelMode": [1],
        "color specularEdgeColor": [0.01, 0.01, 0.01],
        "color specularIor": [4.3696842, 2.916713, 1.654698],
        "color specularExtinctionCoeff": [5.20643, 4.2313662, 3.7549689],
        "float specularRoughness": [0.2],
        "integer specularModelType": [1],
    },
)


# ------------------
# TUBE
# ------------------

# central tube


ri.Translate(0, -1, 0)
ri.Scale(1,4,1)
ri.Rotate(-90,1,0,0)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()

#ri.AttributeEnd()


goldR = 191 / 255
goldG = 115 / 255
goldB = 37 / 255
ri.AttributeBegin()
ri.Bxdf(
    "PxrSurface",
    "metal",
    {
        "float diffuseGain": [0],
        "int specularFresnelMode": [1],
        "color specularEdgeColor": [goldR, goldG, goldB],
        "color specularIor": [4.3696842, 2.916713, 1.654698],
        "color specularExtinctionCoeff": [5.20643, 4.2313662, 3.7549689],
        "float specularRoughness": [0.1],
        "integer specularModelType": [1],
    },
)



tubePosX = 1.3

tubePosZ = 0.3

tubeWidth = 0.3



# L tube
ri.TransformBegin()
ri.Translate(-tubePosX, tubePosZ, 0)
ri.Scale(tubeWidth,tubeWidth,1)
ri.Rotate(0,1,0,0)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()

# R tube
ri.TransformBegin()
ri.Translate(tubePosX, tubePosZ, 0)
ri.Scale(tubeWidth,tubeWidth,1)
ri.Rotate(0,1,0,0)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()


# -------------------
# RING
# -------------------



baseYPos = 0.475

middleYPos = 0.15

ringRadius = 1.075

ringHeight = 0.05


# bottom ring
ri.TransformBegin()
ri.Translate(0,0,-baseYPos)
ri.Scale(ringRadius,ringRadius,ringHeight)
ri.Cylinder(1,-0.5,0.5, 360)
ri.TransformEnd()

# bottom third
ri.TransformBegin()
ri.Translate(0,0,-middleYPos)
ri.Scale(ringRadius,ringRadius,ringHeight)
ri.Cylinder(1,-0.5,0.5, 360)
ri.TransformEnd()

# top third
ri.TransformBegin()
ri.Translate(0,0,middleYPos)
ri.Scale(ringRadius,ringRadius,ringHeight)
ri.Cylinder(1,-0.5,0.5, 360)
ri.TransformEnd()

# top ring
ri.TransformBegin()
ri.Translate(0,0,baseYPos)
ri.Scale(ringRadius,ringRadius,ringHeight)
ri.Cylinder(1,-0.5,0.5, 360)
ri.TransformEnd()


#------------------
# TUBE ENDS
#-----------------

endX = 1.3
endZ = 0.3
endY = 0.475

tubeAddRad = 0.3


# bottom left
ri.TransformBegin()
ri.Translate(-endX, endZ, -endY)
ri.Scale(0.35,tubeAddRad ,0.05)
ri.Rotate(0,1,0,0)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()

# bottom right
ri.TransformBegin()
ri.Translate(endX, endZ, -endY)
ri.Scale(0.35, tubeAddRad,0.05)
ri.Rotate(0,1,0,0)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()

# top left
ri.TransformBegin()
ri.Translate(-endX, endZ, endY)
ri.Scale(0.35,tubeAddRad,0.05)
ri.Rotate(0,1,0,0)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()

# top right
ri.TransformBegin()
ri.Translate(endX, endZ, 0.475)
ri.Scale(0.35,tubeAddRad,0.05)
ri.Rotate(0,1,0,0)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()

#--------------------
# UPPER TUBES
#------------------------

# left stack
ri.TransformBegin()
ri.Translate(-endX, endZ, 0.55)
ri.Scale(0.3,tubeAddRad,0.1)
ri.Rotate(0,1,0,0)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()

# left nub???
ri.TransformBegin()
ri.Translate(-endX, endZ, 0.6)
ri.Scale(0.3,tubeAddRad,0.1)
ri.Rotate(0,1,0,0)
ri.Sphere(1, -0.5, 0.5, 360)
ri.TransformEnd()

# right stack
ri.TransformBegin()
ri.Translate(endX, endZ, 0.55)
ri.Scale(0.3,tubeAddRad,0.1)
ri.Rotate(0,1,0,0)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()

# right nub???
ri.TransformBegin()
ri.Translate(endX, endZ, 0.6)
ri.Scale(0.3,tubeAddRad,0.1)
ri.Rotate(0,1,0,0)
ri.Sphere(1, -0.5, 0.5, 360)
ri.TransformEnd()

# right nub???
ri.TransformBegin()
ri.Translate(endX, endZ, 0.65)
ri.Scale(0.3,tubeAddRad,0.15)
ri.Rotate(0,1,0,0)
ri.Sphere(1, -0.5, 0.5, 360)
ri.TransformEnd()



#------------------
# LIGHTER TOP
#-----------------

# rim
ri.TransformBegin()
ri.Translate(0, -1, 0.8)
ri.Scale(1,1,0.05)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()

# hinge bar
ri.TransformBegin()
ri.Translate(0, -1, 0.75)
ri.Scale(3.3,0.04,0.04)
ri.Rotate(90,0,1,0)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()

# hinge bar end
ri.TransformBegin()
ri.Translate(-1.8, -1.0, 0.75)
ri.Scale(0.3,0.25,0.05)
ri.Rotate(90,0,1,0)
ri.Sphere(1, -0.5, 0.5, 360)
ri.TransformEnd()

ri.AttributeEnd()

ri.AttributeBegin()

ri.Pattern("PxrTexture", "circleGrid", {"filename": "circle_edit.tx",})

ri.Bxdf(
    "PxrSurface",
    "metal",
    {
        "float diffuseGain": [0],
        "int specularFresnelMode": [1],
        "color specularEdgeColor": [goldR, goldG, goldB],
        #"reference color specularEdgeColor": ["circleGrid:resultRGB"],
        "color specularIor": [4.3696842, 2.916713, 1.654698],
        "color specularExtinctionCoeff": [5.20643, 4.2313662, 3.7549689],
        "float specularRoughness": [0.1],
        "integer specularModelType": [1],
        "reference float presence": ["circleGrid:resultR"],
    },
)

# grate
ri.TransformBegin()
ri.Translate(0, -1, 0.65)
ri.Scale(0.9,0.9,0.4)
ri.Rotate(30,0,0,1)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()

ri.AttributeEnd()



ri.AttributeBegin()
ri.Pattern("PxrTexture", "wheel", {"filename": "wheelDff.tx",})
ri.Bxdf("PxrDiffuse", "white", {"reference color diffuseColor": ["wheel:resultRGB"]})

ri.Pattern("PxrTexture", "wheelDsp", {"filename": "wheelDsp.tx"})
ri.Displace("PxrDisplace", "white", {"reference float dispScalar": ["wheelDsp:resultR"]})




# flick wheel Cylinder
ri.TransformBegin()
ri.Translate(-1.3, 0.3, 0.575)
ri.Scale(0.4,0.4,0.1)
ri.Rotate(90,1,0,0)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()

ri.AttributeEnd()

ri.AttributeBegin()

ri.Bxdf(
    "PxrSurface",
    "plastic",
    {
        "color diffuseColor": [0.3, 0.3, 0.3],
    },
)


# flick wheel Front
ri.TransformBegin()
ri.Translate(-1.3, 0.4, 0.575)
ri.Scale(0.4,0.4,0.1)
ri.Rotate(90,1,0,0)
ri.Disk(0, 1, 360)
ri.TransformEnd()

# flick wheel Back
ri.TransformBegin()
ri.Translate(-1.3, 0.1, 0.575)
ri.Scale(0.4,0.4,0.1)
ri.Rotate(90,1,0,0)
ri.Disk(0, 1, 360)
ri.TransformEnd()


ri.AttributeEnd()

##### surrounding environment #########

points = [-2, -2, 0, -2, 2, 0, 2, 2, 0, 2, -2, 0]
st = [0, 1, 0, 0, 1, 0, 1, 1]


ri.AttributeBegin()
ri.Pattern("PxrTexture", "wood", {"filename": "plywood.tx",})


ri.Bxdf("PxrDiffuse", "plastic", {
    "reference color diffuseColor": ["wood:resultRGB"],
})

ri.TransformBegin()
ri.Rotate(0,1,0,0)
ri.Scale(9,5,3)
ri.Translate(0,0,-0.168)
ri.GeneralPolygon([4], {ri.P: points, ri.ST: st})
ri.TransformEnd()
ri.AttributeEnd()

ri.AttributeBegin()
ri.Pattern("PxrTexture", "wall", {"filename": "wall.tx",})
ri.Bxdf("PxrDiffuse", "white", {"reference color diffuseColor": ["wall:resultRGB"]})

ri.Pattern("PxrTexture", "wallDisp", {"filename": "wallDisp.tx"})
ri.Displace("PxrDisplace", "whiteDsp", {"reference float dispScalar": ["wallDisp:resultR"]})

ri.TransformBegin()
ri.Rotate(90,1,0,0)
ri.Scale(15,6,1)
ri.Translate(0,0,6)
ri.GeneralPolygon([4], {ri.P: points, ri.ST: st})
ri.TransformEnd()
ri.AttributeEnd()

ri.WorldEnd()
# and finally end the rib file
ri.End()