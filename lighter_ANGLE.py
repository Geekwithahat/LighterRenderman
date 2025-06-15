#!/usr/bin/env -S uv run --script

'''
uv run used over rmanpy environment, prefered colorspace in one over the other.
(The fact they differ is a recent discovery on my end that I will be unlikely to fix in time
I am able and willing to be contacted if it happens to cause issues with assessments)

This is notably not related to the lighter coloring of the uv run images, which is due to 
a compressed lightmap. 
'''



# import the python renderman library
import prman
import math
import random

ri = prman.Ri()  # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "Lighter.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render")

ri.Hider("raytrace", {"int incremental": [1]})
ri.Integrator("PxrPathTracer", "intigrator",{})

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("Lighter.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(1920, 1080, 1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 50})


focusPointX = 0.0
focusPointY =-1.7
focusPointZ = 7.0

ri.Projection("PxrCamera", {
	'float fov' : [39.0], 
	'float fovEnd' : [0], 
	'float fStop' : [4.1], 
	'float focalLength' : [5], 
	'float focalDistance' : [11], 

	'float tilt' : [0.0], 
	'float roll' : [0.0], 
    'point focus1' : [2, -5.9, 6.57], 
})




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
ri.Light("PxrDomeLight", "domeLight", {"string lightColorMap": "txmaketest.tx",
"float intensity": 0.7, })
ri.AttributeEnd()
ri.TransformEnd()

ri.TransformBegin()
ri.AttributeBegin()
ri.Translate(0 ,2, 0)
ri.Declare("coldLight", "string")
ri.Light("PxrRectLight", "cLight", {
    "color lightColor": [192 / 255, 143 / 255, 255 / 255],  
    "float intensity": 20.0,
    "int enableShadows": 1,
})
ri.AttributeEnd()
ri.TransformEnd()
#######################################################################
# end lighting
#######################################################################


ri.Translate(0,0, 10)

ri.Translate(-2,-2, -3)


#ri.Translate(4, -3, 10)
#ri.Translate(0, -2, 6)
#ri.Rotate(-20, 1,0,0)

ri.Translate(1, 1, 0)
ri.Scale(1.3,4.6,0.9)
ri.Rotate(-90,1,0,0)


ri.Rotate(-22, 1,0,0)


ri.Translate(2,-5,-1.8)


def createLighter(x, z):
    ri.TransformBegin()
    ri.Translate(x,0,0)
    ri.Rotate(-30, 0,0,1)

    ri.AttributeBegin()

    ri.Bxdf(
        "PxrSurface",
        "plastic",
        {
            "color diffuseColor": [0, 0, 0],

            "float diffuseGain": [0],
            "int specularFresnelMode": [1],
            "color specularEdgeColor": [0.05,0.05,0.05],
            "color specularIor": [4.3696842, 2.916713, 1.654698],
            "color specularExtinctionCoeff": [5.20643, 4.2313662, 3.7549689],
            "float specularRoughness": [0.3],
            "integer specularModelType": [1],
        },
    )


    # ------------------
    # TUBE
    # ------------------

    # central tube (and general lighter size settings)



    ri.Cylinder(1, -0.5, 0.5, 360)

    #ri.AttributeEnd()


    goldR = 255 / 255
    goldG = 255 / 255
    goldB = 176 / 255


    # MATERIAL VARIABLES
    rustClamp = 0.3
    rustDarken = 2
    dustClamp = 0.1

    ri.AttributeBegin()

    # --------------------
    # DUST CALCULATION
    #----------------------

    ri.Pattern('PxrManifold3D','WORLD',
    {
        'string coordsys' : ['world'], 
    })

    ri.Pattern("PxrWorley", "DustRough", {"float frequency":[16.0], "float jitter": [1.0], "float smoothness": [1],
    'int distancemetric' : [2], "reference struct manifold" : ["WORLD:result"]})

    ri.Pattern('PxrInvert','worleyInvert',
    {
        'reference color inputRGB' : ["DustRough:resultRGB"], 
        'int colorModel' : [1], 
        'int invertChannel0' : [1],
        'int invertChannel1' : [1], 
        'int invertChannel2' : [1], 
    })


    ri.Pattern('PxrClamp', 'worleyClamp', {
        'reference color inputRGB': ['worleyInvert:resultRGB'], 
        'color min': [0.05, 0.05, 0.05], 'color max': [dustClamp, dustClamp, dustClamp]})

    ri.Pattern("noiseMask", "dustMask",{
        "float frequency": [1.5],
        "int bin": [1],
        "float cut": [0.25],
    })

    ri.Pattern('PxrLayeredBlend','applyDust',
    {
        'color backgroundRGB' : [0.05, 0.05, 0.05],
        'int enable_0' : [1], 
        'int operation_0' : [19], 
        'reference color RGB_0' : ["worleyClamp:resultRGB"], 
        'reference float A_0' : ["dustMask:resultR"], 
    })

    ri.Pattern("PxrTexture", "FINAL_DUST", {
        "reference color missingColor": ["applyDust:resultRGB"],
        "reference struct manifold": ["WORLD:result"],
    })
    #--------------
    # RUST CALC
    #--------------

    ri.Pattern("PxrWorley", "RustRough", {"float frequency":[8.0], "float jitter": [1.0],
    'int distancemetric' : [0], "reference struct manifold" : ["WORLD:result"]})


    ri.Pattern('PxrInvert','RustInvert',
    {
        'reference color inputRGB' : ["RustRough:resultRGB"], 
        'int colorModel' : [1], 
        'int invertChannel0' : [1], 
        'int invertChannel1' : [1], 
        'int invertChannel2' : [1], 
    })

    ri.Pattern('PxrClamp', 'RustClamp', {
        'reference color inputRGB': ['RustInvert:resultRGB'], 
        'color min': [rustClamp, rustClamp, rustClamp], 'color max': [1.0, 1.0, 1.0]})

    ri.Pattern('PxrRemap', 'RustRemap', {
        'reference color inputRGB' : ['RustClamp:resultRGB'],
        'float inputMin' : [rustClamp],
        'float inputMax' : [1.0],
        'float outputMin' : [0.0],
        'float outputMax' : [1.0],
    })

    ri.Pattern("noiseMask", "rustMask",{
        "float frequency": [2],
        "float lowClamp": [-0.5],
        "float highClamp": [4.0],
        "float seed":[2],
    })


    ri.Pattern('PxrLayeredBlend','RUST_FINAL',
    {
        'color backgroundRGB' : [0.0,0.0,0.0],
        'int enable_0' : [1], 
        'int operation_0' : [19], 
        'reference color RGB_0' : ["RustRemap:resultRGB"], 
        'reference float A_0' : ["rustMask:resultR"], 
    })

    ri.Pattern('PxrLayeredBlend','mixTextureRust',
    {
        'color backgroundRGB' : [goldR,goldG,goldB],
        'int enable_0' : [1], 
        'int operation_0' : [19], 
        'color RGB_0' : [goldR / rustDarken, goldG / rustDarken, goldB / rustDarken], 
        'reference float A_0' : ["RUST_FINAL:resultR"], 
    })

    # ------------------
    # SCRATCH COMPUTE
    #------------------

    def createScratchArray():
        x = [0] * 120
        for i in range(1, 119, 3) :
            x[i] = (random.random() * 4) - 1
            x[i-1] = (x[i] + random.randrange(-1,1)) * 2 - 1
            x[i+1] = (x[i] + random.randrange(-1,1)) * 2 - 1

        print(x)

    #createScratchArray()

    ri.Pattern("scratchShader", "scratchShader",{})

    ri.Pattern("noiseMask", "scratchMask",{
        "float frequency": [12],
        "int bin":[1],
        "float cut":[0.3],
        "float seed":[3],
    })

    ri.Pattern('PxrLayeredBlend','applyScratchMask',
    {
        'color backgroundRGB' : [0.0,0.0,0.0],
        'int enable_0' : [1], 
        'int operation_0' : [19], 
        'reference color RGB_0' : ["scratchShader:resultRGB"], 
        'reference float A_0' : ["scratchMask:resultR"], 
    })

    ri.Pattern('PxrLayeredBlend','mixTexture',
    {
        'reference color backgroundRGB' : ["mixTextureRust:resultRGB"],
        'int enable_0' : [1], 
        'int operation_0' : [19], 
        'reference color RGB_0' : ["applyScratchMask:resultRGB"], 
        'reference float A_0' : ["applyScratchMask:resultR"], 
    })

    ri.Pattern("PxrNormalMap", "normalScratch", {
        "reference float bumpScale": ["applyScratchMask:resultR"],
        "reference struct manifold": ["WORLD:result"],
    })




    #-----------
    # MATERIAL COMPUTE
    #----------

    ri.Bxdf(
        "PxrSurface",
        "IDmetal",
        {
            "float diffuseGain": [0],
            "int specularFresnelMode": [1],
            "reference color specularEdgeColor": ["mixTexture:resultRGB"],
            "color specularIor": [4.3, 2.9, 1.6],
            "color specularExtinctionCoeff": [5.2, 4.2, 3.7],
            "reference float specularRoughness": ['FINAL_DUST:resultR'],
            "integer specularModelType": [1],
            "reference normal bumpNormal": ["normalScratch:resultN"],
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

    ringRadius = 1.05

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

    # bottom ring cap
    ri.TransformBegin()
    ri.Translate(0,0,-middleYPos + 0.015)
    ri.Scale(ringRadius,ringRadius,ringHeight)
    ri.Disk(0, 1, 360)
    ri.TransformEnd()

    # top third
    ri.TransformBegin()
    ri.Translate(0,0,middleYPos)
    ri.Scale(ringRadius,ringRadius,ringHeight)
    ri.Cylinder(1,-0.5,0.5, 360)
    ri.TransformEnd()

    # top third cap
    ri.TransformBegin()
    ri.Translate(0,0,middleYPos+0.015)
    ri.Scale(ringRadius,ringRadius,ringHeight)
    ri.Disk(0, 1, 360)
    ri.TransformEnd()

    # top ring
    ri.TransformBegin()
    ri.Translate(0,0,baseYPos)
    ri.Scale(ringRadius,ringRadius,ringHeight)
    ri.Cylinder(1,-0.5,0.5, 360)
    ri.TransformEnd()

    # top ring cap
    ri.TransformBegin()
    ri.Translate(0,0,baseYPos + 0.015)
    ri.Scale(ringRadius,ringRadius,ringHeight)
    ri.Disk(0, 1, 360)
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

    # top left gradiant
    ri.TransformBegin()
    ri.Translate(-endX, endZ, endY + 0.0325)
    ri.Scale(0.34,tubeAddRad - 0.01,0.01)
    ri.Rotate(0,1,0,0)
    ri.Cylinder(1, -0.5, 0.5, 360)
    ri.TransformEnd()

    # top right gradiant
    ri.TransformBegin()
    ri.Translate(endX, endZ, endY + 0.0325)
    ri.Scale(0.34,tubeAddRad - 0.01,0.01)
    ri.Rotate(0,1,0,0)
    ri.Cylinder(1, -0.5, 0.5, 360)
    ri.TransformEnd()

    # right end lower cap
    ri.TransformBegin()
    ri.Translate(endX, endZ, -0.45)
    ri.Scale(0.35,tubeAddRad,0.15)
    ri.Rotate(0,1,0,0)
    ri.Disk(0, 1, 360)
    ri.TransformEnd()

    # left end lower cap
    ri.TransformBegin()
    ri.Translate(-endX, endZ, -0.45)
    ri.Scale(0.35,tubeAddRad,0.15)
    ri.Rotate(0,1,0,0)
    ri.Disk(0, 1, 360)
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

    # left nub cap
    ri.TransformBegin()
    ri.Translate(-endX, endZ, 0.65)
    ri.Scale(0.3,tubeAddRad,0.1)
    ri.Rotate(0,1,0,0)
    ri.Disk(0, 1, 360)
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
    ri.Scale(0.3,tubeAddRad,0.19)
    ri.Rotate(0,1,0,0)
    ri.Sphere(1, -0.5, 0.5, 360)
    ri.TransformEnd()

    # right nub cap
    ri.TransformBegin()
    ri.Translate(endX, endZ, 0.695)
    ri.Scale(0.25,tubeAddRad,0.15)
    ri.Rotate(0,1,0,0)
    ri.Disk(0, 1, 360)
    ri.TransformEnd()


    #------------------
    # LIGHTER TOP
    #-----------------

    # rim
    ri.TransformBegin()
    ri.Translate(0, 0.1, 0.72)
    ri.Scale(1,1,0.05)
    ri.Cylinder(1, -0.5, 0.5, 360)
    ri.TransformEnd()

    # rim top
    ri.TransformBegin()
    ri.Translate(0, 0.1, 0.75)
    ri.Scale(0.9,0.9,0.01)
    ri.Cylinder(1, -0.5, 0.5, 360)
    ri.TransformEnd()

    # rim lid
    ri.TransformBegin()
    ri.Translate(0, 0.1, 0.755)
    ri.Scale(0.9,0.9,0.01)
    ri.Disk(0, 1, 360)
    ri.TransformEnd()

    # top lid
    ri.TransformBegin()
    ri.Translate(0, 0.1, 0.745)
    ri.Scale(1,1,0.05)
    ri.Disk(0, 1, 360)
    ri.TransformEnd()

    # bottom lid
    ri.TransformBegin()
    ri.Translate(0, 0.1, 0.7)
    ri.Scale(1.0,1.0,0.05)
    ri.Rotate(180,1,0,0)
    ri.Disk(0, 1, 360)
    ri.TransformEnd()

    hingeBar = 0.65

    # hinge bar
    ri.TransformBegin()
    ri.Translate(-0.2, 0.3, 0.65)
    ri.Scale(3.1,0.1,0.04)
    ri.Rotate(90,0,1,0)
    ri.Cylinder(1, -0.5, 0.5, 360)
    ri.TransformEnd()

    # hinge bar end
    ri.TransformBegin()
    ri.Translate(-1.85, 0.3, 0.65)
    ri.Scale(0.3,0.15,0.03)
    ri.Rotate(90,0,1,0)
    ri.Sphere(1, -0.5, 0.5, 360)
    ri.TransformEnd()


    ri.AttributeEnd()

    ri.AttributeBegin()

    # --------------------
    # DUST CALCULATION
    #----------------------

    ri.Pattern('PxrManifold3D','WORLD',
    {
        'string coordsys' : ['world'], 
    })

    ri.Pattern("PxrWorley", "DustRough", {"float frequency":[16.0], "float jitter": [1.0], "float smoothness": [1],
    'int distancemetric' : [2], "reference struct manifold" : ["WORLD:result"]})

    ri.Pattern('PxrInvert','worleyInvert',
    {
        'reference color inputRGB' : ["DustRough:resultRGB"], 
        'int colorModel' : [1], 
        'int invertChannel0' : [1],
        'int invertChannel1' : [1], 
        'int invertChannel2' : [1], 
    })


    ri.Pattern('PxrClamp', 'worleyClamp', {
        'reference color inputRGB': ['worleyInvert:resultRGB'], 
        'color min': [0.05, 0.05, 0.05], 'color max': [dustClamp, dustClamp, dustClamp]})

    ri.Pattern("noiseMask", "dustMask",{
        "float frequency": [1.5],
        "int bin": [1],
        "float cut": [0.25],
    })

    ri.Pattern('PxrLayeredBlend','applyDust',
    {
        'color backgroundRGB' : [0.05, 0.05, 0.05],
        'int enable_0' : [1], 
        'int operation_0' : [19], 
        'reference color RGB_0' : ["worleyClamp:resultRGB"], 
        'reference float A_0' : ["dustMask:resultR"], 
    })

    ri.Pattern("PxrTexture", "FINAL_DUST", {
        "reference color missingColor": ["applyDust:resultRGB"],
        "reference struct manifold": ["WORLD:result"],
    })
    #--------------
    # RUST CALC
    #--------------

    ri.Pattern("PxrWorley", "RustRough", {"float frequency":[8.0], "float jitter": [1.0],
    'int distancemetric' : [0], "reference struct manifold" : ["WORLD:result"]})


    ri.Pattern('PxrInvert','RustInvert',
    {
        'reference color inputRGB' : ["RustRough:resultRGB"], 
        'int colorModel' : [1], 
        'int invertChannel0' : [1], 
        'int invertChannel1' : [1], 
        'int invertChannel2' : [1], 
    })

    ri.Pattern('PxrClamp', 'RustClamp', {
        'reference color inputRGB': ['RustInvert:resultRGB'], 
        'color min': [rustClamp, rustClamp, rustClamp], 'color max': [1.0, 1.0, 1.0]})

    ri.Pattern('PxrRemap', 'RustRemap', {
        'reference color inputRGB' : ['RustClamp:resultRGB'],
        'float inputMin' : [rustClamp],
        'float inputMax' : [1.0],
        'float outputMin' : [0.0],
        'float outputMax' : [1.0],
    })

    ri.Pattern("noiseMask", "rustMask",{
        "float frequency": [2],
        "float lowClamp": [-0.5],
        "float highClamp": [4.0],
        "float seed":[2],
    })


    ri.Pattern('PxrLayeredBlend','RUST_FINAL',
    {
        'color backgroundRGB' : [0.0,0.0,0.0],
        'int enable_0' : [1], 
        'int operation_0' : [19], 
        'reference color RGB_0' : ["RustRemap:resultRGB"], 
        'reference float A_0' : ["rustMask:resultR"], 
    })

    ri.Pattern('PxrLayeredBlend','mixTextureRust',
    {
        'color backgroundRGB' : [goldR,goldG,goldB],
        'int enable_0' : [1], 
        'int operation_0' : [19], 
        'color RGB_0' : [goldR / rustDarken, goldG / rustDarken, goldB / rustDarken], 
        'reference float A_0' : ["RUST_FINAL:resultR"], 
    })

    # ------------------
    # SCRATCH COMPUTE
    #------------------

    def createScratchArray():
        x = [0] * 60
        for i in range(1, 59, 3) :
            x[i] = random.random()
            x[i-1] = x[i] + random.randrange(-1,1) / 20
            x[i+1] = x[i] + random.randrange(-1,1) / 20

        print(x)

    #createScratchArray()

    ri.Pattern("scratchShader", "scratchShader",{})

    ri.Pattern("noiseMask", "scratchMask",{
        "float frequency": [8],
        "int bin":[1],
        "float cut":[0.25],
        "float seed":[3],
    })

    ri.Pattern('PxrLayeredBlend','applyScratchMask',
    {
        'color backgroundRGB' : [0.0,0.0,0.0],
        'int enable_0' : [1], 
        'int operation_0' : [19], 
        'reference color RGB_0' : ["scratchShader:resultRGB"], 
        'reference float A_0' : ["scratchMask:resultR"], 
    })

    ri.Pattern('PxrLayeredBlend','mixTexture',
    {
        'reference color backgroundRGB' : ["mixTextureRust:resultRGB"],
        'int enable_0' : [1], 
        'int operation_0' : [19], 
        'reference color RGB_0' : ["applyScratchMask:resultRGB"], 
        'reference float A_0' : ["applyScratchMask:resultR"], 
    })

    ri.Pattern("PxrNormalMap", "normalScratch", {
        "reference float bumpScale": ["applyScratchMask:resultR"],
        "reference struct manifold": ["WORLD:result"],
    })




    #-----------
    # MATERIAL COMPUTE
    #----------

    ri.Pattern("PxrTexture", "circleGrid", {"filename": "circle_edit.tx",})

    ri.Bxdf(
        "PxrSurface",
        "IDmetal",
        {
            "float diffuseGain": [0],
            "int specularFresnelMode": [1],
            "reference color specularEdgeColor": ["mixTexture:resultRGB"],
            "color specularIor": [4.3, 2.9, 1.6],
            "color specularExtinctionCoeff": [5.2, 4.2, 3.7],
            "reference float specularRoughness": ['FINAL_DUST:resultR'],
            "integer specularModelType": [1],
            "reference normal bumpNormal": ["normalScratch:resultN"],
            "reference float presence": ["circleGrid:resultR"],
        },
    )

    # grate
    ri.TransformBegin()
    ri.Translate(0, 0.1, 0.6)
    ri.Scale(0.9,0.9,0.4)
    ri.Rotate(30,0,0,1)
    ri.Cylinder(1, -0.5, 0.5, 360)
    ri.TransformEnd()

    ri.AttributeEnd()


    #-----------
    # FLICK WHEEL
    #------------


    ri.AttributeBegin()

    ri.Pattern("PxrPhasorNoise", "wheelColor",
    {
        "float frequency":[16.],
    })


    ri.Pattern("PxrBump", "wheelBump", {

        "reference float inputBump": ["wheelColor:resultF"],
        "float bumpHeight": [100.],
        "float scale":[30.]

    })

    ri.Pattern('PxrClamp', 'wheelClamp', {
        'reference color inputRGB': ['wheelColor:resultRGB'], 
        'color min': [0.4, 0.4, 0.4], 'color max': [1.0, 1.0, 1.0]})


    ri.Bxdf(
        "PxrSurface",
        "wheelSurface",
        {
            "float diffuseGain": [0],
            "int specularFresnelMode": [1],
            "reference color specularEdgeColor": ["wheelClamp:resultRGB"],
            "color specularIor": [4.3696842, 2.916713, 1.654698],
            "color specularExtinctionCoeff": [5.20643, 4.2313662, 3.7549689],
            "float specularRoughness": [1],
            "integer specularModelType": [1],
            "reference normal bumpNormal": ["wheelBump:resultN"],
        },
    )

    # flick wheel Cylinder
    ri.TransformBegin()
    ri.Translate(-1.3, 0.3, 0.6)
    ri.Scale(0.4,0.4,0.08)
    ri.Rotate(90,1,0,0)
    ri.Cylinder(1, -0.25, 0.25, 360)
    ri.TransformEnd()

    ri.AttributeEnd()

    ri.AttributeBegin()

    ri.Pattern("PxrCurvature", "flickEdge",
        {
            "float maxDistance": [0.1],
            "float bias": [1]
        },
    )

    ri.Pattern('PxrLayeredBlend','mixFlick',
    {
        'color backgroundRGB' : [1, 1, 1],
        'int enable_0' : [1], 
        'int operation_0' : [19], 
        'reference color RGB_0' : ["flickEdge:resultRGB"], 
        'float A_0' : [0.2], 
    })


    ri.Bxdf(
        "PxrSurface",
        "wheelSurface",
        {
            "float diffuseGain": [0],
            "int specularFresnelMode": [1],
            "reference color specularEdgeColor": ["mixFlick:resultRGB"],
            "color specularIor": [4.3696842, 2.916713, 1.654698],
            "color specularExtinctionCoeff": [5.20643, 4.2313662, 3.7549689],
            "float specularRoughness": [1],
            "integer specularModelType": [1],
        },
    )

    # flick wheel Front
    ri.TransformBegin()
    ri.Translate(-1.3, 0.4, 0.6)
    ri.Scale(0.4,0.4,0.08)
    ri.Rotate(270,1,0,0)
    ri.Disk(0, 1, 360)
    ri.TransformEnd()

    # flick wheel Back
    ri.TransformBegin()
    ri.Translate(-1.3, 0.2, 0.6)
    ri.Scale(0.4,0.4,0.08)
    ri.Rotate(90,1,0,0)
    ri.Disk(0, 1, 360)
    ri.TransformEnd()

    ri.AttributeEnd()

    #---------------------
    #   SILVER ADDITIONS
    #-----------------------

    ri.AttributeBegin()
    ri.Bxdf(
        "PxrSurface",
        "metal",
        {
            "float diffuseGain": [0],
            "int specularFresnelMode": [1],
            "color specularEdgeColor": [1, 1, 1],
            "color specularIor": [4.3696842, 2.916713, 1.654698],
            "color specularExtinctionCoeff": [5.20643, 4.2313662, 3.7549689],
            "float specularRoughness": [0.5],
            "integer specularModelType": [1],
        },
    )

    # left nub ring
    ri.TransformBegin()
    ri.Translate(-1.28,0.625,0.6)
    ri.Rotate(90,1,0,0)
    ri.Scale(0.1,0.02,0.04)
    ri.Torus(1.00, 0.2, 0, 360, 360)
    ri.TransformEnd()

    # right nub ring
    ri.TransformBegin()
    ri.Translate(1.28,0.625,0.6)
    ri.Rotate(90,1,0,0)
    ri.Scale(0.1,0.02,0.04)
    ri.Torus(1.00, 0.2, 0, 360, 360)
    ri.TransformEnd()

    ri.AttributeEnd()

    ri.AttributeBegin()
    ri.Bxdf(
        "PxrSurface",
        "metal",
        {
            "float diffuseGain": [0],
            "int specularFresnelMode": [1],
            "color specularEdgeColor": [goldR / 4, goldG / 4, goldB / 4],
            "color specularIor": [4.3696842, 2.916713, 1.654698],
            "color specularExtinctionCoeff": [5.20643, 4.2313662, 3.7549689],
            "float specularRoughness": [0.6],
            "integer specularModelType": [1],
        },
    )

    # left ring back
    ri.TransformBegin()
    ri.Translate(-1.2925, 0.57, 0.6)
    ri.Scale(0.08,0.05,0.016)
    ri.Rotate(90,1,0,0)
    ri.Torus(1.00, 1.0, 0, 360, 360)
    ri.TransformEnd()

    # right ring back
    ri.TransformBegin()
    ri.Translate(1.2925, 0.57, 0.6)
    ri.Scale(0.08,0.05,0.016)
    ri.Rotate(90,1,0,0)
    ri.Torus(1.00, 1.0, 0, 360, 360)
    ri.TransformEnd()
    ri.AttributeEnd()



    ri.TransformEnd()


createLighter(-2.5, 0)

#createLighter(5.5,0)

#---------------------------
# SURROUNDING ENVIRONMENT
#--------------------------

points = [-2, -2, 0, -2, 2, 0, 2, 2, 0, 2, -2, 0]
st = [0, 1, 0, 0, 1, 0, 1, 1]


ri.AttributeBegin()
ri.Pattern("PxrTexture", "wood", {"filename": "plywood.tx",})


ri.Bxdf("PxrDiffuse", "plastic", {
    "reference color diffuseColor": ["wood:resultRGB"],
})

ri.TransformBegin()
ri.Scale(9,5,3)
ri.Translate(0,0,-0.17)
ri.GeneralPolygon([4], {ri.P: points, ri.ST: st})
ri.TransformEnd()
ri.AttributeEnd()

ri.AttributeBegin()
ri.Pattern("PxrTexture", "wall", {"filename": "wall.tx",})
ri.Bxdf("PxrDiffuse", "white", {"reference color diffuseColor": ["wall:resultRGB"]})

ri.TransformBegin()
ri.Rotate(-26,1,0,0)
ri.Rotate(90,1,0,0)
ri.Scale(15,6,1)
ri.Translate(0,0,6)
ri.GeneralPolygon([4], {ri.P: points, ri.ST: st})
ri.TransformEnd()
ri.AttributeEnd()



ri.WorldEnd()
# and finally end the rib file
ri.End()