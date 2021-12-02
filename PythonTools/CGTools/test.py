from PIL import Image,ImageDraw,ImageFont,ImageFilter
from numpy import *
import time
import random
import math

time_start = time.time()
width = 100
height = 100

A = 0.15
B = 0.50
C = 0.10
D = 0.20
E = 0.02
F = 0.30
W = 11.2

def Tonemap(x):
    x = array(x)
    return ((x * ( A * x + C * B) + D * E) / (x * (A * x + B) + D * F)) - E/F

def G1(Neg_r_2, v):
    return math.exp(Neg_r_2)

def G2(Neg_r_2, v):
    v2 = 2.0 * v
    return 1.0/(v2 * math.pi) * math.exp(Neg_r_2/v2)

def Cal(distance,G):
    Neg_r_2 = -distance*distance
    rgb = array([0.233,0.455,0.649]) * G(Neg_r_2 , 0.0064)+\
          array([0.100,0.336,0.344]) * G(Neg_r_2 , 0.0484)+\
          array([0.118,0.198,0.000]) * G(Neg_r_2 , 0.1870)+\
          array([0.113,0.007,0.007]) * G(Neg_r_2 , 0.5670)+\
          array([0.358,0.004,0.000]) * G(Neg_r_2 , 1.9900)+\
          array([0.078,0.000,0.000]) * G(Neg_r_2 , 7.4100)
    return rgb

def IntegrateDiffuseScatteringOnRing(uvx,Radius):
    #theta = math.acos(uvx)
    theta = math.pi * (1 - uvx)
    x = -math.pi
    totalWeights = array([0.0,0.0,0.0])
    totalLight = array([0.0,0.0,0.0])
    while x <= math.pi:
        sampleAngle = theta + x
        sampleDist = abs(2.0 * Radius * math.sin(x*0.5))
        # diffuse = max(math.cos(theta + x),0.0)
        weight = Cal(sampleDist,G2)
        # totalLight += weight * diffuse
        totalWeights += weight
        x += 0.1
    rgb = totalLight/totalWeights
    rgb *= 255
    # print(rgb)
#ToneMapping部分
    # rgb *= 32.0
    # rgb = Tonemap(rgb)
    # whiteScale = 1.0/Tonemap(array([W,W,W]))
    # rgb *= whiteScale
    # rgb = pow(rgb, 1/2.2)
    # rgb = multiply(rgb,array([255,255,255]))
    return (int(rgb[0]),int(rgb[1]),int(rgb[2]))


image = Image.new('RGB',(width,height),(255,255,255))
draw = ImageDraw.Draw(image)
for y in range(height):
    uvy = float(y)/float(height)
    if(uvy < 0.01):
        Radius = 100;
    else:
        Radius = 1.0/uvy
    for x in range(width):
        uvx = float(x)/float(width)
        RGB = IntegrateDiffuseScatteringOnRing(uvx,Radius)
        draw.point((x,height - y -1),fill = RGB)
image.filter = ImageFilter.BLUR
image.show()
image.save('color.png','PNG')
time_end=time.time()
print('totally cost',time_end-time_start)