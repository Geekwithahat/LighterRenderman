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
ri.Light("PxrDomeLight", "domeLight", {"string lightColorMap": "txmaketest.tx", "int visibleInCamera": [1] })
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


# L tube
ri.TransformBegin()
ri.Translate(-1.3, 0.3, 0)
ri.Scale(0.3,0.3,1)
ri.Rotate(0,1,0,0)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()

# R tube
ri.TransformBegin()
ri.Translate(1.3, 0.3, 0)
ri.Scale(0.3,0.3,1)
ri.Rotate(0,1,0,0)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()


# -------------------
# RING
# -------------------


# bottom ring
ri.TransformBegin()
ri.Translate(0,0,-0.45)
ri.Scale(1.05,1,0.1)
ri.Cylinder(1,-0.5,0.5, 360)
ri.TransformEnd()

# bottom third
ri.TransformBegin()
ri.Translate(0,0,-0.2)
ri.Scale(1.05,1,0.1)
ri.Cylinder(1,-0.5,0.5, 360)
ri.TransformEnd()

# top third
ri.TransformBegin()
ri.Translate(0,0,0.2)
ri.Scale(1.05,1,0.1)
ri.Cylinder(1,-0.5,0.5, 360)
ri.TransformEnd()

# top ring
ri.TransformBegin()
ri.Translate(0,0,0.45)
ri.Scale(1.05,1,0.1)
ri.Cylinder(1,-0.5,0.5, 360)
ri.TransformEnd()


#------------------
# TUBE ENDS
#-----------------


# bottom left
ri.TransformBegin()
ri.Translate(-1.3, 0.3, -0.45)
ri.Scale(0.35,0.3,0.1)
ri.Rotate(0,1,0,0)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()

# bottom right
ri.TransformBegin()
ri.Translate(1.3, 0.3, -0.45)
ri.Scale(0.35,0.3,0.1)
ri.Rotate(0,1,0,0)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()

# top left
ri.TransformBegin()
ri.Translate(-1.3, 0.3, 0.45)
ri.Scale(0.35,0.3,0.1)
ri.Rotate(0,1,0,0)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()

# top right
ri.TransformBegin()
ri.Translate(1.3, 0.3, 0.45)
ri.Scale(0.35,0.3,0.1)
ri.Rotate(0,1,0,0)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()

#--------------------
# UPPER TUBES
#------------------------

# left stack
ri.TransformBegin()
ri.Translate(-1.3, 0.3, 0.55)
ri.Scale(0.3,0.3,0.1)
ri.Rotate(0,1,0,0)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()

# left nub???
ri.TransformBegin()
ri.Translate(-1.3, 0.3, 0.6)
ri.Scale(0.3,0.3,0.1)
ri.Rotate(0,1,0,0)
ri.Sphere(1, -0.5, 0.5, 360)
ri.TransformEnd()

# right stack
ri.TransformBegin()
ri.Translate(1.3, 0.3, 0.55)
ri.Scale(0.3,0.3,0.1)
ri.Rotate(0,1,0,0)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()

# right nub???
ri.TransformBegin()
ri.Translate(1.3, 0.3, 0.6)
ri.Scale(0.3,0.3,0.1)
ri.Rotate(0,1,0,0)
ri.Sphere(1, -0.5, 0.5, 360)
ri.TransformEnd()

# right nub???
ri.TransformBegin()
ri.Translate(1.3, 0.3, 0.65)
ri.Scale(0.3,0.3,0.15)
ri.Rotate(0,1,0,0)
ri.Sphere(1, -0.5, 0.5, 360)
ri.TransformEnd()



#------------------
# LIGHTER TOP
#-----------------

# grate
ri.TransformBegin()
ri.Translate(0, -1, 0.7)
ri.Scale(0.9,0.9,0.3)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()

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

ri.Bxdf(
    "PxrSurface",
    "plastic",
    {
        "color diffuseColor": [0, 0, 0],
        "color clearcoatFaceColor": [1, 1, 1],
        "float specularRoughness":  [0.9],
    },
)


# flick wheel Cylinder
ri.TransformBegin()
ri.Translate(-1.3, 0.3, 0.575)
ri.Scale(0.4,0.4,0.1)
ri.Rotate(90,1,0,0)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()

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


ri.WorldEnd()
# and finally end the rib file
ri.End()