##DiffusionProfile生成代码
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import  numpy as np
import random
import math


def saturate(v):
    return max((.0, min(v, 1.0)))

def gaussian(r, v):
    return np.exp(-np.power(r, 3.5) / (.05*v))

def gaussian2(r, v):
    return np.exp(-np.power(r, 2) / v)

def gaussian3(r, v):
    return (1 / np.sqrt(2 * np.pi * v)) * np.exp(-np.power(r, 2) / (2 * v))

def gaussian4(r, d):
    return(np.exp(-r / d) + np.exp(-r / (3 * d)))

def Cal(distance,G):
    rgb = np.array([0.233,0.455,0.649]) * G(distance, 0.0064)+\
          np.array([0.100,0.336,0.344]) * G(distance, 0.0484)+\
          np.array([0.118,0.198,0.000]) * G(distance, 0.1870)+\
          np.array([0.113,0.007,0.007]) * G(distance, 0.5670)+\
          np.array([0.358,0.004,0.000]) * G(distance, 1.9900)+\
          np.array([0.078,0.000,0.000]) * G(distance, 7.4100)
    rgb = np.multiply(rgb,255).astype(int)
    return (rgb[0],rgb[1],rgb[2])


def Cal_R(distance,G):
    rgb = 0.233 * G(distance, 0.0064)+\
          0.100 * G(distance, 0.0484)+\
          0.118 * G(distance, 0.1870)+\
          0.113 * G(distance, 0.5670)+\
          0.358 * G(distance, 1.9900)+\
          0.078 * G(distance, 7.4100)
    # rgb *= 255
    return rgb


def Cal_G(distance,G):
    rgb = 0.455 * G(distance, 0.0064)+\
          0.336 * G(distance, 0.0484)+\
          0.198 * G(distance, 0.1870)+\
          0.007 * G(distance, 0.5670)+\
          0.004 * G(distance, 1.9900)+\
          0.000 * G(distance, 7.4100)
    # rgb *= 255
    return rgb


def Cal_B(distance,G):
    rgb =0.649 * G(distance, 0.0064)+\
         0.344 * G(distance, 0.0484)+\
         0.000 * G(distance, 0.1870)+\
         0.007 * G(distance, 0.5670)+\
         0.000 * G(distance, 1.9900)+\
         0.000 * G(distance, 7.4100)
    # rgb *= 255
    return rgb

vl = np.array([.0064, .0484, .187, .567, 1.99, 7.41])

def R_R(d=.0):

    return  0.233 * gaussian(d, 0.0064) +\
            0.1   * gaussian(d, 0.0484) +\
            0.118 * gaussian(d, 0.187 ) +\
            0.113 * gaussian(d, 0.567 ) +\
            0.358 * gaussian(d, 1.99  ) +\
            0.078 * gaussian(d, 7.41  )

def R_G(d=.0):

    return  0.455 * gaussian(d, 0.0064) +\
            0.336 * gaussian(d, 0.0484) +\
            0.198 * gaussian(d, 0.187 ) +\
            0.007 * gaussian(d, 0.567 ) +\
            0.007 * gaussian(d, 1.99  ) +\
            0.000 * gaussian(d, 7.41  )


def R_B(d=.0):

    return  0.649 * gaussian(d, 0.0064)  +\
            0.344 * gaussian(d, 0.0484)  +\
            0.000 * gaussian(d, 0.187 )  +\
            0.007 * gaussian(d, 0.567 )  +\
            0.000 * gaussian(d, 1.99  )  +\
            0.000 * gaussian(d, 7.41  )


width = 180
height = 180
image = Image.new('RGB',(width,height),(255,255,255))

draw = ImageDraw.Draw(image)
for x in range(width):
    uvx = (float(x)/float(width) - .5) * 2
    for y in range(height):
        uvy = (float(y)/float(height) - .5) * 2
        d = math.sqrt((uvx)**2+(uvy)**2)
        draw.point((x,y),fill = Cal(d,gaussian))

image.show()
image.save("profile" + ".png", "png")


# import matplotlib.pyplot as plt
# import numpy as np
#
# # def dipole(r, s, a):
# #     t = s + a
# #     tr = np.sqrt(3 * a * t)
# #     return np.exp(tr*r)/(4 * np.pi * (1 / 3 * t) * r)
# #
# #
# x = np.linspace(0, 2.5, 100)
# # plt.ylim(bottom=0,top=.5)
# r = R_R(x)
# g = R_G(x)
# b = R_B(x)
#
# plt.xlabel("r")  # x轴上的名字
# plt.ylabel("rR(r)")  # y轴上的名字
# plt.plot(x,x * r, color='red', linewidth=1)
# plt.plot(x,x * g, color='green', linewidth=1)
# plt.plot(x,x * b, color='blue', linewidth=1)
# plt.show()

# def normalize(v):
#     return v/np.linalg.norm(v)
#
# print(normalize(np.array([0.233,0.455,0.649])))
# print(normalize(np.array([0.100,0.336,0.344])))
# print(normalize(np.array([0.118,0.198,0.000])))
# print(normalize(np.array([0.113,0.007,0.007])))
# print(normalize(np.array([0.358,0.004,0.000])))
# print(normalize(np.array([0.078,0.000,0.000])))
