from numbers import Number

import numpy as np

from matplotlib import pyplot as plt
from multipledispatch import dispatch

v = [.0064, .0484, .197, .567, 1.99, 7.41]
light_weights_tuples = [
    (.233, .455, .649),
    (.1, .336, .344),
    (.118, .198, .0),
    (.113, .007, .007),
    (.358, .004, .0),
    (.078, .0, .0),
]

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


# plt.axis([0, 2.5, 0, 1])


def gaussian(v, r):
    return (1 / (2 * np.pi * v)) * np.exp(-np.power(r, 2) / (2 * v))


def saturate(v):
    return max(0, min(v, 1))


def gaussian2(v, r):
    return np.exp(-np.power(r, 2) / v)


@dispatch(object)
def R(d, l=light_weights_tuples, vl=v):
    s = [0, 0, 0]
    for i, t in enumerate(l):
        r, g, b = t
        v = [r, g, b]
        # v /= np.linalg.norm(v)
        # print(v)
        s[0] += v[0] * gaussian2(vl[i], d)
        s[1] += v[1] * gaussian2(vl[i], d)
        s[2] += v[2] * gaussian2(vl[i], d)
    return s


@dispatch(Number, Number, Number)
def R(a, b, r):
    d = r * np.sqrt(2 - 2 * np.cos(a) * np.cos(b))
    return R(d)

@dispatch(Number, Number)
def R(a, r):
    d = 2 * r *np.sin(.5 * a)
    return R(d)

@dispatch(Number, Number, Number, list, list)
def R(a, b, r, l=light_weights_tuples, vl=v):
    d = r * np.sqrt(2 - 2 * np.cos(a) * np.cos(b))
    return R(d, l, vl)

def G1(Neg_r_2, v):
    return np.exp(Neg_r_2)

def G2(Neg_r_2, v):
    v2 = 2.0 * v
    return 1.0/(v2 * np.math.pi) * np.exp(Neg_r_2/v2)

def Cal(distance,G):
    Neg_r_2 = -np.multiply(distance,distance)
    rgb = [0,0,0]
    g = [G(Neg_r_2 , 0.0064),
         G(Neg_r_2 , 0.0484),
         G(Neg_r_2 , 0.1870),
         G(Neg_r_2 , 0.5670),
         G(Neg_r_2 , 1.9900),
         G(Neg_r_2 , 7.4100),
         ]
    rgb[0] += 0.233 *g[0] +\
              0.100 *g[1] +\
              0.118 *g[2] +\
              0.113 *g[3] +\
              0.358 *g[4] +\
              0.078 *g[5]
    rgb[1] += 0.455 *g[0] +\
              0.336 *g[1] +\
              0.198 *g[2] +\
              0.007 *g[3] +\
              0.004 *g[4] +\
              0.000 *g[5]
    rgb[2] += 0.649 *g[0] +\
              0.344 *g[1] +\
              0.000 *g[2] +\
              0.007 *g[3] +\
              0.000 *g[4] +\
              0.000 *g[5]
    # rgb += [0.233,0.455,0.649] * G(Neg_r_2 , 0.0064)+\
    #        [0.100,0.336,0.344] * G(Neg_r_2 , 0.0484)+\
    #        [0.118,0.198,0.000] * G(Neg_r_2 , 0.1870)+\
    #        [0.113,0.007,0.007] * G(Neg_r_2 , 0.5670)+\
    #        [0.358,0.004,0.000] * G(Neg_r_2 , 1.9900)+\
    #        [0.078,0.000,0.000] * G(Neg_r_2 , 7.4100)
    return rgb


r = np.arange(0, 2.5, 0.01)

# R2 = lambda x, l: l[0] * gaussian(.036, x) \
#                  + l[1] * gaussian(.14, x) \
#                  + l[2] * gaussian(.91, x) \
#                  + l[3] * gaussian(7.0, x)

Rr = Cal(r,G2)

# RF = R2(r, [.07,.18,.21,.29]) * r
print(R)
plt.xlabel('r')
plt.ylabel('rR(r)')
plt.title("散射拟合")
plt.plot(r, Rr[0] * r, color='red')
plt.plot(r, Rr[1] * r, color='green')
plt.plot(r, Rr[2] * r, color='blue')

# plt.plot(r, 2 * np.pi * RF, color='black')
plt.show()
