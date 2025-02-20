#!/usr/bin/env rmanpy
# import the python renderman library
import prman

ri = prman.Ri()  # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "Primitives.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render")

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("Primitives.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720, 575, 1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 50})

# now we start our world
ri.WorldBegin()

ri.Translate(0, 0, 10)
ri.TransformBegin()

# central tube
ri.Translate(0, -1, 0)
ri.Scale(1,4,1)
ri.Rotate(-90,1,0,0)
ri.Cylinder(1, -0.5, 0.5, 360)
ri.TransformEnd()

ri.WorldEnd()
# and finally end the rib file
ri.End()