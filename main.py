import numpy as np
import svgwrite
from PIL import Image

""" Finds where a lamp at LAMP would project points in an image contained
    in the file named ORIGINAL_IMAGE onto a plane extending at right angles 
    from the bottom of the image and then traces them onto a plane parallel 
    with the image at a distance of PLANE_Z through a point at EYE
"""

ORIGINAL_IMAGE = "rectangle.png"
LAMP = (0.5, -0.5, -1.0)
EYE = (0.5, 5.0, 4.0)
PLANE_Z = 2.0
COLOUR = "rgb(255,127,127)"
MIN_RED = 10

def ground(sourceX, sourceY, lightX, lightY, lightZ):
    differenceY = sourceY - lightY
    return (lightX - lightY * (lightX - sourceX) / differenceY,
            lightZ - lightY * lightZ / differenceY)

def trace(sourceX, sourceY, screenZ, light, eye):
    groundX, groundZ = ground(sourceX, sourceY, *light)
    differenceZ = eye[2] - groundZ
    return (groundX + screenZ * (eye[0] - groundX) / differenceZ,
            screenZ * eye[1] / differenceZ)

if __name__ == '__main__':
    outbasename, outextension = ORIGINAL_IMAGE.split(".")
    originalImage = Image.open(ORIGINAL_IMAGE)
    originalImage.load()
    upright = np.asarray(originalImage, dtype="int32")
    height, width, numChannels = upright.shape
    edgeDistance = 0.5 / width
    svgdrawing = svgwrite.Drawing(".".join([outbasename, "svg"]), size=(2 * height / width, 2))
    heightRange, widthRange = range(height), range(width)
    for pixelY in heightRange:
        middleY = pixelY / width
        lowY, highY = middleY - edgeDistance, middleY + edgeDistance
        for pixelX in widthRange:
            middleX = pixelX / width
            lowX, highX = middleX - edgeDistance, middleX + edgeDistance
            if upright[pixelY][pixelX][0] >= MIN_RED:
                svgdrawing.add(svgwrite.shapes.Polygon((trace(lowX, lowY, PLANE_Z, LAMP, EYE),
                                                        trace(highX, lowY, PLANE_Z, LAMP, EYE),
                                                        trace(highX, highY, PLANE_Z, LAMP, EYE),
                                                        trace(lowX, highY, PLANE_Z, LAMP, EYE),),
                                                       fill=COLOUR))
    svgdrawing.save()