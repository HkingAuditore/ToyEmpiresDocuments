##DiffusionProfile生成代码
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from numpy import *

import random
import math
import SSSLutLibrary

def G1(r, v):
    return exp(-power(r, 2) / v)

def Cal(r,G):
    rgb = array([0.233,0.455,0.649]) * G(r , 0.0064)+\
          array([0.100,0.336,0.344]) * G(r , 0.0484)+\
          array([0.118,0.198,0.000]) * G(r , 0.1870)+\
          array([0.113,0.007,0.007]) * G(r , 0.5670)+\
          array([0.358,0.004,0.000]) * G(r , 1.9900)+\
          array([0.078,0.000,0.000]) * G(r , 7.4100)
    rgb = tuple(multiply(rgb,array([255,255,255])))
    return (int(rgb[0]),int(rgb[1]),int(rgb[2]))

width = 180
height = 180
image = Image.new('RGB',(width,height),(255,255,255))

draw = ImageDraw.Draw(image)
for x in range(width):
    uvx = float(x)/float(width)
    for y in range(height):
        uvy = float(y)/float(height)
        draw.point((x,y),fill = Cal(2.0*math.sqrt((uvx-0.5)**2+(uvy-0.5)**2),G1))

image.show()