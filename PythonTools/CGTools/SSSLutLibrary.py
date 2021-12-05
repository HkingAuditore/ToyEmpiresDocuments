# #######################LIBRARY##########################
import math
import threading
from math import cos

import numpy as np
from PIL import Image
from multipledispatch import dispatch
from numba import jit
from numpy import array
from tqdm import tqdm

@jit(nopython=True)
def gaussian(v, r):
    return (1 / (2 * v * np.pi)) * np.exp(-pow(r, 2) / (2 * v))

@jit(nopython=True)
def gaussian2(v, r):
    return np.exp(-np.power(r, 2) / v)

@jit(nopython=True)
def gaussian3(v, r):
    return (1 / np.sqrt(2 * np.pi * v)) * np.exp(-np.power(r, 2) / (2 * v))

@jit(nopython=True)
def norm_diff(r, d):
    return saturate(np.exp(-r / d) + np.exp(-r / (3 * d)) / (8 * np.pi * d * r))

@jit(nopython=True)
def saturate(v):
    return max((.0, min(v, 1.0)))

@jit
def R_origin(d):

    vl = np.array([.0064, .0484, .187, .567, 1.99, 7.41])
    # 不同颜色光的散射率
    light_weights_tuples = np.array([
        (.233, .455, .649),
        (.1, .336, .344),
        (.118, .198, .0),
        (.113, .007, .007),
        (.358, .004, .0),
        (.078, .0, .0),
    ])
    s = np.zeros(3)
    p = 8
    k = 1.5
    for i, t in enumerate(light_weights_tuples):
        v = np.array(t)
        v = pow(v * k, p)
        s += v * gaussian(vl[i], d)
    return s

@jit
def R(a=0, b=0, r=1):
    d = abs(r * np.sqrt(2 - 2 * cos(a) * cos(b)))
    return R_origin(d)



# #######################LIBRARY##########################
